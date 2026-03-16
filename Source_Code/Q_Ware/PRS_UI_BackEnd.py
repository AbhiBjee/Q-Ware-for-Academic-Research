# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated for Q-WARE (version June 20 2020)
## https://www.healthsmarttechnologies.com//
## Created by Abhinaba Bhattacharjee
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################


###########################################################################
## import all modules necessary for source codes ## 
###########################################################################

import wx, time, serial, string, threading, random
import multiprocessing as mp
#import wx.xrc
#from QwareOpen import QOpenDialog
import wx.grid as gridlib

from QwarePaths import Q_DataBase 

from time import localtime,strftime
import serial.tools.list_ports

import os, shutil, sys, ctypes, win32api
import glob, csv, errno, psutil
import ctypes.wintypes
import concurrent.futures as cf

from subprocess import *



from ConnectBar import DevConBar
from CalibrationBar import DevCalibBar

#import pyqtgraph.multiprocess as mp
#import multiprocessing as mp
import QSTMGraphicalAnalysisQ2 as qstmGAQ2
import QSTMGraphicalAnalysisQ1 as qstmGAQ1

from Q2GUItestOOP3 import Q2_Visual_GUI
from Q1GUItestOOP3 import Q1_Visual_GUI 
#import QSTMGraphicalAnalysis as qstmGA
from QGraphOpen2 import GraphMonitor, Q1Graph, Q2Graph
from QMultiVisualization import Ui_MainWindow
from QRetrieveModule import RetrieveDlgFrontEnd
#from time import localtime,strftime
#import string, time, wx
#import serial.tools.list_ports
from PyQt4 import QtGui, QtCore
#from PyQt4.QtGui import * 
#from PyQt4.QtCore import * 
import pyqtgraph.console
from pyqtgraph.dockarea import *
from pyqtgraph import ptime as t
import numpy as np
import pyqtgraph as pg

from PRS_UI_FrontEnd import PRS_MainWindowFrontEnd

###########################################################################
## Functions Searching ExistingPatients for patient display ##   
###########################################################################

def ExistingPatientDetails(path):
    PatientNames=os.walk(path).next()[1]
    ExistingPatientIds = []
    for names in PatientNames:
        patientPath = path+"\\"+names
        patIDs = os.walk(patientPath).next()[1]
        ExistingPatientIds.append(patIDs)
    return [PatientNames,ExistingPatientIds]


###########################################################################
## GVI (Graphical Visualization Interface) Functions for Treatment Button
## to Start Treatment Mode  ## 
###########################################################################


def resultFile():
    dlg = wx.MessageDialog(None, "Do You want to generate Report?",'Save Result',wx.YES_NO | wx.ICON_QUESTION)
    msgResult = dlg.ShowModal()
    if (msgResult == wx.ID_YES):
        print("Report Generated")
    else:
        print("Thank You")


###########################################################################
## Device Calibration and Device Connection Bar Functions for
## multiprocessing with the Backend UI ##
###########################################################################

def DevConn():
      ex = wx.App(False)
      ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
      DevConBar(None)
      ex.MainLoop()

def DevCalib():
      ex = wx.App(False)
      ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
      DevCalibBar(None, title = "Device Calibration Status", pos = (400,250))  
      ex.MainLoop()


###########################################################################
## Class for Backend Functions of PRS_MainWindow
###########################################################################


class PRS_MainWindowBackend ( PRS_MainWindowFrontEnd ):

       # class QSTM(wx.Frame):

    def __init__(self, *args, **kw):
        super(PRS_MainWindowBackend , self).__init__(*args, **kw)
        
        self.BackEndInit()
           
    #def __init__(self, *args, **kw):
        #super(QSTM, self).__init__(*args, **kw)

    def BackEndInit(self):

        ##-----------Device Registration and Serial Connection Variable Inititalization---------

        self.comData=[]; self.comPortUSB=[]; self.devTypes = []; self.devSrNo = []; self.Connflg=0; self.LastConnflg=0;
        self.serialComObj = []; self.cbIDObj=[]; self.ConnCounter = 0; self.TreatFlg = 0; self.LastTreatFlg = 0;
        self.Q1SbSnCnt = 0; self.Q2SbSnCnt = 0; self.SbSnArr = [];

        ##----------------Save Button Flag------------------------------------------------------

        self.SaveFlag = 0        

        ##----------------Timer Functions Linkage-----------------------

        self.Bind(wx.EVT_TIMER, self.OnWatchNewConn, self.ConnectTimer)#  Check New Serial Connections
        self.ConnectTimer.Start(2000)

        self.DevStateCheckTimer = wx.Timer(self, 4)
        self.Bind(wx.EVT_TIMER, self.TabSwitch2Method, self.DevStateCheckTimer)

        ##----------- Report Panel Widget Items Manipulate---------------

        self.ReportPanel.saveBtn.Bind(wx.EVT_BUTTON, self.saveReportFile)
        self.ReportPanel.OpenRprtBtn.Bind(wx.EVT_BUTTON, self.openReportFile)
        self.ReportPanel.GrphBtn.Bind(wx.EVT_BUTTON, self.showTreatmentGraph)
        #saveReportFile openReportFile showTreatmentGraph

        self.reportPnlButtonEnact()      
        self.ReportPanel.Q_ReportBook.Destroy()

        ##-----------Patient Display Panel Widget Items Manipulate---------------

        self.PatntDisplayPnl.TreatmentBtn.Bind(wx.EVT_BUTTON, self.startTreatment)
        self.PatntDisplayPnl.TreatmentBtn.Disable()

        self.DefaultPatientDetails = ["N/A","N/A","N/A","N/A","N/A","N/A","N/A"]
        self.setCurrentPatientLabel(self.DefaultPatientDetails)

        ##-----------Patient Entry Panel Widget Items Manipulate---------------

        self.PatntEntryPnl.cbRetrievePatient.Bind(wx.EVT_CHECKBOX, self.RetrievePatient)
        self.PatntEntryPnl.cbNewPatient.Bind(wx.EVT_CHECKBOX, self.OnNewPatientEntry)
        self.PatntEntryPnl.cbExistingPatient.Bind(wx.EVT_CHECKBOX, self.OnExistingPatntFunction)

        self.db = Q_DataBase()

        ##----------System Info Panel Widget Items Manipulate------------------------

        #self.ResetConnectedDeviceLabels()

        self.deviceStatusPnl.connDevTxtLbl.SetLabel (str(len(self.comPortUSB)))

        self.deviceStatusPnl.sysModeLbl.SetLabel("Idle Mode")


        self.deviceStatusPnl.cb_Prt1.Disable()
        self.deviceStatusPnl.cb_Prt1.Bind(wx.EVT_CHECKBOX, self.ChkBxPrt1State)
        self.deviceStatusPnl.PrtXX1Lbl.SetForegroundColour( wx.Colour(130, 130, 130 ))
        self.deviceStatusPnl.DevSerLbl1.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.cb_Prt2.Disable()
        self.deviceStatusPnl.cb_Prt2.Bind(wx.EVT_CHECKBOX, self.ChkBxPrt2State)
        self.deviceStatusPnl.PrtXX2Lbl.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.DevSerLbl2.SetForegroundColour( wx.Colour(130, 130, 130 ))

        self.deviceStatusPnl.cb_Prt3.Disable()
        self.deviceStatusPnl.cb_Prt3.Bind(wx.EVT_CHECKBOX, self.ChkBxPrt3State)
        self.deviceStatusPnl.PrtXX3Lbl.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.DevSerLbl3.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.cb_Prt4.Disable()
        self.deviceStatusPnl.cb_Prt4.Bind(wx.EVT_CHECKBOX, self.ChkBxPrt4State)
        self.deviceStatusPnl.PrtXX4Lbl.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.DevSerLbl4.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.connDevCbList = [self.deviceStatusPnl.cb_Prt1, self.deviceStatusPnl.cb_Prt2, self.deviceStatusPnl.cb_Prt3, self.deviceStatusPnl.cb_Prt4]
        self.connDevPrtLblList = [self.deviceStatusPnl.PrtXX1Lbl, self.deviceStatusPnl.PrtXX2Lbl, self.deviceStatusPnl.PrtXX3Lbl, self.deviceStatusPnl.PrtXX4Lbl]
        self.connDevSerLblList = [ self.deviceStatusPnl.DevSerLbl1,  self.deviceStatusPnl.DevSerLbl2,  self.deviceStatusPnl.DevSerLbl3,  self.deviceStatusPnl.DevSerLbl4]

        self.deviceStatusPnl.Ptr1StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr1StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.Ptr2StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr2StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.Ptr3StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr3StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.Ptr4StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr4StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.sysInfoPrtList = [self.deviceStatusPnl.Ptr1StateTxt, self.deviceStatusPnl.Ptr2StateTxt, self.deviceStatusPnl.Ptr3StateTxt, self.deviceStatusPnl.Ptr4StateTxt]
        self.sysInfoPrtStatusList = [self.deviceStatusPnl.Ptr1StateLbl, self.deviceStatusPnl.Ptr2StateLbl, self.deviceStatusPnl.Ptr3StateLbl, self.deviceStatusPnl.Ptr4StateLbl]
    


    def setCurrentPatientLabel(self, EnrolDetails):

        self.PatntDisplayPnl.PatntNameLbl.SetLabel(EnrolDetails[0])
        self.PatntDisplayPnl.PatntSurnameLbl.SetLabel(EnrolDetails[1])
        self.PatntDisplayPnl.PatntEnrlIDLbl.SetLabel(EnrolDetails[2])
        self.PatntDisplayPnl.PatntEnrlDateLbl.SetLabel(EnrolDetails[3])
        self.PatntDisplayPnl.PatntDobLbl.SetLabel(EnrolDetails[4])
        self.PatntDisplayPnl.PatntAgeLbl.SetLabel(EnrolDetails[5])
        self.PatntDisplayPnl.PatntSexLbl.SetLabel(EnrolDetails[6])

###########################################################################
## Functions for Retrieving Past Treatments and
## Displaying them to the Patient Report Panel
###########################################################################


    def RetrievePatient(self,evt):

        sender = evt.GetEventObject()
        self.RetrvCBval = sender.GetValue()

        if self.RetrvCBval == True:

            self.PatntEntryPnl.cbExistingPatient.Disable() 
            self.PatntEntryPnl.cbNewPatient.Disable()
            RetrvDlg = RetrieveDlgBackend(parent = self)
            #self.RetrvDlg = RetrieveDlgFrontEnd(parent = self)
            RetrvDlg.ShowModal()

            if RetrvDlg.PatntTreatFolder == None:
                pass
            else:
                self.Patient_Details = RetrvDlg.PatntDetails
                self.TreatType = RetrvDlg.TreatType
                self.TreatSession = RetrvDlg.PatntTreatFolder
                self.OutputPath = RetrvDlg.PatntFolderPath+"\\Output Data"
                self.ResultPath = RetrvDlg.PatntFolderPath+"\\Result Data"
                self.ReportPath = RetrvDlg.PatntFolderPath+"\\Patient Report"                
                self.setCurrentPatientLabel(self.Patient_Details)
                self.OpenRetrivedChart()
                #5RetrvDlg.Destroy()
                
            del RetrvDlg         

            
        elif self.RetrvCBval == False:
            self.PatntEntryPnl.cbExistingPatient.Enable() 
            self.PatntEntryPnl.cbNewPatient.Enable()
            self.setCurrentPatientLabel(self.DefaultPatientDetails)
            self.SaveFlag = 0
            self.TreatFlg = 0; self.LastTreatFlg = 0;
            self.Q1SbSnCnt = 0; self.Q2SbSnCnt = 0; self.SbSnArr = [];
            self.reportPnlButtonEnact() 
            try:
                self.ReportPanel.Q_ReportBook.Destroy()                
            except AttributeError:
                pass
            print("Retrieve Checkbox Unchecked")
        self.Refresh()
        self.Layout()


    def OpenRetrivedChart(self):

        if self.TreatType.startswith("Single"):
            print("Open Single Chart")
            resultFiles = [n for n in os.listdir(os.path.join(self.ResultPath,self.TreatSession))]
            path = self.ResultPath+"\\"+self.TreatSession+"\\"+resultFiles[0]
            if resultFiles[0].startswith("_Q1"):
                dtype = "Q1"                
            elif resultFiles[0].startswith("_Q2"):
                dtype = "Q2"               
            self.OneReportDisplayOpen( path, dtype)
                       
                
        elif self.TreatType.startswith("Multi"):
            print("Open Multi Chart")
            resultFiles = [n for n in os.listdir(os.path.join(self.ResultPath,self.TreatSession))]
            Q1path = self.ResultPath+"\\"+self.TreatSession+"\\"+resultFiles[1]
            Q2path = self.ResultPath+"\\"+self.TreatSession+"\\"+resultFiles[2]
            Q1Q2path = self.ResultPath+"\\"+self.TreatSession+"\\"+resultFiles[0]
            self.ReportQ1Q2DisplayOpen(Q1path, Q2path, Q1Q2path)
        self.OpenRetrievedReport()
        self.OpenRetrievedGraph()
        self.Refresh()
        self.Layout()

    def OpenRetrievedReport(self):
        self.ReportPanel.OpenRprtBtn.Enable()
        self.patntReportPath = os.path.join(self.ReportPath, self.TreatSession)

    def OpenRetrievedGraph(self):
        self.ReportPanel.GrphBtn.Enable()
        self.patntOutputPath = os.path.join(self.OutputPath, self.TreatSession)
        
            
            

        
        

