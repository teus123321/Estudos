"""INTERFACE wxPython do ConectaVagas.

O aplicativo é DESKTOP e usa wxPython; não tem Flask, HTML nem navegador interno.
Cada classe Tela... representa uma tela navegável (wx.ScrolledWindow).
A classe JanelaPrincipal substitui uma tela pela outra.
O arquivo banco.py faz todo o acesso ao servidor MySQL.
"""

# wxPython fornece as janelas, os botões, os campos e os eventos de interface.
import wx
from sqlalchemy.exc import SQLAlchemyError

from regiao import CIDADE_PADRAO
import banco
from vagas_api import ErroAPI, buscar_vagas_externas, url_pesquisa_linkedin, url_segura

# Cores compartilhadas ajudam a manter a aparência consistente nas telas.
FUNDO = "#F4F7FB"
TEXTO = "#182B45"
AZUL = "#2465C2"
VERDE = "#168358"


def avisar(mensagem, titulo="Atenção"):
    """Exibe uma caixa de mensagem informativa com o texto recebido."""
    wx.MessageBox(mensagem, titulo, wx.OK | wx.ICON_INFORMATION)


def erro_banco():
    """Mostra uma orientação quando uma operação com o MySQL falha."""
    wx.MessageBox("Não foi possível acessar o MySQL. Confira se o servidor está ativo.",
                  "Erro no MySQL", wx.OK | wx.ICON_ERROR)


def criar_texto(parent, texto, tamanho=10, negrito=False):
    """Cria um rótulo visual e aplica fonte e cor padronizadas."""
    componente = wx.StaticText(parent, label=texto)
    componente.SetForegroundColour(TEXTO)
    componente.SetFont(wx.Font(tamanho, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                              wx.FONTWEIGHT_BOLD if negrito else wx.FONTWEIGHT_NORMAL))
    return componente


def criar_botao(parent, legenda, acao):
    """Cria um botão e associa a função acao ao evento de clique."""
    botao = wx.Button(parent, label=legenda, size=(-1, 36))
    # Bind registra a função. O wxPython a chama quando o usuário clica no botão.
    botao.Bind(wx.EVT_BUTTON, acao)
    return botao


def formatar_data(data):
    """Converte uma data para dia/mês/ano e trata a ausência de data."""
    return data.strftime("%d/%m/%Y") if data else "-"


class Pagina(wx.ScrolledWindow):
    """Pequena classe base: evita repetir estilos e criação de formulários."""

    def __init__(self, parent, janela):
        """Prepara a área com rolagem e guarda a janela que controla a navegação."""
        # super() executa a inicialização da classe herdada, wx.ScrolledWindow.
        super().__init__(parent, style=wx.VSCROLL)
        # self é esta página. janela é o objeto central que guarda o login e troca as telas.
        self.janela = janela
        self.SetBackgroundColour(FUNDO)
        self.SetScrollRate(0, 18)
        # O sizer organiza os controles de cima para baixo. SetSizer o associa à página.
        self.conteudo = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.conteudo)

    def titulo(self, principal, subtitulo=""):
        """Adiciona o título e, quando informado, o subtítulo da página."""
        self.conteudo.Add(criar_texto(self, principal, 21, True), 0, wx.ALL, 14)
        if subtitulo:
            desc = criar_texto(self, subtitulo, 10)
            desc.Wrap(920)
            self.conteudo.Add(desc, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 14)

    def campo(self, legenda, valor="", multiline=False, senha=False):
        """Cria um campo, configura senha ou várias linhas e devolve o controle."""
        self.conteudo.Add(criar_texto(self, legenda, 10, True), 0, wx.LEFT | wx.TOP, 14)
        # As opções de estilo são combinadas com |. TE_PASSWORD oculta os caracteres.
        estilo = (wx.TE_MULTILINE if multiline else 0) | (wx.TE_PASSWORD if senha else 0)
        entrada = wx.TextCtrl(self, value=valor, style=estilo,
                              size=(-1, 95 if multiline else 32))
        self.conteudo.Add(entrada, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 14)
        # Devolve o controle para a tela poder ler o conteúdo com GetValue() depois.
        return entrada

    def escolha(self, legenda, opcoes):
        """Cria uma lista de opções e seleciona inicialmente a primeira."""
        self.conteudo.Add(criar_texto(self, legenda, 10, True), 0, wx.LEFT | wx.TOP, 14)
        escolha = wx.Choice(self, choices=opcoes)
        escolha.SetSelection(0)
        self.conteudo.Add(escolha, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 14)
        return escolha

    def linha_botoes(self, botoes):
        """Recebe pares de legenda e função para montar uma fileira de botões."""
        linha = wx.BoxSizer(wx.HORIZONTAL)
        # Cada par contém o texto do botão e a função que será chamada ao clicar.
        for legenda, acao in botoes:
            linha.Add(criar_botao(self, legenda, acao), 0, wx.RIGHT, 10)
        self.conteudo.Add(linha, 0, wx.ALL, 14)

    def paragrafo(self, texto):
        """Adiciona texto com quebra de linha ajustada à largura da página."""
        controle = criar_texto(self, texto, 10)
        controle.Wrap(930)
        self.conteudo.Add(controle, 0, wx.ALL, 14)
        return controle


