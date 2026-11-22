"""Cidade sugerida nos formulários e nas buscas. O usuário pode editar o campo."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))
CIDADE_PADRAO = os.getenv("CIDADE_PADRAO", "").strip() or "Porto Velho"
