@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Ambiente virtual nao encontrado.
  echo Siga a instalacao no README.md ou docs\tutorial_de_uso.md.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" app.py
if errorlevel 1 (
  echo.
  echo Falha na inicializacao. Confira o servidor MySQL e o arquivo .env.
  pause
)
