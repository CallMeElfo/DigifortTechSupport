import requests
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
from passlib.hash import cisco_type7
import time
import threading

#Load Config
ServerRegisterDict = {}
config = configparser.ConfigParser()
config.read('settings.ini')
print (config.sections())
for server in config.sections():
    ServerRegisterDict[server] = {}
    ServerRegisterDict[server]['user'] = config[server]['user']
    ServerRegisterDict[server]['password'] = config[server]['password']
    ServerRegisterDict[server]['address'] = config[server]['address']
    ServerRegisterDict[server]['APIport'] = config[server]['APIport']

class Ui_MainWindow(object):
    #Server Check
    def ServerCheck(self, user, password, address, APIport):
        serverokflag = 1
        url = 'http://{0}:{1}@{2}:{3}/Interface/Cameras/GetStatus?ResponseFormat=JSON'.format(user, password, address, APIport)
        try:
            response = requests.get(url, timeout=100)
            jsonresponse = response.json()
            for line in jsonresponse['Response']['Data']['Cameras']:
                CameraFPS = int(line['RecordingFPS'])
                CameraName = line['Name']
                if self.FPSCheckBox.isChecked():
                    FPSThreshold = int(self.FPSSpinBox.value())
                    if CameraFPS > FPSThreshold:
                        serverokflag = 0
                        self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                        self.OutputViewer.append('<font color =Red>Camera {} recording at {} frames!</font>'.format(CameraName, CameraFPS, address))
            if serverokflag == 1:
                self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.OutputViewer.append('<font color =Green>Server {} OK!</font>'.format(address))
            else:
                self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.OutputViewer.append('<font color =Red>Check Server {}!</font>'.format(address))
        except Exception as error:
            self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.OutputViewer.append('<font color =Red>Check Server {}! Error: {}</font>'.format(address, error))
        self.OutputViewer.append('-------------------------------------------')
    #BitrateTimer Check
    def BitrateServerCheck(self, user, password, address, APIport):
        serverokflag = 1
        url = 'http://{0}:{1}@{2}:{3}/Interface/Cameras/GetStatus?ResponseFormat=JSON'.format(user, password, address, APIport)
        BitrateTimer = self.BitrateTimerSpinBox.value()
        BitrateDict = {}
        while BitrateTimer > 0:
            self.OutputViewer.append('Checking Server {}, {} seconds left...'.format(address, BitrateTimer))
            try:
                if (BitrateTimer == self.BitrateTimerSpinBox.value()) or (BitrateTimer == 1):
                    response = requests.get(url, timeout=100)
                    jsonresponse = response.json()
                    for line in jsonresponse['Response']['Data']['Cameras']:
                        CameraFPS = int(line['RecordingFPS'])
                        CameraName = line['Name']
                        CameraUsedDisk = line['UsedDiskSpace']
                        if line['ConfiguredToRecord'] == True:
                            BitrateDict[CameraName] = BitrateDict.get(CameraName, []) + [CameraUsedDisk]
                        if self.FPSCheckBox.isChecked():
                            FPSThreshold = int(self.FPSSpinBox.value())
                            if (CameraFPS > FPSThreshold) and (BitrateTimer == 1):
                                serverokflag = 0
                                self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                                self.OutputViewer.append('<font color =Red>Camera {} recording at {} frames!</font>'.format(CameraName, CameraFPS, address))
            except Exception as error:
                serverokflag = 0
                self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.OutputViewer.append('<font color =Red>Check Server {}! Error: {}</font>'.format(address, error))
                break
            time.sleep(1)
            BitrateTimer = BitrateTimer - 1
            app.processEvents()
        for key in BitrateDict:
            InitialBitrate = int((BitrateDict[key][0]))
            FinalBitrate = int((BitrateDict[key][1]))
            AverageBitrate = (((FinalBitrate - InitialBitrate)/(self.BitrateTimerSpinBox.value())*8)/1024)
            if AverageBitrate > self.BitrateSpinBox.value():
                serverokflag = 0
                self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
                self.OutputViewer.append('<font color =Red>Camera {} with {:.2f} kbps bitrate!</font>'.format(key, AverageBitrate))
        if serverokflag == 1:
            self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.OutputViewer.append('<font color =Green>Server {} OK!</font>'.format(address))
        else:
            self.OutputViewer.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.OutputViewer.append('<font color =Red>Check Server {}!</font>'.format(address))
        self.OutputViewer.append('======================')
    #Server Register
    def AddServer(self):
        if (self.ServerNameTextBox.text() != '') and (self.UserTextbox.text() != '') and (self.PasswordTextbox.text() != '') and (self.AddressTextbox.text() != '') and (str(self.spinBox.value() != '')):
            ServerRegisterDict[self.ServerNameTextBox.text()] = {}
            ServerRegisterDict[self.ServerNameTextBox.text()]['user'] = self.UserTextbox.text()
            ServerRegisterDict[self.ServerNameTextBox.text()]['password'] = self.PasswordTextbox.text()
            ServerRegisterDict[self.ServerNameTextBox.text()]['address'] = self.AddressTextbox.text()
            ServerRegisterDict[self.ServerNameTextBox.text()]['APIport'] = str(self.spinBox.value())
            config[self.ServerNameTextBox.text()] = {}
            config[self.ServerNameTextBox.text()]['user'] = self.UserTextbox.text()
            config[self.ServerNameTextBox.text()]['password'] = self.PasswordTextbox.text()
            config[self.ServerNameTextBox.text()]['address'] = self.AddressTextbox.text()
            config[self.ServerNameTextBox.text()]['APIport'] = str(self.spinBox.value())
            with open ('settings.ini', 'w') as configfile:
                config.write(configfile)
                configfile.close()
            self.listWidget.clear()
            for key in ServerRegisterDict:
                self.listWidget.addItem(key)
        else:
            self.OutputViewer.clear()
            self.OutputViewer.append('Missing info!')
    #Run!
    def RunTest(self):
        runItems = self.listWidget.selectedItems()
        self.OutputViewer.clear()
        if not runItems:
            for key in ServerRegisterDict:
                print (key)
                user = ServerRegisterDict[key]['user']
                password = ServerRegisterDict[key]['password']
                address = ServerRegisterDict[key]['address']
                APIport = ServerRegisterDict[key]['APIport']
                if self.BitrateCheckbox.isChecked():
                    self.BitrateServerCheck(user, password, address, APIport)
                else:
                    self.ServerCheck(user, password, address, APIport)
        else:
            for item in runItems:
                user = ServerRegisterDict[item.text()]['user']
                password = ServerRegisterDict[item.text()]['password']
                address = ServerRegisterDict[item.text()]['address']
                APIport = ServerRegisterDict[item.text()]['APIport']
                if self.BitrateCheckbox.isChecked():
                    self.BitrateServerCheck(user, password, address, APIport)
                else:
                    self.ServerCheck(user, password, address, APIport)

    #Remove Selected
    def RemoveSelected(self):
        removeItems = self.listWidget.selectedItems()
        config.read('settings.ini')
        if not removeItems: return
        for item in removeItems:
            config.remove_section(item.text())
            with open ('settings.ini', 'w') as configfile:
                config.write(configfile)
                configfile.close()
            del  ServerRegisterDict[item.text()]
            self.listWidget.takeItem(self.listWidget.row(item))