class TelaInicio(Pagina):
    """Apresenta o objetivo do sistema e os caminhos para começar a navegação."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("ConectaVagas", f"Oportunidades de emprego e estágio para {CIDADE_PADRAO} e região.")
        self.paragrafo(
            "Objetivo social: aproximar candidatos e empresas locais. "
            "O candidato encontra vagas e acompanha suas inscrições. "
            "A empresa publica vagas e gerencia seus candidatos."
        )
        self.linha_botoes([
            # lambda cria uma função curta. ev recebe o evento do clique.
            # A troca de tela ocorre quando o botão é clicado.
            ("Encontrar vagas", lambda ev: janela.ir(TelaVagas)),
            ("Buscar vagas externas", lambda ev: janela.ir(TelaExternas)),
            ("Entender o projeto", lambda ev: janela.ir(TelaSobre)),
        ])
        if janela.usuario is None:
            self.linha_botoes([
                ("Criar uma conta", lambda ev: janela.ir(TelaCadastro)),
                ("Já tenho conta", lambda ev: janela.ir(TelaLogin)),
            ])
        self.paragrafo(
            "Trabalho acadêmico demonstrativo. As vagas cadastradas dentro do aplicativo "
            "pertencem às empresas cadastradas no sistema. As vagas da Adzuna são "
            "externas e usam o site original para candidatura."
        )


class TelaCadastro(Pagina):
    """Monta o formulário para registrar uma conta de candidato ou empresa."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Criar conta", "Escolha se você deseja procurar emprego ou anunciar oportunidades.")
        self.nome = self.campo("Nome completo ou nome da empresa")
        self.email = self.campo("E-mail")
        self.senha = self.campo("Senha (mínimo de 8 caracteres)", senha=True)
        self.telefone = self.campo("Telefone (opcional)")
        self.cidade = self.campo("Cidade", CIDADE_PADRAO)
        self.tipo = self.escolha("Tipo de conta", ["Candidato", "Empresa"])
        self.linha_botoes([("Cadastrar", self.salvar),
                           ("Voltar ao login", lambda ev: janela.ir(TelaLogin))])

    def salvar(self, evento):
        """Lê o formulário, solicita o cadastro ao banco e abre o login se der certo."""
        # A primeira opção tem índice 0. O texto visual é convertido no valor usado no banco.
        tipo = "candidato" if self.tipo.GetSelection() == 0 else "empresa"
        try:
            # GetValue() lê o texto atual de cada campo e o envia para a função do banco.
            banco.cadastrar_usuario(self.nome.GetValue(), self.email.GetValue(),
                                   self.senha.GetValue(), tipo,
                                   self.telefone.GetValue(), self.cidade.GetValue())
        # Uma regra de validação impediu a operação. Mostramos a razão ao usuário.
        except ValueError as erro:
            avisar(str(erro), "Verifique o cadastro")
            return
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        avisar("Conta criada! Agora faça o login.", "Cadastro realizado")
        self.janela.ir(TelaLogin)


