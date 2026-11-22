# Roteiro para apresentação em sala — ConectaVagas

O enunciado cita Pontes e Lacerda (MT). Para apresentar nessa região, ajuste `CIDADE_PADRAO=Pontes e Lacerda` no arquivo `.env` e reinicie o aplicativo. A configuração sugere a cidade nos novos cadastros e nas buscas. As vagas já gravadas conservam a cidade informada na publicação.

**Tempo sugerido:** aproximadamente 6 a 8 minutos, dependendo das perguntas.

## 1. Problema e solução (40 segundos)

> "Nosso projeto é o ConectaVagas, um aplicativo desktop em wxPython para facilitar a divulgação e a busca de empregos e estágios em Porto Velho. Ele atende dois grupos: candidatos e empresas. A empresa publica oportunidades, e o candidato procura e se inscreve."

**Mostre:** tela Início.

## 2. Tecnologias e arquitetura (50 segundos)

> "Usamos Python e wxPython para criar a interface. O arquivo app.py contém as telas. O banco.py concentra as regras e usa SQLAlchemy e PyMySQL para conectar ao servidor MySQL. O Workbench é a ferramenta de administração do mesmo banco de dados."

**Mostre:** `docs/diagrama_fluxo.svg`.

## 3. Diagrama ER (1 minuto)

> "Criamos três tabelas: usuarios, vagas e candidaturas. Uma empresa pode publicar várias vagas; cada vaga pode receber várias candidaturas; e cada candidato pode se candidatar a várias vagas. As referências são feitas com chaves estrangeiras. Existe uma restrição que impede duas inscrições da mesma pessoa na mesma vaga."

**Mostre:** `docs/diagrama_er.svg`. Explique `empresa_id`, `candidato_id`, `vaga_id` e `UNIQUE`.

## 4. Demonstração ao vivo (2 a 3 minutos)

1. Entre com a conta **empresa** e publique uma vaga **fictícia de demonstração**.
2. Saia e entre com a conta **candidato**.
3. Localize a vaga, abra detalhes e envie uma candidatura.
4. Mostre **Minhas candidaturas**, com status `Enviada`.
5. Volte à empresa, abra a lista de candidatos e altere para `Em análise`.
6. Se houver tempo, mostre no Workbench um `SELECT` das candidaturas.

**Frase importante:** "A vaga e a candidatura continuam salvas mesmo após fechar o aplicativo, porque ficam no MySQL."

## 5. API externa (30 a 45 segundos)

> "Também implementamos uma consulta opcional à API da Adzuna, que traz anúncios externos de trabalho em JSON. Como o LinkedIn não tem uma API de pesquisa aberta para o nosso caso, usamos o botão LinkedIn só para abrir a busca no site. As candidaturas externas acontecem na página original."

**Mostre:** tela Vagas externas. Se não houver chave ou internet, explique a limitação sem prejudicar a demonstração principal.

## 6. Código: explique o que realmente importa (1 minuto)

- **`TelaDetalhes.candidatar()` em app.py:** captura o ID do candidato, o ID da vaga e a mensagem digitada.
- **`banco.candidatar()` em banco.py:** verifica se é candidato, se a vaga está aberta e se não há inscrição anterior; em seguida salva com `commit()`.
- **`Candidatura` em banco.py:** representa a tabela e o relacionamento entre candidato e vaga.

## 7. Fechamento (20 segundos)

> "Nosso sistema atende ao objetivo social e aos requisitos técnicos: interface wxPython com mais de cinco telas, banco MySQL, organização para publicação no GitHub, diagrama ER e tutorial de uso. As futuras melhorias seriam adicionar currículo em PDF, validação de empresas e notificações."

## Perguntas que podem cair

**O que é uma chave estrangeira?** Uma coluna que referencia a chave primária de outra tabela.

**Por que SQLAlchemy?** Para trabalhar com classes Python que representam tabelas e realizar consultas no MySQL.

**Por que não guardar senha em texto?** Porque usamos hash com salt para reduzir o risco de exposição de senhas em caso de vazamento do banco.

**Como evita candidaturas duplicadas?** A função verifica a duplicidade, e o MySQL possui uma restrição `UNIQUE` composta entre candidato e vaga.

**Como controla permissões?** A função `criar_vaga()` exige usuário do tipo empresa; `candidatar()` exige candidato; `candidatos_da_vaga()` confere se a vaga pertence à empresa.

**Se o MySQL parar, o programa abre?** Não: o programa informa a falha de conexão e solicita verificar o serviço, o banco e o `.env`.

**Se a API cair, o sistema para?** Não: as funcionalidades locais continuam disponíveis; apenas a consulta de vagas externas falha.

**Você usou LinkedIn por API?** Não; usamos Adzuna como API oficial de busca e o LinkedIn apenas como link de pesquisa.
