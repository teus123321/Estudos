# Como entender e apresentar o código do ConectaVagas

Comece com uma empresa e um candidato fictícios cadastrados. Abra o aplicativo, o editor de código e o MySQL Workbench. No editor, use Ctrl+F para procurar os nomes de classes e funções indicados neste guia.

## 1. Entenda como os arquivos trabalham juntos

| Arquivo | O que faz | O que mostrar na defesa |
|---|---|---|
| `app.py` | Cria telas, lê campos e responde aos cliques | Um botão e a função que ele chama |
| `banco.py` | Valida as operações, consulta e grava os dados | As três classes de tabelas e uma função que usa `commit()` |
| `regiao.py` | Lê a cidade sugerida na configuração | `CIDADE_PADRAO` |
| `vagas_api.py` | Busca anúncios externos pela internet | A chamada HTTP e a conversão de JSON |
| `.env.example` | Mostra quais dados configurar na máquina | Host, porta, usuário e nome do banco |

Uma explicação inicial possível é “O aplicativo tem uma parte visual em app.py. Quando alguém clica, ela chama uma função de banco.py. Essa função verifica as regras e usa SQLAlchemy e PyMySQL para acessar o servidor MySQL. No Workbench conseguimos consultar os dados gravados.”

## 2. Como o aplicativo abre

No fim de `app.py`, mostre `if __name__ == "__main__"` e `Programa(False).MainLoop()`.

Você pode explicar “Ao executar app.py, criamos a aplicação e iniciamos o ciclo de eventos. Ele mantém a janela funcionando e espera os cliques. No método OnInit, o programa primeiro tenta iniciar o banco. Se conseguir, cria e mostra JanelaPrincipal.”

Em `banco.iniciar_banco()`, acompanhe a leitura do `.env`, a montagem da URL, `create_engine` e `Base.metadata.create_all(engine)`. O banco `conectavagas` é criado previamente pelo SQL do tutorial. `create_all` cria as tabelas ausentes. Uma alteração futura na estrutura de uma tabela já existente precisa de migração.

## 3. Como um botão executa uma função

Em `criar_botao`, mostre `botao.Bind(wx.EVT_BUTTON, acao)`.

Você pode dizer “Bind liga o clique à função recebida em acao. Na tela de cadastro, o botão Cadastrar recebe self.salvar. Quando clicamos, wxPython chama esse método e entrega o evento do clique.”

| Trecho | Significado concreto |
|---|---|
| `self` | O objeto que está executando o método, por exemplo, esta tela de cadastro |
| `self.email` | O campo visual de e-mail dessa tela |
| `self.email.GetValue()` | O texto que a pessoa digitou nesse campo |
| `self.salvar` | A função que será usada como ação do botão |
| `self.salvar(evento)` | Uma chamada que executa a função agora |
| `lambda ev: janela.ir(TelaVagas)` | Uma pequena função que recebe o evento e pede a abertura da tela de vagas |
| `super().__init__(...)` | A inicialização da classe herdada, para preparar a estrutura da página |
| `return` | Encerra a função e pode devolver um resultado |
| `raise ValueError(...)` | Interrompe a operação informando uma falha de validação |
| `try` e `except` | Tentam uma operação e permitem tratar uma falha prevista |

## 4. Siga o cadastro e o login

Abra `TelaCadastro.salvar` e `banco.cadastrar_usuario` lado a lado.

1. A tela lê nome, e-mail, senha, tipo, telefone e cidade.
2. O banco verifica os tamanhos, o tipo de conta e o e-mail.
3. Cria um salt aleatório e calcula o hash da senha.
4. Monta um objeto `Usuario`, adiciona à sessão e confirma com `commit()`.
5. Se o e-mail já estiver cadastrado, o banco impede a duplicação. O código usa `rollback()` para desfazer a transação que falhou e informa o erro à tela.

No login, abra `TelaLogin.entrar` e `banco.autenticar`.

Você pode explicar “Buscamos a conta pelo e-mail. Recuperamos o salt daquela conta e calculamos o hash da senha digitada. Se os hashes conferirem, devolvemos os dados do usuário. A janela guarda esse dicionário para saber qual conta está usando o aplicativo. O tipo da conta define a próxima tela.”

O sal e o hash ficam no banco. O dicionário devolvido para a interface contém nome, ID, tipo e dados de perfil. A senha digitada é usada no cálculo.

## 5. Siga uma publicação de vaga do começo ao fim

Abra `TelaNovaVaga.__init__`, depois `TelaNovaVaga.salvar`, e por fim `banco.criar_vaga`.

1. `__init__` monta os campos e liga o botão Publicar vaga a `self.salvar`.
2. `salvar` lê os campos com `GetValue()`. Nos controles de escolha, `GetStringSelection()` lê a opção marcada.
3. O ID da empresa vem de `self.janela.usuario["id"]`, preenchido após o login.
4. `criar_vaga` verifica os campos e consulta o usuário para confirmar o tipo empresa.
5. `Vaga(...)` cria o objeto em memória. `sessao.add(vaga)` prepara sua inclusão na sessão.
6. `sessao.commit()` confirma a gravação. O código devolve o ID da nova vaga.
7. A tela mostra a confirmação e abre o painel da empresa.

Uma fala possível é “A vaga precisa saber quem a publicou. Por isso guardamos empresa_id, que aponta para o ID da conta em usuarios. O MySQL gera o ID próprio da vaga. Assim conseguimos identificar o anúncio quando alguém abre os detalhes ou envia uma candidatura.”

