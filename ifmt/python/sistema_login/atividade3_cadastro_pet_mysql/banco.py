"""Banco MySQL: usuários, login e cadastro de PETs."""

import hashlib
import hmac
import os
import re
import secrets
from decimal import Decimal, InvalidOperation
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import ForeignKey, Numeric, String, create_engine, select
from sqlalchemy.engine import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


load_dotenv(Path(__file__).resolve().parent / ".env")


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    # Mesma estrutura da atividade 2: permite usar as contas anteriores.
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    salt: Mapped[str] = mapped_column(String(32), nullable=False)
    hash_senha: Mapped[str] = mapped_column(String(64), nullable=False)


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    nome: Mapped[str] = mapped_column(String(80), nullable=False)
    idade: Mapped[int] = mapped_column(nullable=False)
    raca: Mapped[str] = mapped_column(String(80), nullable=False)
    peso: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)
    cor: Mapped[str] = mapped_column(String(80), nullable=False)


engine = None


def proteger_senha(senha, salt):
    return hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 200_000).hex()


def iniciar_banco():
    global engine
    nome_banco = os.getenv("MYSQL_DATABASE", "sistema_login")
    if not re.fullmatch(r"[A-Za-z0-9_]+", nome_banco):
        raise ValueError("Nome do banco inválido.")

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
            raise FileNotFoundError("Certificado SSL não encontrado.")
        opcoes.update(ssl_ca=str(caminho), ssl_verify_cert=True, ssl_verify_identity=True)

    engine = create_engine(url, pool_pre_ping=True, connect_args=opcoes)
    Base.metadata.create_all(engine)

    # Login inicial de exemplo, criado somente se não houver usuários no banco.
    with Session(engine) as sessao:
        if sessao.scalar(select(Usuario.id).limit(1)) is None:
            salt = secrets.token_bytes(16)
            sessao.add(Usuario(nome="Fulano", salt=salt.hex(), hash_senha=proteger_senha("1234", salt)))
            sessao.commit()


def autenticar(login, senha):
    with Session(engine) as sessao:
        usuario = sessao.scalar(select(Usuario).where(Usuario.nome == login.strip()))
        if usuario is None:
            return None
        senha_recebida = proteger_senha(senha, bytes.fromhex(usuario.salt))
        if hmac.compare_digest(senha_recebida, usuario.hash_senha):
            return usuario.id, usuario.nome
        return None


def cadastrar_usuario(login, senha):
    login = login.strip()
    if not login or len(login) > 80 or not senha:
        raise ValueError("Informe um login (até 80 caracteres) e uma senha.")
    salt = secrets.token_bytes(16)
    with Session(engine) as sessao:
        sessao.add(Usuario(nome=login, salt=salt.hex(), hash_senha=proteger_senha(senha, salt)))
        try:
            sessao.commit()
            return True
        except IntegrityError:
            sessao.rollback()
            return False


def cadastrar_pet(usuario_id, nome, idade, raca, peso, cor):
    nome, raca, cor = nome.strip(), raca.strip(), cor.strip()
    if not all((nome, raca, cor)) or any(len(x) > 80 for x in (nome, raca, cor)):
        raise ValueError("Preencha nome, raça e cor (até 80 caracteres cada).")
    try:
        idade = int(idade)
    except (TypeError, ValueError) as erro:
        raise ValueError("A idade precisa ser um número inteiro.") from erro
    if not 0 <= idade <= 200:
        raise ValueError("A idade deve ser de 0 a 200 anos.")
    try:
        peso = Decimal(str(peso).strip().replace(",", "."))
    except (InvalidOperation, ValueError) as erro:
        raise ValueError("Informe o peso em kg, por exemplo: 4,5.") from erro
    if not peso.is_finite() or not Decimal("0") < peso <= Decimal("99999.99"):
        raise ValueError("O peso deve ser maior que zero.")
    peso = peso.quantize(Decimal("0.01"))
    if peso == 0:
        raise ValueError("Informe um peso de pelo menos 0,01 kg.")

    with Session(engine) as sessao:
        sessao.add(Pet(
            usuario_id=usuario_id,
            nome=nome,
            idade=idade,
            raca=raca,
            peso=peso,
            cor=cor,
        ))
        sessao.commit()


def listar_pets(usuario_id):
    # O filtro impede que uma conta veja os PETs de outra.
    with Session(engine) as sessao:
        pets = sessao.scalars(
            select(Pet).where(Pet.usuario_id == usuario_id).order_by(Pet.id)
        ).all()
        return [(p.nome, p.idade, p.raca, p.peso, p.cor) for p in pets]
