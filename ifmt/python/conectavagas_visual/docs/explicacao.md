# Entenda o código e apresente em sala

Abra `app.py` e `banco.py` no editor. Use Ctrl+F para procurar as funções citadas aqui. O código contém comentários em português nos blocos que precisam de explicação.

## Primeiro entenda o caminho de uma ação

A pessoa clica em Salvar vaga. `salvar_vaga`, em `app.py`, lê os campos. Em seguida chama `publicar_vaga`, em `banco.py`. Essa função valida os valores e executa um INSERT. `commit()` confirma a gravação. Por fim, o programa abre a consulta de vagas.

Na apresentação, uma fala possível é “A interface recebe as informações e chama uma função que executa o SQL. No Workbench podemos consultar os mesmos registros gravados pelo programa.”

## Como o wxPython organiza o programa

| Trecho | Explicação |
|---|---|
| `wx.App(False)` | Cria a aplicação gráfica |
| `Janela(wx.Frame)` | Define a janela principal usando a classe de janela do wxPython |
| `__init__` | Prepara a janela assim que o objeto é criado |
| `self` | Representa o objeto atual, a janela que estamos usando |
| `nova_tela` | Destrói o painel anterior e cria o painel da próxima tela |
| `wx.BoxSizer(wx.VERTICAL)` | Organiza os componentes de cima para baixo |
| `campo` | Cria um campo e o devolve para a tela guardar e ler depois |
| `GetValue()` | Lê o texto digitado no campo |
| `botao` | Cria o botão e recebe a função que ele deve executar |
| `Bind(wx.EVT_BUTTON, ao_clicar)` | Liga o clique do botão à função ao_clicar |
| `MainLoop()` | Mantém o programa aberto aguardando os eventos |

O argumento `acao` de `botao` recebe uma função como `self.salvar_vaga`. Dentro de `ao_clicar`, `acao()` executa essa função. O `try/except` mostra uma mensagem se houver dados inválidos ou erro de conexão. O parâmetro `evento` é enviado pelo wxPython quando o clique acontece.

## As seis telas

| Método de app.py | O que explicar |
|---|---|
| `tela_login` | Cria e-mail, senha e botões. `fazer_login` confere a conta e guarda o usuário |
| `tela_cadastro` | Cria nome, e-mail e senha. `salvar_usuario` envia esses valores ao banco |
| `tela_inicio` | Mostra o nome de quem entrou e os caminhos de consulta, publicação e saída |
| `tela_vagas` | Cria a pesquisa e a lista. `pesquisar` busca os registros e preenche as linhas |
| `tela_detalhes` | Mostra os campos da vaga escolhida e o contato para candidatura |
| `tela_publicar` | Cria o formulário da vaga. `salvar_vaga` grava o anúncio |

Cada método monta um painel navegável dentro da mesma janela. Ao clicar em Voltar, outro método monta a próxima tela.

## Como explicar o banco

O arquivo `banco.sql` cria duas tabelas. `usuarios` guarda as contas. `vagas` guarda os anúncios. Uma conta pode publicar várias vagas, e cada vaga referencia uma conta por `usuario_id`.

| Termo | Significado no projeto |
|---|---|
| `PRIMARY KEY` | Identifica cada registro por um ID exclusivo |
| `AUTO_INCREMENT` | Faz o MySQL gerar o próximo ID |
| `FOREIGN KEY` | Relaciona `vagas.usuario_id` com `usuarios.id` |
| `UNIQUE` no e-mail | Impede duas contas com o mesmo e-mail |
| `NOT NULL` | Exige um valor diferente de NULL |
| `INSERT` | Insere uma conta ou uma vaga |
| `SELECT` | Consulta os registros existentes |
| `JOIN` | Liga vagas e usuários para mostrar o nome de quem publicou |
| `LIKE` | Procura parte do título da vaga |
| `DELETE` | Exclui um anúncio do autor logado |
| `commit()` | Confirma a gravação ou a exclusão |
| `finally` e `close()` | Fecham a conexão mesmo se ocorrer uma falha |

Em `conectar()`, o conector usa o dicionário `BANCO`. `**BANCO` passa os valores desse dicionário como argumentos de conexão.

O cursor executa o SQL. Quando usamos `dictionary=True`, ele entrega cada linha como um dicionário. Isso permite escrever `vaga['titulo']` ou `usuario['nome']`.

Os `%s` da consulta são marcadores para os valores enviados no segundo argumento de `execute`. O conector trata esses valores como parâmetros.

## Siga a publicação com um exemplo

1. Entre com uma conta de demonstração.
2. Em Publicar vaga, digite Estágio em Suporte, uma empresa fictícia, a cidade, as atividades e um contato fictício.
3. No editor, procure `salvar_vaga`. Mostre `self.usuario['id']` e os cinco campos lidos com `GetValue()`.
4. Abra `banco.publicar_vaga`. Mostre a validação, o INSERT, os seis valores enviados e `commit()`.
5. No Workbench, consulte `vagas`. Compare o `usuario_id` do anúncio com o `id` da conta que entrou.

Uma fala possível é “O usuário não digita quem é o autor da vaga. Esse ID vem da conta que fez login. Assim o anúncio fica associado ao usuário certo.”

## Siga a consulta e a exclusão

`listar_vagas` faz um SELECT com JOIN e retorna uma lista de dicionários. A interface guarda essa lista em `self.vagas` e mostra um resumo na lista visual. Ao escolher uma linha, `GetSelection()` devolve sua posição. Essa posição permite encontrar o dicionário completo e mostrar os detalhes.

A posição da linha pode ser 0 e o ID da vaga pode ser 12. A posição serve para escolher um item na tela, e o ID identifica o registro no MySQL.

Se o usuário logado publicou a vaga, aparece o botão de exclusão. O DELETE exige o ID da vaga e o ID do usuário ao mesmo tempo. Essa condição impede a exclusão de um anúncio de outra conta pela função.

## Como o login confere a senha

`cadastrar_usuario` gera um salt aleatório e calcula um hash com PBKDF2. Guarda ambos na coluna `senha`, separados por dois-pontos. No login, `entrar` busca o e-mail, recupera o salt e calcula novamente o hash da senha digitada. Se o resultado confere, devolve os dados do usuário para a janela.

Explique que o hash é um resultado calculado para conferir a senha. A senha original digitada não é gravada diretamente na tabela.

## Roteiro curto de apresentação

1. Explique que o sistema facilita a divulgação de vagas locais.
2. Mostre o diagrama e as duas tabelas.
3. Cadastre uma conta, entre, publique e consulte uma vaga.
4. Acompanhe `salvar_vaga` e `publicar_vaga` no editor.
5. Mostre o registro no Workbench.
6. Mostre onde o clique é associado à função e como uma tela abre outra.

Antes da defesa, tente responder de onde vem o ID do autor, qual comando insere a vaga, para que serve commit e como o JOIN encontra o nome de quem publicou.
