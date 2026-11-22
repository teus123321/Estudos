"""Cidade sugerida nos formulários e nas buscas. O usuário pode editar o campo."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Lê o arquivo de configuração local antes de procurar CIDADE_PADRAO.
load_dotenv(Path(__file__).with_name(".env"))
# Usa a cidade configurada ou Porto Velho quando a configuração estiver vazia.
CIDADE_PADRAO = os.getenv("CIDADE_PADRAO", "").strip() or "Porto Velho"
