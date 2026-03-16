import wx

class QConnectPanel(wx.Panel):
   

   def __init__(self, *args, **kw):
      super(QConnectPanel, self).__init__(*args, **kw)
      self.InitUI()    


   def InitUI(self):
      bg_img='DevConnPic.jpg'        
      self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
      self.bg = wx.Bitmap(bg_img)
      self._width, self._height = self.bg.GetSize()

      self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )		
      vSizer = wx.BoxSizer( wx.VERTICAL )
      self.hSizer = wx.BoxSizer( wx.HORIZONTAL )

      vSizer.AddSpacer( ( 0, 100), 1, wx.EXPAND, 5 )

      self.progressBar = wx.Gauge( self, wx.ID_ANY, 130, wx.DefaultPosition, wx.Size( 450,25 ), wx.GA_HORIZONTAL|wx.TRANSPARENT_WINDOW )
      self.progressBar.SetValue( 0 ) 
      vSizer.Add( self.progressBar, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


      vSizer.AddSpacer( ( 0, 5), 1, wx.EXPAND, 5 )

      self.progressText = TransparentText( self, u" " )
      self.TextFont = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
      self.progressText.SetFont(self.TextFont)
      #self.progressText.Wrap( -1 )
      self.hSizer.Add(self.progressText, 0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5  )
      
      vSizer.Add( self.hSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


      vSizer.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )

      self.SetSizer( vSizer )
      self.Layout()

      self.Centre( wx.BOTH )


      self.Bind(wx.EVT_SIZE, self.OnSize)
      self.Bind(wx.EVT_PAINT, self.OnPaint)
      #self.Bind(wx.EVT_UPDATE_UI, self.On)

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


class TransparentText(wx.StaticText):


   #def __init__(self, parent, title): 
      #super(DevConBar, self).__init__(parent, title = title,size = (500,275))  


   
   def __init__(self, parent, label):
      super(TransparentText, self).__init__(parent, label = label)
      self.Bind(wx.EVT_PAINT, self._DoPaint)
      self.Bind(wx.EVT_ERASE_BACKGROUND, self._DoEraseBG)
      #self.Bind(wx.EVT_UPDATE_UI, self.OnUpdate)

   def OnUpdate(self, evt):
      #self.Layout()
      #self.Refresh()
      self.Update()
      #self.Refresh()

   def setNewText(self, newLabel):
      self.Update()

   def _DoPaint(self, evt):
      """
      """
      #print "paint statictext"
      #self.GetParent()._bmp
      dc = wx.PaintDC(self)
      dc.SetBackgroundMode(wx.TRANSPARENT)
      dc.SetTextForeground( self.GetForegroundColour() )
      dc.SetFont( self.GetFont() )
      dc.DrawText(self.GetLabel(), 0, 0)
    
   def _DoEraseBG(self, evt):
      """
      """
      pass
      #print "erase"
   


class DevConBar(wx.Frame):

   def __init__(self, parent, id=wx.ID_ANY, title=" Q-Device Autoconnect", pos=wx.DefaultPosition,size=(500,275),
                style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER) & ~(wx.MAXIMIZE_BOX) &~(wx.MINIMIZE_BOX)):    


      super(DevConBar, self).__init__(parent, id, title, pos, size, style)
      self.InitUI()
            
##   def __init__(self, parent, title): 
##      super(DevConBar, self).__init__(parent, title = title,size = (500,275))  
##      self.InitUI()

      self.progressTimer = wx.Timer(self, 101)
      self.Bind(wx.EVT_TIMER, self.OnTimerStart, self.progressTimer)
      self.progressTimer.Start(100)
         
   def InitUI(self):    
      self.Counter = 0

      Width, Height = self.GetClientSize()
        
      self.panel = QConnectPanel(self, wx.ID_ANY, pos=(0,0), size = (Width,Height))


      

      self.Show(True)

   def MakeModal(self, modal=True):
      if modal and not hasattr(self, '_disabler'):
         self._disabler = wx.WindowDisabler(self)
      if not modal and hasattr(self, '_disabler'):
         del self._disabler


   def OnClosed(self, evt):
      self.MakeModal(False) # (Re-enables parent window)
      self.eventLoop.Exit()
      self.Destroy() # (Closes window without recursion errors)
      #self.Flag=0
      
      #self.Destroy()

   def ShowModal(self):
      self.MakeModal(True) # (Explicit call to MakeModal)
      self.Show()
      if self.progressTimer.IsRunning():
         pass
      else:
         self.progressTimer.Start(100)

      # now to stop execution start a event loop 
      #self.eventLoop = wx.EventLoop()
      #self.eventLoop.Run()
      
       
		
   def OnTimerStart(self, evt):
      #self.panel.Refresh()

      if self.Counter >= 15000:
         self.progressTimer.Stop()
         self.Close()
         #self.EndModal(10)
      elif self.Counter==100:
         self.panel.progressText.Destroy()

      elif self.Counter==200:
         #self.panel.progressText.Destroy()
         self.Text = TransparentText( self.panel, u"Processing Please Wait......" )
         self.Text.SetFont(self.panel.TextFont)
         self.Text.Wrap( -1 )
         self.panel.hSizer.Add(self.Text )
         self.panel.Layout()
         #self.panel.progressText.SetLabelText("Please Wait")
         #self.panel.progressText.Refresh()
         #self.panel.progressText.Update()
      elif self.Counter==5900:
         self.Text.Destroy()

      elif self.Counter==6000:
         #self.panel.progressText.Destroy()
         self.Text = TransparentText( self.panel, u"Connecting And Registering Devices" )
         self.Text.SetFont(self.panel.TextFont)
         self.Text.Wrap( -1 )
         self.panel.hSizer.Add(self.Text )
         self.panel.Layout()
         #self.panel.progressText.SetLabelText("Please Wait")
         #self.panel.progressText.Refresh()
         #self.panel.progressText.Update()
         
      elif self.Counter==12900:
         self.Text.Destroy()        

      elif self.Counter==13000:
         
         self.Text2 = TransparentText( self.panel, u"Getting Ready" )
         self.Text2.SetFont(self.panel.TextFont)
         self.Text2.Wrap( -1 )
         self.panel.hSizer.Add(self.Text2 )
         self.panel.Layout()
         #self.panel.Refresh()
         
         
      if self.progressTimer.IsRunning():
         self.Counter = self.Counter+ evt.GetInterval()
         #print(self.Counter/100)
         self.panel.progressBar.SetValue(self.Counter/100)



def main():
    
    ex = wx.App()
    ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    DevConBar(None)
    #DevConBar.ShowModal()
    #Dialog.Show()
##    frame = wx.Frame(None, id=wx.ID_ANY, title="Openning Q-WARE", pos=wx.DefaultPosition,
##                           size=(640,360), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER)& ~(wx.CLOSE_BOX) & ~(wx.MAXIMIZE_BOX) &~(wx.MINIMIZE_BOX))
##    QwareOpenPanel(frame)
##    frame.Show()
    
    
    ex.MainLoop()    

if __name__ == '__main__':
    main()   

      
				
