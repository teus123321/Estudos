import hashlib
import hmac
import json
import secrets
from pathlib import Path


ARQUIVO = Path(__file__).resolve().parent / "usuario.json"
ITERACOES = 200_000


def salvar_login(usuario, senha):
    salt = secrets.token_bytes(16)
    hash_senha = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), salt, ITERACOES
    )
    dados = {
        "usuario": usuario,
        "salt": salt.hex(),
        "hash_senha": hash_senha.hex(),
    }
    ARQUIVO.write_text(json.dumps(dados, indent=4, ensure_ascii=False), encoding="utf-8")


def iniciar_arquivo():
    if not ARQUIVO.exists():
        salvar_login("Fulano", "1234")


def ler_login():
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


def autenticar(usuario, senha):
    dados = ler_login()
    if usuario != dados["usuario"]:
        return False

    salt = bytes.fromhex(dados["salt"])
    esperado = bytes.fromhex(dados["hash_senha"])
    recebido = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), salt, ITERACOES
    )
    return hmac.compare_digest(recebido, esperado)


def redefinir_senha(usuario, nova_senha):
    dados = ler_login()
    if usuario != dados["usuario"]:
        return False

    salvar_login(usuario, nova_senha)
    return True
