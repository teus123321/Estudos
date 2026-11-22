"""Teste de parsing da API sem usar rede nem gastar requisições."""
import sys
from pathlib import Path
from unittest.mock import patch
import io
import json

import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import vagas_api


def test_converter_json_e_link():
    vaga = vagas_api.formatar_vaga({
        "title": "Estagiário de Desenvolvimento", "company": {"display_name": "Exemplo LTDA"},
        "location": {"display_name": "Rondônia"},
        "description": "Aprendizado de tecnologias", "redirect_url": "https://www.adzuna.com.br/jobs/details/123"
    })
    assert vaga["titulo"] == "Estagiário de Desenvolvimento"
    assert vaga["empresa"] == "Exemplo LTDA"
    assert vaga["url"].startswith("https://")


def test_bloqueia_links_perigosos():
    assert not vagas_api.url_segura("javascript:alert(1)")
    assert not vagas_api.url_segura("file:///etc/passwd")
    assert vagas_api.url_segura("https://www.linkedin.com/jobs/search/")


def test_falta_de_chave_api(monkeypatch):
    monkeypatch.delenv("ADZUNA_APP_ID", raising=False)
    monkeypatch.delenv("ADZUNA_APP_KEY", raising=False)
    with pytest.raises(vagas_api.ErroAPI, match="preencha ADZUNA"):
        vagas_api.buscar_vagas_externas()


class RespostaFalsa:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False
    def read(self, *args):
        return json.dumps({"results": [{"title": "Estágio em TI", "redirect_url": "https://example.com/vaga"}]}).encode()


def test_chamada_http_simulada(monkeypatch):
    monkeypatch.setenv("ADZUNA_APP_ID", "teste")
    monkeypatch.setenv("ADZUNA_APP_KEY", "chave_teste")
    with patch.object(vagas_api, "urlopen", return_value=RespostaFalsa()) as mock_urlopen:
        resultados = vagas_api.buscar_vagas_externas("estágio", "Ji-Paraná")
    assert len(resultados) == 1
    assert resultados[0]["titulo"] == "Estágio em TI"
    assert mock_urlopen.call_args.kwargs["timeout"] == 10
