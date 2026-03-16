#from matplotlib.cbook import get_sample_data
import csv, sys;
from math import *
from scipy import signal
import os, shutil, sys, ctypes, win32api
import glob, csv, errno, psutil
import ctypes.wintypes
from PyQt4 import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
#import matplotlib.pyplot as plt

#aCntr=0;fCntr=0;FrcArr=[];AccArr=[];
'''lastFrcData = 0.0; lastGradSt = 0; gradSt=0;     
lastTimeData = 0.0001;lastAccRms = 1
upCnt=0;dwnCnt=0;pkCnt=0;valleyCnt=0;
BurstSt = 0;lastBurstSt=0;arrcnt=0;arrGcnt=0;  
CSV1_Row=[]; flag = 1
bStrtArr=[]; bEndArr=[];processCSV_Row=[];
Force_Row=[];PitchArr=[];YawArr=[];RollArr=[];FrcZarr = []
ForceAvgRow=[];ForceGaussRow=[];
upCntArr=[];dwnCntArr=[];
pkFrcArr=[];valleyFrcArr=[];
timeStamp=[];valleyStampArr=[];pkStampArr=[];
TimeStream = [];TimeShiftStream=[];accRMSdiffGaussAvg=[];
AccelRMS = [];accRMSdiff=[];accRMSdiffAvg =[]; accSpikeArr=[];
FrcArr = [];AccArr = [];TimeDiffArr=[];AccDDArr=[];
aCntr=0;fCntr=0;accPkStmpArr=[];accPeakArr =[];accSpikeStmpArr=[];
lastAccDiff =0;accPeak = 0.0;accPeakStamp = 0.05
#long axSq, aySq, azSq;
#float rmsAcc'''