###########################################################################
## Functions for New Patient Enrollment, Patient Entry
## and Display in Patient Entry Panel
###########################################################################


    def OnNewPatientEntry(self,evt):
        sender = evt.GetEventObject()
        self.NewEntryCBval = sender.GetValue()
        
        if self.NewEntryCBval == True:
            dlg = GetNewEnrollData(parent = self.PatntEntryPnl)
            dlg.ShowModal()
            if dlg.result_name or dlg.result_surname:
                self.F2name = dlg.result_name
                self.L2name = dlg.result_surname
                self.FullName = dlg.result_name+"_"+dlg.result_surname
                self.dob = dlg.result_dob
                self.age = dlg.PatntAge
                self.gender=dlg.gender
                self.enrollDate = dlg.Today_Date
                self.EnrollId = dlg.EnrollId
                self.PatientDetails = [self.F2name,self.L2name,self.EnrollId, self.enrollDate, self.dob, self.age, self.gender]
                self.db.formNewPatientFolder( self.db.Q_PatientsListPath, self.db.Q_PatientsFolderPath, self.PatientDetails)
                self.PatientDetails.append(self.db.PatientQName)
                self.PatientDetails.append(self.db.PatientPathFile)
                self.setCurrentPatientLabel(self.PatientDetails)
                

            self.PatntEntryPnl.cbExistingPatient.Disable() 
            self.PatntEntryPnl.cbRetrievePatient.Disable()           
            

        elif self.NewEntryCBval == False:
            self.PatntEntryPnl.cbExistingPatient.Enable() 
            self.PatntEntryPnl.cbRetrievePatient.Enable()
            self.setCurrentPatientLabel(self.DefaultPatientDetails)
            self.SaveFlag = 0
            self.TreatFlg = 0; self.LastTreatFlg = 0;
            self.Q1SbSnCnt = 0; self.Q2SbSnCnt = 0; self.SbSnArr = [];
            self.reportPnlButtonEnact() 
            
            try:
                self.ReportPanel.Q_ReportBook.Destroy()                
            except AttributeError:
                pass
            print("New Enrollment Unchecked")
        self.Refresh()
        self.Layout()
            
###########################################################################
## Functions for Existing Patient Enrollment, Patient Entry
## and Display in Patient Entry Panel
###########################################################################
    def OnExistingPatntFunction(self, evt):
        sender = evt.GetEventObject()
        self.ExistingEntryCBval = sender.GetValue()
        if self.ExistingEntryCBval == True:
            self.setupSearchBar()
            self.PatntEntryPnl.cbNewPatient.Disable() 
            self.PatntEntryPnl.cbRetrievePatient.Disable()
            

        elif self.ExistingEntryCBval == False:
            self.DestroySearchUI()
            self.PatntEntryPnl.cbNewPatient.Enable() 
            self.PatntEntryPnl.cbRetrievePatient.Enable()
            self.SaveFlag = 0
            self.TreatFlg = 0; self.LastTreatFlg = 0;
            self.Q1SbSnCnt = 0; self.Q2SbSnCnt = 0; self.SbSnArr = [];
            self.reportPnlButtonEnact()
            self.setCurrentPatientLabel(self.DefaultPatientDetails)
            try:
                self.ReportPanel.Q_ReportBook.Destroy()                
            except AttributeError:
                pass
        self.Refresh()
        self.Layout()
        

    def setupSearchList(self):
        self.SearchList = wx.ListCtrl(self.PatntEntryPnl.searchBox, size=(330,110), pos = (5,35), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        #self.SearchList.SetBackground(wx.TRANSPARENT)
        self.SearchList.InsertColumn(0, 'Index', width = 40)
        self.SearchList.InsertColumn(1, 'Patient Full Name', width = 220)
        self.SearchList.InsertColumn(2, 'DOB', width=100)    
        

    
    def setupSearchBar(self):
        self.PatientSearchBar = wx.SearchCtrl(self.PatntEntryPnl.searchBox, id=1, value="", size=(330,25), pos=(5, 5), style = wx.TE_PROCESS_ENTER)
        self.PatientSearchBar.ShowCancelButton(True)
        self.PatientSearchBar.SetSearchMenuBitmap
        self.PatientSearchBar.Bind(wx.EVT_TEXT_ENTER, self.OnPatientSearch, self.PatientSearchBar )

    def DestroySearchUI(self):
        try:
            self.SearchList.Destroy()
        except AttributeError :
            print("No Patient Searched")
        self.PatientSearchBar.Destroy()


    def OnPatientSearch(self, evt):
        self.ListPatientNames, self.ListQPatient = self.ExistingPatientDetails(self.db.Q_PatientsFolderPath)
        #print(self.ListPatientDetails[][1])
        self.SearchedString = evt.GetString()
        print(self.SearchedString)
        self.SearchedStringList = []
        self.PatientIndxList = []

        self.searchedPatient_menu = wx.Menu()

        for item in self.ListPatientNames:
            if str(item).lower().startswith(str(self.SearchedString).lower()):
                self.SearchedStringList.append(item)
                self.PatientIndxList.append(self.ListPatientNames.index(item))
        
        print (self.SearchedStringList)

        #self.setupSearchList()

        try:
            self.SearchList.DeleteAllItems()
        except AttributeError:
            self.setupSearchList()
            

        self.SearchList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClickPatientName)

        for i in range(0,len(self.SearchedStringList)):
            self.index = 10*i
            #self.nameitem = wx.MenuItem(self.searchedPatient_menu,self.index , text = self.PatientNameList[0][i],kind = wx.ITEM_NORMAL)
            self.IdMenu = wx.Menu()
            for j in range(0,len(self.ListQPatient [self.PatientIndxList[i]])):
                self.indx = self.index+(j+1)
                self.patientText = self.ListQPatient [self.PatientIndxList[i]][j].split("_")
                DOBtxt = "DOB : " + str(self.patientText[4])
                FullName = str(self.patientText[0])+ " " + str(self.patientText[1])
                self.Iditem = wx.MenuItem(self.IdMenu,self.indx , text = DOBtxt, kind = wx.ITEM_NORMAL)

                self.SearchList.InsertStringItem(j, str(self.PatientIndxList[i]))
                self.SearchList.SetStringItem(j, 1, str(FullName))
                self.SearchList.SetStringItem(j, 2, str(self.patientText[4]))
                
                self.IdMenu.AppendItem(self.Iditem)
            self.IdMenu.AppendSeparator()
            self.searchedPatient_menu.AppendMenu(self.index, self.SearchedStringList[i], self.IdMenu)
            #self.searchedPatient_menu.AppendItem(self.nameitem) 		
        self.searchedPatient_menu.AppendSeparator()

        self.PatientSearchBar.SetMenu(self.searchedPatient_menu)

        self.searchedPatient_menu.Bind(wx.EVT_MENU, self.searchMenuHandler)
        


    def AllExistingPatientDetails(self,listPath):
        AllPatientDetails = []
        AllPatientNames = []

        with open(listPath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for rows in readCSV:
                if rows[0].startswith("FirstName"):
                    continue
                line= rows
                name = line[7]
                AllPatientDetails.append(line)
                AllPatientNames.append(name)

        return AllPatientDetails,AllPatientNames
    
    def ExistingPatientDetails(self, path):
        PatientNames=os.walk(path).next()[1]
        ExistingPatientIds = []
        for names in PatientNames:
            patientPath = path+"\\"+names
            patIDs = os.walk(patientPath).next()[1]
            ExistingPatientIds.append(patIDs)
        return [PatientNames,ExistingPatientIds]


    def DoubleClickPatientName(self, evt):
        print("Patient Double Clicked")
        print("Patient Selected from List")
        ListItemValue = evt.GetItem().GetText()        
        self.SelectedPatients = self.ListQPatient[(int)(ListItemValue)]
        self.QPatient= self.SelectedPatients[0]
        print("Selected Patient ID :", self.QPatient)
        self.UploadSelectedPatientInfo(self.QPatient)

    def searchMenuHandler(self, event):
        print("Patient Selected from Search Menu")
        evtObj = event.GetEventObject()
        self.MenuId=event.GetId()
        self.menuhandler(self)

    def UploadSelectedPatientInfo(self,QPatnt):
        AllDetails, Qpatients = self.AllExistingPatientDetails(self.db.QPatntListCsvPath)
        for item in range (0,len(Qpatients)):
            if str(QPatnt).startswith(str(Qpatients[item])):
                QPatientDetails = AllDetails[item]
                #print(QPatientDetails)
            else:
                continue
        self.PatientDetails = QPatientDetails
        #print(self.PatientDetails)
        self.setCurrentPatientLabel(self.PatientDetails)
        self.Refresh()
        self.Layout()    
        


###########################################################################
## Functions for Device Registration, Serial Device Connectivity Checking
## and Display in Device Selection Panel
###########################################################################

    def OnWatchNewConn(self, evt):

         

        if self.ConnectTimer.IsRunning():
            self.SerialCommDevCheck()

            

            if len(self.comPortUSB)>0 and (self.Connflg == 1 or self.Connflg == 3 ) :

                print("ConnectFlag Value" + str(self.Connflg) )

                self.deviceStatusPnl.connDevTxtLbl.SetLabel (str(len(self.comPortUSB)))
                
                for item in range(0, len(self.comPortUSB)):
                    #pass
                    self.connDevCbList[item].Enable() #self.connDevSerLblList
                    self.connDevCbList[item].SetId((int)(self.availableUSBserial[item]))                    
                    
                    self.connDevPrtLblList[item].SetLabel(self.comPortUSB[item])
                    self.connDevSerLblList[item].SetLabel("Dev-"+self.devTypes[item]+" | "+ self.availableUSBserial[item])

                    self.sysInfoPrtList[item].SetLabel("Dev-"+self.devTypes[item])
                    self.sysInfoPrtStatusList[item].SetLabel("Connected")
                    
                    self.connDevPrtLblList[item].SetForegroundColour( wx.Colour(0, 0, 0 ))
                    self.connDevSerLblList[item].SetForegroundColour( wx.Colour(0, 0, 0 ))

                    self.sysInfoPrtList[item].SetForegroundColour( wx.Colour(0, 0, 0 ))
                    self.sysInfoPrtStatusList[item].SetForegroundColour( wx.Colour(0, 0, 0 ))

##            elif len(self.comPortUSB)>0 and len(self.comlist)==len(self.comPortUSB): 
            elif self.ConnCounter % 40000 == 0:
                self.Refresh()
                self.Layout()
                
            self.ConnCounter = self.ConnCounter + 2000                

            #self.LastConnflg = self.Connflg
        else:
            pass

    def ResetConnectedDeviceLabels(self):

        self.deviceStatusPnl.connDevTxtLbl.SetLabel (str(len(self.comPortUSB)))
        self.ConnCounter = 0

        if len(self.serialComObj)>0:
            for conn in self.serialComObj:
                try:
                    conn.flush()
                    conn.close()
                except serial.SerialException:
                    print("Lost Connection ")

        self.serialComObj=[]
        self.cbIDObj=[]
        self.PatntDisplayPnl.TreatmentBtn.Disable()
                

        self.deviceStatusPnl.cb_Prt1.SetId(wx.ID_ANY)
        self.deviceStatusPnl.cb_Prt1.SetValue(False)
        self.deviceStatusPnl.cb_Prt1.Disable()
        

        self.deviceStatusPnl.PrtXX1Lbl.SetLabel("COM-XX")
        self.deviceStatusPnl.PrtXX1Lbl.SetForegroundColour( wx.Colour(130, 130, 130 ))
        self.deviceStatusPnl.DevSerLbl1.SetLabel("No Device")
        self.deviceStatusPnl.DevSerLbl1.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.cb_Prt2.SetId(wx.ID_ANY)
        self.deviceStatusPnl.cb_Prt2.SetValue(False)
        self.deviceStatusPnl.cb_Prt2.Disable()
        self.deviceStatusPnl.PrtXX2Lbl.SetLabel("COM-XX")
        self.deviceStatusPnl.PrtXX2Lbl.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.DevSerLbl2.SetLabel("No Device")
        self.deviceStatusPnl.DevSerLbl2.SetForegroundColour( wx.Colour(130, 130, 130 ))

        self.deviceStatusPnl.cb_Prt3.SetId(wx.ID_ANY)
        self.deviceStatusPnl.cb_Prt3.SetValue(False)
        self.deviceStatusPnl.cb_Prt3.Disable()
        self.deviceStatusPnl.PrtXX3Lbl.SetLabel("COM-XX")
        self.deviceStatusPnl.PrtXX3Lbl.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.DevSerLbl3.SetLabel("No Device")
        self.deviceStatusPnl.DevSerLbl3.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.cb_Prt4.SetId(wx.ID_ANY)
        self.deviceStatusPnl.cb_Prt4.SetValue(False)
        self.deviceStatusPnl.cb_Prt4.Disable()
        self.deviceStatusPnl.PrtXX4Lbl.SetLabel("COM-XX")
        self.deviceStatusPnl.PrtXX4Lbl.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.DevSerLbl4.SetLabel("No Device")
        self.deviceStatusPnl.DevSerLbl4.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.connDevCbList = [self.deviceStatusPnl.cb_Prt1, self.deviceStatusPnl.cb_Prt2, self.deviceStatusPnl.cb_Prt3, self.deviceStatusPnl.cb_Prt4]
        self.connDevPrtLblList = [self.deviceStatusPnl.PrtXX1Lbl, self.deviceStatusPnl.PrtXX2Lbl, self.deviceStatusPnl.PrtXX3Lbl, self.deviceStatusPnl.PrtXX4Lbl]
        self.connDevSerLblList = [ self.deviceStatusPnl.DevSerLbl1,  self.deviceStatusPnl.DevSerLbl2,  self.deviceStatusPnl.DevSerLbl3,  self.deviceStatusPnl.DevSerLbl4]

        self.deviceStatusPnl.Ptr1StateTxt.SetLabel("PORT-1")
        self.deviceStatusPnl.Ptr1StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr1StateLbl.SetLabel("Status")
        self.deviceStatusPnl.Ptr1StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.Ptr2StateTxt.SetLabel("PORT-2")
        self.deviceStatusPnl.Ptr2StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr2StateLbl.SetLabel("Status")
        self.deviceStatusPnl.Ptr2StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.Ptr3StateTxt.SetLabel("PORT-3")
        self.deviceStatusPnl.Ptr3StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr3StateLbl.SetLabel("Status")
        self.deviceStatusPnl.Ptr3StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))

        self.deviceStatusPnl.Ptr4StateTxt.SetLabel("PORT-4")
        self.deviceStatusPnl.Ptr4StateTxt.SetForegroundColour( wx.Colour(130, 130, 130  ))
        self.deviceStatusPnl.Ptr4StateLbl.SetLabel("Status")
        self.deviceStatusPnl.Ptr4StateLbl.SetForegroundColour( wx.Colour(130, 130, 130  ))        

        self.sysInfoPrtList = [self.deviceStatusPnl.Ptr1StateTxt, self.deviceStatusPnl.Ptr2StateTxt, self.deviceStatusPnl.Ptr3StateTxt, self.deviceStatusPnl.Ptr4StateTxt]
        self.sysInfoPrtStatusList = [self.deviceStatusPnl.Ptr1StateLbl, self.deviceStatusPnl.Ptr2StateLbl, self.deviceStatusPnl.Ptr3StateLbl, self.deviceStatusPnl.Ptr4StateLbl]
        
        


    def readDeviceInfo (self, serialCommObj):
            
        while True:
            while (serialCommObj.inWaiting()==0):
                pass
            dataStream = serialCommObj.readline()
            dataString = str(dataStream)
            
            #time.sleep(0.2)
            if dataString.startswith("QSTM DAQ") :
                serialCommObj.write(str("DevType"))
            elif dataString.startswith("Dev"):
                devStr, Typ = dataString.split("-")
                Type,nullStr = Typ.split("\r\n")
                print("This QSTM device is: " + str(Type))
                serialCommObj.write(str("QSrNo"))
            elif dataString.startswith("Serial "):
                devStr, Sr = dataString.split(": ")
                SrNo,nullStr = Sr.split("\r\n")
                print("This Q-Dev Ser# is: " + str(SrNo))
                print("Return")
                return Type, SrNo
