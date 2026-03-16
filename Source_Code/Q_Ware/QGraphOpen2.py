from PyQt4 import QtGui, QtCore, QtGui 
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
#import pyqtgraph.console
#from pyqtgraph.dockarea import *
import numpy as np
import pyqtgraph as pg
from pyqtgraph.dockarea import *
import QSTMGraphicalAnalysisQ1 as qstmGAQ1
import QSTMGraphicalAnalysisQ2 as qstmGAQ2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def configForceGraph(obj, grphVars, pkStArr, pkArr):

    rmsPlt = obj.plot(grphVars[11],grphVars[6],pen=(0,0,0), name="Force RMS Channel")#TimeStream,Force_Row
    #widget.plotItem.plot(grphVars[11],grphVars[13],pen=(0,0,255))#TimeStream,ForceAvgRow
    rmsFiltPlt = obj.plotItem.plot(grphVars[12],grphVars[22],pen=(128,0,0), name="Force Filtered(RMS)")#TimeStream,ForceButterRow
    frcYPlt = obj.plotItem.plot(grphVars[11],grphVars[19],pen=(0,155,0), name="Force Y Channel")#TimeStream,Force_Y_Row
    frcXPlt = obj.plotItem.plot(grphVars[11],grphVars[20],pen=(255,0,0), name="Force X Channel")#TimeStream,Force_X_Row
    frcZPlt = obj.plotItem.plot(grphVars[11],grphVars[7],pen=(0,0,255), name="Force Z Channel")#TimeStream,Force_Z_Row
    #obj.plotItem.plot(grphVars[12],grphVars[14],pen=(12,63,18), name="Force GaussFilt Channel")# TimeShiftStream,ForceGaussRow
    #obj.plot(grphVars[11],grphVars[21],pen=(9,165,166))#TimeStream,GyroRMS
    frcVlyPlt = obj.plotItem.plot(grphVars[3],grphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w', name="Force Valleys")# valleyStampArr,valleyFrcArr
    frcPkPlt = obj.plotItem.plot(pkStArr,pkArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w', name="Force Peaks")# pkStampArr,pkFrcArr,
    
    #obj.plot(grphVars[11],grphVars[15],pen=(131,81,193))#TimeStream,AccelRMS
    #obj.plot(grphVars[11],grphVars[16],pen=(255,255,0))#TimeStream,AccDDArr
    #obj.plot(grphVars[17],grphVars[18],pen=(255,0,255))#accSpikeStmpArr,accSpikeArr
    return frcXPlt, frcYPlt, frcZPlt, rmsPlt, rmsFiltPlt, frcPkPlt, frcVlyPlt

def configGeoAngGraph(obj, grphVars):
    geoPitchPlt = obj.plotItem.plot(grphVars[11],grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row
    geoYawPlt = obj.plotItem.plot(grphVars[11],grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
    geoRollPlt = obj.plotItem.plot(grphVars[11],grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row
    return geoYawPlt, geoPitchPlt, geoRollPlt



class GraphMonitor(object):
    
    def setupUi(self, MainWindow, GrphPathQ1, GrphPathQ2):
        
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1438, 860)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))

        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        #Q2gui.Q2_Visual_GUI().setupUI(self.tab_1)# calling Q2 GUI MainFrame Object

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        pg.setConfigOptions(antialias=True)

        GraphQ1UI = Q1Graph()
        GraphQ1UI.setupUI(self.tab_1,GrphPathQ1)

        GraphQ2UI = Q2Graph()
        GraphQ2UI.setupUI(self.tab_2,GrphPathQ2)

        #grphSet = GraphPnl()
        #grphSet.setupUI(Frame)

        #self.addQ1Graph()
        #self.addQ2Graph()        
        
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)     
       

        self.visTimer = QtCore.QTimer()
        self.visTimer.timeout.connect(self.currentTabIndex)
        self.visTimer.start(500)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def currentTabIndex(self):
        self.tabIndex = self.tabWidget.currentIndex()
        #print("Current Tab Index" + str(self.tabIndex))
        return self.tabIndex   
        

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Treatment Session Graph", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", " Q1 Waveforms", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", " Q2 Waveforms", None))


class GraphPnl(object):
    def setupUI (self, Frame):

        self.grphPnl = QtGui.QWidget(Frame)
        self.grphPnl.setGeometry(QtCore.QRect(0, 0, 165, 821))
        self.grphPnl.setObjectName(_fromUtf8("grphPnl"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.grphPnl)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.cbDfltGrph = QtGui.QCheckBox(self.grphPnl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cbDfltGrph.setFont(font)
        self.cbDfltGrph.setObjectName(_fromUtf8("cbDfltGrph"))
        self.verticalLayout_2.addWidget(self.cbDfltGrph)
        self.cbFrcPlt = QtGui.QCheckBox(self.grphPnl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cbFrcPlt.setFont(font)
        self.cbFrcPlt.setObjectName(_fromUtf8("cbFrcPlt"))
        self.cbFrcPlt.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbFrcPlt)
        self.cbGAplt = QtGui.QCheckBox(self.grphPnl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cbGAplt.setFont(font)
        self.cbGAplt.setObjectName(_fromUtf8("cbGAplt"))
        self.cbGAplt.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbGAplt)
        self.cbSAplt = QtGui.QCheckBox(self.grphPnl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.cbSAplt.setFont(font)
        self.cbSAplt.setObjectName(_fromUtf8("cbSAplt"))
        self.cbSAplt.setEnabled (False)
        self.verticalLayout_2.addWidget(self.cbSAplt)
        spacerItem = QtGui.QSpacerItem(20, 94, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.FChnlLbl = QtGui.QLabel(self.grphPnl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.FChnlLbl.setFont(font)
        self.FChnlLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.FChnlLbl.setObjectName(_fromUtf8("FChnlLbl"))
       
        self.verticalLayout_2.addWidget(self.FChnlLbl)
        self.cbFrcX = QtGui.QCheckBox(self.grphPnl)
        self.cbFrcX.setObjectName(_fromUtf8("cbFrcX"))
        self.cbFrcX.setEnabled (False)
        self.verticalLayout_2.addWidget(self.cbFrcX)
        self.cbFrcY = QtGui.QCheckBox(self.grphPnl)
        self.cbFrcY.setObjectName(_fromUtf8("cbFrcY"))
        self.cbFrcY.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbFrcY)
        self.cbFrcZ = QtGui.QCheckBox(self.grphPnl)
        self.cbFrcZ.setObjectName(_fromUtf8("cbFrcZ"))
        self.cbFrcZ.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbFrcZ)
        self.cbFrcRMS = QtGui.QCheckBox(self.grphPnl)
        self.cbFrcRMS.setObjectName(_fromUtf8("cbFrcRMS"))
        self.cbFrcRMS.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbFrcRMS)
        self.cbFrcPV = QtGui.QCheckBox(self.grphPnl)
        self.cbFrcPV.setObjectName(_fromUtf8("cbFrcPV"))
        self.cbFrcPV.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbFrcPV)
        spacerItem1 = QtGui.QSpacerItem(20, 93, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.geoAngLbl = QtGui.QLabel(self.grphPnl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.geoAngLbl.setFont(font)
        self.geoAngLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.geoAngLbl.setObjectName(_fromUtf8("geoAngLbl"))
        self.verticalLayout_2.addWidget(self.geoAngLbl)
        self.cbgYaw = QtGui.QCheckBox(self.grphPnl)
        self.cbgYaw.setObjectName(_fromUtf8("cbgYaw"))
        self.cbgYaw.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbgYaw)
        self.cbgPitch = QtGui.QCheckBox(self.grphPnl)
        self.cbgPitch.setObjectName(_fromUtf8("cbgPitch"))
        self.cbgPitch.setEnabled(False)        
        self.verticalLayout_2.addWidget(self.cbgPitch)
        self.cbgRoll = QtGui.QCheckBox(self.grphPnl)
        self.cbgRoll.setObjectName(_fromUtf8("cbgRoll"))
        self.cbgRoll.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbgRoll)
        spacerItem2 = QtGui.QSpacerItem(20, 94, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.skinAngLbl = QtGui.QLabel(self.grphPnl)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.skinAngLbl.setFont(font)
        self.skinAngLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.skinAngLbl.setObjectName(_fromUtf8("skinAngLbl"))
        self.verticalLayout_2.addWidget(self.skinAngLbl)
        self.cbSYaw = QtGui.QCheckBox(self.grphPnl)
        self.cbSYaw.setObjectName(_fromUtf8("cbSYaw"))
        self.cbSYaw.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbSYaw)
        self.cbSPitch = QtGui.QCheckBox(self.grphPnl)
        self.cbSPitch.setObjectName(_fromUtf8("cbSPitch"))
        self.cbSPitch.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbSPitch)
        self.cbSRoll = QtGui.QCheckBox(self.grphPnl)
        self.cbSRoll.setObjectName(_fromUtf8("cbSRoll"))
        self.cbSRoll.setEnabled(False)
        self.verticalLayout_2.addWidget(self.cbSRoll)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        #Frame.setWindowTitle(_translate("Frame", "Frame", None))
        self.cbDfltGrph.setText(_translate("Frame", "Default Graph", None))
        self.cbFrcPlt.setText(_translate("Frame", "Force Plot", None))
        self.cbGAplt.setText(_translate("Frame", "Geo-Angle Plot", None))
        self.cbSAplt.setText(_translate("Frame", "Skin-Angle Plot", None))
        self.FChnlLbl.setText(_translate("Frame", "Force Channels", None))
        self.cbFrcX.setText(_translate("Frame", "Force X Channel", None))
        self.cbFrcY.setText(_translate("Frame", "Force Y Channel", None))
        self.cbFrcZ.setText(_translate("Frame", "Force Z Channel", None))
        self.cbFrcRMS.setText(_translate("Frame", "Force RMS Channel", None))
        self.cbFrcPV.setText(_translate("Frame", "Force Peak-Valley", None))
        self.geoAngLbl.setText(_translate("Frame", "Geo-Angle Curves", None))
        self.cbgYaw.setText(_translate("Frame", "Geo-Yaw Curve", None))
        self.cbgPitch.setText(_translate("Frame", "Geo-Pitch Curve", None))
        self.cbgRoll.setText(_translate("Frame", "Geo-Roll Curve", None))
        self.skinAngLbl.setText(_translate("Frame", "Skin-Angle Curves", None))
        self.cbSYaw.setText(_translate("Frame", "Skin-Yaw Curve", None))
        self.cbSPitch.setText(_translate("Frame", "Skin-Pitch Curve", None))
        self.cbSRoll.setText(_translate("Frame", "Skin-Roll Curve", None))

    

        
class Q1Graph(object):

    def setupUI (self, Frame, path):

        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(1438, 860)
        
        self.gridLayout = QtGui.QGridLayout(Frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.area = DockArea()
        self.gridLayout.addWidget(self.area, 0, 0, 1, 1)        

        self.d1 = Dock("Graph Settings", size=(165,825))
        self.d2 = Dock("Force Plot", size=(1305,550))
        self.d3 = Dock("Angular Orientation Plot", size=(1305,275))
        self.area.addDock(self.d2, 'right')    
        self.area.addDock(self.d1, 'left')
        self.area.addDock(self.d3, 'bottom', self.d2)
       

        self.gSetting = GraphPnl()# Graph settings widget 
        self.gSetting.setupUI(Frame)

        #self.scaleCnt = 0; 

        #self.pltQ1Timer = QtCore.QTimer()
        #self.pltQ1Timer.timeout.connect(self.plotScaling)
        #self.pltQ1Timer.start(1000)


        ##--------------------- Force Plot Fx, Fy, Fz, Frms, Fpeak & Fvalley-----------------------------------------------------------      
        

        pg.setConfigOptions(antialias=True)        
        #self.Q1FrcPlt=pg.PlotWidget(title=" Q1 Force Chart ", enableMouse=True, enableMenu=True)
        self.Q1FrcPlt=pg.PlotWidget(enableMouse=True, enableMenu=True)
        #titleStyle = {'color': '#7F7F7F', 'font-size': '16pt', 'font-style': 'Times New Roman'}
        self.Q1FrcPlt.setTitle("Force Graph", color='#7F7F7F', style = 'Times New Roman', size = '15pt', bold = True)              
       
        self.Q1FrcPlt.setMouseEnabled(x=True, y=True)
        self.Q1FrcPlt.setBackgroundBrush(QtGui.QColor(250,250,255))
        self.Q1FrcPlt.showGrid(x=True, y=True)
        self.labelStyle = {'color': '#576574', 'font-size': '14pt', 'font-style': 'Times New Roman'}
        #FrcPlt.setLabel('left',text="<span style='color: #ff0000; font-weight: bold; font-size: 12pt'>Force</span> <i>Axis</i>")
        self.Q1FrcPlt.setLabel('left',"Force (Newtons)",**self.labelStyle)
        self.Q1FrcPlt.setLabel('bottom',"Time(Seconds)",**self.labelStyle)
        #self.Q1FrcLegend = self.Q1FrcPlt.addLegend(offset=(0,0)) #pen=pg.mkPen(color=(128, 0, 0), width=2), fillLevel=UpdateLevelVal, fillBrush=(128,0,0,30)

        self.Q1grphVars, self.Q1pkStArr, self.Q1pkArr = qstmGAQ1.GraphShow(path)
        self.FrcPlts = configForceGraph(self.Q1FrcPlt, self.Q1grphVars, self.Q1pkStArr, self.Q1pkArr)

        self.gSetting.cbDfltGrph.setChecked(True)        
        self.gSetting.cbDfltGrph.stateChanged.connect(lambda:self.defaultGraph(self.gSetting.cbDfltGrph))
        self.gSetting.cbFrcPlt.stateChanged.connect(lambda:self.FrcPlotCheck(self.gSetting.cbFrcPlt))

        self.gSetting.cbFrcX.stateChanged.connect(lambda:self.FrcXCheck(self.gSetting.cbFrcX))
        self.gSetting.cbFrcY.stateChanged.connect(lambda:self.FrcYCheck(self.gSetting.cbFrcY))
        self.gSetting.cbFrcZ.stateChanged.connect(lambda:self.FrcZCheck(self.gSetting.cbFrcZ))
        self.gSetting.cbFrcRMS.stateChanged.connect(lambda:self.FrcRMSCheck(self.gSetting.cbFrcRMS))
        self.gSetting.cbFrcPV.stateChanged.connect(lambda:self.FrcPVCheck(self.gSetting.cbFrcPV))


        ##------------------------------------------- Geo-Angle Plot Yaw(Z), Pitch(Y), Roll(X)-----------------------------------------------------------

        self.Q1GeoAngPlt=pg.PlotWidget(enableMouse=True, enableMenu=True)
        #titleStyle = {'color': '#7F7F7F', 'font-size': '16pt', 'font-style': 'Times New Roman'}
        self.Q1GeoAngPlt.setTitle("Geo-Angle Graph", color='#7F7F7F', style = 'Times New Roman', size = '15pt', bold = True)
                
       
        self.Q1GeoAngPlt.setMouseEnabled(x=True, y=True)
        self.Q1GeoAngPlt.setBackgroundBrush(QtGui.QColor(250,250,255))
        self.Q1GeoAngPlt.showGrid(x=True, y=True)
        #self.labelStyle = {'color': '#576574', 'font-size': '14pt', 'font-style': 'Times New Roman'}
        #FrcPlt.setLabel('left',text="<span style='color: #ff0000; font-weight: bold; font-size: 12pt'>Force</span> <i>Axis</i>")
        self.Q1GeoAngPlt.setLabel('left',"Angular Orientation (Degrees)",**self.labelStyle)
        self.Q1GeoAngPlt.setLabel('bottom',"Time(Seconds)",**self.labelStyle)
        #self.Q1FrcLegend = self.Q1FrcPlt.addLegend(offset=(0,0)) #pen=pg.mkPen(color=(128, 0, 0), width=2), fillLevel=UpdateLevelVal, fillBrush=(128,0,0,30)

        self.GeoAngPlts = configGeoAngGraph(self.Q1GeoAngPlt, self.Q1grphVars)

        
        self.gSetting.cbGAplt.stateChanged.connect(lambda:self.GeoAngPlotCheck(self.gSetting.cbGAplt))

        self.gSetting.cbgYaw.stateChanged.connect(lambda:self.gYawCheck(self.gSetting.cbgYaw))
        self.gSetting.cbgPitch.stateChanged.connect(lambda:self.gPitchCheck(self.gSetting.cbgPitch))
        self.gSetting.cbgRoll.stateChanged.connect(lambda:self.gRollCheck(self.gSetting.cbgRoll))


        self.d1.addWidget(self.gSetting.grphPnl)
        #self.d1.hideTitleBar()

        self.d2.addWidget(self.Q1FrcPlt)
        self.d2.hideTitleBar()

        self.d3.addWidget(self.Q1GeoAngPlt)
        self.d3.hideTitleBar()
        self.Q1plotScaling()


    def Q1plotScaling(self):

        
        self.fVB = self.Q1FrcPlt.getViewBox()
        self.gVB = self.Q1GeoAngPlt.getViewBox()
        self.gVB.linkView(self.fVB.XAxis,self.fVB)
        #print (self.gRect)

    
    def defaultGraph(self, cb):
        cbType = cb.objectName()
        if cbType == "cbDfltGrph":
            if cb.isChecked() == True:
                #print ("is selected")
                self.gSetting.cbFrcPlt.setEnabled(False)
                self.FrcPlts = configForceGraph(self.Q1FrcPlt, self.Q1grphVars, self.Q1pkStArr, self.Q1pkArr)

                self.gSetting.cbGAplt.setEnabled(False)
                self.GeoAngPlts = configGeoAngGraph(self.Q1GeoAngPlt, self.Q1grphVars)
                #self.geoYawPlt, self.geoPitchPlt, self.geoRollPlt = configGeoAngGraph(self.Q1GeoAngPlt, self.Q1grphVars)
                
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.gSetting.cbFrcPlt.setEnabled(True)
                self.gSetting.cbGAplt.setEnabled(True)
                self.Q1FrcPlt.removeItem(self.FrcPlts[0])
                self.Q1FrcPlt.removeItem(self.FrcPlts[1])
                self.Q1FrcPlt.removeItem(self.FrcPlts[2])
                self.Q1FrcPlt.removeItem(self.FrcPlts[3])
                self.Q1FrcPlt.removeItem(self.FrcPlts[4])
                self.Q1FrcPlt.removeItem(self.FrcPlts[5])
                self.Q1FrcPlt.removeItem(self.FrcPlts[6])

                self.Q1GeoAngPlt.removeItem(self.GeoAngPlts[0])
                self.Q1GeoAngPlt.removeItem(self.GeoAngPlts[1])
                self.Q1GeoAngPlt.removeItem(self.GeoAngPlts[2])


    def GeoAngPlotCheck(self,cb):
        print("GeoCurves")

        cbType = cb.objectName()
        if cbType == "cbGAplt":
            if cb.isChecked() == True:
                #print ("is selected")
                self.gSetting.cbDfltGrph.setEnabled(False)

                self.gSetting.cbgYaw.setEnabled(True)
                self.gSetting.cbgYaw.setChecked(True)
                #self.geoYawPlt = self.Q1GeoAngPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                
                self.gSetting.cbgPitch.setEnabled (True)
                self.gSetting.cbgPitch.setChecked (True)
                #self.geoPitchPlt = self.Q1GeoAngPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row

                
                self.gSetting.cbgRoll.setEnabled (True)
                self.gSetting.cbgRoll.setChecked (True)
                #self.geoRollPlt = self.Q1GeoAngPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row
                
                
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.gSetting.cbDfltGrph.setEnabled(True)
                self.gSetting.cbgYaw.setEnabled(False)
                self.gSetting.cbgPitch.setEnabled (False)
                self.gSetting.cbgRoll.setEnabled (False)

                self.gSetting.cbgYaw.setChecked(False)
                self.gSetting.cbgPitch.setChecked(False)
                self.gSetting.cbgRoll.setChecked(False)

                #self.Q1GeoAngPlt.removeItem(self.geoYawPlt)
                #self.Q1GeoAngPlt.removeItem(self.geoPitchPlt)
                #self.Q1GeoAngPlt.removeItem(self.geoRollPlt)
                

    def gYawCheck(self,cb):
        print("Geo Yaw Curve")
        cbType = cb.objectName()
        if cbType == "cbgYaw":
            if cb.isChecked() == True:                
               # print ("is selected")
                #geoPitchPlt = obj.plotItem.plot(grphVars[11],grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row
                self.geoYawPlt = self.Q1GeoAngPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                #geoRollPlt = obj.plotItem.plot(grphVars[11],grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row                
            elif cb.isChecked() == False:                
                #print ("is unselected")                
                self.Q1GeoAngPlt.removeItem(self.geoYawPlt)

    

    def gPitchCheck(self,cb):
        print("Geo Pitch Curve")
        cbType = cb.objectName()
        if cbType == "cbgPitch":
            if cb.isChecked() == True:                
               # print ("is selected")
                self.geoPitchPlt = self.Q1GeoAngPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row
                #self.geoYawPlt = obj.plotItem.plot(grphVars[11],grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                #geoRollPlt = obj.plotItem.plot(grphVars[11],grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row                
            elif cb.isChecked() == False:                
                #print ("is unselected")                
                self.Q1GeoAngPlt.removeItem(self.geoPitchPlt)

    def gRollCheck(self,cb):
        print("Geo Roll Curve")
        cbType = cb.objectName()
        if cbType == "cbgRoll":
            if cb.isChecked() == True:                
               # print ("is selected")
                #geoRollPlt = obj.plotItem.plot(grphVars[11],grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row
                #geoPitchPlt = obj.plotItem.plot(grphVars[11],grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                self.geoRollPlt = self.Q1GeoAngPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row                
            elif cb.isChecked() == False:                
                #print ("is unselected")
                #self.Q1FrcPlt.removeItem(self.frcXPlt)
                self.Q1GeoAngPlt.removeItem(self.geoRollPlt)

    def FrcPlotCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcPlt":
            if cb.isChecked() == True:
                #print ("is selected")
                self.gSetting.cbDfltGrph.setEnabled(False)
                self.gSetting.cbFrcX.setEnabled(True)
                self.gSetting.cbFrcY.setEnabled (True)
                self.gSetting.cbFrcZ.setEnabled (True)
                self.gSetting.cbFrcRMS.setEnabled (True)
                self.gSetting.cbFrcPV.setEnabled (True)

                self.gSetting.cbFrcX.setChecked(True)
                self.gSetting.cbFrcY.setChecked(True)
                self.gSetting.cbFrcZ.setChecked(True)
                self.gSetting.cbFrcRMS.setChecked(True)
                self.gSetting.cbFrcPV.setChecked(True)
                
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.gSetting.cbDfltGrph.setEnabled(True)
                self.gSetting.cbFrcX.setEnabled(False)
                self.gSetting.cbFrcY.setEnabled (False)
                self.gSetting.cbFrcZ.setEnabled (False)
                self.gSetting.cbFrcRMS.setEnabled (False)
                self.gSetting.cbFrcPV.setEnabled (False)

                self.gSetting.cbFrcX.setChecked(False)
                self.gSetting.cbFrcY.setChecked(False)
                self.gSetting.cbFrcZ.setChecked(False)
                self.gSetting.cbFrcRMS.setChecked(False)
                self.gSetting.cbFrcPV.setChecked(False)
    

    def FrcXCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcX":
            if cb.isChecked() == True:
               # print ("is selected")
                self.frcXPlt = self.Q1FrcPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[20],pen=(255,0,0), name="Force X Channel")#TimeStream,Force_X_Row
            elif cb.isChecked() == False:                
                #print ("is unselected")
                self.Q1FrcPlt.removeItem(self.frcXPlt)

    def FrcYCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcY":
            if cb.isChecked() == True:
               # print ("is selected")
                self.frcYPlt = self.Q1FrcPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[19],pen=(0,155,0), name="Force Y Channel")#TimeStream,Force_Y_Row
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q1FrcPlt.removeItem(self.frcYPlt)

    def FrcZCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcZ":
            if cb.isChecked() == True:
                #print ("is selected")
                self.frcZPlt = self.Q1FrcPlt.plotItem.plot(self.Q1grphVars[11],self.Q1grphVars[7],pen=(0,0,255), name="Force Z Channel")#TimeStream,Force_Z_Row                 
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q1FrcPlt.removeItem(self.frcZPlt)


    def FrcRMSCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcRMS":
            if cb.isChecked() == True:
                #print ("is selected")
                self.rmsPlt = self.Q1FrcPlt.plot(self.Q1grphVars[11],self.Q1grphVars[6],pen=(0,0,0), name="Force RMS Channel")#TimeStream,Force_Row
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q1FrcPlt.removeItem(self.rmsPlt)

    def FrcPVCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcPV":
            if cb.isChecked() == True:
                #print ("is selected")
                self.rmsFiltPlt = self.Q1FrcPlt.plotItem.plot(self.Q1grphVars[12],self.Q1grphVars[22],pen=(128,0,0), name="Force Filtered(RMS)")#TimeStream,ForceButterRow
                self.frcVlyPlt = self.Q1FrcPlt.plotItem.plot(self.Q1grphVars[3],self.Q1grphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w', name="Force Valleys")# valleyStampArr,valleyFrcArr
                self.frcPkPlt = self.Q1FrcPlt.plotItem.plot(self.Q1pkStArr,self.Q1pkArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w', name="Force Peaks")# pkStampArr,pkFrcArr,
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q1FrcPlt.removeItem(self.rmsFiltPlt)
                self.Q1FrcPlt.removeItem(self.frcVlyPlt)
                self.Q1FrcPlt.removeItem(self.frcPkPlt)
                
            
            

class Q2Graph(object):

    def setupUI (self, Frame, path):

        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(1438, 860)
        
        self.gridLayout = QtGui.QGridLayout(Frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        self.area = DockArea()
        self.gridLayout.addWidget(self.area, 0, 0, 1, 1)        

        self.d1 = Dock("Graph Settings", size=(165,825))
        self.d2 = Dock("Force Plot", size=(1305,550))
        self.d3 = Dock("Angular Orientation Plot", size=(1305,275))
        self.area.addDock(self.d2, 'right')    
        self.area.addDock(self.d1, 'left')
        self.area.addDock(self.d3, 'bottom', self.d2)
       

        self.gSetting = GraphPnl()# Graph settings widget 
        self.gSetting.setupUI(Frame)

        #self.scaleCnt = 0; 

        #self.pltQ2Timer = QtCore.QTimer()
        #self.pltQ2Timer.timeout.connect(self.plotScaling)
        #self.pltQ2Timer.start(1000)


        ##--------------------- Force Plot Fx, Fy, Fz, Frms, Fpeak & Fvalley-----------------------------------------------------------      
        

        pg.setConfigOptions(antialias=True)        
        #self.Q2FrcPlt=pg.PlotWidget(title=" Q2 Force Chart ", enableMouse=True, enableMenu=True)
        self.Q2FrcPlt=pg.PlotWidget(enableMouse=True, enableMenu=True)
        #titleStyle = {'color': '#7F7F7F', 'font-size': '16pt', 'font-style': 'Times New Roman'}
        self.Q2FrcPlt.setTitle("Force Graph", color='#7F7F7F', style = 'Times New Roman', size = '15pt', bold = True)              
       
        self.Q2FrcPlt.setMouseEnabled(x=True, y=True)
        self.Q2FrcPlt.setBackgroundBrush(QtGui.QColor(250,250,255))
        self.Q2FrcPlt.showGrid(x=True, y=True)
        self.labelStyle = {'color': '#576574', 'font-size': '14pt', 'font-style': 'Times New Roman'}
        #FrcPlt.setLabel('left',text="<span style='color: #ff0000; font-weight: bold; font-size: 12pt'>Force</span> <i>Axis</i>")
        self.Q2FrcPlt.setLabel('left',"Force (Newtons)",**self.labelStyle)
        self.Q2FrcPlt.setLabel('bottom',"Time(Seconds)",**self.labelStyle)
        #self.Q2FrcLegend = self.Q2FrcPlt.addLegend(offset=(0,0)) #pen=pg.mkPen(color=(128, 0, 0), width=2), fillLevel=UpdateLevelVal, fillBrush=(128,0,0,30)

        self.Q2grphVars, self.Q2pkStArr, self.Q2pkArr = qstmGAQ2.GraphShow(path)
        self.FrcPlts = configForceGraph(self.Q2FrcPlt, self.Q2grphVars, self.Q2pkStArr, self.Q2pkArr)

        self.gSetting.cbDfltGrph.setChecked(True)        
        self.gSetting.cbDfltGrph.stateChanged.connect(lambda:self.defaultGraph(self.gSetting.cbDfltGrph))
        self.gSetting.cbFrcPlt.stateChanged.connect(lambda:self.FrcPlotCheck(self.gSetting.cbFrcPlt))

        self.gSetting.cbFrcX.stateChanged.connect(lambda:self.FrcXCheck(self.gSetting.cbFrcX))
        self.gSetting.cbFrcY.stateChanged.connect(lambda:self.FrcYCheck(self.gSetting.cbFrcY))
        self.gSetting.cbFrcZ.stateChanged.connect(lambda:self.FrcZCheck(self.gSetting.cbFrcZ))
        self.gSetting.cbFrcRMS.stateChanged.connect(lambda:self.FrcRMSCheck(self.gSetting.cbFrcRMS))
        self.gSetting.cbFrcPV.stateChanged.connect(lambda:self.FrcPVCheck(self.gSetting.cbFrcPV))


        ##------------------------------------------- Geo-Angle Plot Yaw(Z), Pitch(Y), Roll(X)-----------------------------------------------------------

        self.Q2GeoAngPlt=pg.PlotWidget(enableMouse=True, enableMenu=True)
        #titleStyle = {'color': '#7F7F7F', 'font-size': '16pt', 'font-style': 'Times New Roman'}
        self.Q2GeoAngPlt.setTitle("Geo-Angle Graph", color='#7F7F7F', style = 'Times New Roman', size = '15pt', bold = True)
                
       
        self.Q2GeoAngPlt.setMouseEnabled(x=True, y=True)
        self.Q2GeoAngPlt.setBackgroundBrush(QtGui.QColor(250,250,255))
        self.Q2GeoAngPlt.showGrid(x=True, y=True)
        #self.labelStyle = {'color': '#576574', 'font-size': '14pt', 'font-style': 'Times New Roman'}
        #FrcPlt.setLabel('left',text="<span style='color: #ff0000; font-weight: bold; font-size: 12pt'>Force</span> <i>Axis</i>")
        self.Q2GeoAngPlt.setLabel('left',"Angular Orientation (Degrees)",**self.labelStyle)
        self.Q2GeoAngPlt.setLabel('bottom',"Time(Seconds)",**self.labelStyle)
        #self.Q2FrcLegend = self.Q2FrcPlt.addLegend(offset=(0,0)) #pen=pg.mkPen(color=(128, 0, 0), width=2), fillLevel=UpdateLevelVal, fillBrush=(128,0,0,30)

        self.GeoAngPlts = configGeoAngGraph(self.Q2GeoAngPlt, self.Q2grphVars)

        
        self.gSetting.cbGAplt.stateChanged.connect(lambda:self.GeoAngPlotCheck(self.gSetting.cbGAplt))

        self.gSetting.cbgYaw.stateChanged.connect(lambda:self.gYawCheck(self.gSetting.cbgYaw))
        self.gSetting.cbgPitch.stateChanged.connect(lambda:self.gPitchCheck(self.gSetting.cbgPitch))
        self.gSetting.cbgRoll.stateChanged.connect(lambda:self.gRollCheck(self.gSetting.cbgRoll))


        self.d1.addWidget(self.gSetting.grphPnl)
        #self.d1.hideTitleBar()

        self.d2.addWidget(self.Q2FrcPlt)
        self.d2.hideTitleBar()

        self.d3.addWidget(self.Q2GeoAngPlt)
        self.d3.hideTitleBar()
        self.Q2plotScaling()


    def Q2plotScaling(self):

        
        self.fVB = self.Q2FrcPlt.getViewBox()
        self.gVB = self.Q2GeoAngPlt.getViewBox()
        self.gVB.linkView(self.fVB.XAxis,self.fVB)
        #print (self.gRect)

    
    def defaultGraph(self, cb):
        cbType = cb.objectName()
        if cbType == "cbDfltGrph":
            if cb.isChecked() == True:
                #print ("is selected")
                self.gSetting.cbFrcPlt.setEnabled(False)
                self.FrcPlts = configForceGraph(self.Q2FrcPlt, self.Q2grphVars, self.Q2pkStArr, self.Q2pkArr)

                self.gSetting.cbGAplt.setEnabled(False)
                self.GeoAngPlts = configGeoAngGraph(self.Q2GeoAngPlt, self.Q2grphVars)
                #self.geoYawPlt, self.geoPitchPlt, self.geoRollPlt = configGeoAngGraph(self.Q2GeoAngPlt, self.Q2grphVars)
                
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.gSetting.cbFrcPlt.setEnabled(True)
                self.gSetting.cbGAplt.setEnabled(True)
                self.Q2FrcPlt.removeItem(self.FrcPlts[0])
                self.Q2FrcPlt.removeItem(self.FrcPlts[1])
                self.Q2FrcPlt.removeItem(self.FrcPlts[2])
                self.Q2FrcPlt.removeItem(self.FrcPlts[3])
                self.Q2FrcPlt.removeItem(self.FrcPlts[4])
                self.Q2FrcPlt.removeItem(self.FrcPlts[5])
                self.Q2FrcPlt.removeItem(self.FrcPlts[6])

                self.Q2GeoAngPlt.removeItem(self.GeoAngPlts[0])
                self.Q2GeoAngPlt.removeItem(self.GeoAngPlts[1])
                self.Q2GeoAngPlt.removeItem(self.GeoAngPlts[2])


    def GeoAngPlotCheck(self,cb):
        print("GeoCurves")

        cbType = cb.objectName()
        if cbType == "cbGAplt":
            if cb.isChecked() == True:
                #print ("is selected")
                self.gSetting.cbDfltGrph.setEnabled(False)

                self.gSetting.cbgYaw.setEnabled(True)
                self.gSetting.cbgYaw.setChecked(True)
                #self.geoYawPlt = self.Q2GeoAngPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                
                self.gSetting.cbgPitch.setEnabled (True)
                self.gSetting.cbgPitch.setChecked (True)
                #self.geoPitchPlt = self.Q2GeoAngPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row

                
                self.gSetting.cbgRoll.setEnabled (True)
                self.gSetting.cbgRoll.setChecked (True)
                #self.geoRollPlt = self.Q2GeoAngPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row
                
                
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.gSetting.cbDfltGrph.setEnabled(True)
                self.gSetting.cbgYaw.setEnabled(False)
                self.gSetting.cbgPitch.setEnabled (False)
                self.gSetting.cbgRoll.setEnabled (False)

                self.gSetting.cbgYaw.setChecked(False)
                self.gSetting.cbgPitch.setChecked(False)
                self.gSetting.cbgRoll.setChecked(False)

                #self.Q2GeoAngPlt.removeItem(self.geoYawPlt)
                #self.Q2GeoAngPlt.removeItem(self.geoPitchPlt)
                #self.Q2GeoAngPlt.removeItem(self.geoRollPlt)
                

    def gYawCheck(self,cb):
        print("Geo Yaw Curve")
        cbType = cb.objectName()
        if cbType == "cbgYaw":
            if cb.isChecked() == True:                
               # print ("is selected")
                #geoPitchPlt = obj.plotItem.plot(grphVars[11],grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row
                self.geoYawPlt = self.Q2GeoAngPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                #geoRollPlt = obj.plotItem.plot(grphVars[11],grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row                
            elif cb.isChecked() == False:                
                #print ("is unselected")                
                self.Q2GeoAngPlt.removeItem(self.geoYawPlt)

    

    def gPitchCheck(self,cb):
        print("Geo Pitch Curve")
        cbType = cb.objectName()
        if cbType == "cbgPitch":
            if cb.isChecked() == True:                
               # print ("is selected")
                self.geoPitchPlt = self.Q2GeoAngPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row
                #self.geoYawPlt = obj.plotItem.plot(grphVars[11],grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                #geoRollPlt = obj.plotItem.plot(grphVars[11],grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row                
            elif cb.isChecked() == False:                
                #print ("is unselected")                
                self.Q2GeoAngPlt.removeItem(self.geoPitchPlt)

    def gRollCheck(self,cb):
        print("Geo Roll Curve")
        cbType = cb.objectName()
        if cbType == "cbgRoll":
            if cb.isChecked() == True:                
               # print ("is selected")
                #geoRollPlt = obj.plotItem.plot(grphVars[11],grphVars[8],pen=(0,155,0), name="Geo Pitch Y Channel")#TimeStream,Geo_Pitch_Y_Row
                #geoPitchPlt = obj.plotItem.plot(grphVars[11],grphVars[9],pen=(255,0,0), name="Geo Yaw Z Channel")#TimeStream,Geo_Yaw_Z_Row
                self.geoRollPlt = self.Q2GeoAngPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[10],pen=(0,0,255), name="Geo Roll X Channel")#TimeStream,Geo_Roll_X_Row                
            elif cb.isChecked() == False:                
                #print ("is unselected")
                #self.Q2FrcPlt.removeItem(self.frcXPlt)
                self.Q2GeoAngPlt.removeItem(self.geoRollPlt)

    def FrcPlotCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcPlt":
            if cb.isChecked() == True:
                #print ("is selected")
                self.gSetting.cbDfltGrph.setEnabled(False)
                self.gSetting.cbFrcX.setEnabled(True)
                self.gSetting.cbFrcY.setEnabled (True)
                self.gSetting.cbFrcZ.setEnabled (True)
                self.gSetting.cbFrcRMS.setEnabled (True)
                self.gSetting.cbFrcPV.setEnabled (True)

                self.gSetting.cbFrcX.setChecked(True)
                self.gSetting.cbFrcY.setChecked(True)
                self.gSetting.cbFrcZ.setChecked(True)
                self.gSetting.cbFrcRMS.setChecked(True)
                self.gSetting.cbFrcPV.setChecked(True)
                
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.gSetting.cbDfltGrph.setEnabled(True)
                self.gSetting.cbFrcX.setEnabled(False)
                self.gSetting.cbFrcY.setEnabled (False)
                self.gSetting.cbFrcZ.setEnabled (False)
                self.gSetting.cbFrcRMS.setEnabled (False)
                self.gSetting.cbFrcPV.setEnabled (False)

                self.gSetting.cbFrcX.setChecked(False)
                self.gSetting.cbFrcY.setChecked(False)
                self.gSetting.cbFrcZ.setChecked(False)
                self.gSetting.cbFrcRMS.setChecked(False)
                self.gSetting.cbFrcPV.setChecked(False)
    

    def FrcXCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcX":
            if cb.isChecked() == True:
               # print ("is selected")
                self.frcXPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[20],pen=(255,0,0), name="Force X Channel")#TimeStream,Force_X_Row
            elif cb.isChecked() == False:                
                #print ("is unselected")
                self.Q2FrcPlt.removeItem(self.frcXPlt)

    def FrcYCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcY":
            if cb.isChecked() == True:
               # print ("is selected")
                self.frcYPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[19],pen=(0,155,0), name="Force Y Channel")#TimeStream,Force_Y_Row
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q2FrcPlt.removeItem(self.frcYPlt)

    def FrcZCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcZ":
            if cb.isChecked() == True:
                #print ("is selected")
                self.frcZPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[7],pen=(0,0,255), name="Force Z Channel")#TimeStream,Force_Z_Row                 
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q2FrcPlt.removeItem(self.frcZPlt)


    def FrcRMSCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcRMS":
            if cb.isChecked() == True:
                #print ("is selected")
                self.rmsPlt = self.Q2FrcPlt.plot(self.Q2grphVars[11],self.Q2grphVars[6],pen=(0,0,0), name="Force RMS Channel")#TimeStream,Force_Row
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q2FrcPlt.removeItem(self.rmsPlt)

    def FrcPVCheck(self, cb):
        cbType = cb.objectName()
        if cbType == "cbFrcPV":
            if cb.isChecked() == True:
                #print ("is selected")
                self.rmsFiltPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[12],self.Q2grphVars[22],pen=(128,0,0), name="Force Filtered(RMS)")#TimeStream,ForceButterRow
                self.frcVlyPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[3],self.Q2grphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w', name="Force Valleys")# valleyStampArr,valleyFrcArr
                self.frcPkPlt = self.Q2FrcPlt.plotItem.plot(self.Q2pkStArr,self.Q2pkArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w', name="Force Peaks")# pkStampArr,pkFrcArr,
            elif cb.isChecked() == False:
                #print ("is unselected")
                self.Q2FrcPlt.removeItem(self.rmsFiltPlt)
                self.Q2FrcPlt.removeItem(self.frcVlyPlt)
                self.Q2FrcPlt.removeItem(self.frcPkPlt)            

        
        
##        
##class Q2Graph(object):
##
##    def setupUI (self, Frame, path):
##
##        Frame.setObjectName(_fromUtf8("Frame"))
##        Frame.resize(1438, 860)
##        
##        self.gridLayout = QtGui.QGridLayout(Frame)
##        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
##
##        self.area = DockArea()
##        self.gridLayout.addWidget(self.area, 0, 0, 1, 1)        
##
##        self.d1 = Dock("Graph Settings", size=(165,825))
##        self.d2 = Dock("Graph Plot", size=(1305,825))
##        self.area.addDock(self.d2, 'right')    
##        self.area.addDock(self.d1, 'left')
##       
##
##        self.gSetting = GraphPnl()# Graph settings widget 
##        self.gSetting.setupUI(Frame)
##
##
##        ## Force Plot Fx, Fy, Fz, Frms, Fpeak & Fvalley     
##
##        pg.setConfigOptions(antialias=True)
##
##        self.Q2FrcPlt=pg.PlotWidget(title=" Q2 Force Chart ", enableMouse=True, enableMenu=True)
##        self.Q2FrcPlt.setMouseEnabled(x=True, y=True)
##        self.Q2FrcPlt.setBackgroundBrush(QtGui.QColor(250,250,255))
##        self.Q2FrcPlt.showGrid(x=True, y=True)
##        self.labelStyle = {'color': '#576574', 'font-size': '14pt', 'font-style': 'Times New Roman'}
##        #FrcPlt.setLabel('left',text="<span style='color: #ff0000; font-weight: bold; font-size: 12pt'>Force</span> <i>Axis</i>")
##        self.Q2FrcPlt.setLabel('left',"Force (Newtons)",**self.labelStyle)
##        self.Q2FrcPlt.setLabel('bottom',"Time(Seconds)",**self.labelStyle)
##        #self.Q2FrcLegend = self.Q2FrcPlt.addLegend(offset=(0,0)) #pen=pg.mkPen(color=(128, 0, 0), width=2), fillLevel=UpdateLevelVal, fillBrush=(128,0,0,30)       
##
##        self.Q2grphVars, self.Q2pkStArr, self.Q2pkArr = qstmGAQ2.GraphShow(path)
##        self.FrcPlts = configForceGraph(self.Q2FrcPlt, self.Q2grphVars, self.Q2pkStArr, self.Q2pkArr)
##
##        self.gSetting.cbDfltGrph.setChecked(True)        
##        self.gSetting.cbDfltGrph.stateChanged.connect(lambda:self.defaultGraph(self.gSetting.cbDfltGrph))
##        self.gSetting.cbFrcPlt.stateChanged.connect(lambda:self.FrcPlotCheck(self.gSetting.cbFrcPlt))
##
##        self.gSetting.cbFrcX.stateChanged.connect(lambda:self.FrcXCheck(self.gSetting.cbFrcX))
##        self.gSetting.cbFrcY.stateChanged.connect(lambda:self.FrcYCheck(self.gSetting.cbFrcY))
##        self.gSetting.cbFrcZ.stateChanged.connect(lambda:self.FrcZCheck(self.gSetting.cbFrcZ))
##        self.gSetting.cbFrcRMS.stateChanged.connect(lambda:self.FrcRMSCheck(self.gSetting.cbFrcRMS))
##        self.gSetting.cbFrcPV.stateChanged.connect(lambda:self.FrcPVCheck(self.gSetting.cbFrcPV))
##
##        self.gSetting.cbDfltGrph.setChecked(True)
##
##        self.d1.addWidget(self.gSetting.grphPnl)
##        #self.d1.hideTitleBar()
##
##        self.d2.addWidget(self.Q2FrcPlt)
##        self.d2.hideTitleBar()
##        
##        #FrcLegend.paint(p.setPen = 250, 250, 255)
##        
##        #self.gridLayout.addWidget(self.Q2FrcPlt, 0, 0, 1, 1)
##
##
##    def defaultGraph(self, cb):
##        cbType = cb.objectName()
##        if cbType == "cbDfltGrph":
##            if cb.isChecked() == True:
##                #print ("is selected")
##                self.gSetting.cbFrcPlt.setEnabled(False)
##                self.FrcPlts = configForceGraph(self.Q2FrcPlt, self.Q2grphVars, self.Q2pkStArr, self.Q2pkArr)
##            elif cb.isChecked() == False:
##                #print ("is unselected")
##                self.gSetting.cbFrcPlt.setEnabled(True)
##                self.Q2FrcPlt.removeItem(self.FrcPlts[0])
##                self.Q2FrcPlt.removeItem(self.FrcPlts[1])
##                self.Q2FrcPlt.removeItem(self.FrcPlts[2])
##                self.Q2FrcPlt.removeItem(self.FrcPlts[3])
##                self.Q2FrcPlt.removeItem(self.FrcPlts[4])
##                self.Q2FrcPlt.removeItem(self.FrcPlts[5])
##                self.Q2FrcPlt.removeItem(self.FrcPlts[6])
##
##    def FrcPlotCheck(self, cb):
##        cbType = cb.objectName()
##        if cbType == "cbFrcPlt":
##            if cb.isChecked() == True:
##                #print ("is selected")
##                self.gSetting.cbDfltGrph.setEnabled(False)
##                self.gSetting.cbFrcX.setEnabled(True)
##                self.gSetting.cbFrcY.setEnabled (True)
##                self.gSetting.cbFrcZ.setEnabled (True)
##                self.gSetting.cbFrcRMS.setEnabled (True)
##                self.gSetting.cbFrcPV.setEnabled (True)
##                
##            elif cb.isChecked() == False:
##                #print ("is unselected")
##                self.gSetting.cbDfltGrph.setEnabled(True)
##                self.gSetting.cbFrcX.setEnabled(False)
##                self.gSetting.cbFrcY.setEnabled (False)
##                self.gSetting.cbFrcZ.setEnabled (False)
##                self.gSetting.cbFrcRMS.setEnabled (False)
##                self.gSetting.cbFrcPV.setEnabled (False)
##    
##
##    def FrcXCheck(self, cb):
##        cbType = cb.objectName()
##        if cbType == "cbFrcX":
##            if cb.isChecked() == True:
##               # print ("is selected")
##                self.frcXPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[20],pen=(255,0,0), name="Force X Channel")#TimeStream,Force_X_Row
##            elif cb.isChecked() == False:                
##                #print ("is unselected")
##                self.Q2FrcPlt.removeItem(self.frcXPlt)
##
##    def FrcYCheck(self, cb):
##        cbType = cb.objectName()
##        if cbType == "cbFrcY":
##            if cb.isChecked() == True:
##               # print ("is selected")
##                self.frcYPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[19],pen=(0,155,0), name="Force Y Channel")#TimeStream,Force_Y_Row
##            elif cb.isChecked() == False:
##                #print ("is unselected")
##                self.Q2FrcPlt.removeItem(self.frcYPlt)
##
##    def FrcZCheck(self, cb):
##        cbType = cb.objectName()
##        if cbType == "cbFrcZ":
##            if cb.isChecked() == True:
##                #print ("is selected")
##                self.frcZPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[11],self.Q2grphVars[7],pen=(0,0,255), name="Force Z Channel")#TimeStream,Force_Z_Row                 
##            elif cb.isChecked() == False:
##                #print ("is unselected")
##                self.Q2FrcPlt.removeItem(self.frcZPlt)
##
##
##    def FrcRMSCheck(self, cb):
##        cbType = cb.objectName()
##        if cbType == "cbFrcRMS":
##            if cb.isChecked() == True:
##                #print ("is selected")
##                self.rmsPlt = self.Q2FrcPlt.plot(self.Q2grphVars[11],self.Q2grphVars[6],pen=(0,0,0), name="Force RMS Channel")#TimeStream,Force_Row
##            elif cb.isChecked() == False:
##                #print ("is unselected")
##                self.Q2FrcPlt.removeItem(self.rmsPlt)
##
##    def FrcPVCheck(self, cb):
##        cbType = cb.objectName()
##        if cbType == "cbFrcPV":
##            if cb.isChecked() == True:
##                #print ("is selected")
##                self.rmsFiltPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[12],self.Q2grphVars[22],pen=(128,0,0), name="Force Filtered(RMS)")#TimeStream,ForceButterRow
##                self.frcVlyPlt = self.Q2FrcPlt.plotItem.plot(self.Q2grphVars[3],self.Q2grphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w', name="Force Valleys")# valleyStampArr,valleyFrcArr
##                self.frcPkPlt = self.Q2FrcPlt.plotItem.plot(self.Q2pkStArr,self.Q2pkArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w', name="Force Peaks")# pkStampArr,pkFrcArr,
##            elif cb.isChecked() == False:
##                #print ("is unselected")
##                self.Q2FrcPlt.removeItem(self.rmsFiltPlt)
##                self.Q2FrcPlt.removeItem(self.frcVlyPlt)
##                self.Q2FrcPlt.removeItem(self.frcPkPlt)
                



    

    


    

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)  # F:\Pendrive Folders\QSTM Software IUDevLaptop\Qware Development 2022\Q-Ware modified ( 3-16-2022) CSV Data Play 

    Q1grphPath = "F:\Pendrive Folders\QSTM Software IUDevLaptop\Qware Development 2022\Q-Ware modified ( 3-16-2022) CSV Data Play\_Q1RawOutputChart_15-58-04_05-11-2021.csv"
    Q2grphPath = "F:\Pendrive Folders\QSTM Software IUDevLaptop\Qware Development 2022\Q-Ware modified ( 3-16-2022) CSV Data Play\_Q2RawOutputChart_14-10-05_09-03-2021.csv "
        
    #Q1grphPath = "C:\Users\ABHINABA\Documents\QSTM\Qware_DataBase\Qware Patients Folder\Abhinaba_Bhattacharjee\Abhinaba_Bhattacharjee__06-25-2020_11-02-1991\Output Data\Abhinaba_Bhattacharjee_Q-Treatment_15-05-27_07-01-2020\_Q1RawOutputChart_15-05-27_07-01-2020.csv "
    #Q2grphPath = "C:\Users\ABHINABA\Documents\QSTM\Qware_DataBase\Qware Patients Folder\Abhinaba_Bhattacharjee\Abhinaba_Bhattacharjee__06-25-2020_11-02-1991\Output Data\Abhinaba_Bhattacharjee_Q-Treatment_15-05-27_07-01-2020\_Q2RawOutputChart_15-05-27_07-01-2020.csv "
    #Q1grphVars, Q1pkStArr, Q1pkArr = qstmGAQ1.GraphShow(Q1grphPath)
    #Q2grphVars, Q2pkStArr, Q2pkArr = qstmGAQ2.GraphShow(Q2grphPath)
    #configForceGraph(ui.tab_1, Q1grphVars, Q1pkStArr, Q1pkArr)
    #configForceGraph(ui.tab_2, Q2grphVars, Q2pkStArr, Q2pkArr)

    MainWindow = QtGui.QMainWindow()
    ui = GraphMonitor()
    ui.setupUi(MainWindow, Q1grphPath , Q2grphPath)

##    Frame = QtGui.QFrame()
##    gui = Q1Graph()
##    gui.setupUI(Frame,Q1grphPath)
    
    #ui.tab_1.setTabtext("Q2 Tab")
    #print("Tab current index" + str(ui.tabWidget.currentIndex()))
    MainWindow.show()
    #Frame.show()
    sys.exit(app.exec_())
