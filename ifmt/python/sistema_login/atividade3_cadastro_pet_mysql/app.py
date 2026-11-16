"""Terceira atividade avaliativa: login e cadastro de PETs com wxPython."""

import wx
from sqlalchemy.exc import SQLAlchemyError
from wx.lib.buttons import GenButton

from banco import (
    SITUACOES,
    autenticar,
    atualizar_pet,
    cadastrar_pet,
    criar_usuario,
    excluir_pet,
    iniciar_banco,
    listar_pets,
)


FUNDO = "#F3F6FB"
BRANCO = "#FFFFFF"
TEXTO = "#17243C"
SUAVE = "#697892"
AZUL = "#2E5BCE"
AZUL_ESCURO = "#2049B4"
VERDE = "#1FA77A"
VERDE_ESCURO = "#18845F"
VERMELHO = "#E45D69"
VERMELHO_ESCURO = "#C94855"


def rotulo(parent, mensagem, tamanho=10, cor=TEXTO, negrito=False):
    label = wx.StaticText(parent, label=mensagem)
    label.SetFont(wx.Font(
        tamanho, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
        wx.FONTWEIGHT_BOLD if negrito else wx.FONTWEIGHT_NORMAL,
    ))
    label.SetForegroundColour(cor)
    return label


def campo_texto(parent, senha=False):
    estilo = wx.TE_PROCESS_ENTER | (wx.TE_PASSWORD if senha else 0)
    entrada = wx.TextCtrl(parent, style=estilo, size=(-1, 34))
    entrada.SetMinSize((180, 34))
    return entrada


class Botao(GenButton):
    def __init__(self, parent, legenda, cor=AZUL, cor_hover=AZUL_ESCURO):
        super().__init__(parent, label=legenda, size=(-1, 39))
        self.SetBezelWidth(0)
        self.SetUseFocusIndicator(False)
        self.SetBackgroundColour(cor)
        self.SetForegroundColour(BRANCO)
        self.SetMinSize((135, 39))
        self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.normal, self.hover = cor, cor_hover
        self.Bind(wx.EVT_ENTER_WINDOW, self.entrar)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.sair)

    def entrar(self, evento):
        self.SetBackgroundColour(self.hover)
        self.Refresh()
        evento.Skip()

    def sair(self, evento):
        self.SetBackgroundColour(self.normal)
        self.Refresh()
        evento.Skip()


