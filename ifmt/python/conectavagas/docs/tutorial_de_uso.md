# Tutorial de instalação e uso — ConectaVagas (wxPython + MySQL)

O enunciado cita Pontes e Lacerda (MT). Para apresentar nessa região, ajuste `CIDADE_PADRAO=Pontes e Lacerda` no arquivo `.env` e reinicie o aplicativo. A configuração sugere a cidade nos novos cadastros e nas buscas. As vagas já gravadas conservam a cidade informada na publicação.

Este tutorial foi escrito para ser seguido **na máquina Windows da apresentação**, usando MySQL Workbench. Todos os comandos devem ser executados **na pasta extraída do projeto**, onde está `app.py`.

## 1. O que você precisa ter instalado

- **Python 3.11 ou 3.12 de 64 bits**. Escolhemos essas versões para reduzir problemas de compatibilidade do wxPython. Para verificar, rode `py -0p` ou `python --version` no PowerShell.
- **MySQL Server** iniciado na máquina (o serviço que guarda os dados).
- **MySQL Workbench** instalado e conectado ao servidor MySQL.
- Acesso à internet apenas para instalar pacotes e, opcionalmente, consultar a API Adzuna.

**Atenção:** o Workbench é uma ferramenta gráfica que permite administrar o MySQL; **não é o banco de dados em si**. O Python acessa o mesmo servidor que você vê no Workbench.

## 2. Criar o banco no MySQL Workbench

1. Abra o MySQL Workbench e entre na sua conexão local (geralmente `localhost:3306`).
2. Abra uma nova aba SQL.
3. Copie o comando abaixo, ou abra `sql/criar_banco.sql`:

   ```sql
   CREATE DATABASE IF NOT EXISTS conectavagas
       CHARACTER SET utf8mb4
       COLLATE utf8mb4_unicode_ci;
   ```

4. Clique no botão de raio (**Execute**) do Workbench.
5. Atualize `SCHEMAS` e procure o banco `conectavagas`.

Para estudar o SQL escrito por extenso, consulte também `sql/modelo_tabelas_opcional.sql` (não é necessário executá-lo).

**Por que só criar o banco?** As três tabelas (`usuarios`, `vagas` e `candidaturas`) são criadas automaticamente por `Base.metadata.create_all(engine)` no arquivo `banco.py`, na primeira execução do app.

## 3. Preparar o Python

Abra o PowerShell na pasta do projeto. Execute **um comando por vez**:

```powershell
py -3.11 -m venv .venv
```

Cria um ambiente virtual isolado para o projeto. Agora instale as bibliotecas:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

O arquivo instala `wxPython`, `SQLAlchemy`, `PyMySQL` e `python-dotenv`.

Se `py -3.11` não encontrar uma versão instalada, use `py -3.12` (se estiver instalado). Evite um Python muito novo sem pacote wxPython compatível.

## 4. Configurar a conexão

No PowerShell:

```powershell
Copy-Item .env.example .env
```

Abra o arquivo **`.env`** em um editor de texto. Exemplo:

```ini
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=SUA_SENHA_REAL
MYSQL_DATABASE=conectavagas
ADZUNA_APP_ID=
ADZUNA_APP_KEY=
```

Utilize o **mesmo host, porta, usuário e senha do servidor MySQL** usados na conexão do Workbench. Se não usa `root`, troque `MYSQL_USER` para o usuário real. A senha deve ser a do usuário no servidor, não a do login do aplicativo ConectaVagas.

**Segurança:** `.env` fica na sua máquina. Nunca envie esse arquivo para o GitHub, para colegas ou para o professor. O `.gitignore` já está configurado para impedir sua inclusão normal.

## 5. Executar o programa

Na pasta do projeto:

```powershell
.\.venv\Scripts\python.exe app.py
```

O aplicativo abrirá a janela **ConectaVagas | wxPython + MySQL**. Se aparecer erro de conexão, verifique:

- Se o **MySQL Server** está em execução.
- Se a conexão do Workbench utiliza `127.0.0.1` / `3306`, ou outra porta.
- Se o banco `conectavagas` existe.
- Se a senha em `.env` está correta.
- Se o usuário tem permissão para criar tabelas e gravar registros no banco.

Após abrir uma vez, no Workbench rode:

```sql
USE conectavagas;
SHOW TABLES;
```

Devem aparecer `usuarios`, `vagas` e `candidaturas`.

## 6. Demonstrar o sistema, passo a passo

### Etapa A — criar empresa e publicar uma vaga

1. Clique em **Cadastro**.
2. Selecione o tipo **Empresa**.
3. Informe nome da empresa (pode ser `Empresa Exemplo — demonstração`), e-mail e senha com pelo menos 8 caracteres.
4. Clique **Cadastrar**, depois **Login** e entre com essas credenciais.
5. Clique em **Publicar vaga** e preencha:

   - Título: `Estágio em Suporte Técnico (demonstração)`
   - Área: `Tecnologia da Informação`
   - Descrição: `Auxiliar no atendimento, configuração básica de computadores e registro de chamados.`
   - Requisitos: `Estar estudando informática; vontade de aprender.`
   - Cidade: `Porto Velho - RO`
   - Modalidade: `Presencial`
   - Contrato: `Estágio`
   - Remuneração: `Bolsa a combinar`

