import hashlib
import hmac
import os
import re
import secrets
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


load_dotenv(Path(__file__).resolve().parent / ".env")


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    salt: Mapped[str] = mapped_column(String(32), nullable=False)
    hash_senha: Mapped[str] = mapped_column(String(64), nullable=False)


engine = None


def senha_protegida(senha, salt):
    return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 200_000).hex()


def conectar():
    banco = os.getenv("MYSQL_DATABASE", "sistema_login")
    if not re.fullmatch(r"[a-zA-Z0-9_]+", banco):
        raise ValueError("O nome do banco deve conter somente letras, números e _.")

    url = URL.create(
        "mysql+pymysql",
        username=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=banco,
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
        opcoes["ssl_ca"] = str(caminho)
        opcoes["ssl_verify_cert"] = True
        opcoes["ssl_verify_identity"] = True

    conexao_banco = create_engine(url, pool_pre_ping=True, connect_args=opcoes)
    Base.metadata.create_all(conexao_banco)
    return conexao_banco


def iniciar_banco():
    global engine
    if engine is None:
        engine = conectar()

    with Session(engine) as sessao:
        usuario = sessao.scalar(select(Usuario.id).limit(1))
        if usuario is None:
            salt = secrets.token_bytes(16)
            novo = Usuario(
                nome="Fulano",
                salt=salt.hex(),
                hash_senha=senha_protegida("1234", salt),
            )
            sessao.add(novo)
            sessao.commit()


def autenticar(usuario, senha):
    with Session(engine) as sessao:
        cadastrado = sessao.scalar(select(Usuario).where(Usuario.nome == usuario))
        if cadastrado is None:
            return False
        recebido = senha_protegida(senha, bytes.fromhex(cadastrado.salt))
        return hmac.compare_digest(recebido, cadastrado.hash_senha)


def redefinir_senha(usuario, nova_senha):
    with Session(engine) as sessao:
        cadastrado = sessao.scalar(select(Usuario).where(Usuario.nome == usuario))
        if cadastrado is None:
            return False
        salt = secrets.token_bytes(16)
        cadastrado.salt = salt.hex()
        cadastrado.hash_senha = senha_protegida(nova_senha, salt)
        sessao.commit()
        return True


def cadastrar_usuario(nome, senha):
    nome = nome.strip()
    if not nome or len(nome) > 80:
        raise ValueError("O nome deve ter entre 1 e 80 caracteres.")
    if not senha:
        raise ValueError("Informe uma senha para o novo usuário.")

    with Session(engine) as sessao:
        existente = sessao.scalar(select(Usuario.id).where(Usuario.nome == nome))
        if existente is not None:
            return False

        salt = secrets.token_bytes(16)
        sessao.add(
            Usuario(
                nome=nome,
                salt=salt.hex(),
                hash_senha=senha_protegida(senha, salt),
            )
        )
        try:
            sessao.commit()
        except IntegrityError:
            sessao.rollback()
            return False
        return True


def listar_usuarios():
    with Session(engine) as sessao:
        linhas = sessao.execute(select(Usuario.id, Usuario.nome).order_by(Usuario.id)).all()
        return [(identificador, nome) for identificador, nome in linhas]


def consultar_usuario(nome):
    with Session(engine) as sessao:
        linha = sessao.execute(
            select(Usuario.id, Usuario.nome).where(Usuario.nome == nome)
        ).first()
        if linha is None:
            return None
        return linha.id, linha.nome
