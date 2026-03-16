# -*- coding: utf-8 -*- 

###########################################################################
## Python SourceCode generated partially with wxFormBuilder 
## http://www.healthsmarttechnologies.com/
## Developed by Abhinaba Bhattacharjee (version Jan 20 2020)
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
#import wx.xrc
from time import localtime,strftime


###########################################################################
## Function to draw Boxes on Panels
###########################################################################

def PanelBoxDraw(dc, drawLabel, Width, Height): 

    # get the box width and height
    #dc = wx.GCDC(self)
    #dc = wx.PaintDC(self)
    dc.SetBackground(wx.Brush(wx.Colour(181, 240, 249), wx.CROSSDIAG_HATCH))
    dc.SetTextForeground( wx.Colour(101, 33, 33) )
    drawFont = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
    dc.SetFont( drawFont )

    boxLabel = drawLabel

    #dc.Clear()

    labelWidth,labelHeight = dc.GetTextExtent(boxLabel)# get the 


    #rect = wx.Rect(0,0,(cliWidth-10),(cliHeight-10))

    #dc.SetBrush(wx.Brush("black", wx.TRANSPARENT)) #set brush transparent for non-filled rectangle

    dc.SetBrush(wx.Brush(wx.Colour(181, 240, 249), wx.CROSSDIAG_HATCH)) #wx.TRANSPARENT
    dc.SetPen(wx.Pen(wx.Colour(215, 215, 215), 5))# here 5 is width of the box
    #dc.SetPen(wx.Pen("black", wx.TRANSPARENT))
    #rect.Deflate(1, 1)
    dc.DrawRoundedRectangle(2,2,(Width-4),(Height-4), 10)#parameters(x,y,width,heigth,radius) here 10 pixel is radius of the curved rectangle.
    dc.DrawLine(0,labelHeight+5, Width-6, labelHeight+5)#parameters(x1,y1,x2,y2) two points (x1,y1) and (x2,y2)

    #dc.GradientFillLinear( rect, wx.Colour(160, 160, 160), wx.Colour(255, 255, 255), wx.DOWN)
    dc.DrawText(boxLabel,(Width-Width/2 - labelWidth/2),3)

    #black non-filled rectangle
    ##        dc.SetPen(wx.Pen("black"))
    ##        dc.SetBrush(wx.Brush("black", wx.TRANSPARENT)) #set brush transparent for non-filled rectangle
    ##        dc.DrawRoundedRectangle(0,0,(cliWidth-10),(cliHeight-10), 10)

    dc.EndDrawing()



###########################################################################
## Class PRS_MainWindow for FrontEnd UI
###########################################################################

class PRS_MainWindowFrontEnd ( wx.Frame ):

       # class QSTM(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="Q-WARE - PRS", pos=wx.DefaultPosition,
                 size=(1365,740), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER)):#& ~(wx.RESIZE_BORDER)
        super(PRS_MainWindowFrontEnd, self).__init__(parent, id, title, pos, size, style)
           
    #def __init__(self, *args, **kw):
        #super(QSTM, self).__init__(*args, **kw) 
        
        self.InitUI()
        
    def InitUI(self):

        ##================PRS BackGround Image======================###
        bg_img='PRS_BgPic2.jpg'
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.bg = wx.Bitmap(bg_img)
        self.bgImg_width, self.bgImg_height = self.bg.GetSize()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        ##===================PRS Panel Layout=========================##

        #self.boxFont = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)

        self.boxFont = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_BOLD)

        self.FormPRS_UI()
        #self.FormPRS_UIprev()  

        ##=================Timer Object Initialization=======###
        

        self.WallClock = wx.Timer(self, 1)
        self.Bind(wx.EVT_TIMER, self.OnWallClock, self.WallClock)
        self.WallClock.Start(100)
        
        self.VisualizationTimer = wx.Timer(self, 2)
        self.ConnectTimer = wx.Timer(self, 3)
                ###self.Bind(wx.EVT_TIMER, self.OnVisualization_Timer, self.Visualization_Timer)
                ###self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

                ###self.timer.Start(100)
                ###self.WallClock.Start(100)

                #timeFont = wx.Font(16, wx.ROMAN, wx.NORMAL, wx.BOLD)
                #self.LocalTime = TransparentText(self.dateHeadingPnl, label='Date Time & Heading', pos=(277, 50))
                #self.LocalTime.SetFont(timeFont)
