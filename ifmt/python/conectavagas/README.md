# ConectaVagas — Aplicativo de empregos e estágios para Porto Velho

O enunciado cita Pontes e Lacerda (MT). Para apresentar nessa região, ajuste `CIDADE_PADRAO=Pontes e Lacerda` no arquivo `.env` e reinicie o aplicativo. A configuração sugere a cidade nos novos cadastros e nas buscas. As vagas já gravadas conservam a cidade informada na publicação.

**Trabalho acadêmico — Python + wxPython + MySQL + SQLAlchemy.**

O ConectaVagas é um **aplicativo desktop** voltado a uma necessidade social regional: facilitar o encontro entre pessoas que procuram uma primeira oportunidade de emprego/estágio e empresas que precisam contratar. O aplicativo não utiliza Flask, HTML ou CSS.

## Principais funções

- Candidato: criar conta, entrar, atualizar perfil, pesquisar vagas e se candidatar uma vez por vaga, acompanhar status.
- Empresa: criar conta, entrar, publicar/encerrar vagas e consultar/avaliar candidaturas recebidas.
- Visitante: pesquisar vagas locais e consultar vagas externas via Adzuna (se configurada).
- Integração com uma **API real de vagas**: Adzuna (opcional); os anúncios abrem no site de origem para candidatura. Há também um botão para **abrir uma busca no site do LinkedIn**, mas ele **não consulta a API do LinkedIn**.

## Tecnologias

| Parte | Tecnologia | Função |
|---|---|---|
| Interface | wxPython | Cria as janelas, botões, listas e formulários |
| Lógica | Python | Validação, navegação e regras do sistema |
| Persistência | SQLAlchemy | Converte objetos Python em consultas SQL |
| Driver | PyMySQL | Abre conexão com servidor MySQL |
| Banco | MySQL Server | Guarda usuários, vagas e candidaturas |
| Administração | MySQL Workbench | Criação, inspeção e consulta do banco |
| API externa | Adzuna via urllib | Consulta anúncios externos em JSON |

> **Workbench não é um banco separado.** Python e Workbench acessam o **mesmo servidor MySQL**, usando os dados de conexão (`host`, `port`, `usuário`, `senha` e banco).

## 12 telas navegáveis

1. Início
2. Login
3. Criar conta
4. Listar/pesquisar vagas locais
5. Detalhes de uma vaga e candidatura
6. Minhas candidaturas
7. Meu perfil
8. Painel da empresa
9. Publicar vaga
10. Ver candidatos da vaga
11. Vagas externas (Adzuna e acesso ao site do LinkedIn)
12. Sobre o sistema

As telas são classes `wx.ScrolledWindow` exibidas na mesma janela principal `wx.Frame`. **São telas navegáveis, não doze janelas independentes.**

## Instalação rápida (Windows)

**Pré-requisitos:** Python 3.11 ou 3.12 (64 bits), MySQL Server em execução e MySQL Workbench.

1. Abra `sql/criar_banco.sql` no Workbench e execute o comando `CREATE DATABASE`.
2. Abra um PowerShell na pasta do projeto e rode:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

3. Edite `.env` e informe `MYSQL_USER`, `MYSQL_PASSWORD` etc. Esse arquivo **não deve ser enviado ao GitHub**.
4. Execute:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

5. Cadastre uma conta **Empresa**, crie uma vaga; saia, crie conta **Candidato** e se inscreva. Nas próximas vezes, você pode usar `iniciar_windows.bat` para abrir o aplicativo.

**Se seu Python não atende `py -3.11`:** use `py -3.12` ou o comando de um Python 3.11/3.12 que já esteja instalado. wxPython exige uma versão com wheel compatível no Windows.

## Estrutura do projeto

```text
ConectaVagas_wxPython/
├── app.py                         # Todas as 12 telas wxPython
├── banco.py                       # Tabelas e funções MySQL/SQLAlchemy
├── vagas_api.py                   # Busca HTTP na Adzuna e link LinkedIn
├── requirements.txt               # Bibliotecas Python
├── iniciar_windows.bat            # Abre o app apos a instalacao (Windows)
├── .env.example                   # Modelo de credenciais
├── .gitignore                     # Protege .env e .venv
├── sql/
│   ├── criar_banco.sql            # Comando para executar no Workbench
│   └── modelo_tabelas_opcional.sql  # DDL das tabelas para estudar (opcional)
├── docs/
│   ├── diagrama_er.svg            # Diagrama vetorial
│   ├── diagrama_er.dot            # Arquivo-fonte editável do diagrama
│   ├── diagrama_fluxo.svg         # Comunicação entre partes do sistema
│   ├── relatorio_academico.md     # Documento descritivo do projeto
│   ├── explicacao_do_codigo.md    # Explicação didática de cada parte
│   ├── tutorial_de_uso.md         # Passo a passo de instalação e uso
│   └── roteiro_defesa.md          # Como apresentar ao professor
└── testes/
    ├── test_banco.py
    └── test_vagas_api.py
```

## Integração com vagas externas

O LinkedIn não oferece uma API comum de leitura/pesquisa pública de anúncios para um aplicativo acadêmico genérico; suas integrações de recrutamento envolvem acesso autorizado. Assim:

- **Adzuna**: usa endpoint de busca de anúncios `https://api.adzuna.com/v1/api/jobs/br/search/1`, com credenciais `app_id` e `app_key` cadastradas em `.env`.
- **LinkedIn**: abre uma busca de vagas no navegador usando o endereço oficial `https://www.linkedin.com/jobs/search/`, sem copiar ou coletar os anúncios.
- **Se não tiver API key**: cadastro, login, MySQL, vagas locais e candidaturas **continuam funcionando**. Somente a busca Adzuna não funciona até configurar.
- Não há garantia de vagas em Porto Velho na Adzuna. Se o resultado for vazio, tente `Rondônia`, `Ji-Paraná` ou buscas mais amplas.
- Vagas externas **não são gravadas como vagas locais** e suas inscrições não são feitas dentro do app.

Documentação: [API Adzuna](https://developer.adzuna.com/docs/search) · [Integrações de recrutamento do LinkedIn](https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/overview).

## Testes

O diretório `testes/` contém **11 testes**. Execute, após instalar `pytest` na máquina de desenvolvimento:

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest testes -q
```

Os testes usam um **banco SQLite temporário apenas durante o teste** para verificar as regras de negócio. O programa **não usa SQLite em produção**: `app.py` conecta ao **MySQL**. A interface wxPython e a conexão real com o MySQL precisam ser testadas no computador em que os serviços estão instalados.

## Segurança e limitações

- Senhas protegidas por hash `PBKDF2-HMAC-SHA256` com `salt` aleatório individual.
- A conta do candidato não pode publicar vagas; a conta da empresa não pode se candidatar.
- Uma empresa só consulta candidatos da própria vaga.
- Um candidato só pode se inscrever uma vez por vaga (`UNIQUE(candidato_id,vaga_id)`).
- O trabalho é um **protótipo acadêmico**. Ainda não possui recuperação de senha, verificação de e-mail, LGPD completa, currículo em PDF ou verificação real de empresas/anúncios. Não publique dados reais de pessoas sem base legal e consentimentos adequados.

## Para defender em sala

Leia `docs/explicacao_do_codigo.md`, `docs/tutorial_de_uso.md`, `docs/roteiro_defesa.md` e mostre `docs/diagrama_er.svg`.

[Diagrama ER](docs/diagrama_er.svg) · [Tutorial](docs/tutorial_de_uso.md) · [Entenda o código](docs/explicacao_do_codigo.md) · [Roteiro de defesa](docs/roteiro_defesa.md)