def PathFinder():
    processCSV_Row=[];
    CSIDL_PERSONAL= 5
    SHGFP_TYPE_CURRENT= 0
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
    DefaultDestinationPath=''
    DefaultSearchPath = str(buf.value)

    processFilePath = DefaultSearchPath+"\QSTM\QSTM_Temp\Process_Data\ProcessQ1data.csv"
    if os.path.exists(processFilePath):    
        with open(processFilePath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for rows in readCSV:
                line= rows         
                processCSV_Row.append(line)

        pathFound=processCSV_Row
        print ("Path Found " + str(pathFound))
        return pathFound
    else:
        print ("No Path Found")

def GraphPathFinder():
    processCSV_Row=[];
    CSIDL_PERSONAL= 5
    SHGFP_TYPE_CURRENT= 0
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
    DefaultDestinationPath=''
    DefaultSearchPath = str(buf.value)

    processFilePath = DefaultSearchPath+"\QSTM\QSTM_Temp\Process_Data\GraphAnalysisData.csv"
    if os.path.exists(processFilePath):    
        with open(processFilePath) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for rows in readCSV:
                line= rows         
                processCSV_Row.append(line)

        pathFound=processCSV_Row
        print ("Path Found " + str(pathFound))
        return pathFound
    else:
        print ("No Path Found")



def ButterWorthFilter():
    #Creation of the Frequency Domain ButterWorth filter
    sF = 100 # Sampling Frequency
    cutOff = 11 # Cutoff frequency
    nyq = 0.5 * sF # Nyquist Rate
    N  = 10    # Filter order
    FcNorm = cutOff / nyq # Cutoff frequency normal
    b, a = signal.butter(N, FcNorm)# butter worth Filter
    #print ("Numerator is " + str(b) +"\n")
    #print ("denomenator is " + str(a) +"\n")   

    return b, a


def getPascalTriangleRow(nSize):
    global pRow, pTriangle
    pRow = []
    pTriangle = []
    n= nSize
    element = 0
    for i in range(0,(n+1)):
        pRow = []
        for j in range(0,i):
            if (i==0):
                element = 1
                pRow.append(element)
                break
            elif(j==0):
                element = 1
            elif(j==(i-1)):
                element = 1
            elif((j>=1) and (j<i)):
                element = pTriangle[i-1][j-1]+pTriangle[i-1][j]
            pRow.append(element)
        #print(pRow)
        #if(len(pRow)>1):
            #pRow = list(np.array(pRow)*(sqrt((len(pRow))-1)/(2**((len(pRow))-1))))
        pTriangle.append(pRow)
    #print("Total Triangle")
    #print(pTriangle)
    return pRow

def rmsAccelData(Ax, Ay, Az):
    #long axSq, aySq, azSq;
    #float rmsAcc
    axSq = Ax*Ax; aySq = Ay*Ay; azSq = Az*Az;
    rmsAcc = sqrt(axSq+aySq+azSq)
    return rmsAcc
def getForceArray(val):
    global FrcArr,fCntr 
    if fCntr >= 100:
        fcntr = 99
        FrcArr.pop(0)
        FrcArr.append(val)
    else:
        FrcArr.append(val)
    fCntr+=1
    return FrcArr

def getAccArray(val):
    global AccArr,aCntr 
    if aCntr >= 500:
        acntr = 499
        AccArr.pop(0)
        AccArr.append(val)
    else:
        AccArr.append(val)
    aCntr+=1
    return AccArr    
    
    
def getAvg(Arr,avgCnt):
    #global arrcnt, avgArr
    Sum = 0
    Size = len(Arr)
    if(Size<=avgCnt):
        for i in range(Size):
            Sum+=Arr[i]
        if(Size<1):
            Avg =0
        else:
            Avg = Sum/Size
    else:
        for i in range((Size-avgCnt),Size):
            Sum+=Arr[i]
        Avg = Sum/avgCnt    
    return Avg
        


def getAvgGauss (Arr, gaussCnt):
    #global arrGcnt,avgGaussArr;
    Sum =0
    gWtCtr=0
    weightSum =0.001    
    gSize = len(Arr)
    if(gSize<=gaussCnt):
        gaussWtRow = pTriangle[gSize]
        for i in range(gSize):
            Sum+=Arr[i]*gaussWtRow[i]
            weightSum+=gaussWtRow[i]
            #gWtCtr+=1
        gaussAvg = Sum/weightSum
    else:
        gaussWtRow = pTriangle[gaussCnt]
        for i in range((gSize-gaussCnt),gSize):
            Sum+=Arr[i]*gaussWtRow[i-(gSize-gaussCnt)]
            weightSum+=gaussWtRow[i-(gSize-gaussCnt)]
            #gWtCtr+=1
        gaussAvg = Sum/weightSum    
    return gaussAvg


def noisyHumpReduction(pkArr,pkStArr,vArr,vStArr):
    global iArr;
    hillSlopeArr=[]; lstRatio=0; ctr=0; iArr =[]
    vArr.append(4)
    for i in range (0,len(pkArr)):
        riseDiff = pkArr[i]-vArr[i]
        fallDiff = pkArr[i]-vArr[i+1]
        hillSlopeRatio = riseDiff/fallDiff
        ratioDiff = round((lstRatio-hillSlopeRatio),1)
        hillSlopeArr.append(hillSlopeRatio)
        if(riseDiff>1 or fallDiff>1):
            ctr+=1
            if((ratioDiff>1) and ((int)(ratioDiff) == (int)(lstRatio))):
                print(i)
                indx = pkArr.index(min(pkArr[i],pkArr[i-1]))
                iArr.append(indx)
                continue
            lstRatio = hillSlopeRatio

        else:
            iArr.append(i)
        

    iArr = sorted(iArr, key=int, reverse=True)
    print(hillSlopeArr)
    for j in range (0,len(iArr)):
        pkArr.pop(iArr[j])
        pkStArr.pop(iArr[j])
    
    
            
    vArr.pop(len(vArr)-1)
    return iArr


def PkRiseFallDiffAvg(pArr,vArr):
    rDiffArr=[];fDiffArr=[]
    vArr.append(4)
    for m in range (0,len(pArr)):
        riseDiff = pArr[m]-vArr[m]
        fallDiff = pArr[m]-vArr[m+1]
        hillSlopeRatio = riseDiff/fallDiff
        if(riseDiff>0.8 or fallDiff>0.8):
        #if(riseDiff>rfDiffAvg[0] or fallDiff>rfDiffAvg[1]):
            #ctr+=1
            if (hillSlopeRatio>0.5)and (hillSlopeRatio<2):
                rDiffArr.append(riseDiff)
                fDiffArr.append(fallDiff)
            elif (hillSlopeRatio>2):
                rDiffArr.append(riseDiff)
                #print(i)
            elif(hillSlopeRatio< 0.5):
                fDiffArr.append(fallDiff)
        

    rDiffAvg = round((getAvg(rDiffArr,len(rDiffArr))),2)
    fDiffAvg = round((getAvg(fDiffArr,len(fDiffArr))),2)
    rDAvg = (rDiffAvg*9)/20
    fDAvg = (fDiffAvg*9)/20
    vArr.pop(len(vArr)-1)
    return rDAvg,fDAvg
    

def HumpReduction(pkArr,pkStArr,vArr,vStArr):
    #global iArr, flag, lstFlag, flag, hillSlopeArr
    hillSlopeArr=[]; lstRatio=0; ctr=0; iArr =[]; fPkArr=[]; lstFlag =1; fPkValArr=[];flag=1
    rfDiffAvg = PkRiseFallDiffAvg(pkArr,vArr)
    vArr.append(4)
    for i in range (0,len(pkArr)):
        riseDiff = pkArr[i]-vArr[i]
        fallDiff = pkArr[i]-vArr[i+1]
        hillSlopeRatio = riseDiff/fallDiff
        ratioDiff = round((lstRatio-hillSlopeRatio),1)
        hillSlopeArr.append(hillSlopeRatio)
        #if(riseDiff>0.9 or fallDiff>0.9):
        if(riseDiff>rfDiffAvg[0] or fallDiff>rfDiffAvg[1]):
            ctr+=1
            if (hillSlopeRatio>0.5)and (hillSlopeRatio<2):
                continue
            elif (hillSlopeRatio>2):
                flag = 1
                #print(i)
            elif(hillSlopeRatio< 0.5):
                flag = 0
            
            if (flag>lstFlag):
                #print(fPkArr)                
                if len(fPkArr)>1:
                    maxPeak = max(fPkValArr)
                    indx = fPkValArr.index(maxPeak)
                    fPkArr.pop(indx)
                    #print("indx"+str(indx))
                    for k in range(0,len(fPkArr)):
                        iArr.append(fPkArr[k])
                elif len(fPkArr) is 1:
                    iArr.append(fPkArr[0])
                #iArr.append(fPkArr)
                fPkArr = []
                fPkValArr=[]
                
            fPkArr.append(i)
            fPkValArr.append(pkArr[i])
            lstRatio = hillSlopeRatio
            lstFlag = flag   

        else:
            iArr.append(i)
    #print(fPkArr)
    if len(fPkArr)>1:
        for l in range(0,len(fPkArr)):
            iArr.append(fPkArr[l])
        maxPeak = max(fPkValArr)
        indx = fPkValArr.index(maxPeak)
        iArr.pop(iArr.index(fPkArr[indx]))
    elif len(fPkArr) is 1:
        iArr.append(fPkArr[0])
    
    iArr = sorted(iArr, key=int, reverse=True)
    #print(hillSlopeArr)
    for j in range (0,len(iArr)):
        pkArr.pop(iArr[j])
        pkStArr.pop(iArr[j])
    
    
            
    vArr.pop(len(vArr)-1)
    return iArr

'''def removeFaultypeaks(pkArr,pkStArr,bArr):
    for j in range (0,len(bArr)):
        pkArr.pop(bArr[j])
        pkStArr.pop(bArr[j])
    return pkArr, pkStArr'''

def csvReadWholeFile(path):
    CSV1_Row=[];rstStArr =[];rstEndArr =[];lstRst =0;TimeArr = []; cntr = 0
    with open(path) as csvfile1:
        readCSV1 = csv.reader(csvfile1, delimiter=',')
        for row in readCSV1:
            #ROW1= row            
            if (str(row[12]) == "RST"):
                print("Skip")
                continue
            rst = (int)(row[12])
            cntr+=1
            if (rst<lstRst):
                rstIndex = cntr
                rstStrtTime = CSV1_Row[cntr-2][0]
                rstStArr.append(rstStrtTime)
                rstEndTime = row[0]
                rstEndArr.append(rstEndTime)                
            #rst = (row[12])
           
            CSV1_Row.append(row)
            TimeArr.append(row[0])
            lstRst = rst
           
##    if (len(rstEndArr)>len(rstStArr)):
##        rstStArr.append(TimeArr[len(TimeArr)-1])

    print(rstStArr,rstEndArr)
    return CSV1_Row,rstStArr,rstEndArr,TimeArr

    

def csvReadFile(path):
    CSV1_Row=[];rstStArr =[];rstEndArr =[];lstRst =1;TimeArr = []
    with open(path) as csvfile1:
        readCSV1 = csv.reader(csvfile1, delimiter=',')
        for row in readCSV1:
            #ROW1= row            
            if (str(row[12]) == "RST"):
                print("Skip")
                continue
            rst = (int)(row[12])
            #rst = (row[12])
            if (rst>lstRst):
                rstStrtTime = row[0]
                rstStArr.append(rstStrtTime)
            elif(rst<lstRst):
                rstEndTime = row[0]
                rstEndArr.append(rstEndTime)
            CSV1_Row.append(row)
            TimeArr.append(row[0])
            lstRst = rst
##    if (len(rstEndArr)>len(rstStArr)):
##        rstStArr.append(TimeArr[len(TimeArr)-1])

    print(rstStArr,rstEndArr)
    return CSV1_Row,rstStArr,rstEndArr,TimeArr


def CalculateReportTable(n,bStrtArr,bEndArr,Force_Row,FrcZarr,FrcYarr,FrcXarr,PitchArr,YawArr,RollArr,TimeStream,pkFrcArr):# Calculate Params For Total Graph
    fz = [];fy = [];fx = [];fRez=[];p=[];r=[];y=[];TotalActTime=0; FullTime=0; 
##    grphData = csvReadFile(p)
##    GraphAnalyse(p)    
##    noisyHumpReduction(pkFrcArr,pkStampArr,valleyFrcArr,valleyStampArr)
    if (len(bStrtArr)>0):        
        for i in range (0, len(bStrtArr)):
            start = TimeStream.index(bStrtArr[i])
            end = TimeStream.index(bEndArr[i])
            FrcRezAvg = getAvg(Force_Row[start:(end+1)],len(Force_Row[start:(end+1)]))
            FrcZavg = getAvg(FrcZarr[start:(end+1)],len(FrcZarr[start:(end+1)]))
            FrcYavg = getAvg(FrcYarr[start:(end+1)],len(FrcYarr[start:(end+1)]))
            FrcXavg = getAvg(FrcXarr[start:(end+1)],len(FrcXarr[start:(end+1)]))
            pitchAvg = getAvg(PitchArr[start:(end+1)],len(PitchArr[start:(end+1)]))
            YawAvg = getAvg(YawArr[start:(end+1)],len(YawArr[start:(end+1)]))
            RollAvg = getAvg(RollArr[start:(end+1)],len(RollArr[start:(end+1)]))
            Time = bEndArr[i]-bStrtArr[i]
            fz.append(FrcZavg);fRez.append(FrcRezAvg);
            fy.append(FrcYavg);fx.append(FrcXavg);
            r.append(RollAvg);p.append(pitchAvg);y.append(YawAvg);
            TotalActTime += Time
            #print("Force Avg of Burst "+str(i+1)+" is "+str(FrcRezAvg))
            #print("Force Z Avg of Burst "+str(i+1)+" is "+str(FrcZavg))
            #print("Yaw Avg of Burst "+str(i+1)+" is "+str(YawAvg))
            #print("Pitch Avg of Burst "+str(i+1)+" is "+str(pitchAvg))
            #print("Roll Avg of Burst "+str(i+1)+" is "+str(RollAvg))
        BurstNumber = len(bStrtArr)
        StrokeNumber = round(len(pkFrcArr),5)
        StrokeFrequency = round((StrokeNumber/TotalActTime),5)
        MaxPeak =round(max(pkFrcArr),5)
        AvgPeak = round((getAvg(pkFrcArr,StrokeNumber)),5)    
        FRavg = round((getAvg(fRez,len(fRez))),5); FZavg = round((getAvg(fz,len(fz))),5);
        FYavg = round((getAvg(fy,len(fy))),5);FXavg = round((getAvg(fx,len(fx))),5);
        pAvg = round((getAvg(p,len(p))),5);yAvg= round((getAvg(y,len(y))),5);rAvg = round((getAvg(r,len(r))),5)
        FullTime = round((bEndArr[(len(bEndArr)-1)] - bStrtArr[0]),5)
        TotalActTime = round(TotalActTime,5)
       # if (BurstNumber>StrokeNumber):
            #StrokeNumber = BurstNumber
##        print("Total active time of Rst "+str(n+1)+" is "+str(TotalActTime))
##        print("Burst number of Rst "+str(n+1)+" is " + str(BurstNumber))
##        print("Stroke number of Rst "+str(n+1)+" is " + str(StrokeNumber))
##        print("Stroke frequency of Rst "+str(n+1)+" is " + str(StrokeFrequency))
##        print("Maximum Peak of Rst "+str(n+1)+" is " + str(MaxPeak))
##        print("Average Peak of Rst "+str(n+1)+" is " + str(AvgPeak))
##        print("F Rez avg of Rst "+str(n+1)+" is " + str(FRavg))
##        print("F Z avg of Rst "+str(n+1)+" is " + str(FZavg))
##        print("P avg of Rst "+str(n+1)+" is " + str(pAvg))
##        print("R avg of Rst "+str(n+1)+" is " + str(rAvg))
##        print("Y avg of Rst "+str(n+1)+" is " + str(yAvg))
##        print("Full Session time of Rst "+str(n+1)+" is "+str(FullTime))
        Parameters = [FXavg,FYavg,FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,round(FullTime,5),pAvg,rAvg,yAvg,round(TotalActTime,5)]    
        return Parameters
    else:
        Parameter = [0]        
        return Parameter



def CalculateVisTable(bStrtArr,bEndArr,Force_Row,FrcZarr,PitchArr,YawArr,RollArr,TimeStream,pkFrcArr): # Calculate Params For Every Reset Graph
    fz = [];fRez=[];p=[];r=[];y=[];TotalActTime=0;FullTime=0 
##    grphData = csvReadFile(p)
##    GraphAnalyse(p)    
##    noisyHumpReduction(pkFrcArr,pkStampArr,valleyFrcArr,valleyStampArr)
    if (len(bStrtArr)>0):        
        for i in range (0, len(bStrtArr)):
            start = TimeStream.index(bStrtArr[i])
            end = TimeStream.index(bEndArr[i])
            FrcRezAvg = getAvg(Force_Row[start:(end+1)],len(Force_Row[start:(end+1)]))
            FrcZavg = getAvg(FrcZarr[start:(end+1)],len(FrcZarr[start:(end+1)]))
            pitchAvg = getAvg(PitchArr[start:(end+1)],len(PitchArr[start:(end+1)]))
            YawAvg = getAvg(YawArr[start:(end+1)],len(YawArr[start:(end+1)]))
            RollAvg = getAvg(RollArr[start:(end+1)],len(RollArr[start:(end+1)]))
            Time = bEndArr[i]-bStrtArr[i]
            fz.append(FrcZavg);fRez.append(FrcRezAvg);
            r.append(RollAvg);p.append(pitchAvg);y.append(YawAvg);
            TotalActTime += Time
            #print("Force Avg of Burst "+str(i+1)+" is "+str(FrcRezAvg))
            #print("Force Z Avg of Burst "+str(i+1)+" is "+str(FrcZavg))
            #print("Yaw Avg of Burst "+str(i+1)+" is "+str(YawAvg))
            #print("Pitch Avg of Burst "+str(i+1)+" is "+str(pitchAvg))
            #print("Roll Avg of Burst "+str(i+1)+" is "+str(RollAvg))
        BurstNumber = len(bStrtArr)
        StrokeNumber = round(len(pkFrcArr),2)
        StrokeFrequency = round((StrokeNumber/TotalActTime),2)
        MaxPeak =round(max(pkFrcArr),2)
        AvgPeak = round((getAvg(pkFrcArr,StrokeNumber)),2)    
        FRavg = round((getAvg(fRez,len(fRez))),2); FZavg = round((getAvg(fz,len(fz))),2);
        pAvg = round((getAvg(p,len(p))),2);yAvg= round((getAvg(y,len(y))),2);rAvg = round((getAvg(r,len(r))),2)
        FullTime = bEndArr[(len(bEndArr)-1)] - bStrtArr[0]
        #if (BurstNumber>StrokeNumber):
            #StrokeNumber = BurstNumber
        #print("Total active time "+str(TotalActTime))
        #print("Burst number is " + str(BurstNumber))
        ##print("Stroke number is " + str(StrokeNumber))
        #print("Stroke frequency is " + str(StrokeFrequency))
        #print("Maximum Peak is " + str(MaxPeak))
        #print("Average Peak is " + str(AvgPeak))
        #print("F Rez avg is " + str(FRavg))
        #print("F Z avg is " + str(FZavg))
        #print("P avg is " + str(pAvg))
        #print("R avg is " + str(rAvg))
        #print("Y avg is " + str(yAvg))
        #print("Full Session time "+str(FullTime))
        Parameters = [FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,pAvg,rAvg,yAvg,TotalActTime]    
        return Parameters
    else:
        Parameter = [0]        
        return Parameter
            
def GraphAnalyse(readGraph):
    #global Force_Row, ForceAvgRow, ForceGaussRow, PitchArr, AccelRMS,YawArr,RollArr,FrcZarr
    #global timeStamp, TimeStream, TimeShiftStream, TimeDiffArr;        
    #global accRMSdiff, accRMSdiffAvg, accRMSdiffGaussAvg, AccDDArr,accSpikeArr,accSpikeStmpArr
    #global pkFrcArr,pkStampArr,valleyFrcArr,valleyStampArr;
    #global lastFrcData, lastGradSt, lastBurstSt, lastAccRms, lastTimeData,lastAccDiff;
    #global gradSt, upCnt, valleyCnt, dwnCnt, pkCnt, bStrtArr,bEndArr
    global aCntr,fCntr,FrcArr,AccArr;

    lastFrcData = 0.0; lastFrcButtrData=0.0; lastGradSt = 0; gradSt=0;     
    lastTimeData = 0.0001;lastAccRms = 1
    upCnt=0;dwnCnt=0;pkCnt=0;valleyCnt=0;
    BurstSt = 0;lastBurstSt=0;arrcnt=0;arrGcnt=0;  
    CSV1_Row=[]; flag = 1
    bStrtArr=[]; bEndArr=[];processCSV_Row=[];
    Force_Row=[];PitchArr=[];YawArr=[];RollArr=[];
    FrcZarr = [];FrcYarr = [];FrcXarr = []
    ForceAvgRow=[];ForceGaussRow=[];
    upCntArr=[];dwnCntArr=[];
    pkFrcArr=[];valleyFrcArr=[];
    timeStamp=[];valleyStampArr=[];pkStampArr=[];
    TimeStream = [];TimeShiftStream=[];accRMSdiffGaussAvg=[];
    AccelRMS = [];accRMSdiff=[];accRMSdiffAvg =[]; accSpikeArr=[];
    FrcArr = [];AccArr = [];TimeDiffArr=[];AccDDArr=[]; GyroRMSArr=[]
    aCntr=0;fCntr=0;accPkStmpArr=[];accPeakArr =[];accSpikeStmpArr=[];
    lastAccDiff =0;accPeak = 0.0;accPeakStamp = 0.05

    ButterFilt = ButterWorthFilter()
    readGraph = np.array(readGraph)
    RezFrcArray = list(readGraph[: ,4].astype(np.float))
    
    ButtrFiltFrcArr = signal.lfilter(ButterFilt[0], ButterFilt[1],RezFrcArray )

    #print(len(readGraph))
    #print(len(ButtrFiltFrcArr))



    
    #readGraph = csvReadFile(path) 
#for i in range(2, 2940):
    for i in range(2, len(readGraph)):
        ForceData=float(readGraph[i][4])
        ForceZdata=float(readGraph[i][3])
        ForceYdata=float(readGraph[i][2])
        ForceXdata=float(readGraph[i][1])
        PitchData=float(readGraph[i][6])
        YawData=float(readGraph[i][5])        
        RollData=float(readGraph[i][7])
        TimeData = float(readGraph[i][0])
        accRMS = float(readGraph[i][11])
        gyroRMS = float(readGraph[i][13])
        #accRMS = rmsAccelData((float)(CSV1_Row[i][8]),(float)(CSV1_Row[i][9]),(float)(CSV1_Row[i][10]))
        FrcButtrData = ButtrFiltFrcArr[i]
        timeDiff = TimeData-lastTimeData;
##        if(timeDiff == 0):
##            timeDiff = 0.001;
        gyroRMS = gyroRMS/100
        accDiff = (accRMS-lastAccRms)/(timeDiff*100)
        accDoubleDiff = accDiff-lastAccDiff
        arrFrc = getForceArray(ForceData)
        arrAcc = getAccArray(accDiff)
        forceAvgData = getAvg(arrFrc,25)
        forceGaussData = getAvgGauss(arrFrc,25)
        accDiffavg = getAvg(arrAcc,10)
        accDiffGaussAvg = getAvgGauss(arrAcc,25)   
        #print("abc")
        if(forceGaussData>4):
            BurstSt = 1

            if(FrcButtrData>lastFrcButtrData):           
            #if(forceGaussData>lastFrcData):
                gradSt = 1
                upCnt=upCnt+1
                valleyFrc=lastFrcButtrData
                valleyStamp=TimeData-timeDiff-0.15

            elif(FrcButtrData<lastFrcButtrData):                         
            #elif(forceGaussData<lastFrcData):
                gradSt = 0
                peakFrc=lastFrcButtrData
                dwnCnt=dwnCnt+1
                peakStamp=TimeData-timeDiff-0.15

            if ((accDoubleDiff)<(lastAccDD)):
                accPeak = (lastAccDD)
                accPeakStamp = TimeData-timeDiff

            if ((accDoubleDiff)>(lastAccDD)):
                accValley = (lastAccDD)
                accValleyStamp = TimeData-timeDiff

            accSpike = abs(accValley - accPeak)
            accSpikeStmp = TimeData-timeDiff
        else:
            BurstSt = 0
            accPeak = 0.0
            accValley=0.0
            accSpike = 0.0
            accPeakStamp = TimeData-timeDiff
            accValleyStamp = TimeData-timeDiff
            accSpikeStmp = TimeData-timeDiff

    ## finding burst start and end timestamps

        if(BurstSt>lastBurstSt):
            bStrtStmp = TimeData-timeDiff
            bStrtArr.append(bStrtStmp)

        elif(BurstSt<lastBurstSt):
            bEndStmp = TimeData-timeDiff
            bEndArr.append(bEndStmp)
            #valleyFrcArr.append(0.2)
            #valleyStampArr.append(bEndStmp)

            
    ##finding peaks and valleys 
        if(BurstSt==1):
            bStrtStmp=i-1
            if(gradSt<lastGradSt):
                pkCnt=pkCnt+1
                upCntArr.append(upCnt)
                pkFrcArr.append(peakFrc)
                pkStampArr.append(peakStamp)
                upCnt=0
            elif(gradSt>lastGradSt):
                valleyCnt=valleyCnt+1
                dwnCntArr.append(dwnCnt)
                valleyFrcArr.append(valleyFrc)
                valleyStampArr.append(valleyStamp)
                dwnCnt=0
            accPeakArr.append(accPeak)
            accSpikeArr.append(accSpike)
            accPkStmpArr.append(accPeakStamp)
            accSpikeStmpArr.append(accSpikeStmp)
        elif(BurstSt<1):
            #valleyFrcArr.append(0.2)
            bEndStmp=TimeData-timeDiff
            accPeakArr.append(accPeak)
            accPkStmpArr.append(accPeakStamp)
            #valleyStampArr.append(bEndStmp)
        
        Force_Row.append(ForceData)
        FrcZarr.append(ForceZdata)
        FrcYarr.append(ForceYdata)
        FrcXarr.append(ForceXdata)
        ForceAvgRow.append(forceAvgData)
        ForceGaussRow.append(forceGaussData)
        PitchArr.append(PitchData)
        YawArr.append(YawData);
        RollArr.append(RollData)
        AccelRMS.append(accRMS)
        GyroRMSArr.append(gyroRMS)
        timeStamp.append(i)
        TimeStream.append(TimeData)
        TimeShiftStream.append(TimeData-(1*0.15))
        TimeDiffArr.append(timeDiff)
        accRMSdiff.append(accDiff)
        accRMSdiffAvg.append(abs(accDiffavg))
        accRMSdiffGaussAvg.append(abs(accDiffGaussAvg))
        AccDDArr.append(accDoubleDiff)        
        lastFrcData = forceGaussData
        lastFrcButtrData = FrcButtrData
        lastGradSt = gradSt
        lastBurstSt = BurstSt
        lastAccRms=accRMS
        lastTimeData = TimeData
        lastAccDiff = accDiff
        lastAccDD = accDoubleDiff

    ButtrFiltFrcArr = list(ButtrFiltFrcArr[2:len(ButtrFiltFrcArr)])

    return pkFrcArr,pkStampArr,valleyFrcArr,valleyStampArr,bStrtArr,bEndArr,\
           Force_Row,FrcZarr,PitchArr,YawArr,RollArr,TimeStream,TimeShiftStream,\
           ForceAvgRow,ForceGaussRow,AccelRMS,AccDDArr,accSpikeStmpArr,accSpikeArr,FrcYarr,FrcXarr,GyroRMSArr,ButtrFiltFrcArr

    
#bStrtArr,bEndArr,Force_Row,FrcZarr,PitchArr,YawArr,RollArr,TimeStream    
##plt.plot(timeStamp,Force_Row,lw=2.0,color='#1f77b4')
##plt.plot(pkStampArr,pkFrcArr,'ro')
##plt.plot(valleyStampArr,valleyFrcArr,'bo')
##plt.plot(timeStamp,PitchArr,lw=1.5,color='#17becf')
###,count,CSV3_Row,lw=2.5,color='#9edae5')
###plt.plot(count,CSV2_Row,'k')
##plt.show()
##nhrArr = noisyHumpReduction(pkFrcArr,pkStampArr,valleyFrcArr,valleyStampArr)
##print(nhrArr)

def TableDataCalculation(FilePath):
    csvRows = csvReadWholeFile(FilePath)
    print (csvRows[2])
    if (len(csvRows[2])>0):
        rstStopTmstmp = csvRows[2][len(csvRows[2])-1]
    else:
        rstStopTmstmp = csvRows[3][3]
        
    rstIndex = csvRows[3].index(rstStopTmstmp)
    PascalTriangle = getPascalTriangleRow(30)
    graphRSTChart = csvRows[0][rstIndex:]
    grphVars = GraphAnalyse(graphRSTChart)
    HumpReduction(grphVars[0],grphVars[1],grphVars[2],grphVars[3])
    param = CalculateVisTable(grphVars[4],grphVars[5],grphVars[6],grphVars[7],grphVars[8],grphVars[9],grphVars[10],grphVars[11],grphVars[0])
    return param

def listAppend(arr1,arr2):
    for s in range(0,len(arr2)):
        arr1.append(arr2[s])
    return arr1
    

def SessionGraphCalc(pathFile):
    FxArr=[];FyArr=[];FzArr=[];FRezArr=[];pArr=[];rArr=[];yArr=[];strkNum=0;brstNum=0;FTime =0;
    FpkArr =[];FpkStArr =[]; ReportParams = [];
    
##    app = QtGui.QApplication(sys.argv)   
##
##    widget = pg.PlotWidget(title = "Plotting")
##    widget.setWindowTitle("CSV_Graph")
##    widget.setBackgroundBrush(QtGui.QColor(250,250,255))    
##    pg.setConfigOptions(antialias=True)

    
    csvRows = csvReadFile(pathFile)
    PascalTriangle = getPascalTriangleRow(60)
    #PascalTriangle = list(np.array(getPascalTriangleRow(99))*(sqrt(98)*(0.1)/(2**98)))
    rstStTimeArr = csvRows[1]; rstEndTimeArr = csvRows[2]
    FullgraphVars = GraphAnalyse(csvRows[0])
    paramRow = ["Sessions","AvgForc(X)","AvgForce(Y)","AvgForce(Z)","AvgForce(RMS)","MaxPeakForce","AvgPeakForce",
                "BurstNumber","StrokeNumber","StrokeFrequency","FullSessionTime","AvgPitchAngle","AvgRollAngle","AvgYawAngle","Contact/ActiveTime"]
    
    ReportParams.append(paramRow)
    for n in range (0,len(rstEndTimeArr)):
        startIndx = csvRows[3].index(rstEndTimeArr[n])
        if n >= (len(rstEndTimeArr)-1):
            endIndx = (len(csvRows[3])-2)
        else:
            endIndx = csvRows[3].index(rstStTimeArr[n])#pkArr,pkStArr,vArr,vStArr
        grphVars = GraphAnalyse(csvRows[0][startIndx:(endIndx+1)]) #FXavg,FYavg,FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,FullTime,pAvg,rAvg,yAvg,ContactTime
        if (len(grphVars[4])<1):
            continue
        try:
            lstBrstStmp = grphVars[5][len(grphVars[5])-1]
        except IndexError:
            continue
        nhrArr = HumpReduction(grphVars[0],grphVars[1],grphVars[2],grphVars[3])
        print(nhrArr)
        #lstBrstStmp = grphVars[5][len(grphVars[5])-1]
        FpkArr = listAppend(FpkArr,grphVars[0])
        FpkStArr = listAppend(FpkStArr,grphVars[1])
        param = CalculateReportTable(n,grphVars[4],grphVars[5],grphVars[6],grphVars[7],grphVars[19],grphVars[20],grphVars[8],grphVars[9],grphVars[10],grphVars[11],grphVars[0])        
        strkNum += param[7];brstNum +=param[6];FTime+=param[9]
        FxArr.append(param[0]);FyArr.append(param[1]);FzArr.append(param[2]);FRezArr.append(param[3]);pArr.append(param[10]);rArr.append(param[11]);yArr.append(param[12]);
        param.insert(0,("Subsession "+(str)((int)(n)+1)))
        ReportParams.append(param)
    FXavg = round((getAvg(FxArr,len(FxArr))),2);FYavg = round((getAvg(FyArr,len(FyArr))),2);FZavg = round((getAvg(FzArr,len(FzArr))),2);FRezAvg = round((getAvg(FRezArr,len(FRezArr))),2);
    Pavg = round((getAvg(pArr,len(pArr))),2);Ravg = round((getAvg(rArr,len(rArr))),2);Yavg = round((getAvg(yArr,len(yArr))),2);
    #print(FpkStArr)
    #pkRejectArr = sorted(pkRejectArr, key=int, reverse=True)
    #print(pkRejectArr)
    #print(hillSlopeArr)
##    for j in range (0,len(pkRejectArr)):
##        FullgraphVars[0].pop(pkRejectArr[j])
##        FullgraphVars[1].pop(pkRejectArr[j])

    maxPeak = round(max(FullgraphVars[0]),2)
    avgPeak = round(getAvg(FpkArr,len(FpkArr)),2)
    numStrk = len(FpkArr)
    StrkFreq = round((numStrk/FTime),3) #[FXavg,FYavg,FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,FullTime,pAvg,rAvg,yAvg,TotalActTime]
    #FullSessionTime = round((float)(rstStTimeArr[len(rstStTimeArr)-1])- (float)(rstEndTimeArr[0]),2)
    FullSessionTime = round(((float)(lstBrstStmp)- (float)(rstEndTimeArr[0])),2);

    SessionParams = ["Total Session",FXavg,FYavg,FZavg,FRezAvg,maxPeak,avgPeak,brstNum,numStrk,StrkFreq,FullSessionTime,Pavg,Ravg,Yavg,round(FTime,2)]
    ReportParams.append(SessionParams)

    print("Total active time "+str(FTime))
    print("Total Burst number is " + str(brstNum))
    print("Calculated Stroke number is " + str(strkNum))
    print("Total Stroke number is " + str(numStrk))
    print("Stroke frequency is " + str(StrkFreq))
    print("Maximum Peak is " + str(maxPeak))
    print("Average Peak is " + str(avgPeak))
    print("F X avg is " + str(FXavg))
    print("F Y avg is " + str(FYavg))
    print("F Z avg is " + str(FZavg))
    print("F Rez avg is " + str(FRezAvg))    
    print("P avg is " + str(Pavg))
    print("R avg is " + str(Ravg))
    print("Y avg is " + str(Yavg))
    print("Full Session time "+str(FullSessionTime))

    return ReportParams
    # print("Full Session time "+str(FullTime))
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[6],pen=(0,0,0))#TimeStream,ForceRow
##    #widget.plotItem.plot(FullgraphVars[11],FullgraphVars[13],pen=(0,0,255))#TimeStream,ForceAvgRow
##    widget.plotItem.plot(FullgraphVars[12],FullgraphVars[22],pen=(128,0,0))#TimeShiftStream,ForceButterRow
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[19],pen=(0,255,0))#TimeStream,ForceYRow
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[20],pen=(255,0,0))#TimeStream,ForceXRow
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[7],pen=(0,0,255))#TimeStream,ForceZRow    
##    widget.plotItem.plot(FullgraphVars[12],FullgraphVars[14],pen=(12,63,18))# TimeShiftStream,ForceGaussRow
##    widget.plotItem.plot(FullgraphVars[3],FullgraphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w')# valleyStampArr,valleyFrcArr
##    widget.plotItem.plot(FpkStArr,FpkArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w')# pkStampArr,pkFrcArr,
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[15],pen=(131,81,193))#TimeStream,AccelRMS
##    ####widget.plotItem.plot(FullgraphVars[11],FullgraphVars[16],pen=(255,255,0))#TimeStream,AccDDArr
##    #widget.plotItem.plot(TimeStream,accRMSdiff,pen=(255,0,255))#TimeStream,accRMSdiff
##    #widget.plotItem.plot(accPkStmpArr,accPeakArr,pen=(160,130,65))#accPkStmpArr,accPeakArr
##    widget.plotItem.plot(FullgraphVars[17],FullgraphVars[18],pen=(255,0,255))#accSpikeStmpArr,accSpikeArr
##    #widget.plotItem.plot(TimeStream,accRMSdiffGaussAvg,pen=(0,255,255))#TimeStream,accRMSdiffGaussAvg
##    widget.show()
##    return ReportParams, app.exec_()


