"""Seis telas wxPython. Os botões chamam as funções do arquivo banco.py."""
import wx
from mysql.connector import Error

import banco


class Janela(wx.Frame):
    """Uma janela principal troca o painel para navegar entre as seis telas."""

    def __init__(self):
        super().__init__(None, title='ConectaVagas', size=(720, 740))
        self.SetMinSize((600, 580))
        self.usuario = None  # Depois do login, guarda id, nome e e-mail da conta.
        self.painel = None
        self.Centre()
        self.tela_login()

    def nova_tela(self, titulo):
        """Prepara uma página vazia com título e espaço para os componentes."""
        if self.painel:
            self.painel.Destroy()
        # A rolagem permite acessar formulários em uma tela pequena.
        self.painel = wx.ScrolledWindow(self)
        self.painel.SetScrollRate(0, 15)
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.painel.SetSizer(self.layout)
        self.texto(titulo)

    def mostrar_tela(self):
        """Recalcula os espaços depois que os componentes foram adicionados."""
        self.painel.SetSize(self.GetClientSize())
        self.painel.Layout()
        self.painel.FitInside()
        self.Layout()

    def texto(self, mensagem):
        controle = wx.StaticText(self.painel, label=mensagem)
        controle.Wrap(540)
        self.layout.Add(controle, 0, wx.ALL, 10)

    def campo(self, legenda, valor='', estilo=0):
        """Cria um campo e o devolve para que a tela possa ler seu conteúdo."""
        self.texto(legenda)
        controle = wx.TextCtrl(self.painel, value=valor, style=estilo)
        self.layout.Add(controle, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        return controle

    def botao(self, legenda, acao):
        """Liga um botão à ação e mostra uma mensagem se essa ação falhar."""
        controle = wx.Button(self.painel, label=legenda)

        def ao_clicar(evento):
            # wxPython fornece o evento. acao é a função escolhida pela tela.
            try:
                acao()
            except ValueError as erro:
                wx.MessageBox(str(erro), 'Verifique os dados', wx.OK | wx.ICON_INFORMATION)
            except Error:
                wx.MessageBox('Confira o MySQL e os dados em config.py.', 'Erro no banco',
                              wx.OK | wx.ICON_ERROR)

        controle.Bind(wx.EVT_BUTTON, ao_clicar)
        self.layout.Add(controle, 0, wx.ALL, 10)

    # TELA 1 — LOGIN
    def tela_login(self):
        self.usuario = None
        self.nova_tela('Entrar no ConectaVagas')
        self.email = self.campo('E-mail')
        self.senha = self.campo('Senha', estilo=wx.TE_PASSWORD)
        self.botao('Entrar', self.fazer_login)
        self.botao('Criar conta', self.tela_cadastro)
        self.mostrar_tela()

    def fazer_login(self):
        # GetValue() lê o texto digitado no controle visual.
        usuario = banco.entrar(self.email.GetValue(), self.senha.GetValue())
        if usuario is None:
            raise ValueError('E-mail ou senha incorretos.')
        self.usuario = usuario
        self.tela_inicio()

    # TELA 2 — CADASTRO DE CONTA
    def tela_cadastro(self):
        self.nova_tela('Criar conta')
        self.nome = self.campo('Nome')
        self.email = self.campo('E-mail')
        self.senha = self.campo('Senha com pelo menos 8 caracteres', estilo=wx.TE_PASSWORD)
        self.botao('Cadastrar', self.salvar_usuario)
        self.botao('Voltar', self.tela_login)
        self.mostrar_tela()

    def salvar_usuario(self):
        banco.cadastrar_usuario(self.nome.GetValue(), self.email.GetValue(), self.senha.GetValue())
        wx.MessageBox('Conta criada. Agora entre com seu e-mail e senha.', 'Cadastro')
        self.tela_login()

    # TELA 3 — INÍCIO
    def tela_inicio(self):
        self.nova_tela('ConectaVagas')
        self.texto('Olá, ' + self.usuario['nome'] + '!')
        self.texto('Divulgue oportunidades e encontre vagas na sua região.')
        self.botao('Consultar vagas', self.tela_vagas)
        self.botao('Publicar vaga', self.tela_publicar)
        self.botao('Sair da conta', self.tela_login)
        self.mostrar_tela()

    # TELA 4 — CONSULTA DE VAGAS
    def tela_vagas(self):
        self.nova_tela('Consultar vagas')
        self.busca = self.campo('Pesquisar pelo título da vaga')
        self.botao('Pesquisar', self.pesquisar)
        self.lista = wx.ListBox(self.painel, size=(-1, 180))
        self.layout.Add(self.lista, 0, wx.EXPAND | wx.ALL, 10)
        self.botao('Ver detalhes da vaga selecionada', self.abrir_detalhes)
        self.botao('Voltar ao início', self.tela_inicio)
        self.pesquisar()
        self.mostrar_tela()

    def pesquisar(self):
        # Os dados completos ficam na lista Python. A lista visual mostra um resumo.
        self.vagas = banco.listar_vagas(self.busca.GetValue())
        self.lista.Clear()
        for vaga in self.vagas:
            self.lista.Append(vaga['titulo'] + ' — ' + vaga['empresa'] + ' — ' + vaga['cidade'])

    def abrir_detalhes(self):
        indice = self.lista.GetSelection()
        if indice == wx.NOT_FOUND:
            raise ValueError('Selecione uma vaga na lista.')
        self.vaga = self.vagas[indice]  # A posição da linha indica o dicionário escolhido.
        self.tela_detalhes()

    # TELA 5 — DETALHES DA VAGA
    def tela_detalhes(self):
        self.nova_tela(self.vaga['titulo'])
        self.texto('Empresa — ' + self.vaga['empresa'])
        self.texto('Cidade — ' + self.vaga['cidade'])
        self.texto('Publicado por — ' + self.vaga['anunciante'])
        self.texto(self.vaga['descricao'])
        self.texto('Para se candidatar, entre em contato por ' + self.vaga['contato'])
        # Somente o autor recebe o botão de exclusão. O SQL também confere a autoria.
        if self.vaga['usuario_id'] == self.usuario['id']:
            self.botao('Excluir minha vaga', self.excluir)
        self.botao('Voltar às vagas', self.tela_vagas)
        self.mostrar_tela()

    def excluir(self):
        resposta = wx.MessageBox('Excluir esta vaga?', 'Confirmar', wx.YES_NO | wx.NO_DEFAULT)
        if resposta == wx.YES:
            banco.excluir_vaga(self.vaga['id'], self.usuario['id'])
            self.tela_vagas()

    # TELA 6 — PUBLICAÇÃO DE VAGA
    def tela_publicar(self):
        self.nova_tela('Publicar vaga')
        self.titulo = self.campo('Título da vaga')
        self.empresa = self.campo('Empresa')
        self.cidade = self.campo('Cidade', 'Porto Velho')
        self.descricao = self.campo('Descrição e requisitos', estilo=wx.TE_MULTILINE)
        self.contato = self.campo('Contato para candidatura, como e-mail ou telefone')
        self.botao('Salvar vaga', self.salvar_vaga)
        self.botao('Cancelar', self.tela_inicio)
        self.mostrar_tela()

    def salvar_vaga(self):
        # O ID vem do login. Os outros valores são lidos dos campos desta tela.
        banco.publicar_vaga(self.usuario['id'], self.titulo.GetValue(), self.empresa.GetValue(),
                            self.cidade.GetValue(), self.descricao.GetValue(), self.contato.GetValue())
        wx.MessageBox('Vaga publicada!', 'Cadastro de vaga')
        self.tela_vagas()


# MainLoop mantém o programa aberto para receber cliques e outros eventos.
if __name__ == '__main__':
    aplicativo = wx.App(False)
    janela = Janela()
    janela.Show()
    aplicativo.MainLoop()
