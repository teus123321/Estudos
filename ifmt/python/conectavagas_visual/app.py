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

    def nova_tela(self, titulo, secao):
        """Todas as telas usam o mesmo cabeçalho e a mesma área de conteúdo."""
        if self.painel:
            self.painel.Destroy()
        self.painel = wx.ScrolledWindow(self)
        self.painel.SetScrollRate(0, 15)
        self.painel.SetBackgroundColour('#F3F6F5')
        pagina = wx.BoxSizer(wx.VERTICAL)
        self.painel.SetSizer(pagina)

        topo = wx.Panel(self.painel)
        topo.SetBackgroundColour('#143B40')
        faixa = wx.BoxSizer(wx.HORIZONTAL)
        topo.SetSizer(faixa)
        marca = wx.StaticText(topo, label='ConectaVagas')
        marca.SetFont(marca.GetFont().Bold().Scaled(1.45))
        marca.SetForegroundColour('#FFFFFF')
        faixa.Add(marca, 0, wx.ALL, 18)
        faixa.AddStretchSpacer()
        area = wx.StaticText(topo, label=secao)
        area.SetForegroundColour('#C1EFE0')
        faixa.Add(area, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 20)
        pagina.Add(topo, 0, wx.EXPAND)

        self.cartao = wx.Panel(self.painel)
        self.cartao.SetBackgroundColour('#FFFFFF')
        margem = wx.BoxSizer(wx.VERTICAL)
        self.cartao.SetSizer(margem)
        self.layout = wx.BoxSizer(wx.VERTICAL)
        margem.Add(self.layout, 1, wx.EXPAND | wx.ALL, 22)
        pagina.Add(self.cartao, 0, wx.EXPAND | wx.ALL, 20)
        cabecalho = self.texto(titulo, destaque=True)
        cabecalho.SetFont(cabecalho.GetFont().Scaled(1.65))
        cabecalho.Wrap(455)

    def mostrar_tela(self):
        """Recalcula os espaços depois que os componentes foram adicionados."""
        self.painel.SetSize(self.GetClientSize())
        self.painel.Layout()
        self.painel.FitInside()
        self.Layout()

    def texto(self, mensagem, destaque=False):
        controle = wx.StaticText(self.cartao, label=mensagem)
        controle.SetForegroundColour('#173D40' if destaque else '#40585A')
        if destaque:
            controle.SetFont(controle.GetFont().Bold())
        controle.Wrap(455)
        self.layout.Add(controle, 0, wx.BOTTOM, 8)
        return controle

    def campo(self, legenda, valor='', estilo=0):
        """Rótulo e campo ficam juntos. O controle devolvido permite ler o valor."""
        self.texto(legenda, destaque=True)
        controle = wx.TextCtrl(self.cartao, value=valor, style=estilo)
        altura = 82 if estilo == wx.TE_MULTILINE else 36
        controle.SetMinSize((-1, altura))
        self.layout.Add(controle, 0, wx.EXPAND | wx.BOTTOM, 14)
        return controle

    def botao(self, legenda, acao, principal=False):
        """O botão principal recebe destaque. Cada clique chama uma ação da tela."""
        controle = wx.Button(self.cartao, label=legenda)
        controle.SetMinSize((-1, 38))
        if principal:
            controle.SetBackgroundColour('#176456')
            controle.SetForegroundColour('#FFFFFF')
            controle.SetFont(controle.GetFont().Bold())

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
        self.layout.Add(controle, 0, wx.EXPAND | wx.TOP, 8)

    # TELA 1 — LOGIN
    def tela_login(self):
        self.usuario = None
        self.nova_tela('Entrar na sua conta', 'Acesso')
        self.email = self.campo('E-mail')
        self.senha = self.campo('Senha', estilo=wx.TE_PASSWORD)
        self.botao('Entrar', self.fazer_login, principal=True)
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
        self.nova_tela('Criar conta', 'Acesso')
        self.nome = self.campo('Nome')
        self.email = self.campo('E-mail')
        self.senha = self.campo('Senha com pelo menos 8 caracteres', estilo=wx.TE_PASSWORD)
        self.botao('Cadastrar', self.salvar_usuario, principal=True)
        self.botao('Voltar', self.tela_login)
        self.mostrar_tela()

    def salvar_usuario(self):
        banco.cadastrar_usuario(self.nome.GetValue(), self.email.GetValue(), self.senha.GetValue())
        wx.MessageBox('Conta criada. Agora entre com seu e-mail e senha.', 'Cadastro')
        self.tela_login()

    # TELA 3 — INÍCIO
    def tela_inicio(self):
        self.nova_tela('Olá, ' + self.usuario['nome'] + '!', 'Início')
        self.texto('Divulgue oportunidades e encontre vagas na sua região.')
        self.botao('Consultar vagas', self.tela_vagas, principal=True)
        self.botao('Publicar vaga', self.tela_publicar)
        self.botao('Sair da conta', self.tela_login)
        self.mostrar_tela()

    # TELA 4 — CONSULTA DE VAGAS
    def tela_vagas(self):
        self.nova_tela('Consultar vagas', 'Oportunidades')
        self.busca = self.campo('Pesquisar pelo título da vaga')
        self.botao('Pesquisar', self.pesquisar, principal=True)
        self.lista = wx.ListBox(self.cartao, size=(-1, 150), style=wx.LB_HSCROLL)
        self.resultado = self.texto('')
        self.layout.Add(self.lista, 0, wx.EXPAND)
        self.botao('Ver detalhes', self.abrir_detalhes)
        self.botao('Voltar ao início', self.tela_inicio)
        self.pesquisar()
        self.mostrar_tela()

    def pesquisar(self):
        # Os dados completos ficam na lista Python. A lista visual mostra um resumo.
        self.vagas = banco.listar_vagas(self.busca.GetValue())
        self.lista.Clear()
        self.resultado.SetLabel(f'Vagas encontradas: {len(self.vagas)}')
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
        self.nova_tela(self.vaga['titulo'], 'Detalhes da vaga')
        self.texto('Empresa — ' + self.vaga['empresa'])
        self.texto('Cidade — ' + self.vaga['cidade'])
        self.texto('Publicado por — ' + self.vaga['anunciante'])
        self.texto('Descrição e requisitos', destaque=True)
        self.texto(self.vaga['descricao'])
        self.texto('Contato para candidatura', destaque=True)
        self.texto(self.vaga['contato'])
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
        self.nova_tela('Publicar vaga', 'Novo anúncio')
        self.titulo = self.campo('Título da vaga')
        self.empresa = self.campo('Empresa')
        self.cidade = self.campo('Cidade', 'Porto Velho')
        self.descricao = self.campo('Descrição e requisitos', estilo=wx.TE_MULTILINE)
        self.contato = self.campo('Contato para candidatura, como e-mail ou telefone')
        self.botao('Salvar vaga', self.salvar_vaga, principal=True)
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