def GraphShowParams(pathFile):
    FxArr=[];FyArr=[];FzArr=[];FRezArr=[];pArr=[];rArr=[];yArr=[];strkNum=0;brstNum=0;FTime =0;
    FpkArr =[];FpkStArr =[]; ReportParams = [];
    #app = QtGui.QApplication(sys.argv)   

##    widget = pg.PlotWidget(title = "Plotting")
##    widget.setWindowTitle("CSV_Graph")
##    widget.setBackgroundBrush(QtGui.QColor(250,250,255))    
##    pg.setConfigOptions(antialias=True)

    
    csvRows = csvReadFile(pathFile)
    PascalTriangle = getPascalTriangleRow(30)
    #PascalTriangle = list(np.array(getPascalTriangleRow(99))*(sqrt(98)*(0.1)/(2**98)))
    rstStTimeArr = csvRows[1]; rstEndTimeArr = csvRows[2]
    FullgraphVars = GraphAnalyse(csvRows[0])
    #print(FullgraphVars)
    paramRow = ["Sessions","FXavg","FYavg","FZavg","FRavg","MaxPeak","AvgPeak","BurstNumber","StrokeNumber","StrokeFrequency","Full Session Time","pAvg","rAvg","yAvg","Contact/Active Time"]
    ReportParams.append(paramRow)
    for n in range (0,len(rstStTimeArr)):
        startIndx = csvRows[3].index(rstEndTimeArr[n])
        endIndx = csvRows[3].index(rstStTimeArr[n])#pkArr,pkStArr,vArr,vStArr
        grphVars = GraphAnalyse(csvRows[0][startIndx:(endIndx+1)]) #FXavg,FYavg,FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,FullTime,pAvg,rAvg,yAvg,ContactTime
        if (len(grphVars[4])<1):
            continue
        try:
            lstBrstStmp = grphVars[5][len(grphVars[5])-1]
        except IndexError:
            continue
        nhrArr = HumpReduction(grphVars[0],grphVars[1],grphVars[2],grphVars[3])
        print(nhrArr)
        #lstBrstStmp = grphVars[5][len(grphVars[5])-1]
        FpkArr = listAppend(FpkArr,grphVars[0])
        FpkStArr = listAppend(FpkStArr,grphVars[1])
        param = CalculateReportTable(n,grphVars[4],grphVars[5],grphVars[6],grphVars[7],grphVars[19],grphVars[20],grphVars[8],grphVars[9],grphVars[10],grphVars[11],grphVars[0])        
        strkNum += param[7];brstNum +=param[6];FTime+=param[9]
        FxArr.append(param[0]);FyArr.append(param[1]);FzArr.append(param[2]);FRezArr.append(param[3]);pArr.append(param[10]);rArr.append(param[11]);yArr.append(param[12]);
        param.insert(0,("Subsession "+(str)((int)(n)+1)))
        ReportParams.append(param)
    FXavg = round((getAvg(FxArr,len(FxArr))),2);FYavg = round((getAvg(FyArr,len(FyArr))),2);FZavg = round((getAvg(FzArr,len(FzArr))),2);FRezAvg = round((getAvg(FRezArr,len(FRezArr))),2);
    Pavg = round((getAvg(pArr,len(pArr))),2);Ravg = round((getAvg(rArr,len(rArr))),2);Yavg = round((getAvg(yArr,len(yArr))),2);
    #print(FpkStArr)
    #pkRejectArr = sorted(pkRejectArr, key=int, reverse=True)
    #print(pkRejectArr)
    #print(hillSlopeArr)
