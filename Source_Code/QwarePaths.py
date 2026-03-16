import os, shutil, sys, ctypes, win32api
import glob, csv, errno, psutil
import ctypes.wintypes
from time import localtime,strftime

class Q_DataBase:

    def __init__(self):
        self.SetupDbase()

    def SetupDbase(self):        

        CSIDL_PERSONAL= 5
        SHGFP_TYPE_CURRENT= 0
        buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
        DefaultDestinationPath=''
        self.DefaultSearchPath = str(buf.value)
        self.QSTM_Path = self.DefaultSearchPath+"\\QSTM"

        self.tempStorePath = self.QSTM_Path+"\\QSTM_Temp"
        self.Q_DbasePath = self.QSTM_Path+"\\Qware_DataBase"
        self.Q_PatientsListPath = self.Q_DbasePath+"\\Qware Patients List"
        self.QPatntListCsvPath = self.Q_PatientsListPath+"\\Q_Patient_Details_List.csv"
        self.Q_PatientsFolderPath = self.Q_DbasePath+"\\Qware Patients Folder"        
        self.rstDataStorePath = self.tempStorePath+"\\Subsession_Data"
        self.processDataStorePath = self.tempStorePath+"\\Process_Data"

    #def Q_Dbase_Content(self):

        #self.SetupDbase()

        if not os.path.exists(self.QSTM_Path):    
            os.makedirs(self.QSTM_Path)
        else:
            self.Q_Folders=os.walk(self.QSTM_Path).next()[1]

        if not os.path.exists(self.Q_DbasePath ):    
            os.makedirs(self.Q_DbasePath )
        else:
            self.Q_DbaseFolders=os.walk(self.Q_DbasePath ).next()[1]

        if not os.path.exists(self.Q_PatientsListPath ):    
            os.makedirs(self.Q_PatientsListPath )
            #self.QPatntListCsvPath = self.Q_PatientsListPath+"\\Q_Patient_Details_List.csv"
            Row = ["FirstName","LastName","QSTM-ID","Patient Enroll Date", "DOB", "Age", "Sex", "Patient-Qname","Patient Folders Paths" ]
            patntListFile = open(self.QPatntListCsvPath, 'wb')
            FileWriter = csv.writer(patntListFile, delimiter=',')
            FileWriter.writerow(Row)
            patntListFile.close()
        else:
            self.Q_DbasePatientLists=os.walk(self.Q_PatientsListPath ).next()[1]

        if not os.path.exists(self.Q_PatientsFolderPath ):    
            os.makedirs(self.Q_PatientsFolderPath )
        else:
            #self.Q_PatientsFolders=os.walk(self.Q_PatientsFolderPath ).next()[1]
            pass

        if not os.path.exists(self.tempStorePath):    
            os.makedirs(self.tempStorePath)
        else:
            self.TempList=os.walk(self.tempStorePath).next()[1]
            #print(self.TempList)

        if not os.path.exists(self.rstDataStorePath):    
            os.makedirs(self.rstDataStorePath)
        else:
            self.RstList=os.walk(self.rstDataStorePath).next()[1]

        if not os.path.exists(self.processDataStorePath):    
            os.makedirs(self.processDataStorePath)
        else:
            self.ProcessList=os.walk(self.processDataStorePath).next()[1]

        #self.TempList=os.walk(self.tempStorePath).next()[1]
        #print(self.TempList)

    def clearTempFolder(self, tempPath):
        #self.SetupDbase()
        folder = tempPath
        print(folder)
        for the_file in os.listdir(folder):        
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    def PatientFolderCreate(self,FPath,name,dob):       
    
        Enroll_Date=strftime("%m-%d-%Y",localtime())
        
        PatientId = name+"__"+Enroll_Date+"_"+dob
        DesPath = FPath+"\\"+PatientId
        #PatientFrcPath=DesPath+"\\"+"Force Data"
        #PatientAngPath=DesPath+"\\"+"Geo-Angular Data"
        #PatientTrtAngPath=DesPath+"\\"+"Skin Angle Data"
        PatientOpDatPath=DesPath+"\\"+"Output Data"
        PatientResultPath=DesPath+"\\"+"Result Data"
        PatientIdPath = DesPath+"\\"+"Patient Paths"
        PatientReportPath = DesPath+"\\"+"Patient Report"
        if not os.path.exists(FPath):
            os.makedirs(FPath)
            os.makedirs(DesPath)
            #os.makedirs(PatientFrcPath)
            #os.makedirs(PatientAngPath)
            #os.makedirs(PatientTrtAngPath)
            os.makedirs(PatientOpDatPath)
            os.makedirs(PatientResultPath)
            os.makedirs(PatientIdPath)
            os.makedirs(PatientReportPath)
            PatientIdText = PatientIdPath+"\\"+"Paths.txt"
            f1 = open(str(PatientIdText), "w")
            f1.write(str(DesPath)+"\n")
            f1.write(str(PatientId)+"\n")
            f1.write(str(PatientOpDatPath)+"\n")
            f1.write(str(PatientIdPath)+"\n")
            f1.write(str(PatientOpDatPath)+"\n")
            f1.write(str(PatientReportPath)+"\n")
            f1.close()
            return (str(PatientId),str(PatientIdText));
        else:
            os.makedirs(DesPath)
            #os.makedirs(PatientFrcPath)
            #os.makedirs(PatientAngPath)
            #os.makedirs(PatientTrtAngPath)
            os.makedirs(PatientOpDatPath)
            os.makedirs(PatientResultPath)
            os.makedirs(PatientIdPath)
            os.makedirs(PatientReportPath)
            PatientIdText = PatientIdPath+"\\"+"Paths.txt"
            f1 = open(str(PatientIdText), "w")
            f1.write(str(DesPath)+"\n")
            f1.write(str(PatientId)+"\n")
            f1.write(str(PatientOpDatPath)+"\n")
            f1.write(str(PatientIdPath)+"\n")
            f1.write(str(PatientOpDatPath)+"\n")
            f1.write(str(PatientReportPath)+"\n")
            f1.close()
            return (str(PatientId),str(PatientIdText));

    def formNewPatientFolder(self, ListPath, Q_PatntsPath, EnrollDetails):
        
        self.FullName = EnrollDetails[0]+"_"+EnrollDetails[1]
        
        self.PatientPath = Q_PatntsPath+"\\"+self.FullName
        if not os.path.exists(self.PatientPath):
            self.PatientQName, self.PatientPathFile = self.PatientFolderCreate(self.PatientPath,self.FullName,EnrollDetails[4])
            patientListRow = [EnrollDetails[0],EnrollDetails[1],EnrollDetails[2],EnrollDetails[3], EnrollDetails[4],
                              EnrollDetails[5], EnrollDetails[6], self.PatientQName,self.PatientPathFile ]
            patientListFile = open(self.QPatntListCsvPath, 'ab')
            patientListFileWriter = csv.writer(patientListFile, delimiter=',')
            patientListFileWriter.writerow(patientListRow)            
            patientListFile.close()
            
        else:
            
            self.messageDiagBox = wx.MessageDialog(None,
                                                   "Patient is already Enrolled !!! \n Do You want to create another Patient with name "+self.FullName + " ???",
                                                   'Attention',wx.ICON_EXCLAMATION | wx.YES_NO | wx.STAY_ON_TOP)
             
            result = self.messageDiagBox.ShowModal()
            print("Patient already Exists")
            if result==wx.ID_YES:
                self.PatientQName, self.PatientPathFile = self.PatientFolderCreate(self.PatientPath,self.FullName,EnrollDetails[4])
                patientListRow = [EnrollDetails[0],EnrollDetails[1],EnrollDetails[2],EnrollDetails[3], EnrollDetails[4],
                                  EnrollDetails[5], EnrollDetails[6], self.PatientQName,self.PatientPathFile ]
                patientListFile = open(self.QPatntListCsvPath, 'ab')
                patientListFileWriter = csv.writer(patientListFile, delimiter=',')
                patientListFileWriter.writerow(patientListRow)
                patientListFile.close()
                #self.PatientId = PatientFolderCreate(self.PatientPath,self.FullName,self.dob)
                print("New Patient Directory created")
            else:
                print("New Patient Directory Exists")
            #self.RstList=os.walk(self.rstDataStorePath).next()[1]

##    def walkTemp(self):
##
##        #TempFiles = os.listdir(self.tempStorePath)
##        TempCsvFiles = [filename for filename in os.listdir(self.tempStorePath) if filename.endswith(".csv")]
##        for csvFile in TempCsvFiles:
##            fileParts = csvFile.split("_")
##            if fileParts[1] is "TempQ1ResultChart":
##                pass
##            if fileParts[1] is "TempQ2ResultChart":
##                pass
##            if fileParts[1] is "TempQ1Q2ResultChart":
##            
##        csvFileParts = TempCsvFiles[0].split("_")
##
##        print(csvFileParts)
##        
            
        

def main():

    db = Q_DataBase()
    #db.walkTemp()
    #db.SetupDbase()
    db.clearTempFolder(db.tempStorePath)
    print("QSTM Temp Folder Cleared")
    #print(db.TempList)

if __name__ == '__main__':
    main()          
    
                                                  


                                                          
                                                          

    
