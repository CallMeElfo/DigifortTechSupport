import pandas
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import DGFmodule

csvPath = ""
class Ui_MainWindow(object):
    def generatereg(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(icon)
        msgBox.setWindowTitle("CSV to DGF")
        try:
            dict_from_csv
        except NameError:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Select CSV First")
        else:
            try:
                with open('NewCams.reg', 'a+', encoding='ANSI') as newcams:
                    newcams.write('Windows Registry Editor Version 5.00\n')
                    newcams.write('[HKEY_LOCAL_MACHINE\SOFTWARE\Digifort\Gravacao\Cameras]\n')
                    for key in dict_from_csv:
                        name = ''.join(e for e in key['Name'] if e.isascii())
                        name = '[HKEY_LOCAL_MACHINE\SOFTWARE\Digifort\Gravacao\Cameras\\' + name + ']'
                        print (name)
                        if "Description" in key:
                            print ("Descritpion found")
                            description = '"General_Description"=\"' + key['Description'] + '\"'
                        else:
                            description = '"General_Description"=\"' + key['Name'] + '\"'
                        if "Manufacturer" in key:
                            model = '"General_Model"=' + key['Manufacturer'] + key['Model']
                        model = '"General_Model"=\"' + key['Model'] + '\"'
                        if "Channel" in key:
                            channel = '"General_Channel"=\"' + str(key['Channel']) + '\"'
                        else:
                            channel = '"General_Channel"=\"' + "1" + '\"'
                        address = '"General_Connection_Address"=\"' + key['Address'] + '\"'
                        port = '"General_Connection_Port"=\"' + str(key['Port']) + '\"'
                        if "Directory" in key:
                            print ("dir found in csv")
                            directory = '"General_Directory"=\"' + str(key['Directory']).replace("\\", "\\\\") + key['Name'] + '\"'
                        else:
                            print ("dir not foudn in csv")
                            directory = '"General_Directory"=\"' + str(dirPath).replace("\\", "\\\\") + "\\\\" + key['Name'] + '\"'
                        print ("Dir reg = " + directory)
                        newcams.write(name + '\n')
                        newcams.write(description + '\n')
                        newcams.write(model + '\n')
                        newcams.write(address + '\n')
                        newcams.write(port + '\n')
                        newcams.write(channel + '\n')
                        newcams.write(directory + '\n')
                        for line in DGFmodule.DefaultRegistryFile:
                            newcams.write(line)
                newcams.close()
                msgBox.setText("Reg file created!")
                msgBox.setIcon(QMessageBox.Information)
            except Exception as error:
                msgBox.setIcon(QMessageBox.Critical)
                msgBox.setText(str(error))
        msgBox.exec_()
    def checkCSV(self):
        global dict_from_csv
        print (csvPath)
        popup = QMessageBox()
        popup.setWindowIcon(icon)
        popup.setWindowTitle("CSV Check")
        wrongmodels = {}
        try:
            dict_from_csv_comma = pandas.read_csv(csvPath, header=0, encoding = 'ANSI', sep=",")
            dict_from_csv_semicolon = pandas.read_csv(csvPath, header=0, encoding = 'ANSI', sep=";")
            if dict_from_csv_comma.shape[1]>dict_from_csv_semicolon.shape[1]:
                dict_from_csv = dict_from_csv_comma
                print ("Comma delimited!")
            else:
                dict_from_csv = dict_from_csv_semicolon
                print ("Semicolon delimited!")
            if {"Name", "Address", "Port", "Model"}.issubset(dict_from_csv.columns):
                print ("Headers ok!")
            else:
                popup.setIcon(QMessageBox.Warning)
                popup.setText("Please check your headers, you should have at least Name, Model, Address and Port!")
            if {"Directory"}.issubset(dict_from_csv.columns):
                pass
            else:
                popup.setIcon(QMessageBox.Question)
                popup.setText("Please select a folder for recording!")
                popup.exec_()
                self.selectDir()
            dict_from_csv = dict_from_csv.to_dict(orient = 'records')
            print (dict_from_csv)
            for key in dict_from_csv:
                if key['Model'] not in DGFmodule.DGFValidModels:
                    wrongmodels[key['Name']] = key['Model']
                    key['Model'] = 'ONVIF Conformant Device'
            if bool(wrongmodels) == True:
                popup.setText("Please check your CSV, there are models listed that are not part o Digifort's list. If you proceed to import anyway Digifort will register them as ONVIF.\n")
                wrongmodellist = ""
                for key in wrongmodels:
                    wrongmodellist += "\n" + wrongmodels[key]
                popup.setDetailedText(wrongmodellist)
            else:
                popup.setIcon(QMessageBox.Information)
                popup.setText("CSV OK!")
        except Exception as error:
            if type(error) == UnicodeDecodeError:
                popup.setText("Check Encoding! It should be ANSI!")
            else:
                popup.setText(str(error))
            popup.setIcon(QMessageBox.Critical)
        popup.exec_()
    def selectFile(self):
        global csvPath
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(None,"Select CSV File", "","CSV Files (*.csv)", options=options)
        csvPath = Path(filePath)
        self.fileselectbutton.setText(str(csvPath.name))
        self.checkCSV()
    def selectDir(self):
        global dirPath
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folderpath = QFileDialog.getExistingDirectory(None, 'Select Folder')
        dirPath = Path(folderpath)
        if str(dirPath) == ".":
            dirPath = "C:\\Digifort Recording\\"
        print (dirPath)

    def setupUi(self, MainWindow):
        global icon
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(184, 221)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/icone.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LogoLabel = QtWidgets.QLabel(self.centralwidget)
        self.LogoLabel.setGeometry(QtCore.QRect(20, 0, 151, 131))
        self.LogoLabel.setObjectName("LogoLabel")
        self.GenerateRegFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.GenerateRegFileButton.setGeometry(QtCore.QRect(20, 170, 151, 23))
        self.GenerateRegFileButton.setObjectName("GenerateRegFileButton")
        self.GenerateRegFileButton.clicked.connect(self.generatereg)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 140, 151, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CSVFIlelabel = QtWidgets.QLabel(self.layoutWidget)
        self.CSVFIlelabel.setObjectName("CSVFIlelabel")
        self.horizontalLayout.addWidget(self.CSVFIlelabel)
        self.fileselectbutton = QtWidgets.QPushButton(self.layoutWidget)
        self.fileselectbutton.setObjectName("fileselectbutton")
        self.fileselectbutton.clicked.connect(self.selectFile)
        self.horizontalLayout.addWidget(self.fileselectbutton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CSV to DGF"))
        self.LogoLabel.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/logo/png.png\"/></p></body></html>"))
        self.GenerateRegFileButton.setText(_translate("MainWindow", "Generate Registry File"))
        self.CSVFIlelabel.setText(_translate("MainWindow", "CSV File"))
        self.fileselectbutton.setText(_translate("MainWindow", "..."))
import logo_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