class TelaLogin(Pagina):
    """Recebe as credenciais e direciona o usuário conforme o tipo de conta."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Entrar", "Use o e-mail e a senha cadastrados neste aplicativo.")
        self.email = self.campo("E-mail")
        self.senha = self.campo("Senha", senha=True)
        self.linha_botoes([("Entrar", self.entrar),
                           ("Criar conta", lambda ev: janela.ir(TelaCadastro))])

    def entrar(self, evento):
        """Confere as credenciais, guarda o usuário logado e escolhe a próxima tela."""
        try:
            usuario = banco.autenticar(self.email.GetValue(), self.senha.GetValue())
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        if usuario is None:
            avisar("E-mail ou senha incorretos.", "Acesso negado")
            return
        # Guarda os dados da conta em memória para saber quem está usando o aplicativo.
        self.janela.usuario = usuario
        # O tipo de conta define se a próxima tela será o painel da empresa ou a busca.
        if usuario["tipo"] == "empresa":
            self.janela.ir(TelaEmpresa)
        else:
            self.janela.ir(TelaVagas)


class TelaVagas(Pagina):
    """Exibe as vagas locais abertas e permite filtrar por termo e cidade."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Vagas locais", "Oportunidades publicadas pelas empresas cadastradas no ConectaVagas.")
        self.busca = self.campo("Palavra-chave: título ou área (opcional)")
        self.cidade = self.campo("Filtrar por cidade (opcional)", CIDADE_PADRAO)
        self.linha_botoes([("Pesquisar", self.atualizar),
                           ("Limpar filtros", self.limpar)])
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
                                 size=(-1, 290))
        for indice, (nome, largura) in enumerate([
            ("Título", 245), ("Empresa", 180), ("Cidade", 190),
            ("Contrato", 130), ("Modalidade", 120)
        ]):
            self.lista.InsertColumn(indice, nome, width=largura)
        self.conteudo.Add(self.lista, 1, wx.EXPAND | wx.ALL, 14)
        self.lista.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.detalhes)
        self.linha_botoes([("Ver detalhes da vaga", self.detalhes),
                           ("Pesquisar na Adzuna", lambda ev: janela.ir(TelaExternas))])
        # Guarda os dados completos. A lista visual mostra só algumas colunas desses dados.
        self.vagas = []
        # Preenche a lista ao abrir a tela. None indica que a chamada ocorreu sem clique.
        self.atualizar(None)

    def atualizar(self, evento):
        """Consulta o banco com os filtros e preenche novamente a lista visual."""
        try:
            self.vagas = banco.listar_vagas(self.busca.GetValue(), self.cidade.GetValue())
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        # Limpa as linhas visuais antes de exibir a nova consulta, evitando duplicação.
        self.lista.DeleteAllItems()
        for vaga in self.vagas:
            i = self.lista.InsertItem(self.lista.GetItemCount(), vaga["titulo"])
            for coluna, valor in enumerate((vaga["empresa"], vaga["cidade"],
                                            vaga["contrato"], vaga["modalidade"]), 1):
                self.lista.SetItem(i, coluna, str(valor))

    def limpar(self, evento):
        """Apaga os filtros e refaz a consulta de vagas abertas."""
        self.busca.SetValue("")
        self.cidade.SetValue("")
        # Preenche a lista ao abrir a tela. None indica que a chamada ocorreu sem clique.
        self.atualizar(None)

    def detalhes(self, evento):
        """Obtém o ID da vaga selecionada e abre a tela de detalhes."""
        # O índice é a posição da linha visual. -1 significa que nenhuma linha foi escolhida.
        indice = self.lista.GetFirstSelected()
        if indice < 0:
            avisar("Selecione uma vaga na lista.")
            return
        # Usa o ID do banco da vaga escolhida, que pode ser diferente do índice da lista.
        self.janela.ir(TelaDetalhes, vaga_id=self.vagas[indice]["id"])


