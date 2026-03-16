import wx
from PRS_UI_FrontEnd import TransparentText, PanelBoxDraw

class TransparentRadioBox(wx.RadioBox):
    def __init__(self, *args, **kw):
        super(TransparentRadioBox, self).__init__(*args, **kw)
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
        
        dc.DrawText(boxLabel,(cliWidth-cliWidth/2 - labelWidth/2),2)

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



class RetrieveDlgFrontEnd ( wx.Dialog ):
    
	
    def __init__( self, parent ):
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 550,525 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bg_img='RetrievePnlBGpic.jpg'        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.bg = wx.Bitmap(bg_img)
        self._width, self._height = self.bg.GetSize()
        
        dlgSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.HeadingPanel =  HeadingPnlLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 550,115 ), wx.TAB_TRAVERSAL|wx.TRANSPARENT_WINDOW )
        
        dlgSizer.Add( self.HeadingPanel, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.InstructionPnl = InstructionPnlLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 550,50 ), wx.TAB_TRAVERSAL|wx.TRANSPARENT_WINDOW )
        dlgSizer.Add( self.InstructionPnl, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.SelectPnl = SelectPanelLayout( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL|wx.TRANSPARENT_WINDOW )
        dlgSizer.Add( self.SelectPnl, 1, wx.EXPAND |wx.ALL, 3 )
        
        self.retrieveBtn = wx.Button( self, wx.ID_ANY, u" RETRIEVE  TREATMENT ", wx.DefaultPosition, wx.DefaultSize, 0 )
        dlgSizer.Add( self.retrieveBtn, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        self.SetSizer( dlgSizer )
        #self.Layout()
        
        
        self.Centre( wx.BOTH )

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Refresh()
        self.Layout()
        
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




class HeadingPnlLayout(wx.Panel):
    def __init__(self, *args, **kw):
        super(HeadingPnlLayout, self).__init__(*args, **kw)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)
        
        
        #self.timeFont = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
        #self.headingFont = wx.Font( 24, 72, 90, 90, False, "Cambria Math" )
        self.headingFont = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        #self.headingFont.SetFaceName("Cambria Math")
        #self.CopyRightFont = wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        #self.boxFont = wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        

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
     
        self.VSizer = wx.BoxSizer( wx.VERTICAL )

        self.VSizer.AddSpacer( ( 0, 5), 0, wx.EXPAND, 5 )

        self.HSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.HSizer.AddSpacer( ( 85,0), 0, wx.EXPAND, 5 )
        
        #self.HeadingText = TransparentText( self,  " Treatment Retrieve Manager" ) #size=(entryPnlWidth, entryPnlHeight)
        self.HeadingText = TransparentText( self, wx.ID_ANY, " Treatment Retrieval Manager ", wx.DefaultPosition,  wx.DefaultSize, 0 ) #size=(entryPnlWidth, entryPnlHeight)
        
        self.HeadingText.SetFont(self.headingFont)
        #self.HeadingText.Wrap( -1 )
        self.HSizer.Add( self.HeadingText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0 )

        self.VSizer.Add(self.HSizer, 0, wx.ALL, 0)

        self.VSizer.AddSpacer( ( 0, 45), 0, wx.EXPAND, 5 )       
        
        
        self.SetSizer( self.VSizer )
        #self.VSizer.Fit( self )
        #self.Layout()
    
    def _Resize(self, size):
        
        self.Refresh()               
        self.Layout()


class InstructionPnlLayout(wx.Panel):

    def __init__(self, *args, **kw):
        super(InstructionPnlLayout, self).__init__(*args, **kw)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)

        self.PnlFont = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
        self.NewFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        self._FormUI()

        
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