##    for j in range (0,len(pkRejectArr)):
##        FullgraphVars[0].pop(pkRejectArr[j])
##        FullgraphVars[1].pop(pkRejectArr[j])

    maxPeak = round(max(FullgraphVars[0]),3)
    avgPeak = round(getAvg(FpkArr,len(FpkArr)),3)
    numStrk = len(FpkArr)
    StrkFreq = round((numStrk/FTime),3) #[FXavg,FYavg,FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,FullTime,pAvg,rAvg,yAvg,TotalActTime]
    #FullSessionTime = round((float)(rstStTimeArr[len(rstStTimeArr)-1])- (float)(rstEndTimeArr[0]),2)
    FullSessionTime = round(((float)(lstBrstStmp)- (float)(rstEndTimeArr[0])),2);

    SessionParams = ["Total Session",FXavg,FYavg,FZavg,FRezAvg,maxPeak,avgPeak,brstNum,numStrk,StrkFreq,FullSessionTime,Pavg,Ravg,Yavg,FTime]
    ReportParams.append(SessionParams)

    print("Total active time "+str(FTime))
    print("Total Burst number is " + str(brstNum))
    print("Calculated Stroke number is " + str(strkNum))
    print("Total Stroke number is " + str(numStrk))
    print("Stroke frequency is " + str(StrkFreq))
    print("Maximum Peak is " + str(maxPeak))
    print("Average Peak is " + str(avgPeak))
    print("F X avg is " + str(FXavg))
    print("F Y avg is " + str(FYavg))
    print("F Z avg is " + str(FZavg))
    print("F Rez avg is " + str(FRezAvg))    
    print("P avg is " + str(Pavg))
    print("R avg is " + str(Ravg))
    print("Y avg is " + str(Yavg))
    print("Full Session time "+str(FullSessionTime))

    #print(FullgraphVars)