class TelaDetalhes(Pagina):
    """Mostra uma vaga e oferece as ações permitidas para o usuário atual."""
    def __init__(self, parent, janela, vaga_id):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.vaga_id = vaga_id
        try:
            vaga = banco.obter_vaga(vaga_id)
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            vaga = None
        if not vaga:
            self.titulo("Vaga não encontrada")
            self.linha_botoes([("Voltar", lambda ev: janela.ir(TelaVagas))])
            return

        self.titulo(vaga["titulo"], f"{vaga['empresa']} • {vaga['cidade']}")
        self.paragrafo(
            f"Área: {vaga['area']}  |  Contrato: {vaga['contrato']}  |  "
            f"Modalidade: {vaga['modalidade']}\n"
            f"Remuneração: {vaga['remuneracao']}  |  Publicada em: {formatar_data(vaga['criada_em'])}\n"
            f"Situação: {'Aberta' if vaga['ativa'] else 'Encerrada'}"
        )
        self.paragrafo("DESCRIÇÃO DA VAGA\n" + vaga["descricao"])
        self.paragrafo("REQUISITOS\n" + (vaga["requisitos"] or "Não informados"))

        if janela.usuario is None:
            self.paragrafo("Para se candidatar, crie uma conta de candidato ou faça login.")
            self.linha_botoes([("Entrar", lambda ev: janela.ir(TelaLogin)),
                               ("Voltar", lambda ev: janela.ir(TelaVagas))])
        elif janela.usuario["tipo"] == "candidato" and vaga["ativa"]:
            self.mensagem = self.campo("Mensagem para a empresa (opcional)", multiline=True)
            self.linha_botoes([("Enviar candidatura", self.candidatar),
                               ("Voltar", lambda ev: janela.ir(TelaVagas))])
        elif janela.usuario["tipo"] == "empresa" and janela.usuario["id"] == vaga["empresa_id"]:
            self.linha_botoes([("Ver candidatos", lambda ev: janela.ir(TelaCandidatos, vaga_id=vaga_id)),
                               ("Meu painel", lambda ev: janela.ir(TelaEmpresa))])
        else:
            self.linha_botoes([("Voltar para vagas", lambda ev: janela.ir(TelaVagas))])

    def candidatar(self, evento):
        """Envia candidato, vaga e mensagem ao banco e abre as inscrições."""
        try:
            # A conta logada fornece o candidato. A tela fornece o ID da vaga e a mensagem.
            banco.candidatar(self.janela.usuario["id"], self.vaga_id, self.mensagem.GetValue())
        # Uma regra de validação impediu a operação. Mostramos a razão ao usuário.
        except ValueError as erro:
            avisar(str(erro), "Candidatura")
            return
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        avisar("Candidatura registrada no MySQL!", "Inscrição confirmada")
        self.janela.ir(TelaMinhasCandidaturas)


class TelaMinhasCandidaturas(Pagina):
    """Mostra ao candidato as inscrições e a situação de cada uma."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Minhas candidaturas", "Acompanhe as inscrições realizadas dentro deste aplicativo.")
        if not janela.usuario or janela.usuario["tipo"] != "candidato":
            self.paragrafo("Acesso exclusivo aos candidatos.")
            return
        try:
            dados = banco.minhas_candidaturas(janela.usuario["id"])
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        lista = wx.ListCtrl(self, style=wx.LC_REPORT, size=(-1, 360))
        for c, (titulo, largura) in enumerate([("Vaga", 280), ("Empresa", 260),
                                               ("Status", 160), ("Data", 130)]):
            lista.InsertColumn(c, titulo, width=largura)
        for candidatura in dados:
            i = lista.InsertItem(lista.GetItemCount(), candidatura["titulo"])
            for col, val in enumerate((candidatura["empresa"], candidatura["status"],
                                       formatar_data(candidatura["data"])), 1):
                lista.SetItem(i, col, val)
        self.conteudo.Add(lista, 1, wx.EXPAND | wx.ALL, 14)
        self.paragrafo("Se a lista estiver vazia, abra 'Vagas locais' e envie sua primeira candidatura.")


class TelaPerfil(Pagina):
    """Permite consultar e alterar telefone, cidade e apresentação profissional."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Meu perfil", "Informações de contato que podem aparecer para uma empresa após a candidatura.")
        if not janela.usuario:
            self.paragrafo("Entre na sua conta para editar o perfil.")
            return
        try:
            usuario = banco.obter_usuario(janela.usuario["id"])
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        self.paragrafo(f"Conta: {usuario['nome']}  |  E-mail: {usuario['email']}\nTipo: {usuario['tipo']}")
        self.telefone = self.campo("Telefone", usuario["telefone"])
        self.cidade = self.campo("Cidade", usuario["cidade"])
        self.resumo = self.campo("Apresentação profissional (opcional)", usuario["resumo"], multiline=True)
        self.linha_botoes([("Salvar alterações", self.salvar)])

    def salvar(self, evento):
        """Grava o perfil e atualiza a cópia do usuário guardada na janela."""
        try:
            banco.atualizar_perfil(self.janela.usuario["id"], self.telefone.GetValue(),
                                  self.cidade.GetValue(), self.resumo.GetValue())
            self.janela.usuario = banco.obter_usuario(self.janela.usuario["id"])
        # Uma regra de validação impediu a operação. Mostramos a razão ao usuário.
        except ValueError as erro:
            avisar(str(erro))
            return
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        avisar("Perfil atualizado no MySQL!", "Perfil salvo")


