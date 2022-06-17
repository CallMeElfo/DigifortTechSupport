from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import os
import logo_rc
from winreg import *
from collections import Counter
import win32serviceutil
from PyQt5.QtGui import QIcon, QPixmap
#Flags
defaultbuttonflag = "Deactivate"
deactivatecambuttonflag = "Deactivate"
disableautoconnectbuttonflag = "Disable"
servicemanagerbuttonflag = "Stop"
class Ui_MainWindow(object):
    #Config Backup
    def configbkp(self):
        self.SetDefaultButton.setEnabled(False)
        self.textBrowser.clear()
        try:
            os.system('reg export HKLM\SOFTWARE\Digifort DGFBKP.reg /y')
            self.textBrowser.append("Backup Done!")
        except Exception as error:
            self.textBrowser.append("Task failed! Error: " + str(error))
    #Client Backup
    def clientbkp(self):
        self.SetDefaultButton.setEnabled(False)
        self.textBrowser.clear()
        try:
            os.system('reg export HKCU\Software\Digifort DGFCBKP.reg /y')
            self.textBrowser.append("Client Backup Done!")
        except Exception as error:
            self.textBrowser.append("Task failed! Error: " + str(error))
    #Service Check
    def servicecheck(self):
            global defaultbuttonflag
            defaultbuttonflag = "Service Check"
            #Default Port Values
            TCPPortVMS = '8600'
            TCPPortVMSSSL = '8400'
            PortaWEB = '80'
            PortaWEBSSL = '443'
            PortaRTSP = '554'
            PortaRTSPS = '322'
            PortaANL = '8610'
            PortaANLSSL = '8410'
            PortaLPR = '8611'
            PortaLPRSSL = '8411'
            PortaMobileAdmin = '8650'
            PortaMobileHTTP = '8651'
            PortaMobileStream = '8652'
            PortaMobileAdminSSL = '8450'
            PortaMobileHTTPSSL = '8451'
            PortaMobileStreamSSL = '8452'
        #Registry Paths
            VMSConfigGeral = r"SOFTWARE\Digifort\Config\Geral"
            VMSConfigSSL = r"SOFTWARE\Digifort\Config\SSL"
            RTSPConfig = r"SOFTWARE\Digifort\RTSP\Config"
            WebServer = r"SOFTWARE\Digifort\WebServer\Config"
            ANLConfigTCP = r"SOFTWARE\Digifort Analytics\Config\TCP"
            LPRConfigTCP = r"SOFTWARE\Digifort LPR\Config\TCP"
            MobileConfig = r"SOFTWARE\Digifort Mobile Camera Server\Config\Network"

            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            #Clear History
            self.textBrowser.clear()
            #VMS Port Discovery
            try:
                keyconfiggeral = OpenKey(reg, VMSConfigGeral)
                try:
                    str.TCPPortVMS = QueryValueEx(keyconfiggeral,"PortaCommTCP")
                    self.textBrowser.append("VMS = " + TCPPortVMS[0])
                except:
                    self.textBrowser.append("VMS = " + TCPPortVMS)
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            #VMS SSL Port Discovery
            try:
                keysslvms = OpenKey(reg, VMSConfigSSL)
                try:
                    str.TCPPortVMSSSL = QueryValueEx(keysslvms, "Port")
                    self.textBrowser.append("VMS SSL = " + TCPPortVMSSSL[0])
                except:
                    self.textBrowser.append("VMS SSL = " + TCPPortVMSSSL)
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            #Web Server Port Discovery
            try:
                keywebport = OpenKey(reg, WebServer)
                try:
                    str.PortaWEB = QueryValueEx(keywebport, "HTTPPort")
                    self.textBrowser.append("WEB = " + PortaWEB[0])
                except:
                    self.textBrowser.append("WEB = " + PortaWEB)
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            #Web Server SSL Port Discovery
            try:
                keywebport = OpenKey(reg, WebServer)
                try:
                    str.PortaWEBSSL = QueryValueEx(keywebport, "HTTPSPort")
                    self.textBrowser.append("WEB SSL = " + PortaWEBSSL[0])
                except:
                    self.textBrowser.append("WEB SSL = " + PortaWEBSSL)
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            #RTSP Port Discovery
            try:
                keyRTSPport = OpenKey(reg, RTSPConfig)
                try:
                    str.PortaRTSP = QueryValueEx(keyRTSPport, "Port")
                    self.textBrowser.append("RTSP = " + PortaRTSP[0])
                except:
                    self.textBrowser.append("RTSP = " + PortaRTSP)
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            #RTSPS Port Discovery
            try:
                keyRTSPSport = OpenKey(reg, RTSPConfig)
                try:
                    str.PortaRTSPS = QueryValueEx(keyRTSPSport, "RTSPSPort")
                    self.textBrowser.append("RTSPS = " + PortaRTSPS[0])
                except:
                    self.textBrowser.append("RTSPS = " + PortaRTSPS)
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            #LPR Port Discovery
            if self.checkBoxLPR.isChecked():
                try:
                    keyLPRPort = OpenKey(reg, LPRConfigTCP)
                    try:
                        str.PortaLPR = QueryValueEx(keyLPRPort, "Port")
                        self.textBrowser.append("LPR = " + PortaLPR)
                    except:
                        self.textBrowser.append("LPR = " + PortaLPR)
                    #LPR SSL Port Discovery
                    keyLPRSSLPort = OpenKey(reg, LPRConfigTCP)
                    try:
                        str.PortaLPRSSL = QueryValueEx(keyLPRSSLPort, "SSL_Port")
                        self.textBrowser.append("LPR SSL = " + PortaLPRSSL[0])
                    except:
                        self.textBrowser.append("LPR SSL = " + PortaLPRSSL)
                except Exception as error:
                    self.textBrowser.append("Task failed! Error: " + str(error))
            #ANL Port Discovery
            if self.checkBoxANL.isChecked():
                    try:
                        keyANLPort = OpenKey(reg, ANLConfigTCP)
                        try:
                            str.PortaANL = QueryValueEx(keyANLPort, "Port")
                            self.textBrowser.append("Analytics = " + PortaANL[0])
                        except:
                            self.textBrowser.append("Analytics = " + PortaANL)
                    except Exception as error:
                        self.textBrowser.append("Task failed! Error: " + str(error))
            #ANL SSL Port Discovery
                    try:
                        keyANLSSLPort = OpenKey(reg, ANLConfigTCP)
                        try:
                            str.PortaANLSSL = QueryValueEx(keyANLSSLPort, "SSL_Port")
                            self.textBrowser.append("Analytics SSL = " + PortaANLSSL[0])
                        except:
                            self.textBrowser.append("Analytics SSL = " + PortaANLSSL)
                    except Exception as error:
                        self.textBrowser.append("Task failed! Error: " + str(error))
            #Mobile Port Discovery
            try:
                if self.checkBoxMBL.isChecked():
                    try:
                        keyMobileNetwork = OpenKey(reg, MobileConfig)
                        try:
                            str.PortaMobileAdmin = QueryValueEx(keyMobileNetwork, "AdminPort")
                            self.textBrowser.append("Mobile Admin = " + PortaMobileAdmin[0])
                        except:
                            self.textBrowser.append("Mobile Admin = " + PortaMobileAdmin)
                        try:
                            str.PortaMobileHTTP = QueryValueEx(keyMobileNetwork, "HTTPPort")
                            self.textBrowser.append("Mobile HTTP = " + PortaMobileHTTP[0])
                        except:
                            self.textBrowser.append("Mobile HTTP = " + PortaMobileHTTP)
                        try:
                            str.PortaMobileStream = QueryValueEx(keyMobileNetwork, "StreamPort")
                            self.textBrowser.append("Mobile Stream = " + PortaMobileStream[0])
                        except:
                            self.textBrowser.append("Mobile Strem = " + PortaMobileStream)
                        try:
                            str.PortaMobileAdminSSL = QueryValueEx(keyMobileNetwork, "SSL_AdminPort")
                            self.textBrowser.append("Mobile Admin SSL = " + PortaMobileAdminSSL[0])
                        except:
                            self.textBrowser.append("Mobile Admin SSL = " + PortaMobileAdminSSL)
                        try:
                            str.PortaMobileHTTPSSL = QueryValueEx(keyMobileNetwork, "SSL_HTTPPort")
                            self.textBrowser.append("Mobile HTTP SSL = " + PortaMobileHTTPSSL[0])
                        except:
                            self.textBrowser.append("Mobile HTTP SSL = " + PortaMobileHTTPSSL)
                        try:
                            str.PortaMobileStreamSSL = QueryValueEx(keyMobileNetwork, "SSL_StreamPort")
                            self.textBrowser.append("Mobile Stream SSL = " + PortaMobileStreamSSL[0])
                        except:
                            self.textBrowser.append("Mobile Stream SSL = " + PortaMobileStreamSSL)
                    except Exception as error:
                        self.textBrowser.append("Task failed! Error: " + str(error))
                self.SetDefaultButton.setEnabled(True)
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
    #Set Default
    def defaultbutton(self):
        global defaultbuttonflag
        if defaultbuttonflag == "Service Check":
            #Registry Paths
            VMSConfigGeral = r"SOFTWARE\Digifort\Config\Geral"
            VMSConfigSSL = r"SOFTWARE\Digifort\Config\SSL"
            RTSPConfig = r"SOFTWARE\Digifort\RTSP\Config"
            WebServer = r"SOFTWARE\Digifort\WebServer\Config"
            ANLConfigTCP = r"SOFTWARE\Digifort Analytics\Config\TCP"
            LPRConfigTCP = r"SOFTWARE\Digifort LPR\Config\TCP"
            MobileConfig = r"SOFTWARE\Digifort Mobile Camera Server\Config\Network"
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            #Clear History
            self.textBrowser.clear()
            #VMS Port Discovery
            try:
                keyconfiggeral = OpenKeyEx(reg, VMSConfigGeral, 0, KEY_SET_VALUE)
                keysslvms = OpenKeyEx(reg, VMSConfigSSL, 0, KEY_SET_VALUE)
                keywebport = OpenKeyEx(reg, WebServer, 0, KEY_SET_VALUE)
                keyRTSPport = OpenKeyEx(reg, RTSPConfig, 0, KEY_SET_VALUE)
                keyRTSPSport = OpenKeyEx(reg, RTSPConfig, 0, KEY_SET_VALUE)
                if self.checkBoxLPR.isChecked():
                    keyLPRPort = OpenKeyEx(reg, LPRConfigTCP, 0, KEY_SET_VALUE)
                    keyLPRSSLPort = OpenKeyEx(reg, LPRConfigTCP, 0, KEY_SET_VALUE)
                if self.checkBoxANL.isChecked():
                    keyANLPort = OpenKeyEx(reg, ANLConfigTCP, 0, KEY_SET_VALUE)
                    keyANLSSLPort = OpenKeyEx(reg, ANLConfigTCP, 0, KEY_SET_VALUE)
                if self.checkBoxMBL.isChecked():
                    keyMobileNetwork = OpenKeyEx(reg, MobileConfig, 0, KEY_SET_VALUE)
                try:
                    SetValueEx(keyconfiggeral, "PortaCommTCP", 0, REG_DWORD, 8600)
                    SetValueEx(keysslvms, "Port", 0, REG_DWORD, 8400)
                    SetValueEx(keywebport, "HTTPPort", 0, REG_DWORD, 80)
                    SetValueEx(keywebport, "HTTPSPort", 0, REG_DWORD, 443)
                    SetValueEx(keyRTSPport, "Port", 0, REG_DWORD, 554)
                    SetValueEx(keyRTSPSport, "RTSPSPort", 0, REG_DWORD, 322)
                    if self.checkBoxANL.isChecked():
                        SetValueEx(keyANLPort, "Port", 0, REG_DWORD, 8610)
                        SetValueEx(keyANLSSLPort, "SSL_Port", 0, REG_DWORD, 8410)
                    if self.checkBoxLPR.isChecked():
                        SetValueEx(keyLPRPort, "Port", 0, REG_DWORD, 8611)
                        SetValueEx(keyLPRSSLPort, "SSL_Port", 0, REG_DWORD, 8411)
                    if self.checkBoxMBL.isChecked():
                        SetValueEx(keyMobileNetwork, "AdminPort", 0, REG_DWORD, 8650)
                        SetValueEx(keyMobileNetwork, "HTTPPort", 0, REG_DWORD, 8651)
                        SetValueEx(keyMobileNetwork, "StreamPort", 0, REG_DWORD, 8652)
                        SetValueEx(keyMobileNetwork, "SSL_AdminPort", 0, REG_DWORD, 8450)
                        SetValueEx(keyMobileNetwork, "SSL_HTTPPort", 0, REG_DWORD, 8451)
                        SetValueEx(keyMobileNetwork, "SSL_StreamPort", 0, REG_DWORD, 8452)
                    self.textBrowser.append("Network Ports Reseted!")
                except Exception as error:
                    self.textBrowser.append("Task failed! Error: " + str(error))
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
                #Set Defaults

            defaultbuttonflag = "Deactivated"
            self.SetDefaultButton.setEnabled(False)
    #Machine Code Check
    def machinecodecheck(self):
        self.SetDefaultButton.setEnabled(False)
        self.textBrowser.clear()
        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            CPUIDPath = r"SOFTWARE\Digifort\CPU\ID"
            CPUIDFolder = OpenKeyEx(reg, CPUIDPath)
            i = 0
            while True:
                CPUIDFolderPath = r"SOFTWARE\Digifort\CPU\ID"
                IDDate = EnumKey(CPUIDFolder, i)
                MCodeID = CPUIDFolderPath + "\\" + IDDate
                self.textBrowser.append("Date = " + MCodeID[25:33])
                MCode = OpenKeyEx(reg, MCodeID)
                MCodeValue = QueryValueEx(MCode, "MachineCode")
                self.textBrowser.append("Machine Code = " + MCodeValue[0] + "\n")
                i += 1
        except Exception as error:
            if error == 259:
                self.textBrowser.append("Done!\n")
            else:
                self.textBrowser.append("Task failed! Error: " + str(error))
    #Directory Check
    def directorycheck(self):
        self.SetDefaultButton.setEnabled(False)
        self.textBrowser.clear()
        RecordingList = []
        ArchivingList = []
        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            CamFolderPath = r"SOFTWARE\Digifort\Gravacao\Cameras"
            CamFolder = OpenKeyEx(reg, CamFolderPath)
            i = 0
            while True:
                CamFolderPath = r"SOFTWARE\Digifort\Gravacao\Cameras"
                CamName = EnumKey(CamFolder, i)
                CamNamePath = CamFolderPath + "\\" + CamName
                CamDir = OpenKeyEx(reg, CamNamePath)
                RecordingDir = QueryValueEx(CamDir, "General_Directory")
                ArchivingDir = QueryValueEx(CamDir, "Recording_Archiving_Directory")
                if ArchivingDir[0] == "":
                    self.textBrowser.append("Camera " + CamName + " records on " + RecordingDir[0] + " and doesn't archive.\n")
                else:
                    self.textBrowser.append("Camera " + CamName + " records on " + RecordingDir[0] + " and archives on " + ArchivingDir[0] + "\n")
                    ArchivingDir = ArchivingDir[0]
                    ArchivingList.append(ArchivingDir[0])
                i += 1
                RecordingDir = RecordingDir[0]
                RecordingList.append(RecordingDir[0])
        except Exception as error:
            if error == 259:
                self.textBrowser.append("Done!\n")
                self.textBrowser.append("*********************************************************\n")
                RecordingCount = Counter(RecordingList)
                for key, value in RecordingCount.items():
                    self.textBrowser.append("Recording on drive " + key + ": " + str(value) + " cameras.")
                ArchivingCount = Counter(ArchivingList)
                for key, value in ArchivingCount.items():
                    self.textBrowser.append("Archiving on drive " + key + ": " + str(value) + " cameras.")
                self.textBrowser.append("\n*********************************************************\n")
            else:
                self.textBrowser.append("Task failed! Error: " + str(error))
    #Deactivate All Cameras
    def deactivateall(self):
        global deactivatecambuttonflag
        global reg
        global CamFolder
        self.textBrowser.clear()
        self.SetDefaultButton.setEnabled(False)
        try:
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            CamFolderPath = r"SOFTWARE\Digifort\Gravacao\Cameras"
            CamFolder = OpenKeyEx(reg, CamFolderPath)
            if deactivatecambuttonflag == "Activate":
                try:
                    i = 0
                    while True:
                        CamFolderPath = r"SOFTWARE\Digifort\Gravacao\Cameras"
                        CamName = EnumKey(CamFolder, i)
                        CamNamePath = CamFolderPath + "\\" + CamName
                        CamDir = OpenKeyEx(reg, CamNamePath, 0, KEY_ALL_ACCESS)
                        Activation = QueryValueEx(CamDir, "General_Activate")
                        SetValueEx(CamDir, "General_Activate", 0, REG_DWORD, 1)
                        self.textBrowser.append("Camera " + CamName + " activated!\n")
                        i += 1
                except Exception as error:
                    if error == 259:
                        self.textBrowser.append("Done!\n")
                        self.DeactivateCamButton.setText("Deactivate Cameras")
                        deactivatecambuttonflag = "Deactivate"
                    else:
                        self.textBrowser.append("Task failed! Error: " + str(error))
            else:
                try:
                    i = 0
                    CamFolder = OpenKeyEx(reg, CamFolderPath)
                    while True:
                        CamName = EnumKey(CamFolder, i)
                        CamNamePath = CamFolderPath + "\\" + CamName
                        CamDir = OpenKeyEx(reg, CamNamePath, 0, KEY_ALL_ACCESS)
                        Activation = QueryValueEx(CamDir, "General_Activate")
                        SetValueEx(CamDir, "General_Activate", 0, REG_DWORD, 0)
                        self.textBrowser.append("Camera " + CamName + " deactivated!\n")
                        i += 1
                except Exception as error:
                    if error == 259:
                        self.textBrowser.append("Done!\n")
                        self.DeactivateCamButton.setText("Activate Cameras")
                        deactivatecambuttonflag = "Activate"
                    else:
                        self.textBrowser.append("Task failed! Error: " + str(error))
        except Exception as error:
            self.textBrowser.append("Task failed! Error: " + str(error))
    #Disable Auto-Connect
    def disableautoconnect(self):
        global disableautoconnectbuttonflag
        global reg
        global SrvFolder
        self.textBrowser.clear()
        self.SetDefaultButton.setEnabled(False)
        if disableautoconnectbuttonflag == "Disable":
            try:
                reg = ConnectRegistry(None, HKEY_CURRENT_USER)
                SrvFolderPath = r"SOFTWARE\Digifort\CM\Config\Servidores"
                SrvFolder = OpenKeyEx(reg, SrvFolderPath)
                i = 0
                while True:
                    SrvFolderPath = r"SOFTWARE\Digifort\CM\Config\Servidores"
                    SrvName = EnumKey(SrvFolder, i)
                    SrvNamePath = SrvFolderPath + "\\" + SrvName
                    SrvDir = OpenKeyEx(reg, SrvNamePath, 0, KEY_ALL_ACCESS)
                    AutoConnect = QueryValueEx(SrvDir, "Auto")
                    SetValueEx(SrvDir, "Auto", 0, REG_DWORD, 0)
                    i += 1
                    self.textBrowser.append("Server " + SrvName + " connection disabled!")
            except Exception as error:
                if error == 259:
                    self.textBrowser.append("Done!")
                    disableautoconnectbuttonflag = "Enable"
                    self.DisableAutoConnectButton.setText("Enable Auto-Connect")
                else:
                    self.textBrowser.append("Task Failed! Error: " + str(error))
        else:
            try:
                i = 0
                while True:
                    SrvFolderPath = r"SOFTWARE\Digifort\CM\Config\Servidores"
                    SrvName = EnumKey(SrvFolder, i)
                    SrvNamePath = SrvFolderPath + "\\" + SrvName
                    SrvDir = OpenKeyEx(reg, SrvNamePath, 0, KEY_ALL_ACCESS)
                    AutoConnect = QueryValueEx(SrvDir, "Auto")
                    SetValueEx(SrvDir, "Auto", 0, REG_DWORD, 1)
                    i += 1
                    self.textBrowser.append("Server " + SrvName + " connection enabled!")
            except Exception as error:
                if error == 259:
                    self.textBrowser.append("Done!")
                    disableautoconnectbuttonflag = "Disable"
                    self.DisableAutoConnectButton.setText("Disable Auto-Connect")
                else:
                    self.textBrowser.append("Task Failed! Error: " + str(error))
    #Service Manager
    def servicemanager(self):
        global servicemanagerbuttonflag
        self.textBrowser.clear()
        self.SetDefaultButton.setEnabled(False)
        if servicemanagerbuttonflag == "Start":
            try:
                os.system('sc start DigifortServer')
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            try:
                os.system('sc start FirebirdServerDigifort')
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            if self.checkBoxLPR.isChecked():
                try:
                    os.system('sc start DigifortLPRServer')
                except Exception as error:
                    self.textBrowser.append(str(error))
            if self.checkBoxANL.isChecked():
                try:
                    os.system('sc start DigifortAnalyticsServer')
                except Exception as error:
                    self.textBrowser.append("Taks failed! Error: " + str(error))
            if self.checkBoxMBL.isChecked():
                try:
                    os.system('sc start MobileCameraSrv')
                except Exception as error:
                    self.textBrowser.append("Task failed! Error: " + str(error))
            servicemanagerbuttonflag = "Stop"
            self.ServiceManButton.setText("Stop Services")
        else:
            try:
                os.system('sc stop DigifortServer')
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            try:
                os.system('sc stop FirebirdServerDigifort')
            except Exception as error:
                self.textBrowser.append("Task failed! Error: " + str(error))
            if self.checkBoxLPR.isChecked():
                try:
                    os.system('sc stop DigifortLPRServer')
                except Exception as error:
                    self.textBrowser.append(str(error))
            if self.checkBoxANL.isChecked():
                try:
                    os.system('sc stop DigifortAnalyticsServer')
                except Exception as error:
                    self.textBrowser.append("Taks failed! Error: " + str(error))
            if self.checkBoxMBL.isChecked():
                try:
                    os.system('sc stop MobileCameraSrv')
                except Exception as error:
                    self.textBrowser.append("Task failed! Error: " + str(error))
            servicemanagerbuttonflag = "Start"
            self.ServiceManButton.setText("Start Services")
    #Service Status Check
    def getServiceStatus(self):
        try:
            servicestatus = win32serviceutil.QueryServiceStatus('DigifortServer')
        except Exception as error:
            self.VMSStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.VMSStatusLBL.setText('Error!')
        else:
            if servicestatus[1] == 4:
                self.VMSStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.VMSStatusLBL.setText('<font color =Green>Running!</font>')
            if servicestatus[1] == 1:
                self.VMSStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.VMSStatusLBL.setText('<font color =Red>Stopped!</font>')
            if servicestatus [1] == 3:
                self.VMSStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.VMSStatusLBL.setText('<font color =Orange>Stopping!</font>')
            if servicestatus [1] == 2:
                self.VMSStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.VMSStatusLBL.setText('<font color=Orange>Starting!</font>')
        try:
            servicestatus = win32serviceutil.QueryServiceStatus('DigifortLPRServer')
        except Exception as error:
            self.LPRStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.LPRStatusLBL.setText('Error!')
        else:
            if servicestatus[1] == 4:
                self.LPRStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.LPRStatusLBL.setText('<font color =Green>Running!</font>')
            if servicestatus[1] == 1:
                self.LPRStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.LPRStatusLBL.setText('<font color =Red>Stopped!</font>')
            if servicestatus [1] == 3:
                self.LPRStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.LPRStatusLBL.setText('<font color =Orange>Stopping!</font>')
            if servicestatus [1] == 2:
                self.LPRStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.LPRStatusLBL.setText('<font color=Orange>Starting!</font>')
        try:
            servicestatus = win32serviceutil.QueryServiceStatus('DigifortAnalyticsServer')
        except Exception as error:
            self.ANLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.ANLStatusLBL.setText('Error!')
        else:
            if servicestatus[1] == 4:
                self.ANLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.ANLStatusLBL.setText('<font color =Green>Running!</font>')
            if servicestatus[1] == 1:
                self.ANLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.ANLStatusLBL.setText('<font color =Red>Stopped!</font>')
            if servicestatus [1] == 3:
                self.ANLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.ANLStatusLBL.setText('<font color =Orange>Stopping!</font>')
            if servicestatus [1] == 2:
                self.ANLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.ANLStatusLBL.setText('<font color=Orange>Starting!</font>')
        try:
            servicestatus = win32serviceutil.QueryServiceStatus('MobileCameraSrv')
        except Exception as error:
            self.MBLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.MBLStatusLBL.setText('Error!')
        else:
            if servicestatus[1] == 4:
                self.MBLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.MBLStatusLBL.setText('<font color =Green>Running!</font>')
            if servicestatus[1] == 1:
                self.MBLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.MBLStatusLBL.setText('<font color =Red>Stopped!</font>')
            if servicestatus [1] == 3:
                self.MBLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.MBLStatusLBL.setText('<font color =Orange>Stopping!</font>')
            if servicestatus [1] == 2:
                self.MBLStatusLBL.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.MBLStatusLBL.setText('<font color=Orange>Starting!</font>')
    #UI
    def setupUi(self, MainWindow):
        #Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(805, 400)

        #Set Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/icone.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, -15, 211, 141))
        self.label.setObjectName("label")
        #Text Browser
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(240, 10, 371, 341))
        self.textBrowser.setObjectName("textBrowser")
        #Network Group Box
        self.NetworkGBox = QtWidgets.QGroupBox(self.centralwidget)
        self.NetworkGBox.setGeometry(QtCore.QRect(10, 120, 221, 231))
        self.NetworkGBox.setObjectName("NetworkGBox")
        #Default Button
        self.SetDefaultButton = QtWidgets.QPushButton(self.NetworkGBox)
        self.SetDefaultButton.setGeometry(QtCore.QRect(10, 170, 201, 23))
        self.SetDefaultButton.setObjectName("SetDefaultButton")
        self.SetDefaultButton.clicked.connect(self.defaultbutton)
        #Service Check Button
        self.ServicePortCheckButton = QtWidgets.QPushButton(self.NetworkGBox)
        self.ServicePortCheckButton.setGeometry(QtCore.QRect(10, 200, 201, 23))
        self.ServicePortCheckButton.setObjectName("ServicePortCheckButton")
        self.ServicePortCheckButton.clicked.connect(self.servicecheck)
        #LPR Check Box
        self.checkBoxLPR = QtWidgets.QCheckBox(self.NetworkGBox)
        self.checkBoxLPR.setGeometry(QtCore.QRect(10, 20, 41, 17))
        self.checkBoxLPR.setObjectName("checkBoxLPR")
        #MBL Check Box
        self.checkBoxMBL = QtWidgets.QCheckBox(self.NetworkGBox)
        self.checkBoxMBL.setGeometry(QtCore.QRect(150, 20, 61, 17))
        self.checkBoxMBL.setObjectName("checkBoxMBL")
        #ANL Check Box
        self.checkBoxANL = QtWidgets.QCheckBox(self.NetworkGBox)
        self.checkBoxANL.setGeometry(QtCore.QRect(70, 20, 61, 17))
        self.checkBoxANL.setObjectName("checkBoxANL")
        #Service Manager Button
        self.ServiceManButton = QtWidgets.QPushButton(self.NetworkGBox)
        self.ServiceManButton.setGeometry(QtCore.QRect(10, 140, 201, 23))
        self.ServiceManButton.setObjectName("ServiceManButton")
        self.ServiceManButton.clicked.connect(self.servicemanager)
        #Service Status Label
        self.VMSServiceLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.VMSServiceLBL.setGeometry(QtCore.QRect(10, 50, 81, 16))
        self.VMSServiceLBL.setObjectName("VMSServiceLBL")
        self.LPRServiceLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.LPRServiceLBL.setGeometry(QtCore.QRect(10, 70, 81, 16))
        self.LPRServiceLBL.setObjectName("LPRServiceLBL")
        self.ANLServiceLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.ANLServiceLBL.setGeometry(QtCore.QRect(10, 90, 81, 16))
        self.ANLServiceLBL.setObjectName("ANLServiceLBL")
        self.MBLServiceLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.MBLServiceLBL.setGeometry(QtCore.QRect(10, 110, 81, 16))
        self.MBLServiceLBL.setObjectName("MBLServiceLBL")
        self.VMSStatusLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.VMSStatusLBL.setGeometry(QtCore.QRect(100, 50, 71, 16))
        self.VMSStatusLBL.setObjectName("VMSStatusLBL")
        self.LPRStatusLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.LPRStatusLBL.setGeometry(QtCore.QRect(100, 70, 71, 16))
        self.LPRStatusLBL.setObjectName("LPRStatusLBL")
        self.ANLStatusLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.ANLStatusLBL.setGeometry(QtCore.QRect(100, 90, 71, 16))
        self.ANLStatusLBL.setObjectName("ANLStatusLBL")
        self.MBLStatusLBL = QtWidgets.QLabel(self.NetworkGBox)
        self.MBLStatusLBL.setGeometry(QtCore.QRect(100, 110, 71, 16))
        self.MBLStatusLBL.setObjectName("MBLStatusLBL")
        #Backup Group Box
        self.BackupGBox = QtWidgets.QGroupBox(self.centralwidget)
        self.BackupGBox.setGeometry(QtCore.QRect(620, 210, 171, 81))
        self.BackupGBox.setObjectName("BackupGBox")
        #Client Backup Button
        self.ClientBackupButton = QtWidgets.QPushButton(self.BackupGBox)
        self.ClientBackupButton.setGeometry(QtCore.QRect(10, 50, 151, 23))
        self.ClientBackupButton.setObjectName("ClientBackupButton")
        self.ClientBackupButton.clicked.connect(self.clientbkp)
        #Config Backup Button
        self.ConfigBackupButton = QtWidgets.QPushButton(self.BackupGBox)
        self.ConfigBackupButton.setGeometry(QtCore.QRect(10, 20, 151, 23))
        self.ConfigBackupButton.setObjectName("ConfigBackupButton")
        self.ConfigBackupButton.clicked.connect(self.configbkp)
        #Maintenance Group Box
        self.MaintenanceGBox = QtWidgets.QGroupBox(self.centralwidget)
        self.MaintenanceGBox.setGeometry(QtCore.QRect(620, 40, 171, 141))
        self.MaintenanceGBox.setObjectName("MaintenanceGBox")
        #Machine Code Check Button
        self.MachineCodeCheckButton = QtWidgets.QPushButton(self.MaintenanceGBox)
        self.MachineCodeCheckButton.setGeometry(QtCore.QRect(10, 20, 151, 23))
        self.MachineCodeCheckButton.setObjectName("MachineCodeCheckButton")
        self.MachineCodeCheckButton.clicked.connect(self.machinecodecheck)
        #Directory Check Button
        self.DirectoryCheckButton = QtWidgets.QPushButton(self.MaintenanceGBox)
        self.DirectoryCheckButton.setGeometry(QtCore.QRect(10, 50, 151, 23))
        self.DirectoryCheckButton.setObjectName("DirectoryCheckButton")
        self.DirectoryCheckButton.clicked.connect(self.directorycheck)
        #Deactive Cam Button
        self.DeactivateCamButton = QtWidgets.QPushButton(self.MaintenanceGBox)
        self.DeactivateCamButton.setGeometry(QtCore.QRect(10, 80, 151, 23))
        self.DeactivateCamButton.setObjectName("DeactivateCamButton")
        self.DeactivateCamButton.clicked.connect(self.deactivateall)
        #Disable Auto-Connect Button
        self.DisableAutoConnectButton = QtWidgets.QPushButton(self.MaintenanceGBox)
        self.DisableAutoConnectButton.setGeometry(QtCore.QRect(10, 110, 151, 23))
        self.DisableAutoConnectButton.setObjectName("DisableAutoConnectButton")
        self.DisableAutoConnectButton.clicked.connect(self.disableautoconnect)
        # make QTimer
        self.qTimer = QTimer()
        # set interval to 0.5 s
        self.qTimer.setInterval(500)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getServiceStatus)
        # start timer
        self.qTimer.start()

        self.NetworkGBox.raise_()
        self.MaintenanceGBox.raise_()
        self.BackupGBox.raise_()
        self.textBrowser.raise_()
        self.label.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Digifort Quick Support"))
        self.NetworkGBox.setTitle(_translate("MainWindow", "Network"))
        self.SetDefaultButton.setText(_translate("MainWindow", "Set Default"))
        self.ServicePortCheckButton.setText(_translate("MainWindow", "Service Port Check"))
        self.checkBoxLPR.setText(_translate("MainWindow", "LPR"))
        self.checkBoxMBL.setText(_translate("MainWindow", "Mobile"))
        self.checkBoxANL.setText(_translate("MainWindow", "Analytics"))
        self.ServiceManButton.setText(_translate("MainWindow", "Stop Services"))
        self.VMSServiceLBL.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:10pt;\">VMS service</span></p></body></html>"))
        self.LPRServiceLBL.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">LPR service</span></p></body></html>"))
        self.ANLServiceLBL.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">ANL service</span></p></body></html>"))
        self.MBLServiceLBL.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">MBL service</span></p></body></html>"))
        self.VMSStatusLBL.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">&lt;STATUS&gt;</span></p></body></html>"))
        self.LPRStatusLBL.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">&lt;STATUS&gt;</span></p></body></html>"))
        self.ANLStatusLBL.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">&lt;STATUS&gt;</span></p></body></html>"))
        self.MBLStatusLBL.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">&lt;STATUS&gt;</span></p></body></html>"))
        self.BackupGBox.setTitle(_translate("MainWindow", "Backup"))
        self.ClientBackupButton.setText(_translate("MainWindow", "Client Backup"))
        self.ConfigBackupButton.setText(_translate("MainWindow", "Config Backup"))
        self.MaintenanceGBox.setTitle(_translate("MainWindow", "Maintenance"))
        self.MachineCodeCheckButton.setText(_translate("MainWindow", "Machine Code Check"))
        self.DirectoryCheckButton.setText(_translate("MainWindow", "Directory Check"))
        self.DeactivateCamButton.setText(_translate("MainWindow", "Deactivate Cameras"))
        self.DisableAutoConnectButton.setText(_translate("MainWindow", "Disable Client Auto-Connect"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/logo/png.png\"/></p></body></html>"))

    #Check Registry Paths
        try:
            reg32 = r'SOFTWARE\WOW6432Node\Digifort'
            reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            k = OpenKey(reg, reg32)
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('ATTENTION! Legacy config found!')
            error_dialog.exec_()
            self.textBrowser.append("ATTENTION!\nLegacy config found!\n")
        except:
            pass
import logo_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