Confira no Workbench depois de publicar uma vaga fictícia.

```sql
USE conectavagas;
SELECT id, nome, tipo FROM usuarios;
SELECT id, empresa_id, titulo, cidade, ativa FROM vagas;
```

## 6. Siga uma candidatura

Abra `TelaDetalhes.candidatar`, depois `banco.candidatar` e a classe `Candidatura`.

Use, por exemplo, o candidato de ID 2 e a vaga de ID 5. Esses números são ilustrativos. Confira os IDs gerados no banco da demonstração.

1. O botão envia o ID da conta logada, o ID da vaga e a mensagem.
2. A função do banco confirma que a conta é de candidato e que a vaga está aberta.
3. Consulta se já existe uma inscrição daquele candidato naquela vaga.
4. Cria `Candidatura(candidato_id=2, vaga_id=5, mensagem=...)`.
5. `commit()` confirma a inscrição com o status inicial `Enviada`.
6. A tela abre Minhas candidaturas para a pessoa acompanhar o resultado.

Você pode explicar “Candidatura é a ligação entre uma pessoa e uma vaga. Cada uma pode ter várias inscrições, então precisamos dessa tabela para guardar cada combinação e seu status. A restrição UNIQUE impede repetir candidato_id e vaga_id juntos. O mesmo candidato pode se inscrever em outra vaga.”

```sql
SELECT id, candidato_id, vaga_id, status FROM candidaturas;
```

## 7. Mostre uma consulta com relacionamento

Em `banco.listar_vagas`, `select(Vaga, Usuario.nome)` define o que buscar. `join` liga `Vaga.empresa_id` a `Usuario.id` para trazer também o nome da empresa. `where` limita os resultados às vagas ativas e acrescenta os filtros preenchidos. `order_by` coloca as publicações recentes primeiro.

O trecho `ilike` pesquisa sem diferenciar maiúsculas e minúsculas. `%suporte%` procura suporte em qualquer posição do texto. O operador `|` combina a pesquisa por título ou área. Os valores são enviados como parâmetros pelo SQLAlchemy.

Em `TelaVagas.atualizar`, o resultado fica em `self.vagas`. A tabela visual exibe título, empresa e outras colunas. O índice da linha indica uma posição nessa lista. O ID guardado no dicionário identifica o registro no banco.

## 8. Explique navegação e permissões

Em `JanelaPrincipal.ir`, a página anterior sai do organizador visual, seus controles são destruídos e a nova página é criada. `**dados` permite passar argumentos como `vaga_id` para a tela de detalhes.

`montar_menu` escolhe os botões conforme o tipo de conta. As funções do banco também fazem verificações nas operações, como confirmar que a vaga pertence à empresa ao consultar candidatos e alterar status.

Para demonstrar uma alteração, entre como empresa, escolha uma candidatura e marque Em análise. Mostre `TelaCandidatos.salvar_status`, `banco.mudar_status_candidatura` e o resultado no Workbench. Entre novamente como candidato e confira o status em Minhas candidaturas.

## 9. Entenda as palavras do banco

| Palavra | Como explicar |
|---|---|
| Classe mapeada | Uma definição Python que descreve uma tabela para o SQLAlchemy |
| Objeto | Uma instância, como a vaga criada com `Vaga(...)` |
| Chave primária | O ID exclusivo de um registro na tabela |
| Chave estrangeira | O campo que referencia o ID de um registro de outra tabela |
| `nullable=False` | A coluna exige um valor diferente de NULL |
| `unique=True` | O banco exige que aquele valor seja exclusivo |
| `Session` | A área usada para consultar e acompanhar operações de uma transação |
| `with sessao_banco() as sessao` | Abre uma sessão e garante seu fechamento ao sair do bloco |
| `commit()` | Confirma as alterações da transação |
| `rollback()` | Desfaz as alterações ainda não confirmadas da transação que falhou |
| `get(Usuario, id)` | Busca uma conta por sua chave primária |
| Dicionário | Estrutura com pares de chave e valor, como `usuario["nome"]` |

## 10. Explique a busca externa se o professor perguntar

Em `vagas_api.buscar_vagas_externas`, o programa lê as credenciais, monta os parâmetros e faz uma requisição HTTPS. `json.load` transforma a resposta em estruturas Python. `formatar_vaga` organiza os campos para a tela. A candidatura ocorre no site do anúncio.

O botão do LinkedIn abre a pesquisa no navegador. A demonstração de cadastro, publicação e candidatura local usa os registros do MySQL e pode funcionar sem consultar a API externa.

## 11. Ensaie com pequenas perguntas

Antes da defesa, faça o fluxo no aplicativo e responda olhando o trecho de código correspondente.

- Qual método recebe o clique em Publicar vaga?
- De onde vem o ID da empresa?
- Em qual linha a transação é confirmada?
- Qual tabela liga candidato e vaga?
- Por que dois candidatos podem se inscrever na mesma vaga?
- Por que o mesmo candidato pode se inscrever em vagas diferentes?
- O que acontece se ele repetir a inscrição na mesma vaga?
- Como o nome da empresa aparece ao lado do título da vaga?
- Qual é a diferença entre a posição da linha na tela e o ID do banco?
- Onde o sistema verifica se a empresa é dona da vaga?

Se cada integrante conseguir seguir uma operação desde o clique até a consulta no Workbench, vocês terão uma base concreta para explicar as funções utilizadas.
