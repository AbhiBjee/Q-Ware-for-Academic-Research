import wx

class QCalibPanel(wx.Panel):
   

   def __init__(self, *args, **kw):
      super(QCalibPanel, self).__init__(*args, **kw)
      self.InitUI()

   def InitUI(self):
      self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )		
      vSizer = wx.BoxSizer( wx.VERTICAL )
      self.txtHsizer = wx.BoxSizer(wx.VERTICAL)

      vSizer.AddSpacer( ( 0, 100), 1, wx.EXPAND, 5 )
     

      self.progressBar = wx.Gauge( self, wx.ID_ANY, 80, wx.DefaultPosition, wx.Size( 450,25 ), wx.GA_HORIZONTAL|wx.TRANSPARENT_WINDOW )
      self.progressBar.SetValue( 0 ) 
      vSizer.Add( self.progressBar, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


      vSizer.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )

      self.progressText = wx.StaticText( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0 )

      #self.progressText.Wrap( -1 )
      self.TextFont = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
      self.progressText.SetFont(self.TextFont)
      self.txtHsizer.Add(self.progressText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
      
      vSizer.Add( self.txtHsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


      vSizer.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )

      self.SetSizer( vSizer )
      self.Layout()

      self.Centre( wx.BOTH )



class DevCalibBar(wx.Frame):

   def __init__(self, parent, id=wx.ID_ANY, title=" ", pos=wx.DefaultPosition,size=(500,125),
                style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER) & ~(wx.MAXIMIZE_BOX) &~(wx.MINIMIZE_BOX)):    


      super(DevCalibBar, self).__init__(parent, id, title, pos, size, style)
            
##   def __init__(self, parent, title): 
##      super(DevCalibBar, self).__init__(parent, title = title,size = (500,120))  
      self.InitUI()

      self.progressTimer = wx.Timer(self, 101)
      self.Bind(wx.EVT_TIMER, self.OnTimerStart, self.progressTimer)
      self.progressTimer.Start(100)
         
   def InitUI(self):    
      self.Counter = 0

      Width, Height = self.GetClientSize()
        
      self.panel = QCalibPanel(self, wx.ID_ANY, pos=(0,0), size = (Width,Height))


      
      self.Show(True)     
      
       
		
   def OnTimerStart(self, evt):

      if  self.Counter >= 15000:
         self.progressTimer.Stop()
         self.Close()
         #self.EndModal(10)
      elif self.Counter==100:
         self.panel.txtHsizer.Detach(self.panel.progressText)
         self.panel.progressText.SetLabel("Processing Please Wait")
         self.panel.txtHsizer.Add( self.panel.progressText )
         self.panel.Layout()
      elif self.Counter==2500:
         self.panel.txtHsizer.Detach(self.panel.progressText)
         self.panel.progressText.SetLabel("Device Calibration in Progress")
         self.panel.txtHsizer.Add( self.panel.progressText )
         self.panel.Layout()
         
         #self.panel.progressText.Destroy()

      elif self.Counter==10000:
         self.panel.txtHsizer.Detach(self.panel.progressText)
         self.panel.progressText.SetLabel("Getting Ready")
         self.panel.txtHsizer.Add( self.panel.progressText )
         self.panel.Layout()
         
##         
      if self.progressTimer.IsRunning():
         self.Counter = self.Counter+ evt.GetInterval()
         #print(self.Counter/100)
         self.panel.progressBar.SetValue(self.Counter/100)

def main():
    
    ex = wx.App()
    ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    DevCalibBar(None, title = "Device Calibration Status", pos = (400,250))  
    
    ex.MainLoop()

if __name__ == '__main__':
    main()   

      
				
