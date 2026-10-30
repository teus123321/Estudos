import wx
from sqlalchemy.exc import SQLAlchemyError
from wx.lib.buttons import GenButton

from credenciais import (
    autenticar,
    cadastrar_usuario,
    consultar_usuario,
    iniciar_banco,
    listar_usuarios,
    redefinir_senha,
)


FUNDO = "#F3F6FB"
BRANCO = "#FFFFFF"
TEXTO = "#17243C"
TEXTO_SUAVE = "#697892"
AZUL = "#2E5BCE"
AZUL_ESCURO = "#2049B4"
AZUL_CLARO = "#E8EEFF"
VERDE = "#1FA77A"
VERDE_ESCURO = "#18845F"
VERMELHO = "#E45D69"
VERMELHO_ESCURO = "#C94855"
MARINHO = "#1D3156"
MARINHO_SUAVE = "#C6D5F7"
BORDA = "#DCE4F0"


def fonte(tamanho, negrito=False):
    return wx.Font(
        tamanho,
        wx.FONTFAMILY_DEFAULT,
        wx.FONTSTYLE_NORMAL,
        wx.FONTWEIGHT_BOLD if negrito else wx.FONTWEIGHT_NORMAL,
    )


def texto(parent, legenda, tamanho=10, cor=TEXTO, negrito=False):
    elemento = wx.StaticText(parent, label=legenda)
    elemento.SetFont(fonte(tamanho, negrito))
    elemento.SetForegroundColour(cor)
    return elemento


class BotaoCor(GenButton):
    def __init__(self, parent, legenda, cor, cor_hover, largura=130):
        super().__init__(parent, label=legenda, size=(largura, 40))
        self.cor_normal = cor
        self.cor_hover = cor_hover
        self.SetBackgroundColour(cor)
        self.SetForegroundColour(BRANCO)
        self.SetFont(fonte(10, True))
        self.SetBezelWidth(0)
        self.SetUseFocusIndicator(False)
        self.SetMinSize((largura, 40))
        self.Bind(wx.EVT_ENTER_WINDOW, self.ao_entrar)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.ao_sair)

    def ao_entrar(self, evento):
        self.SetBackgroundColour(self.cor_hover)
        self.Refresh()
        evento.Skip()

    def ao_sair(self, evento):
        self.SetBackgroundColour(self.cor_normal)
        self.Refresh()
        evento.Skip()


def painel_com_faixa(parent, cor_faixa):
    painel = wx.Panel(parent)
    painel.SetBackgroundColour(BRANCO)
    layout = wx.BoxSizer(wx.VERTICAL)
    faixa = wx.Panel(painel, size=(-1, 5))
    faixa.SetBackgroundColour(cor_faixa)
    layout.Add(faixa, 0, wx.EXPAND)
    conteudo = wx.Panel(painel)
    conteudo.SetBackgroundColour(BRANCO)
    layout.Add(conteudo, 1, wx.EXPAND)
    painel.SetSizer(layout)
    return painel, conteudo