##    # print("Full Session time "+str(FullTime))
##    #widget.plotItem.plot(FullgraphVars[11],FullgraphVars[6],pen=(255,0,0))#TimeStream,ForceRow
##    #widget.plotItem.plot(FullgraphVars[11],FullgraphVars[13],pen=(0,0,255))#TimeStream,ForceAvgRow
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[19],pen=(0,255,0))#TimeStream,ForceYRow
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[20],pen=(255,0,0))#TimeStream,ForceXRow
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[7],pen=(0,0,255))#TimeStream,ForceZRow    
##    widget.plotItem.plot(FullgraphVars[12],FullgraphVars[14],pen=(0,0,0))# TimeShiftStream,ForceGaussRow
##    widget.plotItem.plot(FullgraphVars[3],FullgraphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w')# valleyStampArr,valleyFrcArr
##    widget.plotItem.plot(FpkStArr,FpkArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w')# pkStampArr,pkFrcArr,
##    widget.plotItem.plot(FullgraphVars[11],FullgraphVars[15],pen=(131,81,193))#TimeStream,AccelRMS
##    ####widget.plotItem.plot(FullgraphVars[11],FullgraphVars[16],pen=(255,255,0))#TimeStream,AccDDArr
##    #widget.plotItem.plot(TimeStream,accRMSdiff,pen=(255,0,255))#TimeStream,accRMSdiff
##    #widget.plotItem.plot(accPkStmpArr,accPeakArr,pen=(160,130,65))#accPkStmpArr,accPeakArr
##    widget.plotItem.plot(FullgraphVars[17],FullgraphVars[18],pen=(255,0,255))#accSpikeStmpArr,accSpikeArr
##    #widget.plotItem.plot(TimeStream,accRMSdiffGaussAvg,pen=(0,255,255))#TimeStream,accRMSdiffGaussAvg
##    widget.show()
    return FullgraphVars
   

    
    