##            elif dataString.startswith("NACK"):
##                #print ("Ready Serial")
##                print("Port Ready")    
##                
##                return "R","S"
            print (dataString)
                    
            
    def readDeviceTypeSerial (self, serialCommObj2):
        flg=0
                
        while True:
            while (serialCommObj2.inWaiting()==0):
                pass
            dataStream = serialCommObj2.readline()
            dataString = str(dataStream)
            
            #time.sleep(0.2)
            if dataString.startswith("QSTM DAQ") and flg == 0:
                flg = 1           
                serialCommObj2.write(str("DevType"))
            if dataString.startswith("NACK") and flg == 0:
                flg = 1           
                serialCommObj2.write(str("DevType"))
            elif dataString.startswith("Dev"):
                devStr, Typ = dataString.split("-")
                Type,nullStr = Typ.split("\r\n")
                print("This QSTM device is: " + str(Type))
                serialCommObj2.write(str("QSrNo"))
            elif dataString.startswith("Serial "):
                devStr, Sr = dataString.split(": ")
                SrNo,nullStr = Sr.split("\r\n")
                print("This Q-Dev Ser# is: " + str(SrNo))
                print("Return")
                return Type, SrNo
                #serialCommObj.write(str("QSrNo"))

    def ReadPortDetails(self, portName):        

        try:             
            tryConnect= serial.Serial(port=str(portName),baudrate = 115200)
            tryConnect.baudrate = 115200
            print("Available Port " +str(portName))
            devType, devSrNo = self.readDeviceTypeSerial(tryConnect)
            if devType is "R":
                print ("Port already Read")
                #devType, devSrNo = self.readDeviceTypeSerial(tryConnect)
                tryConnect.flush()
                tryConnect.close()
                return
            else:
                tryConnect.flush()
                tryConnect.close()            
                Str,Prt = str(portName).split("M")
                #self.availablePorts.append(Prt)
                self.devTypes.append(str(devType))
                self.devSrNo.append(str(devSrNo))

        except serial.SerialException:
            print("Blocked Port " +str(portName))



    ###----------------------------Comm Ports select and connect----------------

    def ReadNewPorts(self):
        for element in self.availableUSB:    

            self.ReadPortDetails(element.device)
            self.comPortUSB.append(str(element.device))
            
    def SerialCommDevCheck(self):
        #global Local_time,storeCSVpath,processCSVpath,resultCSVpath,rstTimeCSVpath,ofile, mainCSVwriter,serialComm, noDeviceFlag

        self.availableUSB = []; self.availableUSBPorts = []; self.availableUSBserial = []

        ConnPorts = len(self.comPortUSB)        
        
        #self.comlist = sorted(serial.tools.list_ports.comports())

        for  item in (sorted(serial.tools.list_ports.comports())):
            if str(item.hwid).startswith("USB"):
                self.availableUSBPorts.append(str(item.device))
                self.availableUSBserial.append(str(item.serial_number))
                self.availableUSB.append(item)
            else:
                continue
            
            

        if ConnPorts <= 0 and len(self.availableUSB)>0:

            self.Connflg=1
            print("detectedComList > Comports=0 ")
            self.ResetConnectedDeviceLabels()
            self.p1 = mp.Process(target=DevConn)     
            self.p1.start()
            #os.startfile("ConnectBar.py")
            #Popen('python ConnectBar.pyc')

##            thread1 = threading.Thread(target=self.RunConnBar)
##            thread2 = threading.Thread(target=self.ReadNewPorts)            
##            thread1.start()
##            thread2.start()
            #self.RunConnBar()
            #wx.CallLater(self.RunConnBar)
            self.ReadNewPorts()
            self.p1.join()
            
            

                           
                
        elif  ConnPorts > 0 and len(self.availableUSB)> ConnPorts :
            #pass

            self.Connflg=1
            print("detectedComList > Comports>0 ")

            for ind in range (0,len(self.availableUSB)) :
                print(str(self.availableUSB[ind].device))
                if str(self.comPortUSB[ind]) is str(self.availableUSB[ind].device):
                    print("Same Port")
                    continue
                else:
                   
                    self.comData=[]; self.comPortUSB=[]; self.devTypes = []; self.devSrNo = []

                    print("Com Port reset")

                    self.SerialCommDevCheck()
                    return

        elif  ConnPorts > 0 and len(self.availableUSB)< ConnPorts :
            #pass

            self.comData=[]; self.comPortUSB=[]; self.devTypes = []; self.devSrNo = []

            print("Com Port reset")
            self.ResetConnectedDeviceLabels()
            self.Connflg=3
            #time.sleep(1)
            self.SerialCommDevCheck()
            return
        
        else:
            self.Connflg=2
            return                    
        
        

        #print("\n")                
        #print("Connected COM ports: " + str(connected))
        #print("Comm Data for connected COM ports: " + str(self.comData))
        print(" Detected USB COM ports: " + str(len(self.availableUSBPorts)))
        #print(self.comData)
        print(" Connected USB COM ports: " + str(self.comPortUSB))
        print(" Connected USB Device Types: " + str(self.devTypes))
        print(" Connected USB Device Serial Nos: " + str(self.devSrNo))
        print(" Connected USB Software Serial Nos: " + str(self.availableUSBserial))


    def startConBar(self):
        
        with cf.ThreadPoolExecutor() as eX:# context manager for multithreading using Python Module CONCURRENT.FUTURES                
                eX.submit(self.RunConnBar)
                eX.submit(self.ReadNewPorts())

    def RunConnBar(self):
        self.devConnDlg = DevConBar(None, title = "Device Connection Started", pos = (400,250))            
        self.devConnDlg.ShowModal()
        #DevConBar(None)
        #pass

        
##        if len(self.comPortUSB)<1:
##            print("No Device Found")
##            print("Close Current window")
##            print("UNPLUG and PLUG-IN QSTM Q2 device and try again")
        
                   
            
#######################################################################################
##
## Functions for Device Selection for Treatment Mode
## CheckBox Functions only
##
#######################################################################################

    def ChkBxPrt1State(self, cbEvt):
        sender = cbEvt.GetEventObject()
        cbID = sender.GetId()
        cbVal = sender.GetValue()        

        if cbVal is True and ((int)(cbID) == (int)(self.availableUSBserial[0])):

            self.SerConnPrt1= serial.Serial(port=str(self.comPortUSB[0]),baudrate = 115200)
            self.serialComObj.append(self.SerConnPrt1)
            self.cbIDObj.append(cbID) #self.cbIDObj.pop(self.cbIDObj.index(cbID))
            self.sysInfoPrtStatusList[0].SetLabel("Selected")
            self.PatntDisplayPnl.TreatmentBtn.Enable()
            
            #pass        
        elif cbVal is False:
            self.serialComObj.pop(self.serialComObj.index(self.SerConnPrt1))
            self.cbIDObj.pop(self.cbIDObj.index(cbID))
            self.SerConnPrt1.flush()
            self.SerConnPrt1.close()
            self.sysInfoPrtStatusList[0].SetLabel("Connected")
            if len(self.serialComObj)<=0:
                self.PatntDisplayPnl.TreatmentBtn.Disable()

    def ChkBxPrt2State(self, cbEvt):
        sender = cbEvt.GetEventObject()
        cbID = sender.GetId()
        cbVal = sender.GetValue()        

        if cbVal is True and ((int)(cbID) == (int)(self.availableUSBserial[1])):

            self.SerConnPrt2= serial.Serial(port=str(self.comPortUSB[1]),baudrate = 115200)
            self.serialComObj.append(self.SerConnPrt2)
            self.cbIDObj.append(cbID) 
            self.sysInfoPrtStatusList[1].SetLabel("Selected")
            self.PatntDisplayPnl.TreatmentBtn.Enable()
            
            #pass        
        elif cbVal is False:
            self.serialComObj.pop(self.serialComObj.index(self.SerConnPrt2))
            self.cbIDObj.pop(self.cbIDObj.index(cbID))
            self.SerConnPrt2.flush()
            self.SerConnPrt2.close()
            self.sysInfoPrtStatusList[1].SetLabel("Connected")
            if len(self.serialComObj)<=0:
                self.PatntDisplayPnl.TreatmentBtn.Disable()

    def ChkBxPrt3State(self, cbEvt):
        #pass
        sender = cbEvt.GetEventObject()
        cbID = sender.GetId()
        cbVal = sender.GetValue()        

        if cbVal is True and ((int)(cbID) == (int)(self.availableUSBserial[2])):

            self.SerConnPrt3= serial.Serial(port=str(self.comPortUSB[2]),baudrate = 115200)
            self.cbIDObj.append(cbID) 
            self.serialComObj.append(self.SerConnPrt3)            
            self.sysInfoPrtStatusList[2].SetLabel("Selected")
            self.PatntDisplayPnl.TreatmentBtn.Enable()
            
            #pass        
        elif cbVal is False:
            self.serialComObj.pop(self.serialComObj.index(self.SerConnPrt3))
            self.cbIDObj.pop(self.cbIDObj.index(cbID))
            self.SerConnPrt3.flush()
            self.SerConnPrt3.close()
            self.sysInfoPrtStatusList[2].SetLabel("Connected")
            if len(self.serialComObj)<=0:
                self.PatntDisplayPnl.TreatmentBtn.Disable()

    def ChkBxPrt4State(self, cbEvt):
        #pass
        sender = cbEvt.GetEventObject()
        cbID = sender.GetId()
        cbVal = sender.GetValue()        

        if cbVal is True and ((int)(cbID) == (int)(self.availableUSBserial[3])):

            self.SerConnPrt4= serial.Serial(port=str(self.comPortUSB[3]),baudrate = 115200)
            self.serialComObj.append(self.SerConnPrt4)
            self.cbIDObj.append(cbID) 
            self.sysInfoPrtStatusList[3].SetLabel("Selected")
            self.PatntDisplayPnl.TreatmentBtn.Enable()
            
            #pass        
        elif cbVal is False:
            self.serialComObj.pop(self.serialComObj.index(self.SerConnPrt4))
            self.cbIDObj.pop(self.cbIDObj.index(cbID))
            self.SerConnPrt4.flush()
            self.SerConnPrt4.close()
            self.sysInfoPrtStatusList[3].SetLabel("Connected")
            if len(self.serialComObj)<=0:
                self.PatntDisplayPnl.TreatmentBtn.Disable()


