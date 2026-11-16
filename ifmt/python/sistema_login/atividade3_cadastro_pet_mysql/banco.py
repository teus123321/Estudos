"""Persistência do cadastro de PETs, aproveitando os usuários da atividade 2."""

import hashlib
import hmac
import os
import re
import secrets
from decimal import Decimal, InvalidOperation
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import ForeignKey, Integer, Numeric, String, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


load_dotenv(Path(__file__).resolve().parent / ".env")


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    # A mesma tabela da atividade anterior: as contas já cadastradas continuam válidas.
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    salt: Mapped[str] = mapped_column(String(32), nullable=False)
    hash_senha: Mapped[str] = mapped_column(String(64), nullable=False)


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(80), nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    raca: Mapped[str] = mapped_column(String(80), nullable=False)
    peso: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)
    cor: Mapped[str] = mapped_column(String(80), nullable=False)
    situacao: Mapped[str] = mapped_column(String(20), nullable=False, default="Tenho atualmente")


engine = None
SITUACOES = ("Tenho atualmente", "Já tive")


def _hash_senha(senha, salt):
    return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 200_000).hex()


def iniciar_banco():
    """Conecta ao MySQL, cria as tabelas e mantém compatibilidade com a atividade 2."""
    global engine
    if engine is not None:
        return

    nome_banco = os.getenv("MYSQL_DATABASE", "sistema_login")
    if not re.fullmatch(r"[A-Za-z0-9_]+", nome_banco):
        raise ValueError("Nome do banco de dados inválido.")

    url = URL.create(
        "mysql+pymysql",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=nome_banco,
        query={"charset": "utf8mb4"},
    )
    opcoes = {"connect_timeout": 8}
    certificado = os.getenv("MYSQL_SSL_CA", "").strip()
    if certificado:
        caminho = Path(certificado)
        if not caminho.is_absolute():
            caminho = Path(__file__).resolve().parent / caminho
        if not caminho.is_file():
            raise FileNotFoundError(f"Certificado SSL não encontrado: {caminho}")
        opcoes.update(ssl_ca=str(caminho), ssl_verify_cert=True, ssl_verify_identity=True)

    novo_engine = create_engine(url, pool_pre_ping=True, connect_args=opcoes)
    Base.metadata.create_all(novo_engine)
    engine = novo_engine

    # Exemplo para o professor testar num banco vazio. Não cria duplicatas.
    with Session(engine) as sessao:
        if sessao.scalar(select(Usuario.id).limit(1)) is None:
            salt = secrets.token_bytes(16)
            sessao.add(Usuario(nome="Fulano", salt=salt.hex(), hash_senha=_hash_senha("1234", salt)))
            sessao.commit()


def autenticar(login, senha):
    """Retorna (id, login) da pessoa autenticada, ou None."""
    with Session(engine) as sessao:
        usuario = sessao.scalar(select(Usuario).where(Usuario.nome == login.strip()))
        if usuario is None:
            return None
        recebido = _hash_senha(senha, bytes.fromhex(usuario.salt))
        if not hmac.compare_digest(recebido, usuario.hash_senha):
            return None
        return usuario.id, usuario.nome


def criar_usuario(login, senha):
    login = login.strip()
    if not login or len(login) > 80:
        raise ValueError("O login deve ter entre 1 e 80 caracteres.")
    if not senha:
        raise ValueError("Informe uma senha.")

    salt = secrets.token_bytes(16)
    with Session(engine) as sessao:
        sessao.add(Usuario(nome=login, salt=salt.hex(), hash_senha=_hash_senha(senha, salt)))
        try:
            sessao.commit()
            return True
        except IntegrityError:
            sessao.rollback()
            return False


def _validar_pet(nome, idade, raca, peso, cor, situacao):
    nome, raca, cor = nome.strip(), raca.strip(), cor.strip()
    if not all((nome, raca, cor)):
        raise ValueError("Preencha nome, raça e cor do PET.")
    if any(len(texto) > 80 for texto in (nome, raca, cor)):
        raise ValueError("Nome, raça e cor devem ter até 80 caracteres.")

    try:
        idade = int(idade)
    except (ValueError, TypeError) as exc:
        raise ValueError("Informe uma idade inteira.") from exc
    if not 0 <= idade <= 200:
        raise ValueError("A idade deve estar entre 0 e 200 anos.")

    try:
        peso = Decimal(str(peso).strip().replace(",", "."))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Informe um peso válido em kg (ex.: 4,50).") from exc
    if not peso.is_finite() or not Decimal("0") < peso <= Decimal("99999.99"):
        raise ValueError("O peso deve ser maior que zero e até 99999,99 kg.")
    peso = peso.quantize(Decimal("0.01"))
    if peso == 0:
        raise ValueError("O peso deve ser maior que zero.")

    if situacao not in SITUACOES:
        raise ValueError("Selecione a situação do PET.")
    return nome, idade, raca, peso, cor, situacao


def cadastrar_pet(usuario_id, nome, idade, raca, peso, cor, situacao):
    dados = _validar_pet(nome, idade, raca, peso, cor, situacao)
    with Session(engine) as sessao:
        pet = Pet(usuario_id=usuario_id)
        pet.nome, pet.idade, pet.raca, pet.peso, pet.cor, pet.situacao = dados
        sessao.add(pet)
        sessao.flush()
        identificador = pet.id
        sessao.commit()
        return identificador


def listar_pets(usuario_id):
    """A consulta SEMPRE restringe os resultados ao usuário logado."""
    with Session(engine) as sessao:
        pets = sessao.scalars(
            select(Pet).where(Pet.usuario_id == usuario_id).order_by(Pet.id.desc())
        ).all()
        return [
            (p.id, p.nome, p.idade, p.raca, p.peso, p.cor, p.situacao)
            for p in pets
        ]


def atualizar_pet(usuario_id, pet_id, nome, idade, raca, peso, cor, situacao):
    dados = _validar_pet(nome, idade, raca, peso, cor, situacao)
    with Session(engine) as sessao:
        pet = sessao.scalar(select(Pet).where(Pet.id == pet_id, Pet.usuario_id == usuario_id))
        if pet is None:
            return False
        pet.nome, pet.idade, pet.raca, pet.peso, pet.cor, pet.situacao = dados
        sessao.commit()
        return True


def excluir_pet(usuario_id, pet_id):
    with Session(engine) as sessao:
        pet = sessao.scalar(select(Pet).where(Pet.id == pet_id, Pet.usuario_id == usuario_id))
        if pet is None:
            return False
        sessao.delete(pet)
        sessao.commit()
        return True