#UI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 449)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/icone.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LogoLabel = QtWidgets.QLabel(self.centralwidget)
        self.LogoLabel.setGeometry(QtCore.QRect(40, 0, 161, 131))
        self.LogoLabel.setText("")
        self.LogoLabel.setPixmap(QtGui.QPixmap(":/logo/png.png"))
        self.LogoLabel.setObjectName("LogoLabel")
        self.OutputViewer = QtWidgets.QTextBrowser(self.centralwidget)
        self.OutputViewer.setGeometry(QtCore.QRect(460, 20, 291, 391))
        self.OutputViewer.setObjectName("OutputViewer")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(420, 0, 20, 421))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.RunButton = QtWidgets.QPushButton(self.centralwidget)
        self.RunButton.setGeometry(QtCore.QRect(250, 390, 75, 23))
        self.RunButton.setObjectName("RunButton")
        self.RunButton.clicked.connect(self.RunTest)
        self.ServerAddGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.ServerAddGroup.setGeometry(QtCore.QRect(20, 130, 211, 190))
        self.ServerAddGroup.setObjectName("ServerAddGroup")
        self.widget = QtWidgets.QWidget(self.ServerAddGroup)
        self.widget.setGeometry(QtCore.QRect(12, 20, 189, 126))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ServerNameLabel = QtWidgets.QLabel(self.widget)
        self.ServerNameLabel.setObjectName("ServerNameLabel")
        self.gridLayout.addWidget(self.ServerNameLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.ServerNameTextBox = QtWidgets.QLineEdit(self.widget)
        self.ServerNameTextBox.setObjectName("ServerNameTextBox")
        self.gridLayout.addWidget(self.ServerNameTextBox, 0, 1, 1, 1)
        self.UsernameLabel = QtWidgets.QLabel(self.widget)
        self.UsernameLabel.setObjectName("UsernameLabel")
        self.gridLayout.addWidget(self.UsernameLabel, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.UserTextbox = QtWidgets.QLineEdit(self.widget)
        self.UserTextbox.setObjectName("UserTextbox")
        self.gridLayout.addWidget(self.UserTextbox, 1, 1, 1, 1)
        self.PasswordLabel = QtWidgets.QLabel(self.widget)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.gridLayout.addWidget(self.PasswordLabel, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.PasswordTextbox = QtWidgets.QLineEdit(self.widget)
        self.PasswordTextbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordTextbox.setObjectName("PasswordTextbox")
        self.gridLayout.addWidget(self.PasswordTextbox, 2, 1, 1, 1)
        self.AddressLabel = QtWidgets.QLabel(self.widget)
        self.AddressLabel.setObjectName("AddressLabel")
        self.gridLayout.addWidget(self.AddressLabel, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.AddressTextbox = QtWidgets.QLineEdit(self.widget)
        self.AddressTextbox.setObjectName("AddressTextbox")
        self.gridLayout.addWidget(self.AddressTextbox, 3, 1, 1, 1)
        self.PortLabel = QtWidgets.QLabel(self.widget)
        self.PortLabel.setObjectName("PortLabel")
        self.gridLayout.addWidget(self.PortLabel, 4, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(9998)
        self.spinBox.setProperty("value", 8601)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 4, 1, 1, 1)
        self.AddButton = QtWidgets.QPushButton(self.ServerAddGroup)
        self.AddButton.setGeometry(QtCore.QRect(10, 150, 191, 31))
        self.AddButton.setObjectName("AddButton")
        self.AddButton.clicked.connect(self.AddServer)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(255, 21, 151, 361))
        self.listWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName("listWidget")
        self.RemoveButton = QtWidgets.QPushButton(self.centralwidget)
        self.RemoveButton.setGeometry(QtCore.QRect(330, 390, 75, 23))
        self.RemoveButton.setObjectName("RemoveButton")
        self.RemoveButton.clicked.connect(self.RemoveSelected)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 320, 192, 102))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.FPSCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.FPSCheckBox.setObjectName("FPSCheckBox")
        self.gridLayout_2.addWidget(self.FPSCheckBox, 0, 0, 1, 1)
        self.FPSSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.FPSSpinBox.setObjectName("FPSSpinBox")
        self.gridLayout_2.addWidget(self.FPSSpinBox, 0, 1, 1, 2)
        self.BitrateCheckbox = QtWidgets.QCheckBox(self.groupBox)
        self.BitrateCheckbox.setObjectName("BitrateCheckbox")
        self.gridLayout_2.addWidget(self.BitrateCheckbox, 1, 0, 1, 3)
        self.BitrateTimerSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.BitrateTimerSpinBox.setObjectName("BitrateTimerSpinBox")
        self.gridLayout_2.addWidget(self.BitrateTimerSpinBox, 2, 0, 1, 1)
        self.BitrateTimerLabel = QtWidgets.QLabel(self.groupBox)
        self.BitrateTimerLabel.setObjectName("BitrateTimersLabel")
        self.gridLayout_2.addWidget(self.BitrateTimerLabel, 2, 1, 1, 1)
        self.BitrateSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.BitrateSpinBox.setMinimum(0)
        self.BitrateSpinBox.setMaximum(999999)
        self.BitrateSpinBox.setProperty("value", 1500)
        self.BitrateSpinBox.setObjectName("BitrateSpinBox")
        self.gridLayout_2.addWidget(self.BitrateSpinBox, 2, 2, 1, 1)
        self.BitrateLabel = QtWidgets.QLabel(self.groupBox)
        self.BitrateLabel.setObjectName("BitrateLabel")
        self.gridLayout_2.addWidget(self.BitrateLabel, 2, 3, 1, 1)
        self.groupBox.raise_()
        self.ServerAddGroup.raise_()
        self.UserTextbox.raise_()
        self.LogoLabel.raise_()
        self.AddressTextbox.raise_()
        self.PasswordTextbox.raise_()
        self.OutputViewer.raise_()
        self.UsernameLabel.raise_()
        self.PasswordLabel.raise_()
        self.AddressLabel.raise_()
        self.PortLabel.raise_()
        self.line.raise_()
        self.AddButton.raise_()
        self.RunButton.raise_()
        self.listWidget.raise_()
        self.RunButton.raise_()
        self.RemoveButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Digifort Cloud Check"))
        self.RunButton.setText(_translate("MainWindow", "Run!"))
        self.ServerAddGroup.setTitle(_translate("MainWindow", "Server Add"))
        self.ServerNameLabel.setText(_translate("MainWindow", "Name"))
        self.UsernameLabel.setText(_translate("MainWindow", "Username"))
        self.PasswordLabel.setText(_translate("MainWindow", "Password"))
        self.AddressLabel.setText(_translate("MainWindow", "Address"))
        self.PortLabel.setText(_translate("MainWindow", "Port"))
        self.AddButton.setText(_translate("MainWindow", "Add"))
        self.RemoveButton.setText(_translate("MainWindow", "Remove"))
        self.groupBox.setTitle(_translate("MainWindow", "Maintenance"))
        self.FPSCheckBox.setText(_translate("MainWindow", "FPS  >"))
        self.BitrateCheckbox.setText(_translate("MainWindow", "Bitrate Check"))
        self.BitrateTimerLabel.setText(_translate("MainWindow", "Seconds"))
        self.BitrateLabel.setText(_translate("MainWindow", "kbps"))
        for key in ServerRegisterDict:
            self.listWidget.addItem(key)
import logo_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
