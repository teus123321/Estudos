"""Testes do banco com SQLite TEMPORÁRIO: não substitui o MySQL do trabalho.

Em desenvolvimento, verificam as regras sem precisar de servidor MySQL.
A aplicação real SEMPRE usa MySQL, configurado em banco.iniciar_banco().
"""
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import banco


@pytest.fixture(autouse=True)
def banco_isolado():
    anterior = banco.engine
    banco.engine = create_engine("sqlite+pysqlite:///:memory:")
    banco.Base.metadata.create_all(banco.engine)
    yield
    banco.engine.dispose()
    banco.engine = anterior


def criar_contas():
    empresa = banco.cadastrar_usuario("Empresa de Teste", "empresa@example.com", "senha123456", "empresa")
    candidato = banco.cadastrar_usuario("Pessoa de Teste", "pessoa@example.com", "senha123456", "candidato")
    return empresa, candidato


def criar_vaga(empresa):
    return banco.criar_vaga(empresa, "Estágio em suporte", "Tecnologia",
                           "Auxiliar no suporte ao cliente e na organização do laboratório.",
                           "Estar cursando tecnologia.", "Porto Velho - RO",
                           "Presencial", "Estágio", "Bolsa a combinar")


def test_login_e_hash():
    empresa, candidato = criar_contas()
    assert banco.autenticar("PESSOA@example.com", "senha123456")["id"] == candidato
    assert banco.autenticar("pessoa@example.com", "senhaerrada") is None
    with Session(banco.engine) as sessao:
        usuario = sessao.get(banco.Usuario, candidato)
        assert usuario.hash_senha != "senha123456"
        assert len(usuario.salt) == 32


def test_email_duplicado_e_senha_curta():
    criar_contas()
    with pytest.raises(ValueError, match="já está cadastrado"):
        banco.cadastrar_usuario("Outro", "PESSOA@example.com", "senha123456", "candidato")
    with pytest.raises(ValueError, match="pelo menos 8"):
        banco.cadastrar_usuario("Outro", "outro@example.com", "123", "candidato")


def test_vaga_visivel_na_busca_e_restrita_a_empresa():
    empresa, candidato = criar_contas()
    vaga_id = criar_vaga(empresa)
    assert banco.obter_vaga(vaga_id)["empresa"] == "Empresa de Teste"
    assert len(banco.listar_vagas("suporte", "Porto Velho")) == 1
    assert banco.listar_vagas("marketing", "Porto Velho") == []
    with pytest.raises(ValueError, match="Somente uma conta de empresa"):
        criar_vaga(candidato)


def test_candidatura_duplicada_e_permissoes():
    empresa, candidato = criar_contas()
    vaga_id = criar_vaga(empresa)
    banco.candidatar(candidato, vaga_id, "Tenho disponibilidade para estágio.")
    assert len(banco.minhas_candidaturas(candidato)) == 1
    assert len(banco.candidatos_da_vaga(empresa, vaga_id)) == 1
    with pytest.raises(ValueError, match="já se candidatou"):
        banco.candidatar(candidato, vaga_id)
    with pytest.raises(ValueError, match="Somente candidatos"):
        banco.candidatar(empresa, vaga_id)
    with pytest.raises(ValueError, match="não tem acesso"):
        banco.candidatos_da_vaga(candidato, vaga_id)


def test_empresa_controla_somente_suas_vagas():
    empresa, candidato = criar_contas()
    vaga_id = criar_vaga(empresa)
    outra_empresa = banco.cadastrar_usuario("Empresa 2", "empresa2@example.com", "senha123456", "empresa")
    with pytest.raises(ValueError, match="não encontrada para esta empresa"):
        banco.mudar_situacao_vaga(outra_empresa, vaga_id, False)
    banco.mudar_situacao_vaga(empresa, vaga_id, False)
    assert banco.listar_vagas() == []
    with pytest.raises(ValueError, match="não está disponível"):
        banco.candidatar(candidato, vaga_id)
    banco.mudar_situacao_vaga(empresa, vaga_id, True)
    assert len(banco.listar_vagas()) == 1


def test_aprovacao_apenas_pelo_dono():
    empresa, candidato = criar_contas()
    vaga_id = criar_vaga(empresa)
    banco.candidatar(candidato, vaga_id)
    candidatura = banco.candidatos_da_vaga(empresa, vaga_id)[0]
    with pytest.raises(ValueError, match="não pode alterar"):
        banco.mudar_status_candidatura(candidato, candidatura["id"], "Aprovada")
    banco.mudar_status_candidatura(empresa, candidatura["id"], "Em análise")
    assert banco.minhas_candidaturas(candidato)[0]["status"] == "Em análise"


def test_edicao_perfil():
    _, candidato = criar_contas()
    banco.atualizar_perfil(candidato, "(69) 99999-0000", "Porto Velho", "Estudante buscando estágio.")
    perfil = banco.obter_usuario(candidato)
    assert perfil["resumo"] == "Estudante buscando estágio."
