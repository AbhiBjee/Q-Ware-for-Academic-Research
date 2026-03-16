import wx, time
import multiprocessing as mp
from QOpenningDialog import QOpenDialog
from PRS_UI_BackEnd import PRS_MainWindowBackend
from ConnectBar import DevConBar
#import concurrent.futures as cf


##def main():
##    
##    ex = wx.App()
##    ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
##
##    #PRS_MainWindowBackend(None)  
##
##    QOpenDialog(None, pos = (400, 250))
##    time.sleep(1)
##
##    PRS_MainWindowBackend(None)
##    #DevConBar(None, pos = (400, 100))
##    #OpenDialog.ShowModal()   
##    #time.sleep(2)
##    #OpenDialog.Hide()
##    #OpenDialog.Destroy()
##
##      
##    
##    ex.MainLoop()


def openLogo():
      ex = wx.App(False)
      ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
      QOpenDialog(None)
      ex.MainLoop()

def backendGUI():
      ex = wx.App(False)
      ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
      PRS_MainWindowBackend(None)
      ex.MainLoop()

##def main():
##     p1 = mp.Process(target=openLogo)
##     p2 = mp.Process(target=backendGUI)
##
##     p1.start()
##     time.sleep(1)
##     p2.start()
##
##     p1.join()
##     p2.join()

def main():
     
     #mp.set_start_method('spawn')  # Use spawn to start processes 
     p1 = mp.Process(target=openLogo)     
     p1.start()
     time.sleep(1)       
     backendGUI()
     p1.join()
     
      
if __name__ == '__main__':
      mp.freeze_support()
      main()          

	
