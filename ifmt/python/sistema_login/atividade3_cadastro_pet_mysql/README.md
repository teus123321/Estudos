# Terceira atividade avaliativa — Cadastro de PETs

**Disciplina:** Programação em Python — IFMT  
**Aluno:** Mateus Henrique Gonçalves dos Santos

Aplicação de desktop feita em **Python, wxPython, MySQL e SQLAlchemy**, como continuação da [atividade 2 (sistema de login)](../atividade2_login_mysql/README.md).

## O que o programa faz

- Login com usuário e senha, validados no MySQL.
- Criação de contas com senha armazenada em hash PBKDF2 e salt aleatório.
- Cadastro de PETs com **nome, idade, raça, peso e cor**.
- Campo adicional **situação** ("Tenho atualmente" ou "Já tive") para manter o histórico dos animais ao longo da vida.
- Listagem, edição e exclusão dos PETs cadastrados.
- **Isolamento por usuário:** cada PET pertence ao ID da conta autenticada. Uma pessoa não consegue listar, alterar ou excluir os PETs de outra conta, mesmo que saiba o ID do animal.
- Dados mantidos no MySQL após fechar e reabrir a aplicação.

O programa reutiliza a tabela `usuarios` da atividade anterior e cria automaticamente a tabela `pets` (com a coluna `usuario_id` como chave estrangeira). Cada operação sobre PETs confere a conta que fez login.

## Arquivos

| Arquivo | Função |
| --- | --- |
| `app.py` | Janelas de login, cadastro de conta e gerenciamento de PETs (wxPython). |
| `banco.py` | Tabelas e operações no MySQL, autenticação e vínculo entre usuário e PET. |
| `requirements.txt` | Dependências Python. |
| `.env.example` | Modelo de configuração do banco de dados. |
| `tests/test_banco.py` | Testes das regras de cadastro e isolamento de dados. |

## Como instalar (Windows / PowerShell)

1. Instale Python 3.10 ou superior e tenha um servidor MySQL disponível.
2. Abra o terminal **dentro desta pasta** e execute:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

3. Em um MySQL local, execute uma vez no MySQL Workbench:

   ```sql
   CREATE DATABASE IF NOT EXISTS sistema_login;
   ```

4. Edite o arquivo `.env` com seu usuário e senha do MySQL:

   ```ini
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=SUA_SENHA_DO_MYSQL
   MYSQL_DATABASE=sistema_login
   MYSQL_SSL_CA=
   ```

   Se já utilizou a atividade 2, use **as mesmas informações de conexão** para entrar com as contas anteriores. O sistema não apaga nem altera os usuários já existentes.

   Para MySQL hospedado no Aiven, configure host, porta, usuário, senha e banco conforme o painel do serviço. Se o serviço exigir certificado CA, coloque o arquivo `ca.pem` nesta pasta e informe `MYSQL_SSL_CA=ca.pem`. Não publique o certificado nem as credenciais.

5. Execute:

   ```powershell
   python app.py
   ```

O programa cria automaticamente as tabelas dentro do banco informado, mas **não cria o banco de dados em si**. O MySQL precisa estar iniciado. Não basta ter apenas o MySQL Workbench instalado.

## Como demonstrar ao professor

1. Em um banco novo, entre com login **Fulano** e senha **1234** (conta de demonstração criada apenas quando a tabela de usuários está vazia).
2. Cadastre, por exemplo: **Rex**, 5 anos, **Vira-lata**, **12,50 kg**, **Caramelo**, situação **Tenho atualmente**.
3. Cadastre outro PET com a situação **Já tive**. Ambos aparecerão na lista.
4. Selecione o Rex na lista, altere um campo e clique em **Salvar alterações**.
5. Saia da conta e clique em **Criar conta**; crie outro login e entre nele.
6. Confira que a segunda conta **não vê os PETs do Fulano**. Cadastre um PET próprio.
7. Volte ao Fulano: só os PETs dele estarão visíveis. Selecione um PET e experimente **Excluir selecionado**.
8. Feche e abra o sistema para confirmar que os registros restantes continuam armazenados.

## Testes

Os testes da camada de banco usam SQLite temporário, sem precisar de um servidor MySQL. Com as dependências instaladas, execute na pasta do projeto:

```powershell
python -m unittest discover -s tests -v
```

Para validar a interface gráfica e a conexão real, siga também a demonstração acima com MySQL em execução.

## Importante

- Nunca envie `.env`, `ca.pem` ou senhas reais ao GitHub.
- A conta **Fulano / 1234** é apenas para avaliação. Em um sistema real, altere-a e use regras mais fortes de senha.
- O programa é acadêmico e foi pensado para uso local.