def GraphShow(pathFile):
    FxArr=[];FyArr=[];FzArr=[];FRezArr=[];pArr=[];rArr=[];yArr=[];strkNum=0;brstNum=0;FTime =0;
    FpkArr =[];FpkStArr =[]; ReportParams = [];
    
##    app = QtGui.QApplication(sys.argv)   
##
##    widget = pg.PlotWidget(title = "Plotting")
##    widget.setWindowTitle("CSV_Graph")
##    widget.setBackgroundBrush(QtGui.QColor(250,250,255))    
##    pg.setConfigOptions(antialias=True)

    
    csvRows = csvReadFile(pathFile)
    PascalTriangle = getPascalTriangleRow(60)
    #PascalTriangle = list(np.array(getPascalTriangleRow(99))*(sqrt(98)*(0.1)/(2**98)))
    rstStTimeArr = csvRows[1]; rstEndTimeArr = csvRows[2]
    FullgraphVars = GraphAnalyse(csvRows[0])
    paramRow = ["Sessions","AvgForc(X)","AvgForce(Y)","AvgForce(Z)","AvgForce(RMS)","MaxPeakForce","AvgPeakForce",
                "BurstNumber","StrokeNumber","StrokeFrequency","FullSessionTime","AvgPitchAngle","AvgRollAngle","AvgYawAngle","Contact/ActiveTime"]
    
    ReportParams.append(paramRow)
    for n in range (0,len(rstEndTimeArr)):
        startIndx = csvRows[3].index(rstEndTimeArr[n])
        if n >= (len(rstEndTimeArr)-1):
            endIndx = (len(csvRows[3])-2)
        else:
            endIndx = csvRows[3].index(rstStTimeArr[n])#pkArr,pkStArr,vArr,vStArr
        grphVars = GraphAnalyse(csvRows[0][startIndx:endIndx]) #FXavg,FYavg,FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,FullTime,pAvg,rAvg,yAvg,ContactTime
        if (len(grphVars[4])<1):
            continue
        try:
            lstBrstStmp = grphVars[5][len(grphVars[5])-1]
        except IndexError:
            continue
        nhrArr = HumpReduction(grphVars[0],grphVars[1],grphVars[2],grphVars[3])
        print(nhrArr)
        #lstBrstStmp = grphVars[5][len(grphVars[5])-1]
        FpkArr = listAppend(FpkArr,grphVars[0])
        FpkStArr = listAppend(FpkStArr,grphVars[1])
        param = CalculateReportTable(n,grphVars[4],grphVars[5],grphVars[6],grphVars[7],grphVars[19],grphVars[20],grphVars[8],grphVars[9],grphVars[10],grphVars[11],grphVars[0])        
        strkNum += param[7];brstNum +=param[6];FTime+=param[9]
        FxArr.append(param[0]);FyArr.append(param[1]);FzArr.append(param[2]);FRezArr.append(param[3]);pArr.append(param[10]);rArr.append(param[11]);yArr.append(param[12]);
        param.insert(0,("Subsession "+(str)((int)(n)+1)))
        ReportParams.append(param)
    FXavg = round((getAvg(FxArr,len(FxArr))),2);FYavg = round((getAvg(FyArr,len(FyArr))),2);FZavg = round((getAvg(FzArr,len(FzArr))),2);FRezAvg = round((getAvg(FRezArr,len(FRezArr))),2);
    Pavg = round((getAvg(pArr,len(pArr))),2);Ravg = round((getAvg(rArr,len(rArr))),2);Yavg = round((getAvg(yArr,len(yArr))),2);
    #print(FpkStArr)
    #pkRejectArr = sorted(pkRejectArr, key=int, reverse=True)
    #print(pkRejectArr)
    #print(hillSlopeArr)
