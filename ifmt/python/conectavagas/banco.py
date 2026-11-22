"""Camada de dados do ConectaVagas: SQLAlchemy + servidor MySQL.

As telas nunca executam SQL diretamente: chamam as funções deste arquivo.
Para os testes automatizados, o engine pode ser trocado por SQLite em memória.
"""

from regiao import CIDADE_PADRAO
import hashlib
import hmac
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

load_dotenv(Path(__file__).resolve().parent / ".env")


def agora_utc():
    """Horário em UTC armazenado como DATETIME sem fuso no MySQL."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Base(DeclarativeBase):
    """Classe base que reúne as tabelas mapeadas."""


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    salt: Mapped[str] = mapped_column(String(32), nullable=False)
    hash_senha: Mapped[str] = mapped_column(String(64), nullable=False)
    tipo: Mapped[str] = mapped_column(String(15), nullable=False)  # candidato ou empresa
    telefone: Mapped[str] = mapped_column(String(25), default="", nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), default=CIDADE_PADRAO, nullable=False)
    resumo: Mapped[str] = mapped_column(Text, default="", nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=agora_utc, nullable=False)


class Vaga(Base):
    __tablename__ = "vagas"

    id: Mapped[int] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    area: Mapped[str] = mapped_column(String(80), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    requisitos: Mapped[str] = mapped_column(Text, default="", nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    modalidade: Mapped[str] = mapped_column(String(25), nullable=False)  # Presencial / Híbrido / Remoto
    contrato: Mapped[str] = mapped_column(String(25), nullable=False)  # Estágio / CLT / Jovem Aprendiz
    remuneracao: Mapped[str] = mapped_column(String(100), default="Não informada", nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    criada_em: Mapped[datetime] = mapped_column(DateTime, default=agora_utc, nullable=False)


class Candidatura(Base):
    __tablename__ = "candidaturas"
    __table_args__ = (UniqueConstraint("candidato_id", "vaga_id", name="uq_candidato_vaga"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    candidato_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    vaga_id: Mapped[int] = mapped_column(ForeignKey("vagas.id"), nullable=False)
    mensagem: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Enviada", nullable=False)
    enviada_em: Mapped[datetime] = mapped_column(DateTime, default=agora_utc, nullable=False)


engine = None


def iniciar_banco():
    """Abre a conexão com o MySQL e cria as três tabelas, caso não existam.

    O BANCO em si deve ser criado no MySQL Workbench, usando sql/criar_banco.sql.
    """
    global engine
    database = os.getenv("MYSQL_DATABASE", "conectavagas")
    if not re.fullmatch(r"[A-Za-z0-9_]+", database):
        raise ValueError("Nome do banco inválido no arquivo .env.")

    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=database,
        query={"charset": "utf8mb4"},
    )
    # O SQLAlchemy monta uma URL com senha protegida, sem concatenar SQL manualmente.
    engine = create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 8})
    Base.metadata.create_all(engine)


def sessao_banco():
    """Devolve uma sessão usada dentro de `with Session(...)`."""
    if engine is None:
        raise RuntimeError("O banco não foi iniciado. Execute iniciar_banco() primeiro.")
    return Session(engine)


def senha_para_hash(senha, salt):
    """Protege a senha com PBKDF2-HMAC-SHA256 (não salva a senha original)."""
    return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 260_000).hex()


def _validar_email(email):
    email = email.strip().lower()
    if len(email) > 150 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Digite um e-mail válido (até 150 caracteres).")
    return email


def _usuario_dict(u):
    return {"id": u.id, "nome": u.nome, "email": u.email, "tipo": u.tipo,
            "telefone": u.telefone, "cidade": u.cidade, "resumo": u.resumo}


def cadastrar_usuario(nome, email, senha, tipo, telefone="", cidade=CIDADE_PADRAO):
    """Grava candidato ou empresa; levanta ValueError se o cadastro não for válido."""
    nome, email, telefone, cidade = nome.strip(), _validar_email(email), telefone.strip(), cidade.strip()
    if not 2 <= len(nome) <= 100:
        raise ValueError("O nome deve ter entre 2 e 100 caracteres.")
    if tipo not in {"candidato", "empresa"}:
        raise ValueError("O tipo de usuário precisa ser candidato ou empresa.")
    if len(senha) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres.")
    if len(telefone) > 25 or not 1 <= len(cidade) <= 100:
        raise ValueError("Verifique os campos telefone e cidade.")

    salt = secrets.token_bytes(16)
    with sessao_banco() as sessao:
        usuario = Usuario(nome=nome, email=email, tipo=tipo, telefone=telefone,
                          cidade=cidade, salt=salt.hex(), hash_senha=senha_para_hash(senha, salt))
        sessao.add(usuario)
        try:
            sessao.commit()
            return usuario.id
        except IntegrityError as erro:
            sessao.rollback()
            raise ValueError("Este e-mail já está cadastrado.") from erro


def autenticar(email, senha):
    """Confere e-mail e senha e retorna um dicionário, ou None se estiver incorreto."""
    email = email.strip().lower()
    with sessao_banco() as sessao:
        usuario = sessao.scalar(select(Usuario).where(Usuario.email == email))
        if usuario is None:
            return None
        hash_recebido = senha_para_hash(senha, bytes.fromhex(usuario.salt))
        if hmac.compare_digest(hash_recebido, usuario.hash_senha):
            return _usuario_dict(usuario)
        return None


def obter_usuario(usuario_id):
    with sessao_banco() as sessao:
        usuario = sessao.get(Usuario, usuario_id)
        return _usuario_dict(usuario) if usuario else None


def atualizar_perfil(usuario_id, telefone, cidade, resumo):
    telefone, cidade, resumo = telefone.strip(), cidade.strip(), resumo.strip()
    if len(telefone) > 25 or not 1 <= len(cidade) <= 100 or len(resumo) > 1500:
        raise ValueError("Verifique telefone, cidade (até 100) e resumo (até 1.500 caracteres).")
    with sessao_banco() as sessao:
        usuario = sessao.get(Usuario, usuario_id)
        if usuario is None:
            raise ValueError("Usuário não encontrado.")
        usuario.telefone, usuario.cidade, usuario.resumo = telefone, cidade, resumo
        sessao.commit()


def _vaga_dict(vaga, empresa):
    return {"id": vaga.id, "empresa_id": vaga.empresa_id, "empresa": empresa,
            "titulo": vaga.titulo, "area": vaga.area, "descricao": vaga.descricao,
            "requisitos": vaga.requisitos, "cidade": vaga.cidade, "modalidade": vaga.modalidade,
            "contrato": vaga.contrato, "remuneracao": vaga.remuneracao, "ativa": vaga.ativa,
            "criada_em": vaga.criada_em}


def criar_vaga(empresa_id, titulo, area, descricao, requisitos, cidade, modalidade, contrato, remuneracao):
    """Empresa publica uma vaga local; toda vaga fica vinculada ao criador."""
    titulo, area, descricao, requisitos = [x.strip() for x in (titulo, area, descricao, requisitos)]
    cidade, remuneracao = cidade.strip(), remuneracao.strip() or "Não informada"
    if not 3 <= len(titulo) <= 120 or not 2 <= len(area) <= 80:
        raise ValueError("Preencha título (3 a 120 caracteres) e área (2 a 80).")
    if not 10 <= len(descricao) <= 5000 or len(requisitos) > 3000:
        raise ValueError("Descrição entre 10 e 5.000 caracteres; requisitos até 3.000.")
    if not 2 <= len(cidade) <= 100 or len(remuneracao) > 100:
        raise ValueError("Verifique cidade e remuneração.")
    if modalidade not in {"Presencial", "Híbrido", "Remoto"}:
        raise ValueError("Modalidade inválida.")
    if contrato not in {"Estágio", "CLT", "Jovem Aprendiz", "Temporário"}:
        raise ValueError("Tipo de contrato inválido.")

    with sessao_banco() as sessao:
        empresa = sessao.get(Usuario, empresa_id)
        if empresa is None or empresa.tipo != "empresa":
            raise ValueError("Somente uma conta de empresa pode publicar vagas.")
        vaga = Vaga(empresa_id=empresa_id, titulo=titulo, area=area, descricao=descricao,
                    requisitos=requisitos, cidade=cidade, modalidade=modalidade,
                    contrato=contrato, remuneracao=remuneracao)
        sessao.add(vaga)
        sessao.commit()
        return vaga.id


def listar_vagas(busca="", cidade=""):
    """Lista somente vagas ativas; o SELECT já relaciona vagas com usuários/empresas."""
    with sessao_banco() as sessao:
        comando = (select(Vaga, Usuario.nome).join(Usuario, Vaga.empresa_id == Usuario.id)
                   .where(Vaga.ativa.is_(True)))
        if busca.strip():
            termo = f"%{busca.strip()}%"
            comando = comando.where(Vaga.titulo.ilike(termo) | Vaga.area.ilike(termo))
        if cidade.strip():
            comando = comando.where(Vaga.cidade.ilike(f"%{cidade.strip()}%"))
        resultados = sessao.execute(comando.order_by(Vaga.criada_em.desc(), Vaga.id.desc())).all()
        return [_vaga_dict(v, empresa) for v, empresa in resultados]


def obter_vaga(vaga_id):
    with sessao_banco() as sessao:
        resultado = sessao.execute(select(Vaga, Usuario.nome).join(Usuario).where(Vaga.id == vaga_id)).first()
        return _vaga_dict(*resultado) if resultado else None


def minhas_vagas(empresa_id):
    with sessao_banco() as sessao:
        linhas = sessao.execute(select(Vaga, Usuario.nome).join(Usuario)
                               .where(Vaga.empresa_id == empresa_id)
                               .order_by(Vaga.id.desc())).all()
        return [_vaga_dict(v, e) for v, e in linhas]


def mudar_situacao_vaga(empresa_id, vaga_id, ativa):
    """A empresa só pode fechar/reabrir as vagas que ela própria criou."""
    with sessao_banco() as sessao:
        vaga = sessao.get(Vaga, vaga_id)
        if vaga is None or vaga.empresa_id != empresa_id:
            raise ValueError("Vaga não encontrada para esta empresa.")
        vaga.ativa = bool(ativa)
        sessao.commit()


def candidatar(candidato_id, vaga_id, mensagem=""):
    """Candidatura única por candidato e por vaga; exige vaga ativa."""
    mensagem = mensagem.strip()
    if len(mensagem) > 2000:
        raise ValueError("A mensagem deve ter até 2.000 caracteres.")
    with sessao_banco() as sessao:
        candidato = sessao.get(Usuario, candidato_id)
        vaga = sessao.get(Vaga, vaga_id)
        if candidato is None or candidato.tipo != "candidato":
            raise ValueError("Somente candidatos podem se inscrever.")
        if vaga is None or not vaga.ativa:
            raise ValueError("Esta vaga não está disponível.")
        existe = sessao.scalar(select(Candidatura.id).where(
            Candidatura.candidato_id == candidato_id, Candidatura.vaga_id == vaga_id))
        if existe is not None:
            raise ValueError("Você já se candidatou a esta vaga.")
        sessao.add(Candidatura(candidato_id=candidato_id, vaga_id=vaga_id, mensagem=mensagem))
        try:
            sessao.commit()
        except IntegrityError as erro:
            sessao.rollback()
            raise ValueError("Você já se candidatou a esta vaga.") from erro


def minhas_candidaturas(candidato_id):
    with sessao_banco() as sessao:
        linhas = sessao.execute(
            select(Candidatura, Vaga, Usuario.nome)
            .join(Vaga, Candidatura.vaga_id == Vaga.id)
            .join(Usuario, Vaga.empresa_id == Usuario.id)
            .where(Candidatura.candidato_id == candidato_id)
            .order_by(Candidatura.id.desc())).all()
        return [{"id": c.id, "vaga_id": v.id, "titulo": v.titulo, "empresa": empresa,
                 "status": c.status, "data": c.enviada_em} for c, v, empresa in linhas]


def candidatos_da_vaga(empresa_id, vaga_id):
    """Devolve nome e contato somente se a vaga pertencer à empresa logada."""
    with sessao_banco() as sessao:
        vaga = sessao.get(Vaga, vaga_id)
        if vaga is None or vaga.empresa_id != empresa_id:
            raise ValueError("Você não tem acesso aos candidatos desta vaga.")
        linhas = sessao.execute(
            select(Candidatura, Usuario)
            .join(Usuario, Candidatura.candidato_id == Usuario.id)
            .where(Candidatura.vaga_id == vaga_id)
            .order_by(Candidatura.id.desc())).all()
        return [{"id": c.id, "nome": u.nome, "email": u.email, "telefone": u.telefone,
                 "cidade": u.cidade, "resumo": u.resumo, "mensagem": c.mensagem,
                 "status": c.status, "data": c.enviada_em} for c, u in linhas]


def mudar_status_candidatura(empresa_id, candidatura_id, novo_status):
    if novo_status not in {"Enviada", "Em análise", "Aprovada", "Recusada"}:
        raise ValueError("Situação de candidatura inválida.")
    with sessao_banco() as sessao:
        candidatura = sessao.get(Candidatura, candidatura_id)
        vaga = sessao.get(Vaga, candidatura.vaga_id) if candidatura else None
        if vaga is None or vaga.empresa_id != empresa_id:
            raise ValueError("Você não pode alterar esta candidatura.")
        candidatura.status = novo_status
        sessao.commit()