class TelaEmpresa(Pagina):
    """Mostra as vagas da empresa logada e as ações de gerenciamento."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Painel da empresa", "Publique vagas, encerre anúncios e consulte candidatos cadastrados.")
        if not janela.usuario or janela.usuario["tipo"] != "empresa":
            self.paragrafo("Acesso exclusivo a contas de empresa.")
            return
        self.linha_botoes([("Publicar nova vaga", lambda ev: janela.ir(TelaNovaVaga))])
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
                                 size=(-1, 320))
        for i, (titulo, largura) in enumerate([("Título", 280), ("Contrato", 140),
                                               ("Cidade", 220), ("Situação", 150)]):
            self.lista.InsertColumn(i, titulo, width=largura)
        self.conteudo.Add(self.lista, 1, wx.EXPAND | wx.ALL, 14)
        self.linha_botoes([("Ver detalhes", self.detalhar),
                           ("Ver candidatos", self.candidatos),
                           ("Abrir/encerrar vaga", self.alternar)])
        try:
            self.vagas = banco.minhas_vagas(janela.usuario["id"])
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            self.vagas = []
        for vaga in self.vagas:
            n = self.lista.InsertItem(self.lista.GetItemCount(), vaga["titulo"])
            for col, valor in enumerate((vaga["contrato"], vaga["cidade"],
                                         "Aberta" if vaga["ativa"] else "Encerrada"), 1):
                self.lista.SetItem(n, col, valor)

    def selecionada(self):
        """Devolve a vaga da linha selecionada ou avisa se nenhuma foi escolhida."""
        # O índice é a posição da linha visual. -1 significa que nenhuma linha foi escolhida.
        indice = self.lista.GetFirstSelected()
        if indice < 0:
            avisar("Selecione uma vaga.")
            return None
        return self.vagas[indice]

    def detalhar(self, evento):
        """Abre os detalhes da vaga escolhida no painel da empresa."""
        vaga = self.selecionada()
        if vaga:
            self.janela.ir(TelaDetalhes, vaga_id=vaga["id"])

    def candidatos(self, evento):
        """Abre a lista de candidatos da vaga escolhida."""
        vaga = self.selecionada()
        if vaga:
            self.janela.ir(TelaCandidatos, vaga_id=vaga["id"])

    def alternar(self, evento):
        """Solicita a abertura ou o encerramento da vaga e recarrega o painel."""
        vaga = self.selecionada()
        if vaga is None:
            return
        try:
            # not inverte o booleano. Uma vaga aberta passa a encerrada e vice-versa.
            banco.mudar_situacao_vaga(self.janela.usuario["id"], vaga["id"], not vaga["ativa"])
        except (SQLAlchemyError, ValueError):
            erro_banco()
            return
        self.janela.ir(TelaEmpresa)


class TelaNovaVaga(Pagina):
    """Recolhe os dados que a empresa precisa informar para publicar uma vaga."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Publicar vaga", "Somente empresas cadastradas podem criar anúncios locais.")
        if not janela.usuario or janela.usuario["tipo"] != "empresa":
            self.paragrafo("Acesso exclusivo às empresas.")
            return
        self.titulo_vaga = self.campo("Título da vaga (ex.: Estagiário de Suporte Técnico)")
        self.area = self.campo("Área (ex.: Tecnologia da Informação)")
        self.descricao = self.campo("Descrição das atividades", multiline=True)
        self.requisitos = self.campo("Requisitos (opcional)", multiline=True)
        self.cidade = self.campo("Cidade", CIDADE_PADRAO)
        # Choice permite escolher entre opções previamente definidas.
        self.modalidade = self.escolha("Modalidade", ["Presencial", "Híbrido", "Remoto"])
        self.contrato = self.escolha("Tipo de contrato", ["Estágio", "CLT", "Jovem Aprendiz", "Temporário"])
        self.remuneracao = self.campo("Bolsa ou salário (opcional)", "Não informada")
        self.linha_botoes([("Publicar vaga", self.salvar),
                           ("Cancelar", lambda ev: janela.ir(TelaEmpresa))])

    def salvar(self, evento):
        """Reúne os dados do formulário e pede ao banco a publicação da vaga."""
        try:
            # O primeiro argumento identifica a empresa logada. Os demais vêm do formulário.
            banco.criar_vaga(
                self.janela.usuario["id"], self.titulo_vaga.GetValue(), self.area.GetValue(),
                self.descricao.GetValue(), self.requisitos.GetValue(), self.cidade.GetValue(),
                # GetStringSelection() devolve o texto selecionado no Choice.
                self.modalidade.GetStringSelection(), self.contrato.GetStringSelection(),
                self.remuneracao.GetValue())
        # Uma regra de validação impediu a operação. Mostramos a razão ao usuário.
        except ValueError as erro:
            avisar(str(erro), "Verifique os dados da vaga")
            return
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        avisar("Sua vaga foi gravada no MySQL e aparecerá na busca local!", "Vaga publicada")
        self.janela.ir(TelaEmpresa)