##    for j in range (0,len(pkRejectArr)):
##        FullgraphVars[0].pop(pkRejectArr[j])
##        FullgraphVars[1].pop(pkRejectArr[j])

    maxPeak = round(max(FullgraphVars[0]),2)
    avgPeak = round(getAvg(FpkArr,len(FpkArr)),2)
    numStrk = len(FpkArr)
    StrkFreq = round((numStrk/FTime),3) #[FXavg,FYavg,FZavg,FRavg,MaxPeak,AvgPeak,BurstNumber,StrokeNumber,StrokeFrequency,FullTime,pAvg,rAvg,yAvg,TotalActTime]
    #FullSessionTime = round((float)(rstStTimeArr[len(rstStTimeArr)-1])- (float)(rstEndTimeArr[0]),2)
    FullSessionTime = round(((float)(lstBrstStmp)- (float)(rstEndTimeArr[0])),2);

    SessionParams = ["Total Session",FXavg,FYavg,FZavg,FRezAvg,maxPeak,avgPeak,brstNum,numStrk,StrkFreq,FullSessionTime,Pavg,Ravg,Yavg,round(FTime,3)]
    ReportParams.append(SessionParams)

##    print("Total active time "+str(FTime))
##    print("Total Burst number is " + str(brstNum))
##    print("Calculated Stroke number is " + str(strkNum))
##    print("Total Stroke number is " + str(numStrk))
##    print("Stroke frequency is " + str(StrkFreq))
##    print("Maximum Peak is " + str(maxPeak))
##    print("Average Peak is " + str(avgPeak))
##    print("F X avg is " + str(FXavg))
##    print("F Y avg is " + str(FYavg))
##    print("F Z avg is " + str(FZavg))
##    print("F Rez avg is " + str(FRezAvg))    
##    print("P avg is " + str(Pavg))
##    print("R avg is " + str(Ravg))
##    print("Y avg is " + str(Yavg))
##    print("Full Session time "+str(FullSessionTime))
    
    return FullgraphVars, FpkStArr, FpkArr   
    

