from PyQt4 import QtGui, QtCore, QtGui 
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
#import pyqtgraph.console
#from pyqtgraph.dockarea import *
import numpy as np
import pyqtgraph as pg
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

def configGraph(obj, grphVars, pkStArr, pkArr):

    obj.plot(grphVars[11],grphVars[6],pen=(0,0,0), name="Force RMS Channel")#TimeStream,Force_Row
    #widget.plotItem.plot(grphVars[11],grphVars[13],pen=(0,0,255))#TimeStream,ForceAvgRow
    obj.plotItem.plot(grphVars[12],grphVars[22],pen=(128,0,0), name="Force Filtered(RMS)")#TimeStream,ForceButterRow
    obj.plotItem.plot(grphVars[11],grphVars[19],pen=(0,255,0), name="Force Y Channel")#TimeStream,Force_Y_Row
    obj.plotItem.plot(grphVars[11],grphVars[20],pen=(255,0,0), name="Force X Channel")#TimeStream,Force_X_Row
    obj.plotItem.plot(grphVars[11],grphVars[7],pen=(0,0,255), name="Force Z Channel")#TimeStream,Force_Z_Row
    #obj.plotItem.plot(grphVars[12],grphVars[14],pen=(12,63,18), name="Force GaussFilt Channel")# TimeShiftStream,ForceGaussRow
    #obj.plot(grphVars[11],grphVars[21],pen=(9,165,166))#TimeStream,GyroRMS
    obj.plotItem.plot(grphVars[3],grphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w', name="Force Valleys")# valleyStampArr,valleyFrcArr
    obj.plotItem.plot(pkStArr,pkArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w', name="Force Peaks")# pkStampArr,pkFrcArr,
    #obj.plot(grphVars[11],grphVars[15],pen=(131,81,193))#TimeStream,AccelRMS
    #obj.plot(grphVars[11],grphVars[16],pen=(255,255,0))#TimeStream,AccDDArr
    #obj.plot(grphVars[17],grphVars[18],pen=(255,0,255))#accSpikeStmpArr,accSpikeArr  
    



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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", " Q1 Force Chart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", " Q2 Force Chart", None))

    

        
class Q1Graph(object):

    def setupUI (self, Frame, path):

        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(1438, 860)
        
        self.gridLayout = QtGui.QGridLayout(Frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        pg.setConfigOptions(antialias=True)

        self.Q1FrcPlt=pg.PlotWidget(title=" Q1 Force Chart ", enableMouse=True, enableMenu=True)
        self.Q1FrcPlt.setMouseEnabled(x=True, y=True)
        self.Q1FrcPlt.setBackgroundBrush(QtGui.QColor(250,250,255))
        self.Q1FrcPlt.showGrid(x=True, y=True)
        self.labelStyle = {'color': '#576574', 'font-size': '14pt', 'font-style': 'Times New Roman'}
        #FrcPlt.setLabel('left',text="<span style='color: #ff0000; font-weight: bold; font-size: 12pt'>Force</span> <i>Axis</i>")
        self.Q1FrcPlt.setLabel('left',"Force (Newtons)",**self.labelStyle)
        self.Q1FrcPlt.setLabel('bottom',"Time(Seconds)",**self.labelStyle)
        self.Q1FrcLegend = self.Q1FrcPlt.addLegend(offset=(0,0)) #pen=pg.mkPen(color=(128, 0, 0), width=2), fillLevel=UpdateLevelVal, fillBrush=(128,0,0,30)

        Q1grphVars, Q1pkStArr, Q1pkArr = qstmGAQ1.GraphShow(path)
        configGraph(self.Q1FrcPlt, Q1grphVars, Q1pkStArr, Q1pkArr)
        
        #FrcLegend.paint(p.setPen = 250, 250, 255)
        
        self.gridLayout.addWidget(self.Q1FrcPlt, 0, 0, 1, 1)

class Q2Graph(object):

    def setupUI (self, Frame, path):

        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(1438, 860)
        
        self.gridLayout = QtGui.QGridLayout(Frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))

        pg.setConfigOptions(antialias=True)

        self.Q2FrcPlt=pg.PlotWidget(title=" Q2 Force Chart ", enableMouse=True, enableMenu=True)
        self.Q2FrcPlt.setMouseEnabled(x=True, y=True)
        self.Q2FrcPlt.setBackgroundBrush(QtGui.QColor(250,250,255))
        self.Q2FrcPlt.showGrid(x=True, y=True)
        self.labelStyle = {'color': '#576574', 'font-size': '14pt', 'font-style': 'Times New Roman'}
        #FrcPlt.setLabel('left',text="<span style='color: #ff0000; font-weight: bold; font-size: 12pt'>Force</span> <i>Axis</i>")
        self.Q2FrcPlt.setLabel('left',"Force (Newtons)",**self.labelStyle)
        self.Q2FrcPlt.setLabel('bottom',"Time(Seconds)",**self.labelStyle)
        self.Q2FrcLegend = self.Q2FrcPlt.addLegend(offset=(0,0)) #pen=pg.mkPen(color=(128, 0, 0), width=2), fillLevel=UpdateLevelVal, fillBrush=(128,0,0,30)

        Q2grphVars, Q2pkStArr, Q2pkArr = qstmGAQ2.GraphShow(path)
        configGraph(self.Q2FrcPlt, Q2grphVars, Q2pkStArr, Q2pkArr)
        
        #FrcLegend.paint(p.setPen = 250, 250, 255)
        
        self.gridLayout.addWidget(self.Q2FrcPlt, 0, 0, 1, 1)
    

    


    

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)   
    
        
    Q1grphPath = "C:\Users\ABHINABA\Documents\QSTM\Qware_DataBase\Qware Patients Folder\Abhinaba_Bhattacharjee\Abhinaba_Bhattacharjee__06-25-2020_11-02-1991\Output Data\Abhinaba_Bhattacharjee_Q-Treatment_15-05-27_07-01-2020\_Q1RawOutputChart_15-05-27_07-01-2020.csv "
    Q2grphPath = "C:\Users\ABHINABA\Documents\QSTM\Qware_DataBase\Qware Patients Folder\Abhinaba_Bhattacharjee\Abhinaba_Bhattacharjee__06-25-2020_11-02-1991\Output Data\Abhinaba_Bhattacharjee_Q-Treatment_15-05-27_07-01-2020\_Q2RawOutputChart_15-05-27_07-01-2020.csv "
    #Q1grphVars, Q1pkStArr, Q1pkArr = qstmGAQ1.GraphShow(Q1grphPath)
    #Q2grphVars, Q2pkStArr, Q2pkArr = qstmGAQ2.GraphShow(Q2grphPath)
    #configGraph(ui.tab_1, Q1grphVars, Q1pkStArr, Q1pkArr)
    #configGraph(ui.tab_2, Q2grphVars, Q2pkStArr, Q2pkArr)

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