6. Clique **Publicar vaga**. A vaga deverá aparecer no **Painel da empresa** e na tela **Vagas**.

**Esses exemplos são fictícios** e servem exclusivamente à apresentação acadêmica. Não devem ser anunciados como vagas reais.

### Etapa B — cadastrar candidato e se inscrever

1. Clique em **Sair**.
2. Clique **Cadastro**; selecione **Candidato**.
3. Preencha nome, e-mail **diferente do da empresa** e senha.
4. Faça login como candidato.
5. Em **Perfil**, edite cidade, telefone e apresentação profissional.
6. Na tela **Vagas**, pesquise `suporte` e selecione a vaga da empresa de demonstração.
7. Clique **Ver detalhes da vaga**, escreva uma mensagem opcional e clique **Enviar candidatura**.
8. Abra **Minhas candidaturas**. O status inicial deverá ser `Enviada`.
9. Tente se candidatar novamente: o sistema deverá recusar duplicidade.

### Etapa C — empresa gerencia candidatos

1. Clique **Sair** e faça login novamente na conta de empresa.
2. Acesse **Painel empresa**; selecione a vaga e clique **Ver candidatos**.
3. Selecione a pessoa e clique **Ver contato e mensagem**.
4. Selecione `Em análise` na lista de situações e clique **Salvar situação**.
5. Faça login novamente como candidato e veja que a situação mudou em **Minhas candidaturas**.

**Ponto mais importante para defender:** esse fluxo foi salvo nas **três tabelas** do MySQL.

## 7. Conferir as tabelas no MySQL Workbench

Abra uma aba SQL no Workbench:

```sql
USE conectavagas;

-- Contas registradas
SELECT id, nome, email, tipo, cidade FROM usuarios;

-- Vagas vinculadas às empresas que publicaram
SELECT v.id, v.titulo, u.nome AS empresa, v.ativa
FROM vagas AS v
JOIN usuarios AS u ON v.empresa_id = u.id;

-- Candidaturas, candidatos e vagas
SELECT c.id, u.nome AS candidato, v.titulo AS vaga, c.status
FROM candidaturas AS c
JOIN usuarios AS u ON c.candidato_id = u.id
JOIN vagas AS v ON c.vaga_id = v.id;
```

**Cuidado:** não mostre na apresentação as colunas `salt` e `hash_senha` sem necessidade, e nunca revele senhas reais.

## 8. Consultar vagas reais pela API Adzuna (opcional)

1. Entre em https://developer.adzuna.com/ e verifique as condições para cadastrar uma aplicação e obter um `app_id` e um `app_key`.
2. Insira as credenciais no `.env`:

   ```ini
   ADZUNA_APP_ID=SEU_ID
   ADZUNA_APP_KEY=SUA_CHAVE
   ```

3. Reinicie o aplicativo.
4. Clique em **Vagas externas** e pesquise `estágio` em `Porto Velho`.
5. Caso não existam resultados, teste `Rondônia` ou `Ji-Paraná`. A API depende de anúncios existentes e pode retornar lista vazia.
6. Clique em **Abrir anúncio original** para ser encaminhado à página de origem.

**Sem as credenciais:** o aplicativo continuará funcionando normalmente com as vagas locais. Um aviso explicará por que a busca externa não pode ser feita.

**LinkedIn:** o botão **Pesquisar no site LinkedIn** apenas abre uma busca no navegador; **não retorna vagas para a lista via API**.

## 9. Código do grupo no GitHub

O projeto fica em [teus123321/Estudos, pasta conectavagas](https://github.com/teus123321/Estudos/tree/main/ifmt/python/conectavagas). Para baixar, abra o repositório, clique em **Code → Download ZIP**, extraia e entre em `ifmt/python/conectavagas` antes de executar os comandos.

## 10. Testes automatizados (opcional para o professor)

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest testes -q
```

Os testes automatizados usam **SQLite em memória para testar regras**, sem modificar o MySQL da apresentação. O aplicativo real usa MySQL. Os 11 testes passaram no ambiente de desenvolvimento, mas **não substituem o teste de interface** no Windows e a conexão real ao MySQL Server.

## 11. O que fazer se algo falhar na apresentação

- **Falha de internet:** não consulte a API, demonstre as vagas já gravadas no MySQL.
- **Falha de credenciais Adzuna:** mostre o tratamento de erro e explique a integração opcional.
- **Erro de MySQL:** confirme o serviço, a senha no `.env`, o nome do banco e as permissões.
- **Lista de vagas vazia:** cadastre uma empresa e publique uma vaga, ou clique em **Limpar filtros** na tela de vagas.
- **Falha do pacote wxPython:** revise a versão do Python e reinstale as dependências num ambiente 3.11/3.12 64 bits.
