"""Cadastro de PETs com login, interface wxPython e dados no MySQL."""

import wx
from sqlalchemy.exc import SQLAlchemyError

from banco import autenticar, cadastrar_pet, cadastrar_usuario, iniciar_banco, listar_pets


def titulo(parent, mensagem, tamanho=15):
    texto = wx.StaticText(parent, label=mensagem)
    texto.SetFont(wx.Font(tamanho, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    return texto


def criar_campo(parent, layout, legenda, senha=False):
    layout.Add(wx.StaticText(parent, label=legenda), 0, wx.BOTTOM, 4)
    estilo = wx.TE_PROCESS_ENTER | (wx.TE_PASSWORD if senha else 0)
    campo = wx.TextCtrl(parent, style=estilo)
    layout.Add(campo, 0, wx.EXPAND | wx.BOTTOM, 12)
    return campo


class TelaLogin(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Login - Cadastro de PETs", size=(440, 385))
        self.CenterOnScreen()
        painel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)

        layout.Add(titulo(painel, "Sistema de Cadastro de PETs", 17), 0, wx.BOTTOM, 10)
        layout.Add(wx.StaticText(painel, label="Entre na sua conta para ver seus animais."), 0, wx.BOTTOM, 18)
        self.login = criar_campo(painel, layout, "Login:")
        self.senha = criar_campo(painel, layout, "Senha:", senha=True)

        botoes = wx.BoxSizer(wx.HORIZONTAL)
        entrar = wx.Button(painel, label="Entrar")
        criar = wx.Button(painel, label="Criar usuário")
        botoes.Add(entrar, 1, wx.RIGHT, 10)
        botoes.Add(criar, 1)
        layout.Add(botoes, 0, wx.EXPAND | wx.BOTTOM, 17)
        layout.Add(wx.StaticText(painel, label="Primeiro acesso: Fulano / 1234"), 0)

        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(layout, 1, wx.EXPAND | wx.ALL, 25)
        painel.SetSizer(margem)
        entrar.Bind(wx.EVT_BUTTON, self.entrar)
        criar.Bind(wx.EVT_BUTTON, self.criar_usuario)
        self.senha.Bind(wx.EVT_TEXT_ENTER, self.entrar)

    def entrar(self, evento):
        login, senha = self.login.GetValue().strip(), self.senha.GetValue()
        if not login or not senha:
            wx.MessageBox("Informe login e senha.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        try:
            usuario = autenticar(login, senha)
        except SQLAlchemyError as erro:
            wx.MessageBox(str(erro), "Erro no MySQL", wx.OK | wx.ICON_ERROR)
            return
        if usuario is None:
            wx.MessageBox("Login ou senha incorretos.", "Acesso negado", wx.OK | wx.ICON_ERROR)
            self.senha.Clear()
            return

        usuario_id, nome_usuario = usuario
        self.senha.Clear()
        self.Hide()
        TelaPets(self, usuario_id, nome_usuario).Show()

    def criar_usuario(self, evento):
        login, senha = self.login.GetValue().strip(), self.senha.GetValue()
        if not login or not senha:
            wx.MessageBox("Digite o novo login e a senha nos campos acima.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        try:
            criado = cadastrar_usuario(login, senha)
        except (SQLAlchemyError, ValueError) as erro:
            wx.MessageBox(str(erro), "Erro no cadastro", wx.OK | wx.ICON_ERROR)
            return
        if criado:
            wx.MessageBox("Usuário criado! Clique em Entrar para acessar.", "Sucesso", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Esse login já está cadastrado.", "Atenção", wx.OK | wx.ICON_WARNING)


class TelaPets(wx.Frame):
    def __init__(self, tela_login, usuario_id, nome_usuario):
        super().__init__(None, title="Meus PETs", size=(850, 650))
        self.SetMinSize((720, 580))
        self.CenterOnScreen()
        self.tela_login = tela_login
        self.usuario_id = usuario_id  # Identificação obtida no login.

        painel = wx.Panel(self)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(titulo(painel, f"Cadastro de PETs - {nome_usuario}", 17), 0, wx.BOTTOM, 8)
        layout.Add(wx.StaticText(painel, label="Registre os animais que você tem ou já teve."), 0, wx.BOTTOM, 18)

        formulario = wx.StaticBoxSizer(wx.VERTICAL, painel, "Dados do PET")
        grade = wx.FlexGridSizer(rows=3, cols=2, vgap=6, hgap=20)
        grade.AddGrowableCol(0, 1)
        grade.AddGrowableCol(1, 1)
        self.campos = {}

        for chave, legenda in (
            ("nome", "Nome:"), ("idade", "Idade (anos):"),
            ("raca", "Raça:"), ("peso", "Peso (kg):"),
            ("cor", "Cor:"),
        ):
            coluna = wx.BoxSizer(wx.VERTICAL)
            coluna.Add(wx.StaticText(painel, label=legenda), 0, wx.BOTTOM, 4)
            entrada = wx.TextCtrl(painel)
            coluna.Add(entrada, 0, wx.EXPAND)
            self.campos[chave] = entrada
            grade.Add(coluna, 0, wx.EXPAND)

        formulario.Add(grade, 0, wx.EXPAND | wx.ALL, 12)
        salvar = wx.Button(painel, label="Cadastrar PET")
        formulario.Add(salvar, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 12)
        layout.Add(formulario, 0, wx.EXPAND | wx.BOTTOM, 18)

        layout.Add(titulo(painel, "Meus PETs cadastrados"), 0, wx.BOTTOM, 10)
        self.lista = wx.ListCtrl(painel, style=wx.LC_REPORT | wx.BORDER_SIMPLE)
        for indice, (legenda, largura) in enumerate((
            ("Nome", 160), ("Idade", 100), ("Raça", 160),
            ("Peso (kg)", 120), ("Cor", 160),
        )):
            self.lista.InsertColumn(indice, legenda, width=largura)
        layout.Add(self.lista, 1, wx.EXPAND | wx.BOTTOM, 12)

        botoes = wx.BoxSizer(wx.HORIZONTAL)
        atualizar = wx.Button(painel, label="Atualizar lista")
        sair = wx.Button(painel, label="Sair da conta")
        botoes.Add(atualizar, 0, wx.RIGHT, 12)
        botoes.AddStretchSpacer()
        botoes.Add(sair, 0)
        layout.Add(botoes, 0, wx.EXPAND)

        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(layout, 1, wx.EXPAND | wx.ALL, 22)
        painel.SetSizer(margem)
        salvar.Bind(wx.EVT_BUTTON, self.salvar)
        atualizar.Bind(wx.EVT_BUTTON, self.atualizar)
        sair.Bind(wx.EVT_BUTTON, lambda evento: self.Close())
        self.Bind(wx.EVT_CLOSE, self.fechar)
        self.atualizar(None)

    def salvar(self, evento):
        try:
            cadastrar_pet(
                self.usuario_id,
                self.campos["nome"].GetValue(),
                self.campos["idade"].GetValue(),
                self.campos["raca"].GetValue(),
                self.campos["peso"].GetValue(),
                self.campos["cor"].GetValue(),
            )
        except ValueError as erro:
            wx.MessageBox(str(erro), "Verifique os dados", wx.OK | wx.ICON_WARNING)
            return
        except SQLAlchemyError as erro:
            wx.MessageBox(str(erro), "Erro no MySQL", wx.OK | wx.ICON_ERROR)
            return

        for campo in self.campos.values():
            campo.Clear()
        self.atualizar(None)
        wx.MessageBox("PET cadastrado com sucesso!", "Sucesso", wx.OK | wx.ICON_INFORMATION)

    def atualizar(self, evento):
        try:
            pets = listar_pets(self.usuario_id)
        except SQLAlchemyError as erro:
            wx.MessageBox(str(erro), "Erro no MySQL", wx.OK | wx.ICON_ERROR)
            return
        self.lista.DeleteAllItems()
        for nome, idade, raca, peso, cor in pets:
            linha = self.lista.InsertItem(self.lista.GetItemCount(), nome)
            for coluna, valor in enumerate((idade, raca, f"{peso:.2f}", cor), start=1):
                self.lista.SetItem(linha, coluna, str(valor))

    def fechar(self, evento):
        self.tela_login.Show()
        self.tela_login.Raise()
        self.Destroy()


class Programa(wx.App):
    def OnInit(self):
        try:
            iniciar_banco()
        except (SQLAlchemyError, ValueError, OSError) as erro:
            wx.MessageBox(
                f"Não foi possível conectar ao MySQL. Verifique o .env e o servidor.\n\n{erro}",
                "Erro de conexão", wx.OK | wx.ICON_ERROR,
            )
            return False
        janela = TelaLogin()
        janela.Show()
        self.SetTopWindow(janela)
        return True


if __name__ == "__main__":
    programa = Programa(False)
    programa.MainLoop()
