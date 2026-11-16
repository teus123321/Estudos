# Terceira atividade avaliativa — Cadastro de PETs

**Aluno:** Mateus Henrique Gonçalves dos Santos  
**Curso:** Sistemas de Informação — IFMT

Este programa continua a atividade anterior de login com **Python, wxPython, MySQL e SQLAlchemy**.

## O que faz

1. Permite criar um usuário com **login e senha**.
2. Só permite acessar a tela de PETs após fazer **login**.
3. Cadastra cada PET com os cinco dados solicitados: **nome, idade, raça, peso e cor**.
4. Mostra todos os PETs que o usuário cadastrou, incluindo os que tem ou já teve.
5. Salva os dados no **MySQL**, mesmo após fechar o programa.
6. Cada usuário vê **somente os seus próprios PETs**, porque o cadastro é vinculado ao seu ID.

O programa utiliza a tabela `usuarios` da atividade 2 e cria a tabela `pets` automaticamente no mesmo banco.

## Como executar no Windows

Abra o PowerShell na pasta do projeto e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

No MySQL Workbench, conectado ao **servidor MySQL**, crie o banco caso ainda não exista:

```sql
CREATE DATABASE IF NOT EXISTS sistema_login;
```

Edite o arquivo `.env` e coloque os dados da sua conexão:

```ini
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=SUA_SENHA_DO_MYSQL
MYSQL_DATABASE=sistema_login
MYSQL_SSL_CA=
```

Se o banco da atividade 2 já funciona, pode usar a mesma configuração de conexão. Para MySQL na nuvem que exija certificado, informe o caminho em `MYSQL_SSL_CA` (exemplo: `ca.pem`).

Agora execute:

```powershell
python app.py
```

## Exemplo para apresentar ao professor

- Num banco sem usuários, o sistema cria o login de demonstração **Fulano**, senha **1234**.
- Entre e cadastre: **Rex**, **5** anos, **Vira-lata**, **12,5** kg, cor **Caramelo**.
- O Rex aparecerá na lista. Feche o programa e abra novamente para verificar que foi salvo.
- Para demonstrar o acesso individual, saia, digite outro login e senha e clique em **Criar usuário**. Entre com essa conta: a lista estará vazia, pois cada pessoa acessa somente os próprios PETs.

**Arquivos:** `app.py` (telas), `banco.py` (MySQL), `requirements.txt`, `.env.example` e `.gitignore`.

> Não envie seu arquivo `.env` nem suas senhas reais ao GitHub. A senha 1234 é apenas um exemplo para a atividade.
