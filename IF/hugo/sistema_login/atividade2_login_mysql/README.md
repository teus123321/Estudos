# Atividade 2 — Sistema de login em wxPython com MySQL e SQLAlchemy

Sistema de login e redefinição de senha com uma demonstração de operações no MySQL: cadastro de novos usuários, listagem e consulta por ID e nome.

## Funcionalidades

- Login com usuário e senha consultados no MySQL.
- Acesso à segunda janela somente depois da autenticação.
- Redefinição de senha persistida no banco de dados.
- Consulta do ID e nome do usuário que entrou no sistema.
- Cadastro de novos usuários com nome, senha e confirmação.
- Consulta da lista de usuários cadastrados, mostrando ID e nome.
- Possibilidade de sair e entrar com um usuário recém-criado.

Senhas são armazenadas como hash PBKDF2, com salt aleatório. A tabela `usuarios` contém `id`, `nome`, `salt` e `hash_senha`.

## Instalação (Windows / PowerShell)

Abra o terminal na pasta que contém `sistema_login.py` e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha o `.env` conforme a opção de conexão a seguir.

## Opção A — MySQL no Aiven (nuvem)

Use as informações de conexão do painel Overview do serviço MySQL:

```ini
MYSQL_HOST=HOST_COPIADO_DO_AIVEN
MYSQL_PORT=PORTA_COPIADA_DO_AIVEN
MYSQL_USER=avnadmin
MYSQL_PASSWORD=SENHA_DO_SEU_SERVICO
MYSQL_DATABASE=defaultdb
MYSQL_SSL_CA=ca.pem
```

Baixe o certificado CA do serviço e salve como `ca.pem` ao lado do programa. O serviço precisa estar ativo e o computador precisa de internet.

## Opção B — MySQL Server local do professor

O professor precisa ter **MySQL Server** instalado e rodando. O MySQL Workbench é apenas um cliente de gerenciamento e não substitui o servidor.

No Workbench, conectado ao servidor, execute uma única vez:

```sql
CREATE DATABASE IF NOT EXISTS sistema_login;
```

Configure `.env`:

```ini
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=SENHA_LOCAL_DO_MYSQL
MYSQL_DATABASE=sistema_login
MYSQL_SSL_CA=
```

Não é necessário modificar o código Python: a mesma versão funciona com MySQL local ou na nuvem, bastando preencher o `.env` corretamente e criar o banco local vazio antes da primeira execução.

## Executar

```powershell
python sistema_login.py
```

Se a tabela `usuarios` estiver vazia, será criado um usuário de demonstração:

- Usuário: `Fulano`
- Senha inicial: `1234`

## Demonstração para avaliação

1. Faça login com `Fulano` e `1234`.
2. Clique em **Consultar meu cadastro** para consultar o ID e o nome no MySQL.
3. Clique em **Cadastrar e listar usuários**.
4. Digite um novo nome de usuário, uma senha e sua confirmação; clique em **Cadastrar usuário**.
5. A lista exibirá os usuários existentes com ID e nome. Clique em **Recarregar lista** para realizar nova consulta.
6. Selecione um usuário e clique em **Ver selecionado** para exibir os dados obtidos na consulta.
7. Saia da conta e faça login com o usuário que acabou de cadastrar.
8. Volte à tela de login, redefina uma senha e confirme que a nova senha funciona após reiniciar o aplicativo.

O aplicativo gera automaticamente a tabela `usuarios` no banco já configurado. Ele não tenta criar outro banco de dados.

## Entrega pelo GitHub

Envie somente `sistema_login.py`, `credenciais.py`, `requirements.txt`, `.env.example`, `.gitignore` e `README.md`.

Nunca envie `.env`, `ca.pem`, `.venv`, senhas ou outros arquivos privados. Quem baixar o projeto precisará configurar acesso a um banco MySQL próprio e instalar as dependências.

**Observação:** este é um exemplo acadêmico; a redefinição de senha apenas pelo nome de usuário não seria segura em um sistema de produção.