class DialogoNovaConta(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Criar conta", size=(430, 340))
        painel = wx.Panel(self)
        painel.SetBackgroundColour(FUNDO)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(rotulo(painel, "CADASTRAR USUÁRIO", 16, TEXTO, True), 0, wx.BOTTOM, 15)

        self.login = campo_texto(painel)
        self.senha = campo_texto(painel, senha=True)
        self.confirmacao = campo_texto(painel, senha=True)
        for titulo, entrada in (
            ("Login:", self.login),
            ("Senha:", self.senha),
            ("Confirmar senha:", self.confirmacao),
        ):
            layout.Add(rotulo(painel, titulo), 0, wx.BOTTOM, 4)
            layout.Add(entrada, 0, wx.EXPAND | wx.BOTTOM, 10)

        botoes = wx.BoxSizer(wx.HORIZONTAL)
        salvar = Botao(painel, "Criar conta", VERDE, VERDE_ESCURO)
        cancelar = Botao(painel, "Cancelar", VERMELHO, VERMELHO_ESCURO)
        botoes.Add(salvar, 1, wx.RIGHT, 10)
        botoes.Add(cancelar, 1)
        layout.Add(botoes, 0, wx.EXPAND | wx.TOP, 4)
        painel.SetSizer(layout)
        externo = wx.BoxSizer(wx.VERTICAL)
        externo.Add(painel, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(externo)
        self.CenterOnParent()
        salvar.Bind(wx.EVT_BUTTON, self.confirmar)
        cancelar.Bind(wx.EVT_BUTTON, lambda evento: self.EndModal(wx.ID_CANCEL))

    def confirmar(self, evento):
        login = self.login.GetValue().strip()
        senha = self.senha.GetValue()
        if senha != self.confirmacao.GetValue():
            wx.MessageBox("As senhas são diferentes.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        try:
            criado = criar_usuario(login, senha)
        except (SQLAlchemyError, ValueError) as erro:
            wx.MessageBox(str(erro), "Não foi possível cadastrar", wx.OK | wx.ICON_ERROR)
            return
        if not criado:
            wx.MessageBox("Esse login já existe.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        self.EndModal(wx.ID_OK)


class TelaLogin(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Sistema de PETs | Login", size=(525, 510))
        self.SetMinSize((480, 460))
        self.CenterOnScreen()
        painel = wx.Panel(self)
        painel.SetBackgroundColour(FUNDO)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(rotulo(painel, "TERCEIRA ATIVIDADE AVALIATIVA", 9, AZUL, True), 0, wx.BOTTOM, 8)
        layout.Add(rotulo(painel, "Meu histórico de PETs", 22, TEXTO, True), 0, wx.BOTTOM, 7)
        layout.Add(rotulo(painel, "Entre para visualizar somente os seus animais.", 10, SUAVE), 0, wx.BOTTOM, 23)

        cartao = wx.Panel(painel)
        cartao.SetBackgroundColour(BRANCO)
        formulario = wx.BoxSizer(wx.VERTICAL)
        formulario.Add(rotulo(cartao, "LOGIN", 10, AZUL, True), 0, wx.BOTTOM, 10)
        formulario.Add(rotulo(cartao, "Usuário"), 0, wx.BOTTOM, 5)
        self.login = campo_texto(cartao)
        formulario.Add(self.login, 0, wx.EXPAND | wx.BOTTOM, 13)
        formulario.Add(rotulo(cartao, "Senha"), 0, wx.BOTTOM, 5)
        self.senha = campo_texto(cartao, senha=True)
        formulario.Add(self.senha, 0, wx.EXPAND | wx.BOTTOM, 18)
        botoes = wx.BoxSizer(wx.HORIZONTAL)
        entrar = Botao(cartao, "Entrar", VERDE, VERDE_ESCURO)
        registrar = Botao(cartao, "Criar conta")
        botoes.Add(entrar, 1, wx.RIGHT, 12)
        botoes.Add(registrar, 1)
        formulario.Add(botoes, 0, wx.EXPAND)
        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(formulario, 1, wx.EXPAND | wx.ALL, 24)
        cartao.SetSizer(margem)
        layout.Add(cartao, 0, wx.EXPAND | wx.BOTTOM, 17)
        layout.Add(rotulo(painel, "Primeiro acesso: usuário Fulano | senha 1234", 10, SUAVE), 0)

        externo = wx.BoxSizer(wx.VERTICAL)
        externo.Add(layout, 1, wx.EXPAND | wx.ALL, 24)
        painel.SetSizer(externo)
        entrar.Bind(wx.EVT_BUTTON, self.entrar)
        registrar.Bind(wx.EVT_BUTTON, self.criar_conta)
        self.senha.Bind(wx.EVT_TEXT_ENTER, self.entrar)

    def entrar(self, evento):
        login, senha = self.login.GetValue().strip(), self.senha.GetValue()
        if not login or not senha:
            wx.MessageBox("Informe login e senha.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        try:
            autenticado = autenticar(login, senha)
        except SQLAlchemyError as erro:
            wx.MessageBox(str(erro), "Erro no MySQL", wx.OK | wx.ICON_ERROR)
            return
        if autenticado is None:
            wx.MessageBox("Login ou senha incorretos.", "Acesso negado", wx.OK | wx.ICON_ERROR)
            self.senha.Clear()
            return
        self.senha.Clear()
        identificador, nome = autenticado
        TelaPets(self, identificador, nome).Show()
        self.Hide()

    def criar_conta(self, evento):
        dialogo = DialogoNovaConta(self)
        resultado = dialogo.ShowModal()
        if resultado == wx.ID_OK:
            self.login.SetValue(dialogo.login.GetValue().strip())
            self.senha.Clear()
        dialogo.Destroy()
        if resultado == wx.ID_OK:
            wx.MessageBox("Conta criada! Agora entre com sua senha.", "Sucesso", wx.OK | wx.ICON_INFORMATION)


class TelaPets(wx.Frame):
    def __init__(self, tela_login, usuario_id, login):
        super().__init__(None, title="Meu histórico de PETs", size=(1040, 810))
        self.SetMinSize((790, 640))
        self.CenterOnScreen()
        self.tela_login = tela_login
        self.usuario_id = usuario_id  # Obtido do login; nunca digitado pelo usuário.
        self.pet_em_edicao = None
        self.pets_por_id = {}

        painel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        painel.SetScrollRate(0, 15)
        painel.SetBackgroundColour(FUNDO)
        principal = wx.BoxSizer(wx.VERTICAL)
        principal.Add(rotulo(painel, "MEU HISTÓRICO DE PETS", 9, AZUL, True), 0, wx.BOTTOM, 5)
        principal.Add(rotulo(painel, f"Bem-vindo(a), {login}!", 21, TEXTO, True), 0, wx.BOTTOM, 5)
        principal.Add(rotulo(painel, "Registre os animais que você tem ou já teve.", 10, SUAVE), 0, wx.BOTTOM, 18)

        cartao = wx.Panel(painel)
        cartao.SetBackgroundColour(BRANCO)
        formulario = wx.BoxSizer(wx.VERTICAL)
        self.titulo_formulario = rotulo(cartao, "CADASTRAR NOVO PET", 12, AZUL, True)
        formulario.Add(self.titulo_formulario, 0, wx.BOTTOM, 13)
        grade = wx.FlexGridSizer(rows=3, cols=2, vgap=12, hgap=20)
        grade.AddGrowableCol(0, 1)
        grade.AddGrowableCol(1, 1)

        self.campos = {}
        for legenda, chave in (
            ("Nome do PET", "nome"),
            ("Idade (anos)", "idade"),
            ("Raça", "raca"),
            ("Peso (kg)", "peso"),
            ("Cor", "cor"),
        ):
            coluna = wx.BoxSizer(wx.VERTICAL)
            coluna.Add(rotulo(cartao, legenda), 0, wx.BOTTOM, 5)
            entrada = campo_texto(cartao)
            coluna.Add(entrada, 0, wx.EXPAND)
            grade.Add(coluna, 1, wx.EXPAND)
            self.campos[chave] = entrada

        coluna_situacao = wx.BoxSizer(wx.VERTICAL)
        coluna_situacao.Add(rotulo(cartao, "Situação"), 0, wx.BOTTOM, 5)
        self.situacao = wx.Choice(cartao, choices=list(SITUACOES))
        self.situacao.SetSelection(0)
        coluna_situacao.Add(self.situacao, 0, wx.EXPAND)
        grade.Add(coluna_situacao, 1, wx.EXPAND)
        formulario.Add(grade, 0, wx.EXPAND | wx.BOTTOM, 17)

        botoes_form = wx.BoxSizer(wx.HORIZONTAL)
        self.botao_salvar = Botao(cartao, "Salvar PET", VERDE, VERDE_ESCURO)
        limpar = Botao(cartao, "Novo / Limpar")
        botoes_form.Add(self.botao_salvar, 0, wx.RIGHT, 12)
        botoes_form.Add(limpar, 0)
        formulario.Add(botoes_form, 0)
        margem = wx.BoxSizer(wx.VERTICAL)
        margem.Add(formulario, 1, wx.EXPAND | wx.ALL, 20)
        cartao.SetSizer(margem)
        principal.Add(cartao, 0, wx.EXPAND | wx.BOTTOM, 18)

        principal.Add(rotulo(painel, "MEUS PETS CADASTRADOS", 12, AZUL, True), 0, wx.BOTTOM, 6)
        principal.Add(rotulo(painel, "Selecione um animal na lista para alterar ou excluir.", 10, SUAVE), 0, wx.BOTTOM, 9)
        self.lista = wx.ListCtrl(painel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SIMPLE)
        for indice, (titulo, largura) in enumerate((
            ("ID", 60), ("Nome", 160), ("Idade", 75), ("Raça", 170),
            ("Peso (kg)", 110), ("Cor", 130), ("Situação", 175),
        )):
            self.lista.InsertColumn(indice, titulo, width=largura)
        self.lista.SetBackgroundColour(BRANCO)
        self.lista.SetMinSize((-1, 190))
        principal.Add(self.lista, 1, wx.EXPAND | wx.BOTTOM, 12)

        acoes = wx.BoxSizer(wx.HORIZONTAL)
        recarregar = Botao(painel, "Recarregar lista")
        excluir = Botao(painel, "Excluir selecionado", VERMELHO, VERMELHO_ESCURO)
        sair = Botao(painel, "Sair da conta", VERMELHO, VERMELHO_ESCURO)
        acoes.Add(recarregar, 0, wx.RIGHT, 10)
        acoes.Add(excluir, 0, wx.RIGHT, 10)
        acoes.AddStretchSpacer()
        acoes.Add(sair, 0)
        principal.Add(acoes, 0, wx.EXPAND)

        externo = wx.BoxSizer(wx.VERTICAL)
        externo.Add(principal, 1, wx.EXPAND | wx.ALL, 22)
        painel.SetSizer(externo)
        painel.FitInside()

        self.botao_salvar.Bind(wx.EVT_BUTTON, self.salvar_pet)
        limpar.Bind(wx.EVT_BUTTON, self.limpar)
        recarregar.Bind(wx.EVT_BUTTON, self.recarregar)
        excluir.Bind(wx.EVT_BUTTON, self.excluir_pet)
        sair.Bind(wx.EVT_BUTTON, lambda evento: self.Close())
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selecionar_pet)
        self.Bind(wx.EVT_CLOSE, self.fechar)
        self.recarregar(None)

    def limpar(self, evento):
        self.pet_em_edicao = None
        for entrada in self.campos.values():
            entrada.Clear()
        self.situacao.SetSelection(0)
        self.titulo_formulario.SetLabel("CADASTRAR NOVO PET")
        self.botao_salvar.SetLabel("Salvar PET")
        selecionado = self.lista.GetFirstSelected()
        if selecionado != -1:
            self.lista.SetItemState(selecionado, 0, wx.LIST_STATE_SELECTED)

    def selecionar_pet(self, evento):
        identificador = int(self.lista.GetItemText(evento.GetIndex(), 0))
        pet = self.pets_por_id.get(identificador)
        if pet is None:
            return
        _, nome, idade, raca, peso, cor, situacao = pet
        for chave, valor in (
            ("nome", nome), ("idade", str(idade)), ("raca", raca),
            ("peso", f"{peso:.2f}"), ("cor", cor),
        ):
            self.campos[chave].SetValue(valor)
        self.situacao.SetStringSelection(situacao)
        self.pet_em_edicao = identificador
        self.titulo_formulario.SetLabel(f"EDITAR PET Nº {identificador}")
        self.botao_salvar.SetLabel("Salvar alterações")

    def _dados_formulario(self):
        return (
            self.campos["nome"].GetValue(),
            self.campos["idade"].GetValue(),
            self.campos["raca"].GetValue(),
            self.campos["peso"].GetValue(),
            self.campos["cor"].GetValue(),
            self.situacao.GetStringSelection(),
        )

    def salvar_pet(self, evento):
        try:
            dados = self._dados_formulario()
            if self.pet_em_edicao is None:
                cadastrar_pet(self.usuario_id, *dados)
                mensagem = "PET cadastrado com sucesso!"
            else:
                if not atualizar_pet(self.usuario_id, self.pet_em_edicao, *dados):
                    wx.MessageBox("PET não encontrado na sua conta.", "Atenção", wx.OK | wx.ICON_WARNING)
                    return
                mensagem = "Dados do PET atualizados!"
        except ValueError as erro:
            wx.MessageBox(str(erro), "Confira os campos", wx.OK | wx.ICON_WARNING)
            return
        except SQLAlchemyError as erro:
            wx.MessageBox(str(erro), "Erro no MySQL", wx.OK | wx.ICON_ERROR)
            return
        self.recarregar(None)
        self.limpar(None)
        wx.MessageBox(mensagem, "Sucesso", wx.OK | wx.ICON_INFORMATION)

    def recarregar(self, evento):
        try:
            registros = listar_pets(self.usuario_id)
        except SQLAlchemyError as erro:
            wx.MessageBox(str(erro), "Erro ao consultar o MySQL", wx.OK | wx.ICON_ERROR)
            return
        self.lista.DeleteAllItems()
        self.pets_por_id = {pet[0]: pet for pet in registros}
        for identificador, nome, idade, raca, peso, cor, situacao in registros:
            indice = self.lista.InsertItem(self.lista.GetItemCount(), str(identificador))
            for coluna, valor in enumerate((nome, idade, raca, f"{peso:.2f}", cor, situacao), start=1):
                self.lista.SetItem(indice, coluna, str(valor))

    def excluir_pet(self, evento):
        indice = self.lista.GetFirstSelected()
        if indice == -1:
            wx.MessageBox("Selecione um PET para excluir.", "Atenção", wx.OK | wx.ICON_WARNING)
            return
        identificador = int(self.lista.GetItemText(indice, 0))
        confirmacao = wx.MessageBox(
            "Deseja realmente excluir esse PET?", "Confirmar exclusão",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION,
        )
        if confirmacao != wx.YES:
            return
        try:
            excluido = excluir_pet(self.usuario_id, identificador)
        except SQLAlchemyError as erro:
            wx.MessageBox(str(erro), "Erro no MySQL", wx.OK | wx.ICON_ERROR)
            return
        if not excluido:
            wx.MessageBox("PET não encontrado na sua conta.", "Atenção", wx.OK | wx.ICON_WARNING)
        self.recarregar(None)
        self.limpar(None)

    def fechar(self, evento):
        self.tela_login.senha.Clear()
        self.tela_login.Show()
        self.tela_login.Raise()
        self.Destroy()


class Programa(wx.App):
    def OnInit(self):
        try:
            iniciar_banco()
        except (SQLAlchemyError, ValueError, OSError) as erro:
            wx.MessageBox(
                f"Não foi possível conectar ao MySQL. Confira o serviço e o arquivo .env.\n\n{erro}",
                "Erro de conexão", wx.OK | wx.ICON_ERROR,
            )
            return False
        self.frame = TelaLogin()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = Programa(False)
    app.MainLoop()