###########################################################################
##
## Functions for Treatment Button to Start Treatment Mode
## Q1 Device and Q2 Device only
##
###########################################################################


    def startTreatment(self,evt):# (when the "START TREATMENT" button is clicked)
        print("Treatment Button Clicked")
        self.db.clearTempFolder(self.db.tempStorePath)
        self.p2 = mp.Process(target=DevCalib)
        try:
            self.ReportPanel.Q_ReportBook.Destroy()
            self.Refresh()
            self.Layout()
        except AttributeError:
            pass
        if self.PatntEntryPnl.cbNewPatient.GetValue() == True or self.PatntEntryPnl.cbExistingPatient.GetValue()== True:
            self.Patient_Details = self.PatientDetails
            self.ConnectTimer.Stop()

                 
            self.p2.start()
            
            #Popen('python CalibrationBar.pyc')
            self.SaveFlag = 1
            self.reportPnlButtonEnact()
            self.ReportPanel.OpenRprtBtn.Disable()
            self.ReportPanel.GrphBtn.Disable()
            #self.devCalbiBar = DevCalibBar(None, title = "Device Calibration Started", pos = (400,250))
            #self.devCalbiBar.Show()
            #self.devCalbiBar.progressTimer.Start(100)
            self.RunTreatmentMode()
            self.p2.join()
            
        else:
            dlg = wx.MessageDialog(None, "Do You want to Start Treatment without Patient Info? \n Results won't be saved.",'Treament Mode Question',wx.YES_NO | wx.ICON_QUESTION)
            msgResult = dlg.ShowModal()
            if (msgResult == wx.ID_YES):
                self.Patient_Details = self.DefaultPatientDetails
                self.ConnectTimer.Stop()

                #p2 = mp.Process(target=DevCalibBar)     
                self.p2.start()
                
                #Popen('python CalibrationBar.pyc')
                #self.devCalbiBar = DevCalibBar(None, title = "Device Calibration Started", pos = (400,250))
                #self.devCalbiBar.Show()
                #self.devCalbiBar.progressTimer.Start(100)
                self.RunTreatmentMode()
                self.p2.join()
                
            else:
                print("Thank You")
            
            

    def RunTreatmentMode(self):
        print(self.cbIDObj);
        print(self.serialComObj);
        self.deviceStatusPnl.sysModeLbl.SetLabel("Treatment Mode")
            
        self.PatntDisplayPnl.TreatmentBtn.Disable()
        

        if (len(self.serialComObj)<=0):
            print("No Device Selected")

        elif (len(self.serialComObj)==1):
            print("One Device Selected")

            
            sysIndex=(self.availableUSBserial).index(str(self.cbIDObj[0]))
            print(sysIndex)
            print(self.devTypes[sysIndex])
            
            self.connDevCbList[sysIndex].Disable()
            self.sysInfoPrtStatusList[sysIndex].SetLabel("Running Treatment")
            if self.devTypes[sysIndex].startswith("Q1"):            
                self.Q1visRun(sysIndex, self.devTypes[sysIndex], self.serialComObj[0])
            elif self.devTypes[sysIndex].startswith("Q2"):
                self.Q2visRun(sysIndex, self.devTypes[sysIndex], self.serialComObj[0])
                
        elif (len(self.serialComObj)==2):
            print("Two Device Selected")
            self.Indx1=(self.availableUSBserial).index(str(self.cbIDObj[0]))
            self.Indx2=(self.availableUSBserial).index(str(self.cbIDObj[1]))
            self.Dtype1 = self.devTypes[self.Indx1]
            self.Dtype2 = self.devTypes[self.Indx2]
            self.SerCom1 = self.serialComObj[0]
            self.SerCom2 = self.serialComObj[1]

            self.sysInfoPrtStatusList[self.Indx1].SetLabel("Running Treatment")
            self.sysInfoPrtStatusList[self.Indx2].SetLabel("Running Treatment")

            self.connDevCbList[self.Indx1].Disable()
            self.connDevCbList[self.Indx2].Disable()
            
            self.Q1Q2visRun()

    ###############################################################################################################################
    ###-------------------------------Functions for Q1 and Q2 Multivisualization------------------------------------------------###
    ###############################################################################################################################


    def Q1Q2visRun(self) :# (when the both Q1 and Q2 devices are selected for treatment session)

        app = QtGui.QApplication([])

        self.MainWindow = QtGui.QMainWindow()
        self.Ui = Ui_MainWindow()
        self.Ui.setupUi(self.MainWindow)
        self.visQ2 = Q2_Visual_GUI()
        self.visQ1 = Q1_Visual_GUI()
        #self.Q1Q2ptr = 0

        if (self.Dtype1.startswith("Q1") and self.Dtype2.startswith("Q2")):
            self.setDevUI( self.visQ1, self.Indx1, self.Dtype1)
            self.setDevUI( self.visQ2, self.Indx2, self.Dtype2)

            with cf.ThreadPoolExecutor() as ex1:# context manager for multithreading using Python Module CONCURRENT.FUTURES                
                threadQ1Init = ex1.submit(self.visQ1.SystemInitQ1, self.SerCom1)
                threadQ2Init = ex1.submit(self.visQ2.SystemInitQ2, self.SerCom2)

        elif (self.Dtype1.startswith("Q2") and self.Dtype2.startswith("Q1")):
            self.setDevUI( self.visQ2, self.Indx1, self.Dtype1)
            self.setDevUI( self.visQ1, self.Indx2, self.Dtype2)

            with cf.ThreadPoolExecutor() as ex1:# context manager for multithreading using Python Module CONCURRENT.FUTURES                
                threadQ1Init = ex1.submit(self.visQ1.SystemInitQ1, self.SerCom2)
                threadQ2Init = ex1.submit(self.visQ2.SystemInitQ2, self.SerCom1)        

        self.MainWindow.show()
        
        with cf.ThreadPoolExecutor() as ex2:# context manager for multithreading using Python Module CONCURRENT.FUTURES           
                
            threadQ2started = ex2.submit(self.visQ2.Q2timer.start(1))    
            threadQ1started = ex2.submit(self.visQ1.Q1timer.start(1))
            threadDevCheckstarted = ex2.submit(self.DevStateCheckTimer.Start(2))
            self.TreatStartTime = time.time()

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
            self.visQ2.Q2timer.stop()
            self.visQ1.Q1timer.stop()
            self.DevStateCheckTimer.Stop()
            print ("GVI exit")
            self.SerCom1.flush()
            self.SerCom1.close()
            self.SerCom2.flush()
            self.SerCom2.close()
            if self.visQ1.mainCSVFile.closed is False:
                self.visQ1.mainCSVFile.close()
            elif self.visQ2.mainCSVFile.closed is False:
                self.visQ2.mainCSVFile.close()
            self.deviceStatusPnl.sysModeLbl.SetLabel("Idle Mode")
            self.sysInfoPrtStatusList[self.Indx1].SetLabel("Ended Treatment")
            self.sysInfoPrtStatusList[self.Indx2].SetLabel("Ended Treatment")
            print(self.SbSnArr)
            #resultFile()            
            print ("Q2 startArray ")
            print (self.visQ2.StartTimeArr)
            print ("Q2 stopArray ")
            print (self.visQ2.StopTimeArr)
            self.resultTwoDevGenerate(self.Dtype1, self.Dtype2)
            #self.PatntDisplayPnl.TreatmentBtn.Enable()
            self.connDevCbList[self.Indx1].Enable()
            self.connDevCbList[self.Indx2].Enable()
            self.connDevCbList[self.Indx1].SetValue(False)
            self.connDevCbList[self.Indx2].SetValue(False)
            self.cbIDObj=[]; self.serialComObj=[]
            self.ConnectTimer.Start(2000)            


    def TabSwitch2Method(self, evt):# (function to toggle in between the Q1 and Q2 tab on the Graphical Visualization Interface)
        if (self.visQ2.DevState == 0) and (self.visQ1.DevState == -1 or self.visQ1.DevState == 1) :
            self.TreatFlg = 2
            #print ("Treatment Flag %d" % self.TreatFlg)
            if self.Dtype1.startswith("Q2"):
                self.Ui.tabWidget.setCurrentIndex(self.Indx1)
            elif self.Dtype2.startswith("Q2"):
                self.Ui.tabWidget.setCurrentIndex(self.Indx2)
        elif (self.visQ2.DevState == 1 or self.visQ2.DevState == -1) and (self.visQ1.DevState == 0) :
            self.TreatFlg = 1
            #print ("Treatment Flag %d" % self.TreatFlg)
            if self.Dtype1.startswith("Q1"):
                self.Ui.tabWidget.setCurrentIndex(self.Indx1)
            elif self.Dtype2.startswith("Q1"):
                self.Ui.tabWidget.setCurrentIndex(self.Indx2)

        elif (self.visQ2.DevState==1 and self.visQ1.DevState==1) or (self.visQ2.DevState == -1 and self.visQ1.DevState==1) or (self.visQ2.DevState==1 and self.visQ1.DevState == -1):
            self.TreatFlg = 0
            self.TreatStopTime = time.time() -  self.TreatStartTime
            

        if (self.LastTreatFlg != self.TreatFlg) and (self.TreatFlg > 0):
        #if (self.visQ2.DevState == 1 and self.visQ1.DevState == 1) :
            if self.TreatFlg == 1 :
                self.Q1SbSnCnt += 1
                self.SbSnArr.append("Q%d-SubSession:%d" %(self.TreatFlg,self.Q1SbSnCnt))
            elif self.TreatFlg == 2 :
                self.Q2SbSnCnt += 1
                self.SbSnArr.append("Q%d-SubSession:%d" %(self.TreatFlg,self.Q2SbSnCnt))
            self.Now = time.time()- self.TreatStartTime 
            print(" Session Time %0.2f, Dev-type Q%d, Q1 time %0.2f , Q2 time %0.2f" %(self.Now, self.TreatFlg, self.visQ1.rstStopTime, self.visQ2.rstStopTime))
        self.LastTreatFlg = self.TreatFlg
        
            

    def setDevUI(self, obj, indx, dtype):

        if indx == 0 :
            obj.setupUI(self.Ui.tab_1)
            self.Ui.tabWidget.setTabText(self.Ui.tabWidget.indexOf(self.Ui.tab_1), "Dev-"+dtype)
            self.Ui.tabWidget.setCurrentIndex(self.Ui.tabWidget.indexOf(self.Ui.tab_1))

        elif indx == 1 :
            obj.setupUI(self.Ui.tab_2)
            self.Ui.tabWidget.setTabText(self.Ui.tabWidget.indexOf(self.Ui.tab_2), "Dev-"+dtype)
            self.Ui.tabWidget.setCurrentIndex(self.Ui.tabWidget.indexOf(self.Ui.tab_2))

        elif indx == 2 :
            obj.setupUI(self.Ui.tab_3)
            self.Ui.tabWidget.setTabText(self.Ui.tabWidget.indexOf(self.Ui.tab_3), "Dev-"+dtype)
            self.Ui.tabWidget.setCurrentIndex(self.Ui.tabWidget.indexOf(self.Ui.tab_3))

        elif indx == 3 :
            obj.setupUI(self.Ui.tab_4)
            self.Ui.tabWidget.setTabText(self.Ui.tabWidget.indexOf(self.Ui.tab_4), "Dev-"+dtype)
            self.Ui.tabWidget.setCurrentIndex(self.Ui.tabWidget.indexOf(self.Ui.tab_4))


    ###############################################################################################################################
    ###-------------------------------Functions for indivisdual Q1 and Q2 Visualization-----------------------------------------###
    ###############################################################################################################################

    def Q2visRun(self, Indx, Dtype, serConn):        
        app = QtGui.QApplication([])
        MainWindow = QtGui.QMainWindow()
        Ui = Ui_MainWindow()
        Ui.setupUi(MainWindow)
        #ui.tab_1.setTabtext("Q2 Tab")
        visQ2 = Q2_Visual_GUI()
        if Indx == 0 :
            visQ2.setupUI(Ui.tab_1)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_1), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_1))
            print("Current Tab index :" + str(Ui.tabWidget.indexOf(Ui.tab_1)))
            
        elif Indx == 1 :
            visQ2.setupUI(Ui.tab_2)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_2), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_2))
           

        elif Indx == 2 :
            visQ2.setupUI(Ui.tab_3)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_3), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_3))
            

        elif Indx == 3 :
            visQ2.setupUI(Ui.tab_4)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_4), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_4))
            

        visQ2.SystemInitQ2(serConn)
        visQ2.Q2timer.start(1)

        MainWindow.show()     
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
            visQ2.Q2timer.stop()
            print ("GVI exit")
            serConn.flush()
            serConn.close()
            if visQ2.mainCSVFile.closed is False:
                visQ2.mainCSVFile.close()   
            self.deviceStatusPnl.sysModeLbl.SetLabel("Idle Mode")
            self.sysInfoPrtStatusList[Indx].SetLabel("Ended Treatment")            
            #resultFile()
            self.resultOneDevGenerate(Dtype, visQ2.resultCSVpath, visQ2.storeCSVpath)
            #self.PatntDisplayPnl.TreatmentBtn.Enable()
            self.connDevCbList[Indx].Enable()
            self.connDevCbList[Indx].SetValue(False)
            self.cbIDObj=[]; self.serialComObj=[]
            self.ConnectTimer.Start(2000)


    def Q1visRun(self, Indx, Dtype, serConn):        
        app = QtGui.QApplication([])
        MainWindow = QtGui.QMainWindow()
        Ui = Ui_MainWindow()
        Ui.setupUi(MainWindow)
        #ui.tab_1.setTabtext("Q1 Tab")
        visQ1 = Q1_Visual_GUI()
        if Indx == 0 :
            visQ1.setupUI(Ui.tab_1)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_1), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_1))
            
        elif Indx == 1 :
            visQ1.setupUI(Ui.tab_2)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_2), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_2))
            

        elif Indx == 2 :
            visQ1.setupUI(Ui.tab_3)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_3), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_3))
            

        elif Indx == 3 :
            visQ1.setupUI(Ui.tab_4)
            Ui.tabWidget.setTabText(Ui.tabWidget.indexOf(Ui.tab_4), "Dev-"+Dtype)
            Ui.tabWidget.setCurrentIndex(Ui.tabWidget.indexOf(Ui.tab_4))
            

        visQ1.SystemInitQ1(serConn)
        visQ1.Q1timer.start(1)

        MainWindow.show()        
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
            visQ1.Q1timer.stop()
            print ("GVI exit")
            serConn.flush()
            serConn.close()
            if visQ1.mainCSVFile.closed is False:
                visQ1.mainCSVFile.close()               
            self.deviceStatusPnl.sysModeLbl.SetLabel("Idle Mode")
            self.sysInfoPrtStatusList[Indx].SetLabel("Ended Treatment")
            #resultFile()
            self.resultOneDevGenerate(Dtype, visQ1.resultCSVpath, visQ1.storeCSVpath)
            #self.PatntDisplayPnl.TreatmentBtn.Enable()
            self.connDevCbList[Indx].Enable()
            self.connDevCbList[Indx].SetValue(False)
            self.cbIDObj=[]; self.serialComObj=[]
            self.ConnectTimer.Start(2000)


            
       
