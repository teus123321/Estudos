# Instalação e uso

## Preparar a máquina

Tenha Python 3.11 ou 3.12 de 64 bits, MySQL Server e MySQL Workbench instalados. O servidor MySQL armazena os dados. O Workbench permite criar o banco e consultar suas tabelas.

Extraia o ZIP e abra a pasta `ConectaVagas_simples`. Se baixar pelo GitHub, a pasta é `Estudos/ifmt/python/conectavagas`.

## Criar o banco

1. Abra o Workbench e conecte-se ao seu servidor MySQL.
2. Abra `banco.sql` pelo menu File → Open SQL Script.
3. Execute o arquivo completo pelo botão de raio.
4. Atualize a lista SCHEMAS. O banco `conectavagas_aula` deve aparecer com `usuarios` e `vagas`.

## Instalar as bibliotecas

Abra o PowerShell na pasta que contém `app.py` e execute um comando por vez.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item config_exemplo.py config.py
```

Se tiver Python 3.12, substitua `py -3.11` por `py -3.12` no primeiro comando.

Edite `config.py` e coloque o host, a porta, o usuário e a senha do servidor que você acessou no Workbench. Mantenha o nome `conectavagas_aula`. Use a senha da conexão MySQL nesse arquivo. A conta criada na tela de cadastro pertence ao aplicativo.

`config.py` fica fora dos arquivos enviados ao GitHub por meio do `.gitignore`.

## Abrir o aplicativo

```powershell
.\.venv\Scripts\python.exe app.py
```

Se aparecer erro ao acessar o banco, confira o serviço MySQL, a execução de `banco.sql` e os valores de `config.py`.

## Usar as seis telas

1. Na tela Login, clique em Criar conta.
2. Preencha nome, e-mail e uma senha com pelo menos oito caracteres. Clique em Cadastrar.
3. Faça login. A tela Início mostra os botões de consulta e publicação.
4. Clique em Publicar vaga. Preencha título, empresa, cidade, descrição e contato. Use dados fictícios na demonstração.
5. Clique em Salvar vaga. A tela de consulta mostrará o anúncio.
6. Digite parte do título e clique em Pesquisar. Para listar todas, deixe a pesquisa vazia.
7. Selecione uma vaga e clique em Ver detalhes da vaga selecionada. Leia a descrição e o contato para candidatura.
8. O autor do anúncio pode usar Excluir minha vaga e confirmar a exclusão.
9. Volte ao início e clique em Sair da conta para entrar com outra conta.

Qualquer conta pode publicar e consultar. O campo contato informa como o interessado deve falar com o anunciante.

## Conferir no Workbench

Depois de cadastrar uma conta e publicar uma vaga, execute os comandos abaixo.

```sql
USE conectavagas_aula;
SELECT id, nome, email FROM usuarios;
SELECT id, usuario_id, titulo, empresa, cidade, contato FROM vagas;
```

Compare `vagas.usuario_id` com `usuarios.id` para identificar quem publicou o anúncio. Feche e abra novamente o aplicativo para conferir que o anúncio continua salvo.
