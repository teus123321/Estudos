import wx
import os

class Tela(wx.Frame):

    def __init__ (self, parent, id=wx.ID_ANY,
                  title="Programa com imagem",
                  pos=wx.DefaultPosition, size=(800,800)):
        
        style = wx.DEFAULT_FRAME_STYLE
        name = "Tela"

        super().__init__(parent, id, title, pos,
                                   size, style, name)
        
        self.CenterOnScreen()
        self.panel = wx.Panel(self)

        botao = wx.Button(self.panel, wx.ID_ANY, 
                        "Aperte aqui", pos=(100,100))
        self.Bind(wx.EVT_BUTTON, self.aperta, botao)

    def aperta(self, event):
        pos = self.GetPosition()
        Tela2(pos = pos).Show()
        self.hide
        


class Tela2(wx.Frame):

    def __init__(self, parent=None, id=wx.ID_ANY,
                 title="Título do programa", 
                 pos=wx.DefaultPosition, size=(800,800)):

        style = wx.DEFAULT_FRAME_STYLE
        name = "Tela 2"

        super().__init__(parent, id, title, pos, size, style, name)
        

class Programa(wx.App):

    def OnInit(self):
        self.frame = Tela(parent=None)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

app = Programa(False)
app.MainLoop()

