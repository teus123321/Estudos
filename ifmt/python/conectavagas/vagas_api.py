"""Vagas reais da API pública para desenvolvedores da Adzuna.

NÃO consulta o LinkedIn: a API do LinkedIn para vagas exige parceria/acesso específico.
As vagas externas são apenas exibidas: o usuário se candidata no site de origem.
"""
from regiao import CIDADE_PADRAO
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / ".env")


class ErroAPI(Exception):
    """Falha amigável que a interface pode exibir em uma mensagem."""


def url_segura(url):
    """Só permite links externos HTTP(S) com domínio, nunca javascript:, file:, etc."""
    try:
        partes = urlparse(url)
        return partes.scheme in {"http", "https"} and bool(partes.netloc)
    except (TypeError, ValueError):
        return False


def formatar_vaga(item):
    """Transforma um registro JSON da Adzuna em um dicionário simples para a tela."""
    location = item.get("location") or {}
    area = location.get("display_name", "Não informada") if isinstance(location, dict) else "Não informada"
    company = item.get("company") or {}
    empresa = company.get("display_name", "Não informada") if isinstance(company, dict) else "Não informada"
    link = item.get("redirect_url", "")
    if not url_segura(link):
        link = ""
    return {"titulo": str(item.get("title") or "Sem título"),
            "empresa": str(empresa), "cidade": str(area),
            "descricao": str(item.get("description") or "Consulte o anúncio original."),
            "url": link}


def buscar_vagas_externas(termo="estágio", local=CIDADE_PADRAO, limite=15):
    """Faz GET HTTPS à Adzuna. Requer ADZUNA_APP_ID e ADZUNA_APP_KEY no .env."""
    app_id = os.getenv("ADZUNA_APP_ID", "").strip()
    app_key = os.getenv("ADZUNA_APP_KEY", "").strip()
    if not app_id or not app_key:
        raise ErroAPI("Para buscar vagas externas, preencha ADZUNA_APP_ID e ADZUNA_APP_KEY no .env.")

    if not 1 <= limite <= 50:
        raise ValueError("O limite deve ser entre 1 e 50.")
    params = urlencode({"app_id": app_id, "app_key": app_key,
                        "results_per_page": limite,
                        "what": termo.strip() or "estágio",
                        "where": local.strip(),
                        "content-type": "application/json"})
    url = f"https://api.adzuna.com/v1/api/jobs/br/search/1?{params}"
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "ConectaVagas-Academico/1.0"})
    try:
        with urlopen(request, timeout=10) as response:
            resposta = json.load(response)
    except HTTPError as erro:
        if erro.code in (401, 403):
            raise ErroAPI("API recusou as credenciais. Confira app_id e app_key.") from erro
        if erro.code == 429:
            raise ErroAPI("Limite de consultas à API atingido. Tente mais tarde.") from erro
        raise ErroAPI(f"Não foi possível consultar a API (HTTP {erro.code}).") from erro
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as erro:
        raise ErroAPI("Falha na consulta. Verifique internet, conexão e serviço Adzuna.") from erro
    return [formatar_vaga(item) for item in resposta.get("results", []) if isinstance(item, dict)]


def url_pesquisa_linkedin(termo="estágio", local=CIDADE_PADRAO):
    """Link de pesquisa para o site do LinkedIn, SEM extrair dados por API."""
    params = urlencode({"keywords": termo.strip() or "estágio", "location": local.strip() or "Brasil"})
    return "https://www.linkedin.com/jobs/search/?" + params
