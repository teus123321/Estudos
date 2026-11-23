"""Funções que executam SQL no MySQL. Cada função atende uma ação da tela."""
import hashlib
import hmac
import secrets

import mysql.connector
from config import BANCO


def conectar():
    # BANCO contém host, usuário, senha e nome do banco definidos em config.py.
    return mysql.connector.connect(**BANCO)


def cadastrar_usuario(nome, email, senha):
    """Valida o cadastro e salva uma conta com senha protegida."""
    nome, email = nome.strip(), email.strip().lower()
    if not nome or '@' not in email or len(nome) > 100 or len(email) > 150:
        raise ValueError('Informe nome e e-mail válidos, respeitando o tamanho dos campos.')
    if len(senha) < 8:
        raise ValueError('A senha precisa ter pelo menos 8 caracteres.')
    # O salt aleatório faz duas senhas iguais gerarem hashes diferentes.
    salt = secrets.token_hex(16)
    resumo = hashlib.pbkdf2_hmac('sha256', senha.encode(), bytes.fromhex(salt), 260000).hex()
    conexao = conectar()
    try:
        with conexao.cursor() as cursor:
            # %s são parâmetros. O conector envia os valores de forma segura.
            cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)',
                           (nome, email, salt + ':' + resumo))
        conexao.commit()  # Confirma a gravação no MySQL.
    except mysql.connector.IntegrityError as erro:
        raise ValueError('Este e-mail já está cadastrado.') from erro
    finally:
        conexao.close()  # Fecha a conexão mesmo se acontecer um erro.


def entrar(email, senha):
    """Busca a conta e confere a senha. Devolve o usuário ou None."""
    conexao = conectar()
    try:
        # dictionary=True permite acessar usuario['nome'], por exemplo.
        with conexao.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email.strip().lower(),))
            usuario = cursor.fetchone()  # Recebe uma linha ou None.
        if usuario:
            salt, esperado = usuario['senha'].split(':')
            recebido = hashlib.pbkdf2_hmac('sha256', senha.encode(), bytes.fromhex(salt), 260000).hex()
            if hmac.compare_digest(recebido, esperado):
                del usuario['senha']
                return usuario
        return None
    finally:
        conexao.close()


def listar_vagas(busca):
    """Consulta anúncios com o nome de quem publicou."""
    conexao = conectar()
    try:
        with conexao.cursor(dictionary=True) as cursor:
            # JOIN liga a vaga ao usuário. LIKE permite pesquisar parte do título.
            cursor.execute('''SELECT vagas.*, usuarios.nome AS anunciante
                              FROM vagas JOIN usuarios ON usuarios.id = vagas.usuario_id
                              WHERE vagas.titulo LIKE %s ORDER BY vagas.id DESC''',
                           ('%' + busca.strip() + '%',))
            return cursor.fetchall()  # Devolve uma lista de dicionários.
    finally:
        conexao.close()


def publicar_vaga(usuario_id, titulo, empresa, cidade, descricao, contato):
    """Grava o anúncio, associado ao usuário que está logado."""
    titulo, empresa, cidade = titulo.strip(), empresa.strip(), cidade.strip()
    descricao, contato = descricao.strip(), contato.strip()
    if not all((titulo, empresa, cidade, descricao, contato)):
        raise ValueError('Preencha todos os campos da vaga.')
    if len(titulo) > 120 or len(empresa) > 100 or len(cidade) > 100 or len(contato) > 150:
        raise ValueError('Título até 120, empresa e cidade até 100 e contato até 150 caracteres.')
    conexao = conectar()
    try:
        with conexao.cursor() as cursor:
            cursor.execute('''INSERT INTO vagas
                              (usuario_id, titulo, empresa, cidade, descricao, contato)
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           (usuario_id, titulo, empresa, cidade, descricao, contato))
        conexao.commit()
    finally:
        conexao.close()


def excluir_vaga(vaga_id, usuario_id):
    """Exclui somente se a vaga pertencer ao usuário logado."""
    conexao = conectar()
    try:
        with conexao.cursor() as cursor:
            cursor.execute('DELETE FROM vagas WHERE id = %s AND usuario_id = %s',
                           (vaga_id, usuario_id))
        conexao.commit()
    finally:
        conexao.close()
