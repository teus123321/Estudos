# Sistema de Cadastro — wxPython

Projeto acadêmico com interface colorida em wxPython, validação de usuário e senha, acesso a uma segunda janela e redefinição de senha.

## Execução

Abra um terminal dentro da pasta do projeto e instale a dependência:

```bash
python -m pip install -r requirements.txt
```

Execute:

```bash
python sistema_login.py
```

## Primeiro acesso

- Usuário: `Fulano`
- Senha inicial: `1234`

O programa cria `usuario.json` automaticamente na primeira execução. A senha não é armazenada em texto puro: o programa grava um hash com salt. Quando a senha é redefinida, ela permanece atualizada após fechar o aplicativo. O texto `1234` na tela indica exclusivamente a senha **inicial**; depois de alterada, utilize a nova senha.

## Funcionalidades

- Verificar usuário e senha antes de liberar a segunda janela.
- Recusar credenciais inválidas.
- Fechar a janela e sair do programa.
- Redefinir a senha informando usuário, nova senha e confirmação.
- Voltar à tela de login após acessar a área restrita.