class TelaCandidatos(Pagina):
    """Permite à empresa consultar e avaliar os candidatos de sua própria vaga."""
    def __init__(self, parent, janela, vaga_id):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.vaga_id = vaga_id
        self.titulo("Candidatos da vaga", "O acesso é permitido apenas à empresa que publicou esta vaga.")
        if not janela.usuario or janela.usuario["tipo"] != "empresa":
            self.paragrafo("Acesso exclusivo às empresas.")
            return
        try:
            self.registros = banco.candidatos_da_vaga(janela.usuario["id"], vaga_id)
        # Uma regra de validação impediu a operação. Mostramos a razão ao usuário.
        except ValueError as erro:
            self.paragrafo(str(erro))
            return
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL, size=(-1, 260))
        for i, (nome, largura) in enumerate([("Nome", 205), ("E-mail", 275),
                                             ("Status", 155), ("Data", 115)]):
            self.lista.InsertColumn(i, nome, width=largura)
        self.conteudo.Add(self.lista, 1, wx.EXPAND | wx.ALL, 14)
        for pessoa in self.registros:
            i = self.lista.InsertItem(self.lista.GetItemCount(), pessoa["nome"])
            for col, valor in enumerate((pessoa["email"], pessoa["status"],
                                         formatar_data(pessoa["data"])), 1):
                self.lista.SetItem(i, col, valor)
        self.status = self.escolha("Alterar situação do candidato selecionado", 
                                  ["Enviada", "Em análise", "Aprovada", "Recusada"])
        self.linha_botoes([("Ver contato e mensagem", self.detalhes),
                           ("Salvar situação", self.salvar_status),
                           ("Voltar ao painel", lambda ev: janela.ir(TelaEmpresa))])

    def selecionado(self):
        """Devolve os dados do candidato selecionado na lista visual."""
        # O índice é a posição da linha visual. -1 significa que nenhuma linha foi escolhida.
        indice = self.lista.GetFirstSelected()
        if indice < 0:
            avisar("Selecione um candidato da lista.")
            return None
        return self.registros[indice]

    def detalhes(self, evento):
        """Exibe contato, apresentação e mensagem do candidato escolhido."""
        pessoa = self.selecionado()
        if not pessoa:
            return
        avisar(f"Nome: {pessoa['nome']}\nE-mail: {pessoa['email']}\nTelefone: {pessoa['telefone']}\n"
              f"Cidade: {pessoa['cidade']}\n\nApresentação:\n{pessoa['resumo']}\n\n"
              f"Mensagem da candidatura:\n{pessoa['mensagem']}", "Detalhes do candidato")

    def salvar_status(self, evento):
        """Grava a situação escolhida e recria a tela para mostrar o resultado."""
        pessoa = self.selecionado()
        if not pessoa:
            return
        try:
            # O banco também confere se esta inscrição pertence a uma vaga da empresa.
            banco.mudar_status_candidatura(self.janela.usuario["id"], pessoa["id"],
                                           self.status.GetStringSelection())
        # Uma regra de validação impediu a operação. Mostramos a razão ao usuário.
        except ValueError as erro:
            avisar(str(erro))
            return
        # Uma falha de acesso ao banco é tratada para a tela continuar utilizável.
        except SQLAlchemyError:
            erro_banco()
            return
        avisar("Situação salva no banco de dados.")
        self.janela.ir(TelaCandidatos, vaga_id=self.vaga_id)


