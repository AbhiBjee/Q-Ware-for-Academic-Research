import wx
import time
app = wx.App(False)
w,h = wx.GetDisplaySize()
#del app

class QwareOpenPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(QwareOpenPanel, self).__init__(*args, **kw)
        self.InitUI()    

        
    def InitUI(self):
        bg_img='QwareBG.jpg'        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.bg = wx.Bitmap(bg_img)
        self._width, self._height = self.bg.GetSize()       

       
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)        

    def OnSize(self, size):
        self.Layout()
        self.Refresh()    

    def scale_bitmap(bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def Draw(self, dc):
        cliWidth, cliHeight = self.GetClientSize()
        if not cliWidth or not cliHeight:
            return
        dc.Clear()
        image = wx.ImageFromBitmap(self.bg)
        image = image.Scale(cliWidth, cliHeight, wx.IMAGE_QUALITY_HIGH)
        self.BgImg = wx.BitmapFromImage(image)      
        
        yPos = 0
        xPos = 0
        
        dc.DrawBitmap(self.BgImg, xPos, yPos)

class QOpenDialog(wx.Frame):

##    def __init__( self, parent ):
##        
##        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos=(w/2-320, h/2-180),size=(640,360), style = wx.DEFAULT_DIALOG_STYLE & ~(wx.CLOSE_BOX) )
##        
##        self.InitUI()

    
    def __init__(self, parent, id=wx.ID_ANY, title=" ", pos=(w/2-320, h/2-180),size=(640,360),
                 style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER)& ~(wx.CLOSE_BOX) & ~(wx.MAXIMIZE_BOX) &~(wx.MINIMIZE_BOX)):    
    
    
        super(QOpenDialog, self).__init__(parent, id, title, pos, size, style)
        self.InitUI()
           

    def InitUI(self):
        
        Width, Height = self.GetClientSize()
        
        self.panel = QwareOpenPanel(self, wx.ID_ANY, pos=(0,0), size = (Width,Height))
        self.evtTimer =  wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.loopFunction, self.evtTimer)
        self.evtTimer.Start(100)
        self.Counter = 0
        
        self.Show()

    def loopFunction(self, evt):

        if  self.Counter >= 8000:
            self.Close()
            #self.EndModal(10)
            self.evtTimer.Stop()
        if self.evtTimer.IsRunning():
            self.Counter = self.Counter+ evt.GetInterval()
            #print (self.Counter)
        
            
            
            
            #self.timeNow = time.asctime(time.localtime(time.time())) 
        
        

def main():    
    
    ex = wx.App()
    #ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    QOpenDialog(None)
    #QOpenDialog.SetPosition(w/2-320, h/2-180)
    #Dialog.Show()
##    frame = wx.Frame(None, id=wx.ID_ANY, title="Openning Q-WARE", pos=wx.DefaultPosition,
##                           size=(640,360), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER)& ~(wx.CLOSE_BOX) & ~(wx.MAXIMIZE_BOX) &~(wx.MINIMIZE_BOX))
##    QwareOpenPanel(frame)
##    frame.Show()
    
    
    ex.MainLoop()    

if __name__ == '__main__':
    main()   

##app = wx.App()
##frame = wx.Frame(None, size=(640,360))
##panel = QwareOpenPanel(frame)
##
##frame.Show()
##app.MainLoop()