class Tela(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Sistema de Cadastro", size=(980, 750))
        self.SetMinSize((770, 640))
        self.CenterOnScreen()

        principal = wx.ScrolledWindow(self, style=wx.VSCROLL)
        principal.SetBackgroundColour(FUNDO)
        principal.SetScrollRate(0, 12)
        corpo = wx.BoxSizer(wx.VERTICAL)

        cabecalho = wx.BoxSizer(wx.VERTICAL)
        cabecalho.Add(texto(principal, "ACESSO SEGURO", 9, AZUL, True), 0, wx.BOTTOM, 4)
        cabecalho.Add(texto(principal, "Sistema de Cadastro", 21, TEXTO, True), 0)
        cabecalho.Add(
            texto(principal, "Entre na sua conta ou atualize a senha de acesso.", 10, TEXTO_SUAVE),
            0,
            wx.TOP,
            5,
        )
        corpo.Add(cabecalho, 0, wx.BOTTOM, 15)

        grade = wx.GridBagSizer(vgap=18, hgap=18)
        painel_login, conteudo_login = painel_com_faixa(principal, AZUL)
        self.montar_login(conteudo_login)

        painel_info = wx.Panel(principal)
        painel_info.SetBackgroundColour(MARINHO)
        self.montar_informacoes(painel_info)

        painel_redefinir, conteudo_redefinir = painel_com_faixa(principal, VERDE)
        self.montar_redefinicao(conteudo_redefinir)

        grade.Add(painel_login, pos=(0, 0), flag=wx.EXPAND)
        grade.Add(painel_info, pos=(0, 1), flag=wx.EXPAND)
        grade.Add(painel_redefinir, pos=(1, 0), flag=wx.EXPAND)
        grade.AddGrowableCol(0, 1)
        grade.AddGrowableCol(1, 1)
        grade.AddGrowableRow(0, 1)
        grade.AddGrowableRow(1, 1)
        corpo.Add(grade, 1, wx.EXPAND)

        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(corpo, 1, wx.EXPAND | wx.ALL, 20)
        principal.SetSizer(margem)
        principal.FitInside()

    @staticmethod
    def adicionar_campo(parent, layout, legenda, senha=False, largura_rotulo=115):
        linha = wx.BoxSizer(wx.HORIZONTAL)
        rotulo = texto(parent, legenda, 10, TEXTO, True)
        rotulo.SetMinSize((largura_rotulo, -1))
        estilo = (wx.TE_PASSWORD | wx.TE_PROCESS_ENTER) if senha else wx.TE_PROCESS_ENTER
        campo = wx.TextCtrl(parent, style=estilo, size=(-1, 34))
        campo.SetMinSize((120, 34))
        campo.SetBackgroundColour(BRANCO)
        campo.SetForegroundColour(TEXTO)
        campo.SetFont(fonte(10))
        linha.Add(rotulo, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 9)
        linha.Add(campo, 1, wx.EXPAND)
        layout.Add(linha, 0, wx.EXPAND | wx.BOTTOM, 10)
        return campo

    def montar_login(self, parent):
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(texto(parent, "ENTRAR", 9, AZUL, True), 0, wx.BOTTOM, 5)
        layout.Add(texto(parent, "Bem-vindo de volta", 16, TEXTO, True), 0, wx.BOTTOM, 5)
        layout.Add(texto(parent, "Informe suas credenciais para continuar.", 9, TEXTO_SUAVE), 0, wx.BOTTOM, 12)

        self.campo_usuario = self.adicionar_campo(parent, layout, "Usuário:")
        self.campo_senha = self.adicionar_campo(parent, layout, "Senha:", senha=True)
        self.campo_senha.Bind(wx.EVT_TEXT_ENTER, self.entrar)

        botoes = wx.BoxSizer(wx.HORIZONTAL)
        entrar = BotaoCor(parent, "Entrar", VERDE, VERDE_ESCURO)
        sair = BotaoCor(parent, "Sair", VERMELHO, VERMELHO_ESCURO)
        botoes.Add(entrar, 1, wx.RIGHT, 12)
        botoes.Add(sair, 1)
        layout.Add(botoes, 0, wx.EXPAND | wx.TOP, 5)

        redefinir = wx.Button(parent, label="Redefinir senha", style=wx.BORDER_NONE)
        redefinir.SetFont(fonte(10, True))
        redefinir.SetForegroundColour(AZUL)
        redefinir.SetBackgroundColour(BRANCO)
        layout.Add(redefinir, 0, wx.ALIGN_CENTER | wx.TOP, 8)

        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(layout, 1, wx.EXPAND | wx.ALL, 20)
        parent.SetSizer(margem)

        entrar.Bind(wx.EVT_BUTTON, self.entrar)
        sair.Bind(wx.EVT_BUTTON, lambda evento: self.Close())
        redefinir.Bind(wx.EVT_BUTTON, self.focar_redefinicao)

    def montar_informacoes(self, parent):
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(texto(parent, "INFORMAÇÕES DE ACESSO", 9, MARINHO_SUAVE, True), 0, wx.BOTTOM, 15)
        layout.Add(texto(parent, "Primeiro acesso ao MySQL", 17, BRANCO, True), 0, wx.BOTTOM, 11)
        layout.Add(
            texto(parent, "Utilize as credenciais de exemplo abaixo:", 10, MARINHO_SUAVE),
            0,
            wx.BOTTOM,
            23,
        )
        layout.Add(texto(parent, "USUÁRIO", 9, MARINHO_SUAVE, True), 0, wx.BOTTOM, 5)
        layout.Add(texto(parent, "Fulano", 13, BRANCO, True), 0, wx.BOTTOM, 14)
        layout.Add(texto(parent, "SENHA INICIAL", 9, MARINHO_SUAVE, True), 0, wx.BOTTOM, 5)
        layout.Add(texto(parent, "1234", 13, BRANCO, True), 0)
        layout.AddStretchSpacer()
        self.aviso_info = texto(
            parent,
            "Após redefinir a senha, entre usando a nova senha.",
            9,
            MARINHO_SUAVE,
        )
        self.aviso_info.Wrap(340)
        layout.Add(self.aviso_info, 0, wx.TOP, 12)

        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(layout, 1, wx.EXPAND | wx.ALL, 26)
        parent.SetSizer(margem)

    def montar_redefinicao(self, parent):
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(texto(parent, "RECUPERAÇÃO DE ACESSO", 9, VERDE, True), 0, wx.BOTTOM, 5)
        layout.Add(texto(parent, "Redefinir senha", 16, TEXTO, True), 0, wx.BOTTOM, 5)
        layout.Add(
            texto(parent, "Preencha os campos para atualizar sua senha.", 9, TEXTO_SUAVE),
            0,
            wx.BOTTOM,
            12,
        )

        self.rec_usuario = self.adicionar_campo(parent, layout, "Usuário:", largura_rotulo=142)
        self.rec_senha = self.adicionar_campo(parent, layout, "Nova senha:", senha=True, largura_rotulo=142)
        self.rec_confirmacao = self.adicionar_campo(
            parent,
            layout,
            "Confirme a senha:",
            senha=True,
            largura_rotulo=142,
        )
        self.rec_confirmacao.Bind(wx.EVT_TEXT_ENTER, self.salvar_nova_senha)

        salvar = BotaoCor(parent, "Salvar nova senha", AZUL, AZUL_ESCURO, largura=185)
        layout.Add(salvar, 0, wx.ALIGN_RIGHT | wx.TOP, 3)

        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(layout, 1, wx.EXPAND | wx.ALL, 20)
        parent.SetSizer(margem)
        salvar.Bind(wx.EVT_BUTTON, self.salvar_nova_senha)

    def focar_redefinicao(self, evento):
        self.rec_usuario.SetFocus()

    def entrar(self, evento):
        usuario = self.campo_usuario.GetValue().strip()
        senha = self.campo_senha.GetValue()

        if not usuario or not senha:
            wx.MessageBox("Preencha o usuário e a senha.", "Campos obrigatórios", wx.OK | wx.ICON_WARNING)
            return

        try:
            correto = autenticar(usuario, senha)
        except SQLAlchemyError as erro:
            wx.MessageBox(f"Erro ao consultar o banco MySQL:\n{erro}", "Erro", wx.OK | wx.ICON_ERROR)
            return

        if correto:
            self.campo_senha.Clear()
            Tela2(self, usuario).Show()
            self.Hide()
        else:
            wx.MessageBox("Usuário ou senha incorretos.", "Acesso negado", wx.OK | wx.ICON_ERROR)
            self.campo_senha.Clear()
            self.campo_senha.SetFocus()

    def salvar_nova_senha(self, evento):
        usuario = self.rec_usuario.GetValue().strip()
        nova_senha = self.rec_senha.GetValue()
        confirmacao = self.rec_confirmacao.GetValue()

        if not usuario or not nova_senha or not confirmacao:
            wx.MessageBox("Preencha os três campos.", "Campos obrigatórios", wx.OK | wx.ICON_WARNING)
            return
        if nova_senha != confirmacao:
            wx.MessageBox("As senhas digitadas são diferentes.", "Erro", wx.OK | wx.ICON_ERROR)
            return

        try:
            alterada = redefinir_senha(usuario, nova_senha)
        except SQLAlchemyError as erro:
            wx.MessageBox(f"Erro ao atualizar a senha no MySQL:\n{erro}", "Erro", wx.OK | wx.ICON_ERROR)
            return

        if not alterada:
            wx.MessageBox("Usuário não encontrado.", "Erro", wx.OK | wx.ICON_ERROR)
            return

        self.campo_usuario.SetValue(usuario)
        self.campo_senha.Clear()
        self.rec_senha.Clear()
        self.rec_confirmacao.Clear()
        self.aviso_info.SetLabel("Senha atualizada! Entre com sua nova senha.")
        wx.MessageBox(
            "Senha redefinida com sucesso! Faça o login com a nova senha.",
            "Sucesso",
            wx.OK | wx.ICON_INFORMATION,
        )


class Tela2(wx.Frame):
    def __init__(self, tela_login, usuario):
        super().__init__(None, title="Área restrita", size=(640, 430))
        self.tela_login = tela_login
        self.usuario = usuario
        self.SetMinSize((560, 390))
        self.CenterOnScreen()

        painel = wx.Panel(self)
        painel.SetBackgroundColour(FUNDO)
        layout = wx.BoxSizer(wx.VERTICAL)
        cartao = wx.Panel(painel)
        cartao.SetBackgroundColour(BRANCO)
        conteudo = wx.BoxSizer(wx.VERTICAL)

        conteudo.Add(texto(cartao, "ACESSO AUTORIZADO", 10, VERDE, True), 0, wx.ALIGN_CENTER | wx.BOTTOM, 12)
        conteudo.Add(texto(cartao, f"Bem-vindo(a), {usuario}!", 18, TEXTO, True), 0, wx.ALIGN_CENTER | wx.BOTTOM, 11)
        descricao = texto(cartao, "Faça uma consulta ao MySQL ou cadastre novos usuários.", 10, TEXTO_SUAVE)
        descricao.Wrap(430)
        conteudo.Add(descricao, 0, wx.ALIGN_CENTER | wx.BOTTOM, 21)

        consultar = BotaoCor(cartao, "Consultar meu cadastro", AZUL, AZUL_ESCURO, largura=260)
        conteudo.Add(consultar, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        gerenciar = BotaoCor(cartao, "Cadastrar e listar usuários", VERDE, VERDE_ESCURO, largura=260)
        conteudo.Add(gerenciar, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        sair = BotaoCor(cartao, "Sair da conta", VERMELHO, VERMELHO_ESCURO, largura=260)
        conteudo.Add(sair, 0, wx.ALIGN_CENTER)

        bordas = wx.BoxSizer(wx.VERTICAL)
        bordas.Add(conteudo, 1, wx.ALIGN_CENTER | wx.ALL, 26)
        cartao.SetSizer(bordas)
        layout.AddStretchSpacer()
        layout.Add(cartao, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 24)
        layout.AddStretchSpacer()
        painel.SetSizer(layout)

        consultar.Bind(wx.EVT_BUTTON, self.consultar_cadastro)
        gerenciar.Bind(wx.EVT_BUTTON, self.abrir_gerenciamento)
        sair.Bind(wx.EVT_BUTTON, lambda evento: self.Close())
        self.Bind(wx.EVT_CLOSE, self.fechar)

    def consultar_cadastro(self, evento):
        try:
            registro = consultar_usuario(self.usuario)
        except SQLAlchemyError as erro:
            wx.MessageBox(f"Erro ao consultar o MySQL:\n{erro}", "Erro", wx.OK | wx.ICON_ERROR)
            return

        if registro is None:
            wx.MessageBox("Usuário não encontrado no banco.", "Consulta", wx.OK | wx.ICON_WARNING)
            return

        identificador, nome = registro
        wx.MessageBox(
            f"Consulta feita no MySQL!\n\nID: {identificador}\nUsuário: {nome}",
            "Cadastro encontrado",
            wx.OK | wx.ICON_INFORMATION,
        )

    def abrir_gerenciamento(self, evento):
        janela = GerenciarUsuarios(self)
        janela.ShowModal()
        janela.Destroy()

    def fechar(self, evento):
        self.tela_login.Show()
        self.tela_login.Raise()
        self.Destroy()


class GerenciarUsuarios(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Usuários cadastrados no MySQL", size=(750, 600))
        self.SetMinSize((620, 530))
        self.CenterOnParent()

        painel = wx.Panel(self)
        painel.SetBackgroundColour(FUNDO)
        principal = wx.BoxSizer(wx.VERTICAL)
        principal.Add(texto(painel, "USUÁRIOS DO BANCO MYSQL", 10, AZUL, True), 0, wx.BOTTOM, 5)
        principal.Add(texto(painel, "Cadastrar e consultar usuários", 17, TEXTO, True), 0, wx.BOTTOM, 5)
        principal.Add(
            texto(painel, "Os dados são gravados e consultados diretamente no MySQL.", 10, TEXTO_SUAVE),
            0, wx.BOTTOM, 15,
        )

        cartao = wx.Panel(painel)
        cartao.SetBackgroundColour(BRANCO)
        formulario = wx.BoxSizer(wx.VERTICAL)
        formulario.Add(texto(cartao, "NOVO USUÁRIO", 10, AZUL, True), 0, wx.BOTTOM, 13)
        self.nome = Tela.adicionar_campo(cartao, formulario, "Nome:", largura_rotulo=130)
        self.senha = Tela.adicionar_campo(cartao, formulario, "Senha:", senha=True, largura_rotulo=130)
        self.confirmacao = Tela.adicionar_campo(cartao, formulario, "Confirme a senha:", senha=True, largura_rotulo=130)
        cadastrar = BotaoCor(cartao, "Cadastrar usuário", VERDE, VERDE_ESCURO, largura=190)
        formulario.Add(cadastrar, 0, wx.ALIGN_RIGHT | wx.TOP, 6)
        margem_cartao = wx.BoxSizer(wx.VERTICAL)
        margem_cartao.Add(formulario, 1, wx.EXPAND | wx.ALL, 18)
        cartao.SetSizer(margem_cartao)
        principal.Add(cartao, 0, wx.EXPAND | wx.BOTTOM, 17)

        principal.Add(texto(painel, "USUÁRIOS SALVOS", 10, AZUL, True), 0, wx.BOTTOM, 7)
        self.lista = wx.ListCtrl(painel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SIMPLE)
        self.lista.InsertColumn(0, "ID", width=95)
        self.lista.InsertColumn(1, "Nome do usuário", width=490)
        self.lista.SetBackgroundColour(BRANCO)
        self.lista.SetForegroundColour(TEXTO)
        self.lista.SetFont(fonte(10))
        principal.Add(self.lista, 1, wx.EXPAND | wx.BOTTOM, 10)

        acoes = wx.BoxSizer(wx.HORIZONTAL)
        recarregar = BotaoCor(painel, "Recarregar lista", AZUL, AZUL_ESCURO, largura=175)
        visualizar = BotaoCor(painel, "Ver selecionado", VERDE, VERDE_ESCURO, largura=175)
        fechar = BotaoCor(painel, "Fechar", VERMELHO, VERMELHO_ESCURO, largura=120)
        acoes.Add(recarregar, 0, wx.RIGHT, 10)
        acoes.Add(visualizar, 0, wx.RIGHT, 10)
        acoes.AddStretchSpacer()
        acoes.Add(fechar, 0)
        principal.Add(acoes, 0, wx.EXPAND)

        bordas = wx.BoxSizer(wx.VERTICAL)
        bordas.Add(principal, 1, wx.EXPAND | wx.ALL, 20)
        painel.SetSizer(bordas)
        raiz = wx.BoxSizer(wx.VERTICAL)
        raiz.Add(painel, 1, wx.EXPAND)
        self.SetSizer(raiz)

        cadastrar.Bind(wx.EVT_BUTTON, self.cadastrar)
        recarregar.Bind(wx.EVT_BUTTON, self.recarregar)
        visualizar.Bind(wx.EVT_BUTTON, self.ver_selecionado)
        self.lista.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.ver_selecionado)
        fechar.Bind(wx.EVT_BUTTON, lambda evento: self.EndModal(wx.ID_OK))
        self.recarregar(None)

    def cadastrar(self, evento):
        nome = self.nome.GetValue().strip()
        senha = self.senha.GetValue()
        confirmacao = self.confirmacao.GetValue()

        if not nome or not senha or not confirmacao:
            wx.MessageBox("Preencha nome, senha e confirmação.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        if len(nome) > 80:
            wx.MessageBox("O nome deve ter no máximo 80 caracteres.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        if senha != confirmacao:
            wx.MessageBox("As senhas não coincidem.", "Atenção", wx.OK | wx.ICON_WARNING)
            return

        try:
            criado = cadastrar_usuario(nome, senha)
        except (SQLAlchemyError, ValueError) as erro:
            wx.MessageBox(f"Não foi possível cadastrar no MySQL:\n{erro}", "Erro", wx.OK | wx.ICON_ERROR)
            return

        if not criado:
            wx.MessageBox("Esse nome de usuário já está cadastrado.", "Atenção", wx.OK | wx.ICON_WARNING)
            return

        self.nome.Clear()
        self.senha.Clear()
        self.confirmacao.Clear()
        self.recarregar(None)
        wx.MessageBox("Usuário salvo no MySQL! Você poderá entrar com esse login.", "Sucesso", wx.OK | wx.ICON_INFORMATION)

    def recarregar(self, evento):
        try:
            usuarios = listar_usuarios()
        except SQLAlchemyError as erro:
            wx.MessageBox(f"Erro ao consultar os usuários:\n{erro}", "Erro", wx.OK | wx.ICON_ERROR)
            return

        self.lista.DeleteAllItems()
        for identificador, nome in usuarios:
            indice = self.lista.InsertItem(self.lista.GetItemCount(), str(identificador))
            self.lista.SetItem(indice, 1, nome)

    def ver_selecionado(self, evento):
        indice = self.lista.GetFirstSelected()
        if indice == -1:
            wx.MessageBox("Selecione um usuário na lista.", "Atenção", wx.OK | wx.ICON_WARNING)
            return

        identificador = self.lista.GetItemText(indice, 0)
        nome = self.lista.GetItemText(indice, 1)
        wx.MessageBox(
            f"Usuário obtido do MySQL:\n\nID: {identificador}\nNome: {nome}",
            "Dados do usuário",
            wx.OK | wx.ICON_INFORMATION,
        )


class Programa(wx.App):
    def OnInit(self):
        try:
            iniciar_banco()
        except (SQLAlchemyError, ValueError, OSError) as erro:
            wx.MessageBox(
                f"Não foi possível conectar ao MySQL.\nConfira o serviço, a conexão e o arquivo .env.\n\nDetalhes: {erro}",
                "Erro",
                wx.OK | wx.ICON_ERROR,
            )
            return False

        self.frame = Tela()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = Programa(False)
    app.MainLoop()