##
##       
        self.SetAutoLayout(True)
        #self.SetSizer(box)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)


    def FormPRS_UI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        prsFrameVSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.dateHeadingPnl = DateTimeHeadingPnlLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 1360,100 ), wx.TRANSPARENT_WINDOW|wx.TAB_TRAVERSAL )
        prsFrameVSizer.Add( self.dateHeadingPnl, 0, wx.EXPAND |wx.ALL, 5 )
        
        bodyHSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        InfoAreaVSizer = wx.BoxSizer( wx.VERTICAL )
        
        InfoAreaHSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.PatntEntryPnl = PatientEntryPnlLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 350,400 ), wx.TRANSPARENT_WINDOW|wx.TAB_TRAVERSAL )
        InfoAreaHSizer.Add( self.PatntEntryPnl, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.PatntDisplayPnl = PatntDisplayPnlLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,400 ), wx.TRANSPARENT_WINDOW|wx.TAB_TRAVERSAL )
        InfoAreaHSizer.Add( self.PatntDisplayPnl, 0, wx.EXPAND |wx.ALL, 5 )
        
        
        InfoAreaVSizer.Add( InfoAreaHSizer, 1, wx.EXPAND, 5 )
        
        self.deviceStatusPnl = deviceStatusPnlLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 850,300 ), wx.TRANSPARENT_WINDOW|wx.TAB_TRAVERSAL )
        InfoAreaVSizer.Add( self.deviceStatusPnl, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        #bodyHSizer.Add( InfoAreaVSizer, 0, 0, 5 )

        bodyHSizer.Add( InfoAreaVSizer, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.ReportPanel = reportPnlLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,600 ), wx.TRANSPARENT_WINDOW|wx.TAB_TRAVERSAL )
        bodyHSizer.Add( self.ReportPanel, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        prsFrameVSizer.Add( bodyHSizer, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( prsFrameVSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )


    def OnSize(self, size):
        #pass

        self.Refresh()

               
        self.Layout()        

        ## Heading Panel Box Resize

        self.dateHeadingPnl.Refresh()
        self.dateHeadingPnl.Layout()             

        ## Patient Entry Box Resize

        self.PatntEntryPnl.Refresh()
        self.PatntEntryPnl.Layout()        
       
        ## Patient Info Display Box Resize

        self.PatntDisplayPnl.Refresh()
        self.PatntDisplayPnl.Layout()        

        ## Device Status Panel Box Resize       

        self.deviceStatusPnl.Refresh()
        self.deviceStatusPnl.Layout()       

        ## Report Panel Box Resize

        self.ReportPanel.Refresh()
        self.ReportPanel.Layout()

       
        
        
        

    def OnEraseBackground(self, evt):
        pass

    ###########################################################################
    ##  PRS_Mainwindow Background Pic Drawing and Resizing Functions
    ###########################################################################


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
        
        #self.BgImg = self.scale_bitmap(self.bg, cliWidth, cliHeight)
        #imgSizer = wx.BoxSizer()
        #imgSizer.Add(bg_img)
        #self.SetSizer(imgSizer)
        xPos = 0
        yPos = 0
        #xPos = (cliWidth - self.bgImg_width)/2
        #yPos = (cliHeight - self.bgImg_height)/2
        dc.DrawBitmap(self.BgImg, xPos, yPos)



    ###########################################################################
    ##  PRS_Mainwindow Wall Clock Function
    ###########################################################################


    def OnWallClock(self, evt):
        #self.timer.Start(100)
        if self.WallClock.IsRunning():        
            
            #self.timeNow = time.asctime(time.localtime(time.time()))  
            self.timeNow = strftime("%a %B %d (%Y) - %H:%M:%S",localtime())
            self.dateHeadingPnl.DateText.SetLabel(self.timeNow)
##            
        else:
            print ("WallClock Off")
            #self.count = self.count + 1
            #print(self.count)

        


class TransparentPnlText(wx.StaticText):
    def __init__(self, *args, **kw):
        super(TransparentPnlText, self).__init__(*args, **kw)
        self.Bind(wx.EVT_PAINT, self._DoPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._DoEraseBG)
   
    def _DoPaint(self, evt):
        """
        """
        #print "paint statictext"
        #self.GetParent()._bmp
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush(wx.Colour(181, 240, 249), wx.CROSSDIAG_HATCH))
        #dc.SetBrush(wx.Brush(wx.Colour(181, 240, 249), wx.CROSSDIAG_HATCH)) #wx.TRANSPARENT
        #dc.SetPen(wx.Pen(wx.Colour(215, 215, 215), 5))# here 5 is width of the box
        dc.SetTextForeground( self.GetForegroundColour() )
        dc.SetFont( self.GetFont() )
        dc.DrawText(self.GetLabel(), 0, 0)
       
    def _DoEraseBG(self, evt):
        """
        """
        pass
        #print "erase"
	

class TransparentText(wx.StaticText):
    def __init__(self, *args, **kw):
        super(TransparentText, self).__init__(*args, **kw)
        self.Bind(wx.EVT_PAINT, self._DoPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._DoEraseBG)
   
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

class TransparentStaticBoxType2(wx.StaticBox):
    def __init__(self, *args, **kw):
        super(TransparentStaticBoxType2, self).__init__(*args, **kw)
        self.Bind(wx.EVT_PAINT, self._DoPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._DoEraseBG)
        #self.Bind(wx.EVT_SIZE, self._Resize)
   
    def _DoPaint(self, evt):
        """
        """
        dc = wx.PaintDC(self)
        #print "paint statictext"
        #self.GetParent()._bmp
        self.Draw(dc)
        

    def Draw(self, dc):
    
        cliWidth, cliHeight = self.GetClientSize()# get the box width and height
        #dc = wx.GCDC(self)
        
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetTextForeground( self.GetForegroundColour() )
        dc.SetFont( self.GetFont() )

        boxLabel = self.GetLabel()

        labelWidth,labelHeight = dc.GetTextExtent(boxLabel)# get the text width and height        

        dc.SetBrush(wx.Brush(wx.Colour(181, 240, 249), wx.CROSSDIAG_HATCH)) #wx.TRANSPARENT
        dc.SetPen(wx.Pen(wx.Colour(250,250,250), 0))# here 5 is width of the box
        
        dc.DrawRectangle(0,0,(cliWidth),(cliHeight))#parameters(x,y,width,heigth,radius) here 10 pixel is radius of the curved rectangle.
        #dc.DrawLine(0,labelHeight+5, cliWidth-4, labelHeight+5)#parameters(x1,y1,x2,y2) two points (x1,y1) and (x2,y2)        
        
        #dc.DrawText(boxLabel,(cliWidth-cliWidth/2 - labelWidth/2),2)

        #LabelText = TransparentText( self, wx.ID_ANY, boxLabel, wx.Point((cliWidth-cliWidth/2 - labelWidth/2),0), wx.DefaultSize,0)
        
        dc.EndDrawing()        
        

    def _Resize(self, evt):

        self.Refresh()
        self.Layout()
        
       
       
    def _DoEraseBG(self, evt):
        """
        """
        pass
        #print "erase"

    


class TransparentStaticBox(wx.StaticBox):
    def __init__(self, *args, **kw):
        super(TransparentStaticBox, self).__init__(*args, **kw)
        self.Bind(wx.EVT_PAINT, self._DoPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._DoEraseBG)
        #self.Bind(wx.EVT_SIZE, self._Resize)
   
    def _DoPaint(self, evt):
        """
        """
        dc = wx.PaintDC(self)
        #print "paint statictext"
        #self.GetParent()._bmp
        self.Draw(dc)
        

    def Draw(self, dc):
    
        cliWidth, cliHeight = self.GetClientSize()# get the box width and height
        #dc = wx.GCDC(self)
        #dc = wx.PaintDC(self)
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetTextForeground( self.GetForegroundColour() )
        dc.SetFont( self.GetFont() )

        boxLabel = self.GetLabel()

        labelWidth,labelHeight = dc.GetTextExtent(boxLabel)# get the text width and height        

        dc.SetBrush(wx.Brush(wx.Colour(181, 240, 249), wx.CROSSDIAG_HATCH)) #wx.TRANSPARENT
        dc.SetPen(wx.Pen(wx.Colour(215, 215, 215), 5))# here 5 is width of the box
        
        dc.DrawRoundedRectangle(0,0,(cliWidth),(cliHeight), 10)#parameters(x,y,width,heigth,radius) here 10 pixel is radius of the curved rectangle.
        dc.DrawLine(0,labelHeight+5, cliWidth-4, labelHeight+5)#parameters(x1,y1,x2,y2) two points (x1,y1) and (x2,y2)        
        
        dc.DrawText(boxLabel,(cliWidth-cliWidth/2 - labelWidth/2),2)       
        
        dc.EndDrawing()        
        

    def _Resize(self, evt):

        self.Refresh()
        self.Layout()
        
       
       
    def _DoEraseBG(self, evt):
        """
        """
        pass
        #print "erase"

class DateTimeHeadingPnlLayout(wx.Panel):
    def __init__(self, *args, **kw):
        super(DateTimeHeadingPnlLayout, self).__init__(*args, **kw)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)
        
        #self.Bind(wx.EVT_ERASE_BACKGROUND, self._EraseBG)
        self.timeFont = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
        #self.headingFont = wx.Font( 24, 72, 90, 90, False, "Cambria Math" )
        self.headingFont = wx.Font(24, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
        #self.headingFont.SetFaceName("Cambria Math")
        self.CopyRightFont = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        self.boxFont = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        #self.headingFont = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
##        self.PnlWidth, self.PnlHeight = self.GetClientSize()
##        self.PnlBox = TransparentStaticBox(self, label='Headings and Date Item', pos=(5,5), size=(self.PnlWidth, self.PnlHeight))
##        self.PnlBox.SetFont(self.boxFont)

        self._FormUI()

        #self.Bind(wx.EVT_SIZE, self._Resize)
   
    def _Paint(self, evt):
        """
        """
        #print "paint statictext"
        #self.GetParent()._bmp
        self.cliWidth, self.cliHeight = self.GetClientSize()# get the box width and height
        dc = wx.PaintDC(self)
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetTextForeground( self.GetForegroundColour() )
        dc.SetFont( self.GetFont() )

        self.Layout()


    

       

    def _FormUI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
            
		
##        self = wx.BoxSizer( wx.VERTICAL )
##        
##        self = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
        self.VSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.HeadingText = TransparentText( self, wx.ID_ANY, "QSTM PATIENT INFORMATION & TREATMENT RECORD SYSTEM   ", wx.DefaultPosition, wx.DefaultSize, 0 ) #size=(entryPnlWidth, entryPnlHeight)
        #self.HeadingText = TransparentText( self, wx.ID_ANY, " QSTM PATIENT & TREATMENT RECORD SYSTEM ", wx.DefaultPosition, size=(300, 10), 0 ) #size=(entryPnlWidth, entryPnlHeight)
        
        self.HeadingText.SetFont(self.headingFont)
        #self.HeadingText.Wrap( -1 )
        self.VSizer.Add( self.HeadingText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0 )
        
        self.HSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        
        #self.HSizer.AddSpacer( ( 500, 10), 2, wx.EXPAND|wx.RIGHT, 5 )
        
        #self.leftStaticLine = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 50,1 ), wx.LI_HORIZONTAL )
        #self.HSizer.Add( self.leftStaticLine, 1, wx.EXPAND , 5)

        self.DateSizer = wx.BoxSizer( wx.HORIZONTAL)
        
        self.DateText = wx.StaticText( self, wx.ID_ANY, "Date Time", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.DateText.SetFont(self.timeFont)

        self.DateSizer.Add(self.DateText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)
        #self.DateText.Wrap( -1 )
        self.HSizer.Add( self.DateSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        #self.rightStaticLine = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 50,1 ), wx.LI_HORIZONTAL )
        #self.HSizer.Add( self.rightStaticLine, 1, wx.EXPAND , 5 )

        
        
        
        #self.HSizer.AddSpacer( ( 500, 10), 1, wx.EXPAND|wx.RIGHT, 5 )   
##        
##        self.VSizer.Add( self.HSizer, 0, wx.EXPAND, 5 )
        
##        self.CopyrightText = TransparentText( self, wx.ID_ANY, "Indiana University", wx.DefaultPosition, wx.DefaultSize, 0 )
##        self.CopyrightText.SetFont(self.CopyRightFont)
##        self.CopyrightText.SetForegroundColour(wx.Colour(150,150,150))
##        #self.CopyrightText.Wrap( -1 )
##
##        self.HSizer.Add( self.CopyrightText, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.VSizer.Add( self.HSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
##        self.VSizer.Add( self.CopyrightText, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        
        self.SetSizer( self.VSizer )
        #self.VSizer.Fit( self )
        #self.Layout()

    
    def _Resize(self, size):
        #pass
        self.Refresh()               
        self.Layout()

##        self.PnlBox.Destroy()
        #self._DestroyUI()

##        self.PnlWidth, self.PnlHeight = self.GetClientSize()
##        self.PnlBox = TransparentStaticBox(self, label='Headings and Date Item', pos=(5,5), size=(self.PnlWidth, self.PnlHeight))
##        self.PnlBox.SetFont(self.boxFont)

        #self._FormUI()        
        #self.Layout()

   


class PatientEntryPnlLayout(wx.Panel):
    def __init__(self, *args, **kw):
        super(PatientEntryPnlLayout, self).__init__(*args, **kw)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)

        self.boxFont = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        self.NewFont = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.SearchFont = wx.Font(14, wx.ROMAN, wx.NORMAL,  wx.NORMAL, True)
        self.SearchBoxFont = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL)

##        self.entryPnlWidth, self.entryPnlHeight = self.PatntEntryPnl.GetClientSize()
##        self.PatntEntryBox = TransparentStaticBox(self, label='PATIENT ENTRY', pos=(2,2), size=(self.entryPnlWidth, self.entryPnlHeight))
##        self.PatntEntryBox.SetFont(self.boxFont)
##        
        #self._DrawPnlStaticBox()

        self._FormUI()

        self.Bind(wx.EVT_SIZE, self._Resize)

        self.Centre(wx.BOTH)
        self.Layout()


    def _Paint(self, evt):
        """
        """

        self.PnlBoxLabel = " PATIENT  ENTRY "

        cliWidth, cliHeight = self.GetClientSize()

        dc = wx.PaintDC(self)

        #self.PnlBoxLabel.SetFont(self.boxFont)

        PanelBoxDraw(dc, self.PnlBoxLabel, cliWidth, cliHeight )

    def _Resize(self, size):
        #pass
        self.Refresh()               
        self.Layout() 
   
    

    def activateExistingPatntFunction(self, evt):
        self.SearchList = wx.ListCtrl(self.searchBox, size=(330,110), pos = (5,35), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        #self.SearchList.SetBackground(wx.TRANSPARENT)
        self.SearchList.InsertColumn(0, 'Index', width = 30)
        self.SearchList.InsertColumn(1, 'Patient Full Name', width = 220)
        self.SearchList.InsertColumn(2, 'DOB', width=100)

        self.PatientSearchBar = wx.SearchCtrl(self.searchBox, id=1, value="", size=(330,25), pos=(5, 5), style = wx.TE_PROCESS_ENTER)
        self.PatientSearchBar.ShowCancelButton(True)
        self.PatientSearchBar.SetSearchMenuBitmap
       

    def _FormUI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
        self.PnlVSizer = wx.BoxSizer( wx.VERTICAL )
        self.PnlVSizer.SetMinSize( wx.Size( 300,350 ) )
        #self.PnlVSizer.SetMinSize( wx.Size( 300,350 ) )
        self.PnlVSizer.AddSpacer( ( 10, 50), 0, wx.EXPAND, 5 )
        
        newPatntHSizer = wx.BoxSizer( wx.HORIZONTAL )

        newPatntHSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )
        
        self.cbNewPatient = wx.CheckBox( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        newPatntHSizer.Add( self.cbNewPatient, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.NewPatientLbl = TransparentText( self, wx.ID_ANY, "New Patient Enrollment", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.NewPatientLbl.SetFont(self.NewFont)
        #self.NewPatientLbl.Wrap( -1 )
        newPatntHSizer.Add( self.NewPatientLbl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 5 )
        
        
        self.PnlVSizer.Add( newPatntHSizer, 0, wx.EXPAND, 5 )
        
        
        self.PnlVSizer.AddSpacer( ( 10, 10), 0, wx.EXPAND, 5 )
        
        existPatntHSizer = wx.BoxSizer( wx.HORIZONTAL )

        existPatntHSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )
        
        self.cbExistingPatient = wx.CheckBox( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        existPatntHSizer.Add( self.cbExistingPatient, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        self.cbExistingPatient.Bind(wx.EVT_CHECKBOX, self.activateExistingPatntFunction)
        
        self.ExistingPatientLbl = TransparentText( self, wx.ID_ANY, "Existing Patient Selection", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ExistingPatientLbl.SetFont(self.NewFont)
        #self.ExistingPatientLbl.Wrap( -1 )
        existPatntHSizer.Add( self.ExistingPatientLbl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 5 )
        
        
        self.PnlVSizer.Add( existPatntHSizer, 0, wx.EXPAND, 5 )
        
        
        self.PnlVSizer.AddSpacer( ( 10, 10), 0, wx.EXPAND, 5 )
        
        self.existPatntPnlLbl = TransparentText( self, wx.ID_ANY, "Patient Search Box", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.existPatntPnlLbl.SetFont(self.SearchFont)
        #self.existPatntPnlLbl.Wrap( -1 )
        self.PnlVSizer.Add( self.existPatntPnlLbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        

        self.searchBox = TransparentStaticBox(self, label='Search Patient', pos=(2,2))
        self.searchBox.SetFont(self.SearchBoxFont)

        searchItemSz = wx.StaticBoxSizer(self.searchBox, wx.VERTICAL )
        searchItemSz.SetMinSize( wx.Size( 340,150 ) )
        
        self.PnlVSizer.Add( searchItemSz, 0, wx.EXPAND |wx.ALL, 5 )

        
        
##        self.searchPnl = wx.Panel( self, wx.ID_ANY, wx.Point( 10,90 ), wx.Size( 330,120 ), wx.RAISED_BORDER|wx.FULL_REPAINT_ON_RESIZE )
##        self.searchPnl.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
##        self.searchPnl.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
##        
##        self.PnlVSizer.Add( self.searchPnl, 0, wx.EXPAND |wx.ALL, 5 )

        
        
        
        self.PnlVSizer.AddSpacer( ( 10, 10), 0, wx.EXPAND, 5 )
        
        retrvPatntHSizer = wx.BoxSizer( wx.HORIZONTAL )

        retrvPatntHSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )
        
        self.cbRetrievePatient = wx.CheckBox( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        retrvPatntHSizer.Add( self.cbRetrievePatient, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.RetrievePatientLbl = TransparentText( self, wx.ID_ANY, "Retrieve Past Treatment", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.RetrievePatientLbl.SetFont(self.NewFont)
        #self.RetrievePatientLbl.Wrap( -1 )
        retrvPatntHSizer.Add( self.RetrievePatientLbl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 5 )
        
        
        self.PnlVSizer.Add( retrvPatntHSizer, 0, wx.EXPAND, 5 )
        
        
        self.PnlVSizer.AddSpacer( ( 10, 10), 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( self.PnlVSizer )
        self.Layout()

        self.PnlVSizer.Fit(self)

        #self.GetParent().SendSizeEvent()
        #self.Layout()       

    

class PatntDisplayPnlLayout(wx.Panel):
    def __init__(self, *args, **kw):
        super(PatntDisplayPnlLayout, self).__init__(*args, **kw)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)

        self.boxFont = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        self.TextFont = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.TextLblFont = wx.Font(12, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.LabelFont = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)

        

        self._FormUI()

        self.Bind(wx.EVT_SIZE, self._Resize)

        self.Centre(wx.BOTH)
        self.Layout()


    def _Paint(self, evt):
        """
        """

        self.PnlBoxLabel = " CURRENT  PATIENT  INFORMATION "

        cliWidth, cliHeight = self.GetClientSize()

        dc = wx.PaintDC(self)

        #self.PnlBoxLabel.SetFont(self.boxFont)

        PanelBoxDraw(dc, self.PnlBoxLabel, cliWidth, cliHeight )

    

    def _FormUI(self):
        #pass

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.PnlHSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.PnlHSizer.AddSpacer( ( 10, 10), 0, wx.EXPAND, 5 )
        

        self.PnlVSizer = wx.BoxSizer( wx.VERTICAL )
        self.PnlVSizer.AddSpacer( ( 10, 50), 0, wx.EXPAND, 5 )
        
        PatntInfoSz = wx.GridSizer( 7, 2, 0, 0 )
        
        PatntInfoSz.SetMinSize( wx.Size( 500,300 ) ) 
        self.PatntName = TransparentText( self, wx.ID_ANY, "FIRST NAME :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntName.SetFont(self.TextFont)
        #self.PatntName.Wrap( -1 )
        PatntInfoSz.Add( self.PatntName, 0, wx.ALL, 5 )
        
        self.PatntNameLbl = TransparentText( self, wx.ID_ANY, "firstname", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntNameLbl.SetFont(self.TextLblFont)
        #self.PatntNameLbl.Wrap( -1 )
        PatntInfoSz.Add( self.PatntNameLbl, 0, wx.ALL, 5 )
        
        self.PatntSurname = TransparentText( self, wx.ID_ANY, "LAST NAME :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntSurname.SetFont(self.TextFont)
        #self.PatntSurname.Wrap( -1 )
        PatntInfoSz.Add( self.PatntSurname, 0, wx.ALL, 5 )
        
        self.PatntSurnameLbl = TransparentText( self, wx.ID_ANY, "lastname", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntSurnameLbl.SetFont(self.TextLblFont)
        #self.PatntSurnameLbl.Wrap( -1 )
        PatntInfoSz.Add( self.PatntSurnameLbl, 0, wx.ALL, 5 )
        
        self.PatntEnrlID = TransparentText( self, wx.ID_ANY, "ENROLL ID :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntEnrlID.SetFont(self.TextFont)
        #self.PatntEnrlID.Wrap( -1 )
        PatntInfoSz.Add( self.PatntEnrlID, 0, wx.ALL, 5 )
        
        self.PatntEnrlIDLbl = TransparentText( self, wx.ID_ANY, "id", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntEnrlIDLbl.SetFont(self.TextLblFont)
        self.PatntEnrlIDLbl.Wrap( -1 )
        PatntInfoSz.Add( self.PatntEnrlIDLbl, 0, wx.ALL, 5 )
        
        self.PatntEnrlDate = TransparentText( self, wx.ID_ANY, "ENROLL DATE :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntEnrlDate.SetFont(self.TextFont)
        #self.PatntEnrlDate.Wrap( -1 )
        PatntInfoSz.Add( self.PatntEnrlDate, 0, wx.ALL, 5 )
        
        self.PatntEnrlDateLbl = TransparentText( self, wx.ID_ANY, "enrolldate", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntEnrlDateLbl.SetFont(self.TextLblFont)
        #self.PatntEnrlDateLbl.Wrap( -1 )
        PatntInfoSz.Add( self.PatntEnrlDateLbl, 0, wx.ALL, 5 )
        
        self.PatntDob = TransparentText( self, wx.ID_ANY, "BIRTH DATE :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntDob.SetFont(self.TextFont)
        #self.PatntDob.Wrap( -1 )
        PatntInfoSz.Add( self.PatntDob, 0, wx.ALL, 5 )
        
        self.PatntDobLbl = TransparentText( self, wx.ID_ANY, "Dateofbirth", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntDobLbl.SetFont(self.TextLblFont)
        #self.PatntDobLbl.Wrap( -1 )
        PatntInfoSz.Add( self.PatntDobLbl, 0, wx.ALL, 5 )
        
        self.PatntAge = TransparentText( self, wx.ID_ANY, "AGE :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntAge.SetFont(self.TextFont)
        #self.PatntAge.Wrap( -1 )
        PatntInfoSz.Add( self.PatntAge, 0, wx.ALL, 5 )
        
        self.PatntAgeLbl = TransparentText( self, wx.ID_ANY, "age", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntAgeLbl.SetFont(self.TextLblFont)
        #self.PatntAgeLbl.Wrap( -1 )
        PatntInfoSz.Add( self.PatntAgeLbl, 0, wx.ALL, 5 )
        
        self.PatntSex = TransparentText( self, wx.ID_ANY, "SEX :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntSex.SetFont(self.TextFont)
        #self.PatntSex.Wrap( -1 )
        PatntInfoSz.Add( self.PatntSex, 0, wx.ALL, 5 )
        
        self.PatntSexLbl = TransparentText(self, wx.ID_ANY, "gender", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PatntSexLbl.SetFont(self.TextLblFont)
        #self.PatntSexLbl.Wrap( -1 )
        PatntInfoSz.Add( self.PatntSexLbl, 0, wx.ALL, 5 )
        
        self.PnlVSizer.Add(PatntInfoSz )

        self.TreatmentBtn =  wx.Button( self, wx.ID_ANY, u"START  TREATMENT", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.PnlVSizer.Add(self.TreatmentBtn,0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.PnlHSizer.Add(self.PnlVSizer )
        self.SetSizer( self.PnlHSizer)
        self.Layout()
        #self.Fit(self.PnlHSizer)
        
        self.Centre( wx.BOTH )
    

    def _Resize(self, size):
        #pass
        self.Refresh()               
        self.Layout()   



class deviceStatusPnlLayout(wx.Panel):
    def __init__(self, *args, **kw):
        super(deviceStatusPnlLayout, self).__init__(*args, **kw)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)

        self.TextFont = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.BOLD)



        self._FormUI()
        #self.UI()

        self.Bind(wx.EVT_SIZE, self._Resize)

        self.Centre(wx.BOTH)
        self.Layout()

    def _Paint(self, evt):
        """
        """

        self.PnlBoxLabel = " SYSTEM  AND  DEVICE  STATUS "

        cliWidth, cliHeight = self.GetClientSize()

        dc = wx.PaintDC(self)

        #self.PnlBoxLabel.SetFont(self.boxFont)

        PanelBoxDraw(dc, self.PnlBoxLabel, cliWidth, cliHeight )


    def _FormUI(self):
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
        PnlVSizer = wx.BoxSizer( wx.VERTICAL )
        
        
        PnlVSizer.AddSpacer( ( 10, 25), 0, wx.EXPAND, 5 )
        
        PnlHSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        
        PnlHSizer.AddSpacer( ( 6, 3), 0, wx.EXPAND, 5 )

        self.connDevBox = TransparentStaticBox( self, wx.ID_ANY, "CONNECTED  DEVICES" )
        self.connDevBox.SetFont(self.TextFont)
        
        connDevBoxSz = wx.StaticBoxSizer( self.connDevBox , wx.VERTICAL )


        ConnDevGSz = wx.FlexGridSizer( 5, 3, 0, 0 )
        #ConnDevGSz.AddGrowableCol( 0, proportion=0 )
        ConnDevGSz.AddGrowableCol( 1, proportion=0 )
        ConnDevGSz.AddGrowableCol( 2, proportion=0 )
        ConnDevGSz.AddGrowableRow( 0, proportion=0 )
        ConnDevGSz.AddGrowableRow( 1, proportion=0 )
        ConnDevGSz.AddGrowableRow( 2, proportion=0 )
        ConnDevGSz.AddGrowableRow( 3, proportion=0 )
        ConnDevGSz.AddGrowableRow( 4, proportion=0 )
        
        ConnDevGSz.SetFlexibleDirection( wx.BOTH )
        #ConnDevGSz.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.SelectText = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"SELECT", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.SelectText.Wrap( -1 )
        ConnDevGSz.Add( self.SelectText, 0, wx.ALL, 5 )
        
        self.ComPortText = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"COM PORT", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.ComPortText.Wrap( -1 )
        ConnDevGSz.Add( self.ComPortText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.QDevText = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"QSTM DEVICE", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.QDevText.Wrap( -1 )
        ConnDevGSz.Add( self.QDevText, 0, wx.ALL, 5 )
        
        self.cb_Prt1 = wx.CheckBox( connDevBoxSz.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        ConnDevGSz.Add( self.cb_Prt1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.PrtXX1Lbl = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"COM XX", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.PrtXX1Lbl.Wrap( -1 )
        ConnDevGSz.Add( self.PrtXX1Lbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.DevSerLbl1 = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"No Device", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.DevSerLbl1.Wrap( -1 )
        ConnDevGSz.Add( self.DevSerLbl1, 0, wx.ALL, 5 )
        
        self.cb_Prt2 = wx.CheckBox( connDevBoxSz.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        ConnDevGSz.Add( self.cb_Prt2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.PrtXX2Lbl = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"COM XX", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.PrtXX2Lbl.Wrap( -1 )
        ConnDevGSz.Add( self.PrtXX2Lbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.DevSerLbl2 = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"No Device", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.DevSerLbl2.Wrap( -1 )
        ConnDevGSz.Add( self.DevSerLbl2, 0, wx.ALL, 5 )
        
        self.cb_Prt3 = wx.CheckBox( connDevBoxSz.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        ConnDevGSz.Add( self.cb_Prt3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.PrtXX3Lbl = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"COM XX", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.PrtXX3Lbl.Wrap( -1 )
        ConnDevGSz.Add( self.PrtXX3Lbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.DevSerLbl3 = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"No Device", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.DevSerLbl3.Wrap( -1 )
        ConnDevGSz.Add( self.DevSerLbl3, 0, wx.ALL, 5 )
        
        self.cb_Prt4 = wx.CheckBox( connDevBoxSz.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        ConnDevGSz.Add( self.cb_Prt4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.PrtXX4Lbl = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"COM XX", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.PrtXX4Lbl.Wrap( -1 )
        ConnDevGSz.Add( self.PrtXX4Lbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.DevSerLbl4 = TransparentText( connDevBoxSz.GetStaticBox(), wx.ID_ANY, u"No Device", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.DevSerLbl4.Wrap( -1 )
        ConnDevGSz.Add( self.DevSerLbl4, 0, wx.ALL, 5 )
        
        
        connDevBoxSz.Add( ConnDevGSz, 1, wx.EXPAND, 5 )
        
        
        
        PnlHSizer.Add( connDevBoxSz, 1, wx.EXPAND, 5 )
        
        
        PnlHSizer.AddSpacer( ( 0, 0), 0, wx.EXPAND, 5 )

        self.SysInfoBox = TransparentStaticBox( self, wx.ID_ANY, "SYSTEM  INFORMATION" )
        self.SysInfoBox.SetFont(self.TextFont)
        
        SysInfoBoxSz = wx.StaticBoxSizer( self.SysInfoBox , wx.VERTICAL )


        sysInfo_gSizer = wx.GridSizer( 6, 2, 0, 0 )
        
        self.sysModeTxt = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"System Mode :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sysModeTxt.Wrap( -1 )
        sysInfo_gSizer.Add( self.sysModeTxt, 0, wx.ALL, 5 )
        
        self.sysModeLbl = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"ModeName", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.sysModeLbl.Wrap( -1 )
        sysInfo_gSizer.Add( self.sysModeLbl, 0, wx.ALL, 5 )
        
        self.connDevTxt = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"Total Connected Devices :", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.connDevTxt.Wrap( -1 )
        sysInfo_gSizer.Add( self.connDevTxt, 0, wx.ALL, 5 )
        
        self.connDevTxtLbl = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"Con#", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.connDevTxtLbl.Wrap( -1 )
        sysInfo_gSizer.Add( self.connDevTxtLbl, 0, wx.ALL, 5 )
        
        self.Ptr1StateTxt = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"PORT-1 :", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr1StateTxt.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr1StateTxt, 0, wx.ALL, 5 )
        
        self.Ptr1StateLbl = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr1StateLbl.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr1StateLbl, 0, wx.ALL, 5 )
        
        self.Ptr2StateTxt = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"PORT-2 :", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr2StateTxt.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr2StateTxt, 0, wx.ALL, 5 )
        
        self.Ptr2StateLbl = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr2StateLbl.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr2StateLbl, 0, wx.ALL, 5 )
        
        self.Ptr3StateTxt = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"PORT-3 :", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr3StateTxt.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr3StateTxt, 0, wx.ALL, 5 )
        
        self.Ptr3StateLbl = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr3StateLbl.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr3StateLbl, 0, wx.ALL, 5 )
        
        self.Ptr4StateTxt = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"PORT-4 :", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr4StateTxt.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr4StateTxt, 0, wx.ALL, 5 )
        
        self.Ptr4StateLbl = TransparentText( SysInfoBoxSz.GetStaticBox(), wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.Ptr4StateLbl.Wrap( -1 )
        sysInfo_gSizer.Add( self.Ptr4StateLbl, 0, wx.ALL, 5 )
        
        
        SysInfoBoxSz.Add( sysInfo_gSizer, 1, wx.EXPAND, 5 )
        
        
        
        PnlHSizer.Add( SysInfoBoxSz, 1, wx.EXPAND, 5 )
        
        
        PnlHSizer.AddSpacer( ( 6, 3), 0, wx.EXPAND, 5 )
        
        
        PnlVSizer.Add( PnlHSizer, 1, wx.EXPAND, 5 )
        
        
        PnlVSizer.AddSpacer( ( 5, 5), 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( PnlVSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )


    

    def _Resize(self, size):
        #pass
        self.Refresh()
        self.Layout()

##        cliWidth, cliHeight = self.GetClientSize()
##
##        if cliHeight >= 310 :
##            self.TextFont.SetPointSize(12)
##            self.connDevBox.SetFont(self.TextFont)
##            self.SysInfoBox.SetFont(self.TextFont)
##        else:
##            self.TextFont.SetPointSize(10)
##            self.connDevBox.SetFont(self.TextFont)
##            self.SysInfoBox.SetFont(self.TextFont)
            
                   
        


class reportPnlLayout(wx.Panel):
    def __init__(self, *args, **kw):
        super(reportPnlLayout, self).__init__(*args, **kw)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)

        self._FormUI()

        self.Bind(wx.EVT_SIZE, self._Resize)

        self.Centre(wx.BOTH)
        self.Layout()

    def _Paint(self, evt):
        """
        """

        self.PnlBoxLabel = " TREATMENT  REPORT "

        cliWidth, cliHeight = self.GetClientSize()

        dc = wx.PaintDC(self)

        #self.PnlBoxLabel.SetFont(self.boxFont)

        PanelBoxDraw(dc, self.PnlBoxLabel, cliWidth, cliHeight )

    

    def _FormUI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
        PnlVSizer = wx.BoxSizer( wx.VERTICAL )
        
        
        PnlVSizer.AddSpacer( ( 10, 27), 0, wx.EXPAND, 5 )
        
        PnlBtnHSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        
        PnlBtnHSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.saveBtn = wx.Button( self, wx.ID_ANY, u"SAVE REPORT", wx.DefaultPosition, wx.DefaultSize, 0 )
        PnlBtnHSizer.Add( self.saveBtn, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        PnlBtnHSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.OpenRprtBtn = wx.Button( self, wx.ID_ANY, u"EXPORT", wx.DefaultPosition, wx.DefaultSize, 0 )
        PnlBtnHSizer.Add( self.OpenRprtBtn, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        PnlBtnHSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.GrphBtn = wx.Button( self, wx.ID_ANY, u"SHOW REPORT GRAPH", wx.DefaultPosition, wx.DefaultSize, 0 )
        PnlBtnHSizer.Add( self.GrphBtn, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        PnlBtnHSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        PnlVSizer.Add( PnlBtnHSizer, 0, wx.EXPAND, 5 )
        
        ReportHSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        
        ReportHSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )

        self.ReportBox = TransparentStaticBoxType2( self, wx.ID_ANY, u"Patient Report" )

        RprtBoxWidth, RprtBoxHeight = self.ReportBox.GetClientSize()
        
        self.ReportBoxSz = wx.StaticBoxSizer( self.ReportBox, wx.VERTICAL )

        self.Q_ReportBook = wx.Notebook( self.ReportBox, wx.ID_ANY, wx.Point(0,0), wx.Size(RprtBoxWidth, RprtBoxHeight))
        self.Q1_RprtPnl = wx.Panel( self.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.Q_ReportBook.AddPage( self.Q1_RprtPnl, u"Q1 Report", False )
        self.Q2_RprtPnl = wx.Panel( self.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.Q_ReportBook.AddPage( self.Q2_RprtPnl, u"Q2 Report", False )
        self.TotRprtPnl = wx.Panel( self.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.Q_ReportBook.AddPage( self.TotRprtPnl, u"Full Session Report", False )      
        
        self.ReportBoxSz.Add( self.Q_ReportBook, 1, wx.EXPAND |wx.ALL, 0 )
        
        
        ReportHSizer.Add( self.ReportBoxSz, 1, wx.EXPAND, 5 )
        
        
        ReportHSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )
        
        
        PnlVSizer.Add( ReportHSizer, 1, wx.EXPAND, 5 )
        
        
        PnlVSizer.AddSpacer( ( 0, 5), 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( PnlVSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )

        #self.Q_ReportBook.Show(False) 


       
    def _Resize(self, size):
        #pass
        self.Refresh()               
        self.Layout()

##      



def main():
    
    ex = wx.App()
    ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    PRS_MainWindowFrontEnd(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()          

	