##        HSizer = wx.BoxSizer( wx.HORIZONTAL )
##		
##		
##        HSizer.AddSpacer( ( 10, 0), 0, wx.EXPAND, 5 )
##
##        TxtVSizer = wx.BoxSizer( wx.VERTICAL )
##
##
##        TxtVSizer.AddSpacer( ( 0, 0), 0, wx.EXPAND, 5 )
##
##        self.TxtLabel = TransparentText( self, wx.ID_ANY, u"INSTRUCTIONS :", wx.DefaultPosition, wx.DefaultSize, 0 )
##        self.TxtLabel.SetFont(self.PnlFont)
##        self.TxtLabel.Wrap( -1 )
##        TxtVSizer.Add( self.TxtLabel, 0,  wx.ALIGN_CENTER|wx.ALL, 5 )
##
##
##        HSizer.Add( TxtVSizer, 0, wx.EXPAND, 5 )
##
##
##        HSizer.AddSpacer( ( 10, 0), 0, wx.EXPAND, 5 )
##
##        RuleVSizer = wx.BoxSizer( wx.VERTICAL )
##
##
##        RuleVSizer.AddSpacer( ( 0, 0), 0, wx.EXPAND, 5 )
##
##        self.Rule1 = TransparentText( self, wx.ID_ANY, u"Instruction 1", wx.DefaultPosition, wx.DefaultSize, 0 )
##        self.Rule1.Wrap( -1 )
##        RuleVSizer.Add( self.Rule1, 0, wx.ALL, 5 )
##
##        self.Rule2 = TransparentText( self, wx.ID_ANY, u"Instruction 2", wx.DefaultPosition, wx.DefaultSize, 0 )
##        self.Rule2.Wrap( -1 )
##        RuleVSizer.Add( self.Rule2, 0, wx.ALL, 5 )
##
##
##        HSizer.Add( RuleVSizer, 1, wx.EXPAND, 5 )
##
##
##        self.SetSizer( HSizer )
##        self.Layout()       

        HSizer = wx.BoxSizer( wx.HORIZONTAL )		
		
        HSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )

        self.TxtLabel = TransparentText( self, wx.ID_ANY, u"INSTRUCTIONS :", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.TxtLabel.SetFont(self.NewFont)
        self.TxtLabel.SetForegroundColour( wx.Colour(100, 0, 0 ))
        self.TxtLabel.SetFont(self.PnlFont)
        self.TxtLabel.Wrap( -1 )
        HSizer.Add( self.TxtLabel, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        HSizer.AddSpacer( ( 10, 0), 0, wx.EXPAND, 5 )

        VSizer3 = wx.BoxSizer( wx.VERTICAL )
        VSizer3.AddSpacer( ( 0, 10), 0, wx.EXPAND, 5 )

        self.Rule1 = TransparentText( self, wx.ID_ANY, u"Instruction 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Rule1.SetFont(self.NewFont)
        self.Rule1.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.Rule1.Wrap( -1 )
        VSizer3.Add( self.Rule1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

##        self.Rule2 = TransparentText( self, wx.ID_ANY, u"Instruction 2", wx.DefaultPosition, wx.DefaultSize, 0 )
##        self.Rule2.SetFont(self.NewFont)
##        self.Rule2.SetForegroundColour( wx.Colour(130, 130, 130  ))
##        self.Rule2.Wrap( -1 )
##        VSizer3.Add( self.Rule2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        VSizer3.AddSpacer( ( 0, 10), 0, wx.EXPAND, 5 )


        HSizer.Add( VSizer3, 1, wx.EXPAND, 5 )


        self.SetSizer( HSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )

        

class SelectPanelLayout(wx.Panel):    

    def __init__(self, *args, **kw):
        super(SelectPanelLayout, self).__init__(*args, **kw)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self._Paint)

        self.PnlFont = wx.Font(10, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)

        #self.boxFont = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        self.NewFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        #self.SearchFont = wx.Font(14, wx.ROMAN, wx.NORMAL,  wx.NORMAL, True)
        #self.SearchBoxFont = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL)

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

        self.PnlBoxLabel = " Select Patient Treatment "

        cliWidth, cliHeight = self.GetClientSize()

        dc = wx.PaintDC(self)

        #self.PnlBoxLabel.SetFont(self.boxFont)

        PanelBoxDraw(dc, self.PnlBoxLabel, cliWidth, cliHeight )

    def _Resize(self, size):
        #pass
        self.Refresh()               
        self.Layout()

    def _FormUI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        PnlVSizer = wx.BoxSizer( wx.VERTICAL )
		
		
        PnlVSizer.AddSpacer( ( 0, 27), 0, wx.EXPAND, 5 )
        
        self.searchBar = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 520,-1 ),style = wx.TE_PROCESS_ENTER )
        self.searchBar.ShowSearchButton( True )
        self.searchBar.ShowCancelButton( True )
        PnlVSizer.Add( self.searchBar, 0, wx.ALL|wx.ALIGN_CENTER, 5 )
        
        TreatHSizer = wx.BoxSizer( wx.HORIZONTAL )

        TreatHSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )
        
        self.pnlRadioBoxChoices = [ u"No Selection", u"First Treatment", u"Last Treatment", u"All Treatments", u"Select by Date" ]
        self.pnlRadioBox = TransparentRadioBox( self, wx.ID_ANY, u"View Treatments", wx.DefaultPosition, wx.DefaultSize, self.pnlRadioBoxChoices, 5, wx.RA_SPECIFY_ROWS )
        self.pnlRadioBox.SetSelection( 0 )        
        TreatHSizer.Add( self.pnlRadioBox, 0, wx.ALL, 5 )
        
        
        self.ListBSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        self.SrchListCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,138 ), wx.LC_REPORT|wx.RAISED_BORDER )
        self.ListBSizer.Add( self.SrchListCtrl, 1, wx.ALL, 5 )
        
        
        TreatHSizer.Add( self.ListBSizer, 1, wx.EXPAND, 5 )

        TreatHSizer.AddSpacer( ( 5, 0), 0, wx.EXPAND, 5 )
        
        
        PnlVSizer.Add( TreatHSizer, 0, wx.EXPAND, 5 )
        
        
        PnlVSizer.AddSpacer( ( 0, 0), 0, wx.EXPAND, 5 )
        
        LabelGSizer = wx.GridSizer( 2, 3, 0, 0 )
        #LabelGSizer = wx.FlexGridSizer( 2, 3, 0, 0 )
        
        self.TxtPatnt = TransparentText( self, wx.ID_ANY, u"SELECTED PATIENT :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.TxtPatnt.SetFont(self.PnlFont)
        self.TxtPatnt.Wrap( -1 )
        LabelGSizer.Add( self.TxtPatnt, 0, wx.ALL, 5 )
        
        self.LblPatnt = TransparentText( self, wx.ID_ANY, u"Patient Full Name ... this is not the right time", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LblPatnt.SetFont(self.NewFont)
        self.LblPatnt.Wrap( 180 )
        LabelGSizer.Add( self.LblPatnt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.LblDOB = TransparentText( self, wx.ID_ANY, u"DOB : XX-XX-XX", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LblDOB.SetFont(self.NewFont)
        self.LblDOB.Wrap( -1 )
        LabelGSizer.Add( self.LblDOB, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.TxtTreat = TransparentText( self, wx.ID_ANY, u"SELECTED TREATMENT :", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.TxtTreat.SetFont(self.PnlFont)
        self.TxtTreat.Wrap( -1 )
        LabelGSizer.Add( self.TxtTreat, 0, wx.ALL, 5 )
        
        self.LblTreatDate = TransparentText( self, wx.ID_ANY, u"Date : XX-XX-XX", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LblTreatDate.SetFont(self.NewFont)
        self.LblTreatDate.Wrap( -1 )
        LabelGSizer.Add( self.LblTreatDate, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.LblTreatTime = TransparentText( self, wx.ID_ANY, u"Time :  XX:XX:XX", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LblTreatTime.SetFont(self.NewFont)
        self.LblTreatTime.Wrap( -1 )
        LabelGSizer.Add( self.LblTreatTime, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        PnlVSizer.Add( LabelGSizer, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        self.SetSizer( PnlVSizer )
        self.Layout()
        self.Centre( wx.BOTH )

    





def main():
    
    ex = wx.App()
    ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    dlg = RetrieveDlgFrontEnd(parent = None)
    dlg.ShowModal()

if __name__ == '__main__':
    main() 