class TelaExternas(Pagina):
    """Consulta anúncios da Adzuna e permite abrir o site de origem."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Vagas externas — Adzuna", 
                    "Consulte anúncios reais com a API Adzuna. É preciso internet e credenciais válidas no .env.")
        self.termo = self.campo("Pesquisar cargo ou área", "estágio")
        self.local = self.campo("Localização", CIDADE_PADRAO)
        self.linha_botoes([("Consultar API Adzuna", self.pesquisar),
                           ("Pesquisar no site LinkedIn", self.linkedin)])
        self.paragrafo("Fonte: Jobs by Adzuna — https://www.adzuna.com.br/. "
                       "Não é uma integração com a API do LinkedIn.")
        self.aviso = criar_texto(self, "As vagas da API só aparecem após clicar em 'Consultar API Adzuna'.")
        self.conteudo.Add(self.aviso, 0, wx.ALL, 14)
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL, size=(-1, 280))
        for i, (titulo, largura) in enumerate([("Título", 275), ("Empresa", 250), ("Local", 280)]):
            self.lista.InsertColumn(i, titulo, width=largura)
        self.conteudo.Add(self.lista, 1, wx.EXPAND | wx.ALL, 14)
        self.lista.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.abrir)
        self.linha_botoes([("Ver descrição", self.detalhes),
                           ("Abrir anúncio original", self.abrir)])
        # Guarda os dados completos. A lista visual mostra só algumas colunas desses dados.
        self.vagas = []

    def pesquisar(self, evento):
        """Consulta a Adzuna, trata falhas e mostra os anúncios recebidos."""
        self.aviso.SetLabel("Consultando... (pode levar alguns segundos)")
        wx.YieldIfNeeded()  # Atualiza o aviso antes da chamada HTTP síncrona (simples para estudar).
        try:
            with wx.BusyCursor():
                self.vagas = buscar_vagas_externas(self.termo.GetValue(), self.local.GetValue())
        except ErroAPI as erro:
            self.aviso.SetLabel(str(erro))
            return
        # Limpa as linhas visuais antes de exibir a nova consulta, evitando duplicação.
        self.lista.DeleteAllItems()
        for vaga in self.vagas:
            i = self.lista.InsertItem(self.lista.GetItemCount(), vaga["titulo"])
            self.lista.SetItem(i, 1, vaga["empresa"])
            self.lista.SetItem(i, 2, vaga["cidade"])
        self.aviso.SetLabel(f"{len(self.vagas)} vaga(s) retornada(s). A candidatura acontece no site de origem.")

    def selecionada(self):
        """Devolve o anúncio externo escolhido na lista."""
        # O índice é a posição da linha visual. -1 significa que nenhuma linha foi escolhida.
        indice = self.lista.GetFirstSelected()
        if indice < 0:
            avisar("Selecione um anúncio externo.")
            return None
        return self.vagas[indice]

    def detalhes(self, evento):
        """Mostra uma parte da descrição do anúncio externo selecionado."""
        vaga = self.selecionada()
        if vaga:
            avisar(f"{vaga['titulo']}\n{vaga['empresa']} — {vaga['cidade']}\n\n"
                  f"{vaga['descricao'][:1300]}\n\nAbra o anúncio original para mais informações.",
                  "Descrição externa")

    def abrir(self, evento):
        """Valida o endereço do anúncio e abre o navegador do computador."""
        vaga = self.selecionada()
        if vaga is None:
            return
        if not url_segura(vaga["url"]):
            avisar("Este anúncio não informou um link válido.")
            return
        wx.LaunchDefaultBrowser(vaga["url"])

    def linkedin(self, evento):
        """Abre uma pesquisa no site do LinkedIn; NÃO usa API ou scraping."""
        wx.LaunchDefaultBrowser(url_pesquisa_linkedin(self.termo.GetValue(), self.local.GetValue()))


class TelaSobre(Pagina):
    """Explica ao usuário o objetivo do projeto e as tecnologias utilizadas."""
    def __init__(self, parent, janela):
        """Cria os controles da tela e liga os botões às ações disponíveis."""
        super().__init__(parent, janela)
        self.titulo("Sobre o ConectaVagas", "Protótipo acadêmico para inclusão no mercado de trabalho da região.")
        self.paragrafo("1. Interface: Python + wxPython (telas no app.py).\n"
                       "2. Regras e persistência: SQLAlchemy (funções no banco.py).\n"
                       "3. Dados: servidor MySQL, administrado com MySQL Workbench.\n"
                       "4. Integração externa opcional: API Adzuna (vagas_api.py).\n"
                       "5. Pesquisa LinkedIn: apenas abre o site no navegador, sem consumir API.")
        self.paragrafo("Veja os arquivos da pasta docs/ para o diagrama ER, manual e roteiro da apresentação.")
        self.linha_botoes([("Voltar ao início", lambda ev: janela.ir(TelaInicio))])


class JanelaPrincipal(wx.Frame):
    """Guarda a sessão do usuário e coordena a navegação entre as telas."""

    def __init__(self):
        """Cria a janela, o menu e a área que receberá cada página."""
        super().__init__(None, title="ConectaVagas | wxPython + MySQL",
                         size=(1110, 760))
        self.SetMinSize((950, 620))
        self.CenterOnScreen()
        self.usuario = None  # None = visitante; após login = dicionário do usuário.
        self.raiz = wx.Panel(self)
        self.estrutura = wx.BoxSizer(wx.VERTICAL)
        self.raiz.SetSizer(self.estrutura)
        self.nav = wx.Panel(self.raiz)
        self.nav.SetBackgroundColour("#E2ECFA")
        self.nav_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.nav.SetSizer(self.nav_layout)
        self.estrutura.Add(self.nav, 0, wx.EXPAND)
        self.pagina_atual = None
        self.ir(TelaInicio)

    def montar_menu(self):
        """Reconstrói os botões conforme visitante, candidato ou empresa."""
        # Remove os botões antigos para reconstruir o menu após login, logout ou navegação.
        self.nav_layout.Clear(delete_windows=True)
        botoes = [("Início", lambda ev: self.ir(TelaInicio)),
                  ("Vagas", lambda ev: self.ir(TelaVagas)),
                  ("Vagas externas", lambda ev: self.ir(TelaExternas))]
        if self.usuario is None:
            botoes += [("Login", lambda ev: self.ir(TelaLogin)),
                       ("Cadastro", lambda ev: self.ir(TelaCadastro))]
        elif self.usuario["tipo"] == "candidato":
            botoes += [("Minhas candidaturas", lambda ev: self.ir(TelaMinhasCandidaturas)),
                       ("Perfil", lambda ev: self.ir(TelaPerfil)),
                       ("Sair", self.sair)]
        else:
            botoes += [("Painel empresa", lambda ev: self.ir(TelaEmpresa)),
                       ("Publicar vaga", lambda ev: self.ir(TelaNovaVaga)),
                       ("Perfil", lambda ev: self.ir(TelaPerfil)),
                       ("Sair", self.sair)]
        for legenda, funcao in botoes:
            botao = criar_botao(self.nav, legenda, funcao)
            self.nav_layout.Add(botao, 0, wx.ALL, 6)
        self.nav.Layout()

    def ir(self, pagina, **dados):
        """Remove a tela antiga e desenha a nova; a janela principal permanece."""
        # A página anterior é retirada do sizer e destruída antes da criação da próxima.
        if self.pagina_atual is not None:
            self.estrutura.Detach(self.pagina_atual)
            self.pagina_atual.Destroy()
        self.montar_menu()
        # pagina é uma classe, como TelaDetalhes. **dados entrega argumentos como vaga_id.
        self.pagina_atual = pagina(self.raiz, self, **dados)
        # O valor 1 dá à página o espaço disponível. EXPAND faz ela ocupar a largura.
        self.estrutura.Add(self.pagina_atual, 1, wx.EXPAND)
        self.pagina_atual.FitInside()
        self.raiz.Layout()
        self.Layout()

    def sair(self, evento):
        """Apaga o usuário da sessão visual e volta ao início."""
        self.usuario = None
        self.ir(TelaInicio)


class Programa(wx.App):
    def OnInit(self):
        """Inicia o banco e só mostra a janela principal se a conexão funcionar."""
        try:
            # Lê a configuração do MySQL e cria as tabelas que ainda estiverem ausentes.
            banco.iniciar_banco()
        except (SQLAlchemyError, ValueError, OSError) as erro:
            wx.MessageBox("Não foi possível iniciar o MySQL.\n\n"
                          "1. Abra o MySQL Workbench e conecte-se ao servidor.\n"
                          "2. Execute sql/criar_banco.sql.\n"
                          "3. Confira a senha e demais dados no .env.\n\n"
                          f"Detalhes: {erro}", "Conexão com MySQL", wx.OK | wx.ICON_ERROR)
            return False
        janela = JanelaPrincipal()
        # Torna a janela visível depois de a conexão com o banco estar pronta.
        janela.Show()
        self.SetTopWindow(janela)
        return True


# Este trecho inicia o programa quando o arquivo app.py é executado diretamente.
if __name__ == "__main__":
    # MainLoop mantém o aplicativo aberto aguardando cliques e outros eventos.
    Programa(False).MainLoop()
