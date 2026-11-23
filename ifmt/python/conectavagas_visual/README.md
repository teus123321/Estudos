# ConectaVagas

Trabalho de Ferramentas RAD com wxPython e MySQL para divulgar vagas de emprego da região.

Uma pessoa cria sua conta, entra no programa e publica uma vaga com empresa, cidade, descrição e contato. As outras pessoas consultam as vagas e usam o contato informado para se candidatar. O autor pode excluir seu anúncio.

## Seis telas navegáveis

1. Login
2. Cadastro de conta
3. Início
4. Consulta de vagas
5. Detalhes da vaga
6. Publicação de vaga

## Arquivos para estudar

| Arquivo | Função |
|---|---|
| `app.py` | As seis telas e os cliques dos botões |
| `banco.py` | Cadastro, login e consultas SQL |
| `banco.sql` | Criação do banco e das duas tabelas |
| `config_exemplo.py` | Modelo para configurar a conexão |
| `docs/tutorial.md` | Instalação e uso |
| `docs/explicacao.md` | Explicação do código e roteiro de defesa |
| `docs/diagrama_er.svg` | Diagrama das tabelas e do relacionamento |

Comece pelo [tutorial](docs/tutorial.md). Depois acompanhe o [código explicado](docs/explicacao.md) e abra o [diagrama ER](docs/diagrama_er.svg).

O formulário sugere Porto Velho e permite digitar outra cidade. O enunciado do professor cita Pontes e Lacerda. Para apresentar nessa região, preencha Pontes e Lacerda ao publicar os anúncios.

Esta versão utiliza o banco `conectavagas_aula`. Execute o arquivo SQL e cadastre as contas de demonstração nele.