############################################################################################
##
## Functions for Report Generation and Report Display in the Report Panel
##
############################################################################################

    ###############################################################################################################################
    ###-----------------Functions for producing the Result Files and CSVs for a Single Device Treatment-------------------------###
    ###############################################################################################################################


    def resultOneDevGenerate(self, dtype, resultCSVpath, rawFilePath ):
        dlg = wx.MessageDialog(None, "Do You want to generate Report?",'Save Result',wx.YES_NO | wx.ICON_QUESTION)
        msgResult = dlg.ShowModal()
        if (msgResult == wx.ID_YES):
            csvFile, rstBegin, rstEnd, TimeCol = qstmGAQ1.csvReadFile(rawFilePath)
            del csvFile, rstBegin, rstEnd;   
                      
            if dtype.startswith("Q1"):               
                if len(TimeCol)> 10 :
                    report = qstmGAQ1.SessionGraphCalc(rawFilePath)
                    self.writeReport( report, resultCSVpath )
                    self.OneReportDisplayOpen(resultCSVpath, dtype)
                else:
                    self.SaveFlag = 0
                    self.reportPnlButtonEnact() 
                    msgDlg = wx.MessageDialog(None, "No Treatment Done. \nNo Result Generated",'Result',wx.OK | wx.ICON_QUESTION)
                    msgResult = msgDlg.ShowModal()
                
            elif dtype.startswith("Q2"):
                if len(TimeCol)> 10 :
                    report = qstmGAQ2.SessionGraphCalc(rawFilePath)
                    self.writeReport( report, resultCSVpath )
                    self.OneReportDisplayOpen(resultCSVpath, dtype)
                else:
                    self.SaveFlag = 0
                    self.reportPnlButtonEnact()
                    msgDlg = wx.MessageDialog(None, "No Treatment Done. \nNo Result Generated",'Result',wx.OK | wx.ICON_QUESTION)
                    msgResult = msgDlg.ShowModal()
                #report = qstmGAQ2.SessionGraphCalc(rawFilePath)

            print("Report Generated")                    
            
        else:
            self.SaveFlag = 0
            self.reportPnlButtonEnact()
            print("Thank You")
        

    def OneReportDisplayOpen(self, resultPath, devType):        
        #self.createReportBook()
        if devType.startswith("Q1"):
            self.createQ1Report()
            self.reportPageCreate( resultPath, self.ReportPanel.Q1_RprtPnl.QreportGrid, self.Patient_Details )
        elif devType.startswith("Q2"):
            self.createQ2Report()
            self.reportPageCreate( resultPath, self.ReportPanel.Q2_RprtPnl.QreportGrid, self.Patient_Details )
            

    def writeReport(self, report, resultCSVpath ):

        transposeReport = zip(*report)
        resultFile  = open(resultCSVpath, 'wb')
        resultWriter = csv.writer(resultFile, delimiter=',') 
        for rw in range(0,len(transposeReport)):
        
            resultWriter.writerow(transposeReport[rw])

        resultFile.close()

    ###############################################################################################################################
    ###-----------------------Functions for producing the Result Files and CSVs for a Combined Treatment-------------------------###
    ###############################################################################################################################        

    def resultTwoDevGenerate(self, dtype1, dtype2):     
        dlg = wx.MessageDialog(None, "Do You want to generate Report?",'Save Result',wx.YES_NO | wx.ICON_QUESTION)
        msgResult = dlg.ShowModal()
        if (msgResult == wx.ID_YES):
            print("Report Generated")
            
           
            if (dtype1.startswith("Q1") and dtype2.startswith("Q2")) or (dtype1.startswith("Q2") and dtype2.startswith("Q1")):
                reportTotal=[]
                paramRow = ["Sessions","FXavg","FYavg","FZavg","FRavg","MaxPeak","AvgPeak",
                            "BurstNumber","StrokeNumber","StrokeFrequency","Full Session Time",
                            "pAvg","rAvg","yAvg","Contact/Active Time"]
                
                noParams = ["N/A",0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                fakeParams = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",]
                reportTotal.append(paramRow)

                csvFile, rstBegin, rstEnd, TimeColQ1 = qstmGAQ1.csvReadFile(self.visQ1.storeCSVpath)                
                csvFile, rstBegin, rstEnd, TimeColQ2 = qstmGAQ1.csvReadFile(self.visQ2.storeCSVpath)
                del csvFile, rstBegin, rstEnd;

                if len(TimeColQ1)> 10 :
                    reportQ1 = qstmGAQ1.SessionGraphCalc(self.visQ1.storeCSVpath)
                    reportQ1[len(reportQ1)-1][0] = "Q1 Total Session"
                else:
                    reportQ1 = []
                    reportQ1.append(paramRow)
                    reportQ1.append(noParams)                   

                if len(TimeColQ2)> 10 :
                    reportQ2 = qstmGAQ2.SessionGraphCalc(self.visQ2.storeCSVpath)
                    reportQ2[len(reportQ2)-1][0] = "Q2 Total Session"
                else:
                    reportQ2 = []
                    reportQ2.append(paramRow)
                    reportQ2.append(noParams)

                if len(TimeColQ1)< 10 and len(TimeColQ2)< 10:
                    self.SaveFlag = 0
                    self.reportPnlButtonEnact()

                self.writeReport( reportQ1, self.visQ1.resultCSVpath )
                self.writeReport( reportQ2, self.visQ2.resultCSVpath )

                print(reportQ2)
                
                ReportTuple = list(zip(reportQ1[len(reportQ1)-1],reportQ2[len(reportQ2)-1]))
                ReportTuple.pop(0)

                reportTotal.append(self.generateComboReport(ReportTuple))
                reportTotal.append(reportQ1[len(reportQ1)-1])
                reportTotal.append(reportQ2[len(reportQ2)-1])
                reportTotal.append(fakeParams)
                reportTotal.append(fakeParams)

                for item in self.SbSnArr:
                    colIdx = (int)(item[len(item)-1])
                    if item.startswith("Q1"):##                   
                        reportQ1[colIdx][0] = item                        
                        reportTotal.append(reportQ1[colIdx])
                    elif item.startswith("Q2"):                       
                        reportQ2[colIdx][0] = item                        
                        reportTotal.append(reportQ2[colIdx])
                
                
                            
                
                totRprtPath=self.visQ1.tempStorePath+"\\"+"_Q1Q2ResultChart_"+self.visQ1.Local_time+".csv"
                #print("Report Last Line")
                #print (ReportTuple)
                #print (reportTotal)
                
                
                self.writeReport( reportTotal, totRprtPath )
                self.ReportQ1Q2DisplayOpen( self.visQ1.resultCSVpath, self.visQ2.resultCSVpath, totRprtPath)                      
            
        else:
            self.SaveFlag = 0
            self.reportPnlButtonEnact()
            print("Thank You")

    def generateComboReport(self,tupleList):# Nested function to generate combined report
        ReportArr=[]
        for i in range(0,len(tupleList)):
            if i<=3 or i==5 or i==8 or (i>9 and i<=12):
                tupleList[i] = np.array(tupleList[i])
                ReportArr.append(np.mean(tupleList[i]))
            if i == 4:
                ReportArr.append(max(tupleList[i]))
            if (i >=6 and i<=7) or i==9 or i==13:
                tupleList[i] = np.array(tupleList[i])
                ReportArr.append(np.sum(tupleList[i]))
        ReportArr=[round(item,2)for item in ReportArr]
        ReportArr.insert(0,"Total Combined Session")
        return ReportArr    

    def ReportQ1Q2DisplayOpen(self, resultPathQ1, resultPathQ2, resultPathQ1Q2):
        self.createQ1Q2ReportBook()
        self.reportPageCreate( resultPathQ1, self.ReportPanel.Q1_RprtPnl.QreportGrid, self.Patient_Details )
        self.reportPageCreate( resultPathQ2, self.ReportPanel.Q2_RprtPnl.QreportGrid, self.Patient_Details )
        self.reportPageCreate( resultPathQ1Q2, self.ReportPanel.TotRprtPnl.QreportGrid, self.Patient_Details )


    ###############################################################################################################################
    ###------------------------Functions to create the Report NoteBook on the  Report Panel-------------------------------------###
    ###############################################################################################################################

    def createQ1Q2ReportBook(self): 

        RprtBoxWidth, RprtBoxHeight = self.ReportPanel.ReportBox.GetClientSize()
        self.ReportPanel.Q_ReportBook = wx.Notebook( self.ReportPanel.ReportBox, wx.ID_ANY, wx.Point(0,0), wx.Size(RprtBoxWidth, RprtBoxHeight))

        self.ReportPanel.TotRprtPnl = reportGridPanel( self.ReportPanel.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.ReportPanel.Q_ReportBook.AddPage( self.ReportPanel.TotRprtPnl, u"Total Report", False )        
        self.ReportPanel.Q1_RprtPnl = reportGridPanel( self.ReportPanel.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.ReportPanel.Q_ReportBook.AddPage( self.ReportPanel.Q1_RprtPnl, u"Q1 Report", False )
        self.ReportPanel.Q2_RprtPnl = reportGridPanel( self.ReportPanel.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.ReportPanel.Q_ReportBook.AddPage( self.ReportPanel.Q2_RprtPnl, u"Q2 Report", False )
        

        self.ReportPanel.ReportBoxSz.Add( self.ReportPanel.Q_ReportBook, 1, wx.EXPAND |wx.ALL, 0 )

        #self.ReportPanel.Q_ReportBook.SetSelection(self.ReportPanel.TotRprtPnl)

    def createQ1Report(self):

        RprtBoxWidth, RprtBoxHeight = self.ReportPanel.ReportBox.GetClientSize()
        self.ReportPanel.Q_ReportBook = wx.Notebook( self.ReportPanel.ReportBox, wx.ID_ANY, wx.Point(0,0), wx.Size(RprtBoxWidth, RprtBoxHeight))
        self.ReportPanel.Q1_RprtPnl = reportGridPanel( self.ReportPanel.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.ReportPanel.Q_ReportBook.AddPage( self.ReportPanel.Q1_RprtPnl, u"Q1 Report", False )        

        self.ReportPanel.ReportBoxSz.Add( self.ReportPanel.Q_ReportBook, 1, wx.EXPAND |wx.ALL, 0 )

    def createQ2Report(self):
        
        RprtBoxWidth, RprtBoxHeight = self.ReportPanel.ReportBox.GetClientSize()
        self.ReportPanel.Q_ReportBook = wx.Notebook( self.ReportPanel.ReportBox, wx.ID_ANY, wx.Point(0,0), wx.Size(RprtBoxWidth, RprtBoxHeight))
        self.ReportPanel.Q2_RprtPnl = reportGridPanel( self.ReportPanel.Q_ReportBook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.ReportPanel.Q_ReportBook.AddPage( self.ReportPanel.Q2_RprtPnl, u"Q2 Report", False )

        self.ReportPanel.ReportBoxSz.Add( self.ReportPanel.Q_ReportBook, 1, wx.EXPAND |wx.ALL, 0 )

    ###############################################################################################################################
    ###------------------------Function to create the Report Grid on the Corresponding Report TAB-------------------------------###
    ###############################################################################################################################        

        
    def reportPageCreate(self, resultCSV, Qgrid, EnrolDetails):

        #try:
        print(resultCSV)
        #Qgrid = gridlib.Grid(Panel,1,wx.DefaultPosition, wx.DefaultSize)
        #Qgrid.CreateGrid(28, 100)
        Column=["Patient Info"," "," "," ","Session Info","Avg X Force(N)","Avg Y Force(N)","Avg Z Force(N)","Avg Res Force(N)",
                "Max Peak Force(N)","Avg Peak Force(N)", "Burst Number","Stroke Number","Stroke Frequency(Hz)","Full Session Time(sec)",
               "Avg Pitch(Angle)","Avg Roll(Angle)","Avg Yaw(Angle)","Contact Time (sec)"," "," ","Remarks"," "," "," "," "," ", " ",]
              
        #Name = self.FullName.split('_')
        
        # set the text color and the background color as attribute of the cell

        httr = wx.grid.GridCellAttr()# Cell attribute for Heading
        httr.SetTextColour(wx.Colour(0,0,0))
        #attr.SetBackgroundColour(wx.Colour(237,249,202))
        httr.SetBackgroundColour(wx.Colour(235,235,235))
        httr.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.BOLD))
        
        cttr = wx.grid.GridCellAttr()# Cell Attribute for cells 
        cttr.SetTextColour(wx.Colour(100,0,0))
        #attr.SetBackgroundColour(wx.Colour(237,249,202))
        cttr.SetBackgroundColour(wx.Colour(225,250,255))
        cttr.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.BOLD))

        
        self.ReportName = str(EnrolDetails[0])+" "+str(EnrolDetails[1])
        Qgrid.SetCellValue(0,0,"Patient Name : ")
        Qgrid.SetReadOnly(0,0, True)
        Qgrid.SetCellValue(0,2,self.ReportName)
        Qgrid.SetReadOnly(0,2, True)
        Qgrid.SetCellSize(0, 0, 1, 2)# Merge Multiple cells in the grid
        Qgrid.SetCellAlignment(0, 0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        Qgrid.SetCellSize(0, 2, 1, 3)
        Qgrid.SetCellAlignment(0, 2, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        Qgrid.SetCellSize(21, 1, 7, 5)# Remark Cells
        Qgrid.SetCellAlignment(21, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        
        
        Qgrid.SetCellValue(1,0,"Patient Enroll ID : ")
        Qgrid.SetReadOnly(1,0, True)
        Qgrid.SetCellValue(1,2,EnrolDetails[2])
        Qgrid.SetReadOnly(1,2, True)
        Qgrid.SetCellSize(1, 0, 1, 2)
        Qgrid.SetCellAlignment(1, 0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        Qgrid.SetCellSize(1, 2, 1, 4)
        Qgrid.SetCellAlignment(1, 2, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        Qgrid.SetCellValue(2,3,"Age : ")
        Qgrid.SetReadOnly(2,3, True)
        Qgrid.SetCellValue(2,4,EnrolDetails[5])
        Qgrid.SetReadOnly(2,4, True)
        Qgrid.SetCellValue(2,0,"Birth Date : ")
        Qgrid.SetReadOnly(2,0, True)
        Qgrid.SetCellValue(2,1,EnrolDetails[4])
        Qgrid.SetReadOnly(2,1, True)
        
        
        for item in range(0,len(Column)):
            #rowNum = row + 1
            Qgrid.SetRowLabelValue(item, Column[item])
            Qgrid.SetRowLabelSize(140)
        with open(resultCSV) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            rowCnt = 4
            for row in readCSV:
                for val in range (1,len(row)):
                    Qgrid.SetCellValue(rowCnt,val,row[val])
                    if rowCnt == 4:
                        Qgrid.SetAttr(rowCnt,val, httr)
                        
                    if (rowCnt >=7 and rowCnt <=10) or (rowCnt >=12 and rowCnt <=15) or rowCnt ==18 :
                        Qgrid.SetAttr(rowCnt,val, cttr)
                        
                    Qgrid.SetReadOnly(rowCnt,val, True)
                    #Qgrid.SetCellSize(110)
                rowCnt=rowCnt+1
                
        Qgrid.AutoSize()
                        
##        except AttributeError:
##            print("No Report Generated")



############################################################################################
##
## Functions for Report Saving in Corresponding Patient Folder
## Functions for Save Button, Open Report Button Enable or Disable
##
############################################################################################

    def reportPnlButtonEnact(self): #saveReportFile openReportFile showTreatmentGraph
        if self.SaveFlag == 0:
            self.ReportPanel.saveBtn.Disable()
            self.ReportPanel.OpenRprtBtn.Disable()
            self.ReportPanel.GrphBtn.Disable()
            
        elif self.SaveFlag == 1:
            self.ReportPanel.saveBtn.Enable()
            self.ReportPanel.OpenRprtBtn.Enable()
            self.ReportPanel.GrphBtn.Enable()

    def generateReportFiles(self):
        self.TempCsvFiles = [filename for filename in os.listdir(self.db.tempStorePath) if filename.endswith(".csv")]
        for csvFile in self.TempCsvFiles:
            fileParts = csvFile.split("_")
            timePart = fileParts[2]+"_"+fileParts[3]
            #print(timePart)
            resultPath = self.db.tempStorePath+"\\"+csvFile
            if fileParts[1].startswith("Q1ResultChart"):
                reportPath = self.db.tempStorePath+"\\_Q1ReportChart"+"_"+timePart
                self.createReportFileCsv(reportPath, self.ReportPanel.Q1_RprtPnl.QreportGrid, resultPath)
                #self.TempCsvFiles.append(reportPath)
                #print("TempQ1ReportChart generated")
                
            elif fileParts[1].startswith("Q2ResultChart"):
                reportPath = self.db.tempStorePath+"\\_Q2ReportChart"+"_"+timePart
                self.createReportFileCsv(reportPath, self.ReportPanel.Q2_RprtPnl.QreportGrid, resultPath)
                #self.TempCsvFiles.append(reportPath)
                #print("TempQ2ReportChart generated")
                
            elif fileParts[1].startswith("Q1Q2ResultChart"): 
                reportPath = self.db.tempStorePath+"\\_Q1Q2ReportChart"+"_"+timePart
                self.createReportFileCsv(reportPath, self.ReportPanel.TotRprtPnl.QreportGrid, resultPath)
                #self.TempCsvFiles.append(reportPath)
                #print("TempQ1Q2ReportChart generated")
        self.TimePart, csvStr = timePart.split(".")
        #print ("Time Part ", timePart)
        del csvStr
                
            
        #csvFileParts = TempCsvFiles[0].split("_")
        

    def createReportFileCsv(self, ReportFilePath, QGrid, ResultFilePath):

        ReportRows = []
        
        for row in range(0,4):
            ReportCols = []
            for col in range(0,6):
                CellValue = QGrid.GetCellValue(row,col)
                ReportCols.append(CellValue)
            ReportRows.append(ReportCols)            

        with open(ResultFilePath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                ReportRows.append(row)

        ReportRows.append(" ")
        ReportRows.append(" ")

        for row in range(21,28):
            ReportCols = []
            for col in range(0,5):
                CellValue = QGrid.GetCellValue(row,col)
                ReportCols.append(CellValue)
            ReportRows.append(ReportCols)            

        ofile  = open(ReportFilePath, "wb")
        writer = csv.writer(ofile, delimiter=',')
        #RowLen = len(ReportRows)

        for rows in ReportRows:
            writer.writerow(rows)
        ofile.close()

    def makeTreatmentDirs(self, EnrlDetails):
        self.TreatmentFolder = EnrlDetails[0]+"_"+EnrlDetails[1]+"_Q-Treatment_"+self.TimePart        
        self.patientFolderPath = self.db.Q_PatientsFolderPath+"\\"+EnrlDetails[0]+"_"+EnrlDetails[1]+"\\"+EnrlDetails[7]
        #print(self.patientFolderPath)
        if os.path.exists(self.patientFolderPath):
            self.patntOutputPath =self.patientFolderPath+"\\Output Data"+"\\"+self.TreatmentFolder
            self.patntResultPath =self.patientFolderPath+"\\Result Data"+"\\"+self.TreatmentFolder
            self.patntReportPath =self.patientFolderPath+"\\Patient Report"+"\\"+self.TreatmentFolder

            os.makedirs(self.patntOutputPath)
            os.makedirs(self.patntResultPath)
            os.makedirs(self.patntReportPath)
        else:
            print("Patient Folder Not Found")

    def copyTemp2PatntFolder(self, EnrlDetails):
        name = EnrlDetails[0]+"-"+EnrlDetails[1]
        self.TempCsvFiles = [filename for filename in os.listdir(self.db.tempStorePath) if filename.endswith(".csv")]
        for csvFile in self.TempCsvFiles:
            fileParts = csvFile.split("_")
            timePart = fileParts[2]+"_"+fileParts[3]
            #print(timePart)
            tempFilePath = os.path.join(self.db.tempStorePath,csvFile)            

            if fileParts[1].startswith("Q1RawOutputChart") or fileParts[1].startswith("Q2RawOutputChart"):
                shutil.move(tempFilePath,self.patntOutputPath)                 

            elif fileParts[1].startswith("Q1ResultChart") or fileParts[1].startswith("Q2ResultChart") or fileParts[1].startswith("Q1Q2ResultChart"):                
                shutil.move(tempFilePath,self.patntResultPath)                

            elif fileParts[1].startswith("Q1ReportChart") or fileParts[1].startswith("Q2ReportChart") or fileParts[1].startswith("Q1Q2ReportChart"):
                shutil.move(tempFilePath,self.patntReportPath)         
        

    def saveReportFile(self, evt):
        print("Save Report Clicked")
        self.generateReportFiles()
        self.makeTreatmentDirs(self.Patient_Details)
        self.copyTemp2PatntFolder(self.Patient_Details)
        self.ReportPanel.saveBtn.Disable()
        self.ReportPanel.OpenRprtBtn.Enable()
        self.ReportPanel.GrphBtn.Enable()
        pass
    

    ###############################################################################################################################
    ###------------------------Function to SELECT and OPEN Multiple Reports on EXCEL CSV FORMAT---------------------------------###
    ###############################################################################################################################
    

    def openReportFile(self, evt):
        ReportFiles = [filename for filename in os.listdir(self.patntReportPath) if filename.endswith(".csv")]
        if len(ReportFiles)>=2:
            reprtDlg = openReportDialog(parent = self.ReportPanel)
            #reprtDlg = openReportDialog( self.ReportPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,250 ), wx.DEFAULT_DIALOG_STYLE )
            reprtDlg.InitUI(self.patntReportPath)
            reprtDlg.ShowModal()
        elif len(ReportFiles)< 2:
            filePath = os.path.join(self.patntReportPath,ReportFiles[0])
            os.startfile(filePath)


    ###############################################################################################################################
    ###------------------------Function to OPEN TREATMENT SESSION GRAPH after saving treatment data-----------------------------###
    ###############################################################################################################################     
       

    def showTreatmentGraph(self, evt):
        RawOutputFiles = os.listdir(self.patntOutputPath)
        if len(RawOutputFiles)>=2:
            
            Q1path = os.path.join(self.patntOutputPath,RawOutputFiles[0])
            Q2path = os.path.join(self.patntOutputPath,RawOutputFiles[1])

            app = QtGui.QApplication([])
            MainWindow = QtGui.QMainWindow()
            ui = GraphMonitor()
            ui.setupUi(MainWindow, Q1path, Q2path)
            MainWindow.show()
            if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()             
            
        elif len(RawOutputFiles)<2:
            if RawOutputFiles[0].startswith("_Q1Raw"):
                Q1path = os.path.join(self.patntOutputPath,RawOutputFiles[0])
                app = QtGui.QApplication([])
                Frame = QtGui.QFrame()
                gui = Q1Graph()
                gui.setupUI(Frame,Q1path)
                Frame.setWindowTitle('Q1 Treatment Session')
                Frame.show()
                if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                    QtGui.QApplication.instance().exec_()
                    
            elif RawOutputFiles[0].startswith("_Q2Raw"):
                Q2path = os.path.join(self.patntOutputPath,RawOutputFiles[0])
                app = QtGui.QApplication([])
                Frame = QtGui.QFrame()
                gui = Q2Graph()
                gui.setupUI(Frame,Q2path)
                Frame.setWindowTitle('Q2 Treatment Session')
                Frame.show()
                if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                    QtGui.QApplication.instance().exec_()
                    

                

###############################################################################################################################
###----------------------------------------------END OF PRS BACKEND CLASS---------------------------------------------------###
###############################################################################################################################


                

###########################################################################
##
## Class to Generate the UI for the Report GRID in  REPORT PANEL
##
###########################################################################
            
class reportGridPanel(wx.Panel):

    def __init__(self, *args, **kw):
        super(reportGridPanel, self).__init__(*args, **kw)
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        #self.Bind(wx.EVT_PAINT, self._Paint)

        self.boxFont = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        self.TextFont = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.LabelFont = wx.Font(11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)

        

        self._FormUI()

        self.Bind(wx.EVT_SIZE, self._Resize)

        self.Centre(wx.BOTH)
        self.Layout()

    def _FormUI(self):
        #pass
        QPnlVsizer = wx.BoxSizer( wx.VERTICAL )
		
        self.QreportGrid = gridlib.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        # Grid
        self.QreportGrid.CreateGrid( 28, 100 )
        self.QreportGrid.EnableEditing( True )
        self.QreportGrid.EnableGridLines( True )
        self.QreportGrid.EnableDragGridSize( False )
        self.QreportGrid.SetMargins( 0, 0 )
        
        # Columns
        self.QreportGrid.EnableDragColMove( False )
        self.QreportGrid.EnableDragColSize( True )
        self.QreportGrid.SetColLabelSize( 30 )
        self.QreportGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Rows
        self.QreportGrid.AutoSizeRows()
        self.QreportGrid.EnableDragRowSize( True )
        self.QreportGrid.SetRowLabelSize( 80 )
        self.QreportGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Label Appearance
        
        # Cell Defaults
        self.QreportGrid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        QPnlVsizer.Add( self.QreportGrid, 1, wx.ALL, 5 )
        
        
        self.SetSizer( QPnlVsizer )
        self.Layout()
        QPnlVsizer.Fit( self )

    def _Resize(self, size):
        #pass
        self.Refresh()               
        self.Layout()


####################################################################################
##
## Class to Generate the UI for the NEW PATIENT ENROLLMENT in  PATIENT ENTRY PANEL
## with Corresponding Class Functions
##
####################################################################################
    
        
        
class GetNewEnrollData(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "New Patient Enrollment", size= (650,270))
        self.panel = wx.Panel(self,wx.ID_ANY)
        Genders = ['Male', 'Female', 'Not Specified'] 

        self.lblname = wx.StaticText(self.panel, label="Patient First Name *", pos=(20,40))
        self.name = wx.TextCtrl(self.panel, value="", pos=(130,40), size=(480,-1))
        self.lblsur = wx.StaticText(self.panel, label="Patient Last Name *", pos=(20,80))
        self.surname = wx.TextCtrl(self.panel, value="", pos=(130,80), size=(480,-1))
        self.lblSex = wx.StaticText(self.panel, label="Patient Sex *", pos=(20,120))
        self.SexComboBox = wx.ComboBox(self.panel,pos=(130,120), size=(480,-1),choices = Genders)
        self.SexComboBox.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        #self.Sex = wx.TextCtrl(self.panel, value="", pos=(130,120), size=(480,-1))
        
        self.lbldob = wx.StaticText(self.panel, label="Patient Date of Birth *", pos=(20,160))
        self.PatntDob = wx.StaticText(self.panel, label="", pos=(300,160), size=(300,-1))
        self.datepick = wx.DatePickerCtrl(self.panel,-1, pos=(150,160),
                              style=wx.DP_DROPDOWN|wx.DP_SHOWCENTURY)
        self.datepick.Bind(wx.EVT_DATE_CHANGED, self.DatePickDoB)
        self.saveButton =wx.Button(self.panel, label="Save", pos=(110,200))
        self.closeButton =wx.Button(self.panel, label="Cancel", pos=(210,200))
        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Show()

    def OnCombo(self, evt):
        self.SexChoice = self.SexComboBox.GetValue()
        print(self.SexChoice)
        

    def DatePickDoB(self, event):
        '''Process data from picked date'''
        selected = self.datepick.GetValue()
        print(selected)
        month = selected.Month+1 # its returns an integer lesser than the month number displayed
                                 # So an increment by one is required
        day = selected.Day
        year = selected.Year
        date_str = "%02d/%02d/%4d" % (month, day, year)
        self.dateId ="%02d-%02d-%4d" % (month, day, year) 
        print(date_str)
        print(month)
        #self.PatntDob.SetLabel("Date selected = {}".format(date_str))

    def AgeCalc(self, DOB):
        
        self.Today_Date=strftime("%m-%d-%Y",localtime())
        self.thisMonth = int(str((self.Today_Date.split("-"))[0]))
        self.thisDay = int(str((self.Today_Date.split("-"))[1]))
        self.thisYear = int(str((self.Today_Date.split("-"))[2]))
        self.birthMonth = int(str((DOB.split("-"))[0]))
        self.bDay = int(str((DOB.split("-"))[1]))        
        self.birthYear = int(str((DOB.split("-"))[2]))
        age= self.thisYear-self.birthYear
##        try:
##            self.enrollDate = str(self.PatientId.split("_")[3])
##        except AttributeError:
##            print("Patient ID "+ str(self.PatientId))
        if self.thisMonth >=  self.birthMonth:
            self.age = str(age)
            newAge = str(age)
        else:
            self.age = str(age-1)
            newAge = str(age-1)

        return newAge
        
    def OnQuit(self, event):
        self.result_name = None
        self.result_surname = None
        self.result_ID = None
        self.result_dob = None
        self.Destroy()

    def getEnrollId(self):
        IdArr = [self.thisDay,self.bDay,self.thisMonth,self.birthMonth,self.thisYear,self.birthYear]
        #print(ErIdArr)
        
        random.shuffle(IdArr)# shuffle list elements using pythons's random module
        
        #FNindx = np.random.randint(len(self.result_name), size=1)
        #FNletter = self.result_name[FNindx[0]]
        #LNindx = np.random.randint(len(self.result_surname), size=1)
        #LNletter = self.result_surname[LNindx[0]]
        Id = str(self.result_name[0]).upper()+str(self.result_surname[0]).upper()+str(IdArr[0])+str(IdArr[1])+str(IdArr[2])+str(IdArr[3])+str(IdArr[4])+str(IdArr[5])
        return Id    

    def SaveConnString(self, event):
        self.result_name = self.name.GetValue()
        self.result_surname = self.surname.GetValue()
        self.gender = self.SexChoice
        
        try:
            self.result_dob = self.dateId
            self.PatntAge=self.AgeCalc(self.dateId)
            self.EnrollId = self.getEnrollId()
            print(self.EnrollId)
            
            self.Destroy()
        except AttributeError:
             self.PatntDob.SetLabel(" Select Date Of Birth")

####################################################################################
##
## Class to Generate the UI for OPEN REPORT CHARTS IN EXCEL in  PATIENT REPORT PANEL
## with Corresponding Class Functions
##
####################################################################################


class openReportDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Select Report Dialog", size= (250,250))
        #self.panel = wx.Panel(self,wx.ID_ANY)
        self.FormUI()
        self.openReprtBtn.Bind(wx.EVT_BUTTON, self.openExcelCharts)        
    

    def InitUI(self, reportPath):
        
        self.reportPath = reportPath
        self.reportFiles = [filename for filename in os.listdir(reportPath) if filename.endswith(".csv")]
        if len(self.reportFiles)>=3:
            print("No.of Report Files", len(self.reportFiles))            
        else:
            print("No. of Report Files less than 3")
            pass

    def openExcelCharts(self, evt):
        cbQ1Val = self.cbQ1Reprt.GetValue()
        cbQ2Val = self.cbQ2Reprt.GetValue()
        cbTotVal = self.cbTotReprt.GetValue()
        for fname in self.reportFiles:
            if cbQ1Val == True and fname.startswith("_Q1ReportChart"):
                filePath = os.path.join(self.reportPath,fname)
                os.startfile(filePath)
            elif cbQ2Val == True and fname.startswith("_Q2ReportChart"):
                filePath = os.path.join(self.reportPath,fname)
                os.startfile(filePath)
            elif cbTotVal == True and fname.startswith("_Q1Q2ReportChart"):
                filePath = os.path.join(self.reportPath,fname)
                os.startfile(filePath)
        self.Close()
                
       # pass
    
        

    def FormUI(self):

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
        vSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.diagLabel = wx.StaticText( self, wx.ID_ANY, u"Select Reports", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.diagLabel.Wrap( -1 )
        vSizer.Add( self.diagLabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        hSizerQ1 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        hSizerQ1.AddSpacer( ( 10, 0), 0, wx.ALL|wx.EXPAND, 5 )
        
        self.cbQ1Reprt = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        hSizerQ1.Add( self.cbQ1Reprt, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        hSizerQ1.AddSpacer( ( 10, 0), 0, wx.EXPAND, 5 )
        
        self.Q1RptLbl = wx.StaticText( self, wx.ID_ANY, u"Q1 Report Chart", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Q1RptLbl.Wrap( -1 )
        hSizerQ1.Add( self.Q1RptLbl, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        vSizer.Add( hSizerQ1, 1, wx.EXPAND, 5 )
        
        hSizerQ2 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        hSizerQ2.AddSpacer( ( 10, 0), 0, wx.ALL|wx.EXPAND, 5 )
        
        self.cbQ2Reprt = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        hSizerQ2.Add( self.cbQ2Reprt, 0, wx.ALL, 5 )
        
        
        hSizerQ2.AddSpacer( ( 10, 0), 0, wx.EXPAND, 5 )
        
        self.Q2RptLbl = wx.StaticText( self, wx.ID_ANY, u"Q2 Report Chart", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Q2RptLbl.Wrap( -1 )
        hSizerQ2.Add( self.Q2RptLbl, 0, wx.ALL, 5 )
        
        
        vSizer.Add( hSizerQ2, 1, wx.EXPAND, 5 )
        
        hSizerTot = wx.BoxSizer( wx.HORIZONTAL )
        
        
        hSizerTot.AddSpacer( ( 10, 0), 0, wx.ALL|wx.EXPAND, 5 )
        
        self.cbTotReprt = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        hSizerTot.Add( self.cbTotReprt, 0, wx.ALL, 5 )
        
        
        hSizerTot.AddSpacer( ( 10, 0), 0, wx.EXPAND, 5 )
        
        self.TotRptLbl = wx.StaticText( self, wx.ID_ANY, u"Total Report Chart", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.TotRptLbl.Wrap( -1 )
        hSizerTot.Add( self.TotRptLbl, 0, wx.ALL, 5 )
        
        
        vSizer.Add( hSizerTot, 1, wx.EXPAND, 5 )
        
        
        vSizer.AddSpacer( ( 0, 5), 0, wx.EXPAND, 5 )
        
        self.openReprtBtn = wx.Button( self, wx.ID_ANY, u"Open Report", wx.DefaultPosition, wx.DefaultSize, 0 )
        vSizer.Add( self.openReprtBtn, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        
        self.SetSizer( vSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )


####################################################################################
##
## Backend Class for TREATMENT RETRIEVAL which allows select the Patient Name and
## their correponding past treaments after DateTimeStamp Selection.
##
####################################################################################

class RetrieveDlgBackend(RetrieveDlgFrontEnd):

    def __init__(self, *args, **kw):
        super(RetrieveDlgBackend , self).__init__(*args, **kw)
        
        self.DlgBackEndInit()

    def DlgBackEndInit(self):

        ##------------------------------Patient Retrieval Instructions initialization ----------------------------------------------
        
        self.InstructionPnl.Rule1.SetLabel("Search Patient Name on the SEARCH BAR.\nThen Double Click on Patient Name on the List ")
        self.InstructionPnl.Rule1.SetForegroundColour( wx.Colour(165, 20, 20  ))

        self.db = Q_DataBase()

        ##------------------------------Patient Retrieval Information  initialization ----------------------------------------------

        self.SelectPnl.TxtPatnt.SetForegroundColour( wx.Colour(130, 130, 130 ))
        self.SelectPnl.TxtTreat.SetForegroundColour( wx.Colour(130, 130, 130 ))

        self.SelectPnl.LblPatnt.SetLabel("NAME : N/A ")
        self.SelectPnl.LblPatnt.SetForegroundColour( wx.Colour(130, 130, 130 ))

        self.SelectPnl.LblDOB.SetLabel("DOB : N/A ")
        self.SelectPnl.LblDOB.SetForegroundColour( wx.Colour(130, 130, 130 ))

        
        self.SelectPnl.LblTreatDate.SetForegroundColour( wx.Colour(130, 130, 130 ))        
        self.SelectPnl.LblTreatTime.SetForegroundColour( wx.Colour(130, 130, 130 ))

        ##------------------------------Patient Retrieval Treatment View Options Hide for Dialog initialization --------------------

        [self.SelectPnl.pnlRadioBox.ShowItem( i, show=False) for i, item in enumerate(self.SelectPnl.pnlRadioBoxChoices)]
        self.retrieveBtn.Disable()

        ##------------------------------Retrieve Dialog Event Control Binding Links-------------------------------------------------
        self.SelectPnl.SrchListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClickPatientName)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnPatientSearch, self.SelectPnl.searchBar)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #self.PatientSearchBar.Bind(wx.EVT_TEXT_ENTER, self.OnPatientSearch, self.PatientSearchBar )

        self.SelectPnl.pnlRadioBox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        self.retrieveBtn.Bind(wx.EVT_BUTTON, self.OnRetrieveButton)
        
        
        print("Events Linked")
        pass

    def OnClose(self,evt):

        self.PatntTreatFolder = None
        self.PatntFolderPath = None
        self.PatntDetails = None
        self.TreatType = None
        self.Destroy()
        
    

    def onRadioBox(self, evt):
        evtObj = evt.GetEventObject()
        radioStrng = evtObj.GetStringSelection()
        self.patntName = self.ListPatntDetails[(int)(self.PatntIndx)][0]+"_"+self.ListPatntDetails[(int)(self.PatntIndx)][1]
        treatRprtPath = (self.db.Q_PatientsFolderPath+"\\"+self.patntName+"\\"+
                         self.ListPatntDetails[(int)(self.PatntIndx)][7]+"\\"+"Patient Report")
        self.treatStampList = []
        for item in os.listdir(treatRprtPath):
            name, timeStamp = item.split("_Q-Treatment_")
            self.treatStampList.append(timeStamp)
        self.treatStampList.sort(key=lambda x: time.mktime(time.strptime(x,"%H-%M-%S_%m-%d-%Y")))
        #print(self.treatStampList)           
        self.SelectPnl.searchBar.Disable()
        del name

        try:
            self.SelectPnl.SrchListCtrl.DeleteAllItems()
            self.SelectPnl.SrchListCtrl.DeleteAllColumns()
            self.setupSelectTreatmentList()
        except AttributeError:
            self.setupSelectTreatmentList()


        if radioStrng.startswith("First"):
            treatPathFolder = self.patntName+"_Q-Treatment_"+self.treatStampList[0]
            timeStmp, dateStmp = self.treatStampList[0].split("_")
            if len(os.listdir(os.path.join(treatRprtPath,treatPathFolder)))>1:
                treatType = "MultiDevice-Treatment"
            else:
                 treatType = "SingleDevice-Treatment"

            self.SelectPnl.SrchListCtrl.InsertStringItem(0, "0")
            self.SelectPnl.SrchListCtrl.SetStringItem(0, 1, treatType)
            self.SelectPnl.SrchListCtrl.SetStringItem(0, 2, dateStmp)
            self.SelectPnl.SrchListCtrl.SetStringItem(0, 3, timeStmp)
            #self.SelectPnl.SrchListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClickTreatment)

                
        elif radioStrng.startswith("Last"):
            treatPathFolder = self.patntName+"_Q-Treatment_"+self.treatStampList[len(self.treatStampList)-1]
            timeStmp, dateStmp = self.treatStampList[len(self.treatStampList)-1].split("_")
            if len(os.listdir(os.path.join(treatRprtPath,treatPathFolder)))>1:
                treatType = "MultiDevice-Treatment"
            else:
                 treatType = "SingleDevice-Treatment"

            self.SelectPnl.SrchListCtrl.InsertStringItem(0, str(len(self.treatStampList)-1))
            self.SelectPnl.SrchListCtrl.SetStringItem(0, 1, treatType)
            self.SelectPnl.SrchListCtrl.SetStringItem(0, 2, dateStmp)
            self.SelectPnl.SrchListCtrl.SetStringItem(0, 3, timeStmp)
            #self.SelectPnl.SrchListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClickTreatment)

        elif radioStrng.startswith("All"):
            
            for ind, val in enumerate(self.treatStampList):
                timeStmp, dateStmp = val.split("_")
                treatPathFolder = self.patntName+"_Q-Treatment_"+val
                if len(os.listdir(os.path.join(treatRprtPath,treatPathFolder)))>1:
                    treatType = "MultiDevice-Treatment"
                else:
                    treatType = "SingleDevice-Treatment"

                self.SelectPnl.SrchListCtrl.InsertStringItem(ind, str(ind))
                self.SelectPnl.SrchListCtrl.SetStringItem(ind, 1, treatType)
                self.SelectPnl.SrchListCtrl.SetStringItem(ind, 2, dateStmp)
                self.SelectPnl.SrchListCtrl.SetStringItem(ind, 3, timeStmp)
                #self.SelectPnl.SrchListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClickTreatment)

        elif radioStrng.startswith("Select"):
            msgDlg = wx.MessageDialog(None, "This feature is not available right now. \n Coming soon",'Feature Update',wx.OK)
            msgResult = msgDlg.ShowModal()

        self.SelectPnl.SrchListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.DoubleClickTreatment)
        self.InstructionPnl.Rule1.SetLabel("Find the desired Treatment Session on the Treatment List and Double Click on it. ")
        self.InstructionPnl.Rule1.Wrap(350)
        self.Refresh()
        self.Layout()
        
        pass

    def OnRetrieveButton(self, evt):
        print("Retrieve Button Cliked")
        #self.EndModal()
        self.Destroy()
        return
    
       

    def OnPatientSearch(self, evt):
        self.ListPatntDetails, self.ListPatntNames = self.AllExistingPatientDetails(self.db.QPatntListCsvPath)
        self.SrchStrng = evt.GetString()
        print(self.SrchStrng)
        #self.setupSearchPatientList()
        #self.SelectPnl.SrchListCtrl.DeleteAllItems()

        try:
            self.SelectPnl.SrchListCtrl.DeleteAllItems()
            self.SelectPnl.SrchListCtrl.DeleteAllColumns()
            self.setupSearchPatientList()
        except AttributeError:
            self.setupSearchPatientList()       
        
        indx = 0

        for P_indx, item in enumerate(self.ListPatntNames):
            if str(item).lower().startswith(str(self.SrchStrng).lower()):
                #indx=indx+1
                fullName = str(self.ListPatntDetails[P_indx][0])+" "+str(self.ListPatntDetails[P_indx][1])
                dob = str(self.ListPatntDetails[P_indx][4])
                Q_ID = str(self.ListPatntDetails[P_indx][2])
                self.SelectPnl.SrchListCtrl.InsertStringItem(indx, str(P_indx))
                self.SelectPnl.SrchListCtrl.SetStringItem(indx, 1, str(fullName))
                self.SelectPnl.SrchListCtrl.SetStringItem(indx, 2, str(dob))
                self.SelectPnl.SrchListCtrl.SetStringItem(indx, 3, str(Q_ID))
                indx=indx+1               
        
        pass

    def AllExistingPatientDetails(self,listPath):
        AllPatientDetails = []
        AllPatientNames = []

        with open(listPath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for rows in readCSV:
                if rows[0].startswith("FirstName"):
                    continue
                line= rows
                name = line[7]
                AllPatientDetails.append(line)
                AllPatientNames.append(name)

        return AllPatientDetails,AllPatientNames
    
    def setupSearchPatientList(self):
        
        self.SelectPnl.SrchListCtrl.InsertColumn(0, 'Index', width = 45)
        self.SelectPnl.SrchListCtrl.InsertColumn(1, 'Patient Full Name', width = 200)
        self.SelectPnl.SrchListCtrl.InsertColumn(2, 'DOB', width=80)
        self.SelectPnl.SrchListCtrl.InsertColumn(3, 'QSTM ID', width=120)

    def setupSelectTreatmentList(self):
        
        self.SelectPnl.SrchListCtrl.InsertColumn(0, 'Index', width = 50)
        self.SelectPnl.SrchListCtrl.InsertColumn(1, 'Treat Type', width = 150)
        self.SelectPnl.SrchListCtrl.InsertColumn(2, 'Treat Date Stamp', width=110)
        self.SelectPnl.SrchListCtrl.InsertColumn(3, 'Treat Time Stamp(24Hrs)', width=130)
        

    def DoubleClickPatientName(self, evt):        
        print("Patient name Double Clicked")       
        self.PatntIndx = evt.GetItem().GetText()
        
        [self.SelectPnl.pnlRadioBox.ShowItem( i, show=True) for i, item in enumerate(self.SelectPnl.pnlRadioBoxChoices)]
        self.InstructionPnl.Rule1.SetLabel("Patient name selected.\nNow select Treatment View from the Radio Buttons below.")
        self.SelectPnl.LblPatnt.SetLabel(self.ListPatntDetails[(int)(self.PatntIndx)][0]+" "+
                                         self.ListPatntDetails[(int)(self.PatntIndx)][1])
        self.SelectPnl.LblDOB.SetLabel("DOB : " + self.ListPatntDetails[(int)(self.PatntIndx)][4])
        self.SelectPnl.TxtPatnt.SetForegroundColour( wx.Colour(0, 0, 0 ))
        self.SelectPnl.LblPatnt.SetForegroundColour( wx.Colour(0, 0, 0 ))
        self.SelectPnl.LblDOB.SetForegroundColour( wx.Colour(0, 0, 0 ))
        self.Refresh()
        self.Layout()
        
        print(self.PatntIndx)
        pass

    def DoubleClickTreatment(self, evt):
        print("Treatment Double Clicked")
        #CtrlObj = evt.GetEventObject()
        TreatIndx = evt.GetItem().GetText()
        #self.TreatType = CtrlObj.GetItem(itemId=(int)(TreatIndx), col=1).GetText()
        print(TreatIndx)
       
        self.retrieveBtn.Enable()
        self.SelectPnl.SrchListCtrl.Disable()
        self.SelectPnl.pnlRadioBox.Disable()
        timeStmp, dateStmp = self.treatStampList[(int)(TreatIndx)].split("_")
        
        self.PatntTreatFolder = self.patntName+"_Q-Treatment_"+self.treatStampList[(int)(TreatIndx)]
        self.PatntFolderPath =(self.db.Q_PatientsFolderPath+"\\"+self.patntName+"\\"+
                              self.ListPatntDetails[(int)(self.PatntIndx)][7])        
        if len(os.listdir(os.path.join((self.PatntFolderPath+"\\Patient Report"),self.PatntTreatFolder)))>1:
            self.TreatType = "MultiDevice-Treatment"
        else:
            self.TreatType = "SingleDevice-Treatment"

        print(self.TreatType)
            
                   
        self.PatntDetails = self.ListPatntDetails[(int)(self.PatntIndx)]
        self.InstructionPnl.Rule1.SetLabel("Treatment Session Selected. Now please click the Retrieve Button to retrieve selected treatment session.")
        self.InstructionPnl.Rule1.Wrap(350)
        self.SelectPnl.LblTreatDate.SetLabel("Date : " + dateStmp)
        self.SelectPnl.LblTreatTime.SetLabel("Date : " + timeStmp)
        self.SelectPnl.TxtTreat.SetForegroundColour( wx.Colour(0, 0, 0 ))
        self.SelectPnl.LblTreatDate.SetForegroundColour( wx.Colour(0, 0, 0 ))
        self.SelectPnl.LblTreatTime.SetForegroundColour( wx.Colour(0, 0, 0 ))
        self.Refresh()
        self.Layout()
        #print(self.PatntTreatFolder)
        

    
    

####################################################################################
##
## Main Function of the QSTM Patient Record System 
##
####################################################################################     
        



def main():
    
    ex = wx.App()
    ex.locale = wx.Locale(wx.LANGUAGE_ENGLISH)

##    OpenDialog = QOpenDialog(None)
##   
##    time.sleep(2)
##    OpenDialog.Hide()
##    OpenDialog.Destroy()
    
    PRS_MainWindowBackend(None)
    ex.MainLoop()    

if __name__ == '__main__':
    mp.freeze_support()
    main()          

	