def main():
    
    app = QtGui.QApplication(sys.argv)   

    widget = pg.PlotWidget(title = "Plotting")
    widget.setWindowTitle("CSV_Graph")
    widget.setBackgroundBrush(QtGui.QColor(250,250,255))    
    pg.setConfigOptions(antialias=True)

    PascalTriangle = getPascalTriangleRow(60)
    #print("Enter path")    
    #p1 = raw_input()
    #p1 = "F:\QSTM New Visualization\Adaptive filter\Jesse\Jesse Human treat\_TempQ1Chart_15-19-55_11-02-2018.csv"
    p1 = PathFinder()
    p1 = p1[0][1]
    p1 = "C:\Users\ABHINABA\Documents\QSTM\QSTM Patients Folder\JoshRoy_Terry\JoshRoy_Terry__05-22-2019_08-12-1999\Output Data\JoshRoy_Terry_OutputDat_14-12-49_05-29-2019.csv"
    csvRows = csvReadFile(p1)
    print (p1)
    grphVars = GraphAnalyse(csvRows[0])
    if (len(grphVars[4])<1):
        print("No Activity")
    nhrArr=HumpReduction(grphVars[0],grphVars[1],grphVars[2],grphVars[3])
    print(nhrArr)
    param = CalculateVisTable(grphVars[4],grphVars[5],grphVars[6],grphVars[7],grphVars[8],grphVars[9],grphVars[10],grphVars[11],grphVars[0])
    
    widget.plotItem.plot(grphVars[11],grphVars[6],pen=(0,0,0))#TimeStream,Force_Row
    #widget.plotItem.plot(grphVars[11],grphVars[13],pen=(0,0,255))#TimeStream,ForceAvgRow
    widget.plotItem.plot(grphVars[12],grphVars[22],pen=(128,0,0))#TimeStream,ForceButterRow
    widget.plotItem.plot(grphVars[11],grphVars[19],pen=(0,255,0))#TimeStream,Force_Y_Row
    widget.plotItem.plot(grphVars[11],grphVars[20],pen=(255,0,0))#TimeStream,Force_X_Row
    widget.plotItem.plot(grphVars[11],grphVars[7],pen=(0,0,255))#TimeStream,Force_Z_Row
    widget.plotItem.plot(grphVars[12],grphVars[14],pen=(12,63,18))# TimeShiftStream,ForceGaussRow
    widget.plotItem.plot(grphVars[11],grphVars[21],pen=(9,165,166))#TimeStream,GyroRMS
    widget.plotItem.plot(grphVars[3],grphVars[2],pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w')# valleyStampArr,valleyFrcArr
    widget.plotItem.plot(grphVars[1],grphVars[0],pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w')# pkStampArr,pkFrcArr,
    widget.plotItem.plot(grphVars[11],grphVars[15],pen=(131,81,193))#TimeStream,AccelRMS
    widget.plotItem.plot(grphVars[11],grphVars[16],pen=(255,255,0))#TimeStream,AccDDArr
    widget.plotItem.plot(grphVars[17],grphVars[18],pen=(255,0,255))#accSpikeStmpArr,accSpikeArr

#print (pkFrcArr)
#RpkArr = removeFaultypeaks(pkFrcArr,pkStampArr,nhrArr)
    '''#widget.plotItem.plot(TimeStream,Force_Row,pen=(255,0,0))#TimeStream,Force_Row
    widget.plotItem.plot(TimeStream,ForceAvgRow,pen=(0,0,255))#TimeStream,ForceAvgRow
    widget.plotItem.plot(TimeShiftStream,ForceGaussRow,pen=(0,128,0))#TimeShiftStream,ForceGaussRow
    widget.plotItem.plot(valleyStampArr,valleyFrcArr,pen = (250,250,255),symbolBrush=(255,0,0), symbolPen='w')#valleyStampArr,valleyFrcArr
    widget.plotItem.plot(pkStampArr,pkFrcArr,pen = (250,250,255),symbolBrush=(0,255,0), symbolPen='w')#pkStampArr,pkFrcArr
    widget.plotItem.plot(TimeStream,AccelRMS,pen=(131,81,193))#TimeStream,AccelRMS
    widget.plotItem.plot(TimeStream,AccDDArr,pen=(255,255,0))#TimeStream,AccDDArr
    #widget.plotItem.plot(TimeStream,accRMSdiff,pen=(255,0,255))
    widget.plotItem.plot(accPkStmpArr,accPeakArr,pen=(160,130,65))#accPkStmpArr,accPeakArr
    widget.plotItem.plot(accSpikeStmpArr,accSpikeArr,pen=(255,0,255))#accSpikeStmpArr,accSpikeArr
    #widget.plotItem.plot(TimeStream,accRMSdiffGaussAvg,pen=(0,255,255))'''
    widget.show()
    return app.exec_()
    
##p2 = win.addPlot(title="Force Chart")
##p2.plot(timeStamp,Force_Row,pen=(255,0,0), name="Red curve")




## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    
    main()
##    import sys
##    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
##        QtGui.QApplication.instance().exec_()
##    
#print (upCntArr)
#print (dwnCntArr)
