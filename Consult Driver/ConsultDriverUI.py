import pandas
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class Ui_MainWindow(object):

    def selectFile(self):
        global csvPath
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(None,"Select CSV File", "","CSV Files (*.csv)", options=options)
        csvPath = Path(filePath)
        self.fileselectbutton.setText(str(csvPath.name))
        self.checkCSV()

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
            dict_from_csv = dict_from_csv.to_dict(orient = 'records')
            print (dict_from_csv)
            popup.setIcon(QMessageBox.Information)
            popup.setText("Table Loaded!")
            self.tableStatusIndicator.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
            self.tableStatusIndicator.setText('<font color =Green>Loaded!</font>')
            self.loadTable()
        except Exception as error:
            if type(error) == UnicodeDecodeError:
                popup.setText("Check Encoding! It should be ANSI!")
            else:
                popup.setText(str(error))
            popup.setIcon(QMessageBox.Critical)

        popup.exec_()

    def loadTable(self):
        #Load Manufacturer
        global manufacturerList
        manufacturerList = []
        for dictitem in dict_from_csv:
            if dictitem['Manufacturer'] not in manufacturerList:
                manufacturerList.append(str(dictitem['Manufacturer']))
        #Populate Manufacturer ComboBox
        self.manufacturerComboBox.addItems(manufacturerList)
        #Set Manufacturer List as editable and searchable
        self.manufacturerComboBox.setEditable(True)
        self.manufacturerComboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        #Set completer
        self.manufacturerComboBox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    def loadModels(self):
        #Clear Model ComboBox
        self.modelComboBox.clear()
        #Load Models
        modelList = []
        for dictitem in dict_from_csv:
            if dictitem['Manufacturer'] == str(self.manufacturerComboBox.currentText()):
                modelList.append(str(dictitem['Model']))
        #Populate Manufacturer ComboBox
        self.modelComboBox.addItems(modelList)
        #Set Manufacturer List as editable and searchable
        self.modelComboBox.setEditable(True)
        self.modelComboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        #Set completer
        self.modelComboBox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    def loadDrivers(self):
        #Clear Drivers ComboBox
        self.videoDriver1TextBrowser.clear()
        self.videoDriver2TextBrowser.clear()
        self.videoDriver3TextBrowser.clear()
        self.IODriverTextBrowser.clear()
        self.PTZDriverTextBrowser.clear()
        self.LPRDriverTextBrowser.clear()
        self.edgeRecordingTextBrowser.clear()
        self.analyticsDriverTextBrowser.clear()
        self.eventsDriverTextBrowser.clear()
        self.deviceTypeTextBrowser.clear()
        self.firmwareTextBrowser.clear()
        self.channelsTextBrowser.clear()
        #Find Model
        for dictitem in dict_from_csv:
            if dictitem['Model'] == str(self.modelComboBox.currentText()):
              #Load Drivers
              self.videoDriver1TextBrowser.setText(str(dictitem['VideoDriver1']))
              self.videoDriver2TextBrowser.setText(str(dictitem['VideoDriver2']))
              self.videoDriver3TextBrowser.setText(str(dictitem['VideoDriver3']))
              self.IODriverTextBrowser.setText(str(dictitem['DriverIO']))
              self.PTZDriverTextBrowser.setText(str(dictitem['DriverPTZ']))
              self.LPRDriverTextBrowser.setText(str(dictitem['EdgeLPR']))
              self.edgeRecordingTextBrowser.setText(str(dictitem['EdgeRecording']))
              self.analyticsDriverTextBrowser.setText(str(dictitem['EdgeAnalytics']))
              self.eventsDriverTextBrowser.setText(str(dictitem['EventDriver']))
              self.deviceTypeTextBrowser.setText(str(dictitem['ModelType']))
              self.firmwareTextBrowser.setText(str(dictitem['Firmware']))
              self.channelsTextBrowser.setText(str(dictitem['Channels']))

    def checkBoxControl(self):
        #This is used to avoid deadlocks on the search criteria
        if self.videoDriver1CheckBox.isChecked():
            self.videoDriver1CheckBox_2.setEnabled(False)
        else:
            self.videoDriver1CheckBox_2.setEnabled(True)

        if self.videoDriver2CheckBox.isChecked():
            self.videoDriver2CheckBox_2.setEnabled(False)
        else:
            self.videoDriver2CheckBox_2.setEnabled(True)

        if self.videoDriver3CheckBox.isChecked():
            self.videoDriver3CheckBox_2.setEnabled(False)
        else:
            self.videoDriver3CheckBox_2.setEnabled(True)

        if self.IODriverCheckBox.isChecked():
            self.IODriverCheckBox_2.setEnabled(False)
        else:
            self.IODriverCheckBox_2.setEnabled(True)

        if self.LPRDriverCheckBox.isChecked():
            self.LPRDriverCheckBox_2.setEnabled(False)
        else:
            self.LPRDriverCheckBox_2.setEnabled(True)

        if self.eventDriverCheckBox.isChecked():
            self.eventDriverCheckBox_2.setEnabled(False)
        else:
            self.eventDriverCheckBox_2.setEnabled(True)

        if self.edgeRecordingDriverCheckBox.isChecked():
            self.edgeRecordingDriverCheckBox_2.setEnabled(False)
        else:
            self.edgeRecordingDriverCheckBox_2.setEnabled(True)

        if self.PTZDriverCheckBox.isChecked():
            self.PTZDriverCheckBox_2.setEnabled(False)
        else:
            self.PTZDriverCheckBox_2.setEnabled(True)

        if self.deviceTypeCheckBox.isChecked():
            self.deviceTypeCheckBox_2.setEnabled(False)
        else:
            self.deviceTypeCheckBox_2.setEnabled(True)

        if self.analyticsDriverCheckBox.isChecked():
            self.analyticsDriverCheckBox_2.setEnabled(False)
        else:
            self.analyticsDriverCheckBox_2.setEnabled(True)

        if self.firmwareCheckBox.isChecked():
            self.firmwareCheckBox_2.setEnabled(False)
        else:
            self.firmwareCheckBox_2.setEnabled(True)

        if self.channelCheckBox.isChecked():
            self.channelCheckBox_2.setEnabled(False)
        else:
            self.channelCheckBox_2.setEnabled(True)

        if self.videoDriver1CheckBox_2.isChecked():
            self.videoDriver1CheckBox.setEnabled(False)
        else:
            self.videoDriver1CheckBox.setEnabled(True)

        if self.videoDriver2CheckBox_2.isChecked():
            self.videoDriver2CheckBox.setEnabled(False)
        else:
            self.videoDriver2CheckBox.setEnabled(True)

        if self.videoDriver3CheckBox_2.isChecked():
            self.videoDriver3CheckBox.setEnabled(False)
        else:
            self.videoDriver3CheckBox.setEnabled(True)

        if self.IODriverCheckBox_2.isChecked():
            self.IODriverCheckBox.setEnabled(False)
        else:
            self.IODriverCheckBox.setEnabled(True)

        if self.LPRDriverCheckBox_2.isChecked():
            self.LPRDriverCheckBox.setEnabled(False)
        else:
            self.LPRDriverCheckBox.setEnabled(True)

        if self.eventDriverCheckBox_2.isChecked():
            self.eventDriverCheckBox.setEnabled(False)
        else:
            self.eventDriverCheckBox.setEnabled(True)

        if self.edgeRecordingDriverCheckBox_2.isChecked():
            self.edgeRecordingDriverCheckBox.setEnabled(False)
        else:
            self.edgeRecordingDriverCheckBox.setEnabled(True)

        if self.PTZDriverCheckBox_2.isChecked():
            self.PTZDriverCheckBox.setEnabled(False)
        else:
            self.PTZDriverCheckBox.setEnabled(True)

        if self.deviceTypeCheckBox_2.isChecked():
            self.deviceTypeCheckBox.setEnabled(False)
        else:
            self.deviceTypeCheckBox.setEnabled(True)

        if self.analyticsDriverCheckBox_2.isChecked():
            self.analyticsDriverCheckBox.setEnabled(False)
        else:
            self.analyticsDriverCheckBox.setEnabled(True)

        if self.firmwareCheckBox_2.isChecked():
            self.firmwareCheckBox.setEnabled(False)
        else:
            self.firmwareCheckBox.setEnabled(True)

        if self.channelCheckBox_2.isChecked():
            self.channelCheckBox.setEnabled(False)
        else:
            self.channelCheckBox.setEnabled(True)

    def driverConsultor(self):
        global suggestedModels
        self.modelComboBox_2.clear()
        suggestedModels = []
        workingDrivers = []
        requiredDifference = []
        requiredDrivers = []

        #Set required drivers
        if self.videoDriver1CheckBox_2.isChecked():
            if not self.videoDriver1TextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.videoDriver1TextBrowser.toPlainText())
            requiredDrivers.append('VideoDriver1')
        if self.videoDriver2CheckBox_2.isChecked():
            if not self.videoDriver2TextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.videoDriver2TextBrowser.toPlainText())
            requiredDrivers.append('VideoDriver2')
        if self.videoDriver3CheckBox_2.isChecked():
            if not self.videoDriver3TextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.videoDriver3TextBrowser.toPlainText())
            requiredDrivers.append('VideoDriver3')
        if self.IODriverCheckBox_2.isChecked():
            if not self.IODriverTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.IODriverTextBrowser.toPlainText())
            requiredDrivers.append('DriverIO')
        if self.LPRDriverCheckBox_2.isChecked():
            if not self.LPRDriverTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.LPRDriverTextBrowser.toPlainText())
            requiredDrivers.append('EdgeLPR')
        if self.eventDriverCheckBox_2.isChecked():
            if not self.eventsDriverTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.eventsDriverTextBrowser.toPlainText())
            requiredDrivers.append('EventDriver')
        if self.edgeRecordingDriverCheckBox_2.isChecked():
            if not self.edgeRecordingTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.edgeRecordingTextBrowser.toPlainText())
            requiredDrivers.append('EdgeRecording')
        if self.PTZDriverCheckBox_2.isChecked():
            if not self.PTZDriverTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.PTZDriverTextBrowser.toPlainText())
            requiredDrivers.append('DriverPTZ')
        if self.deviceTypeCheckBox_2.isChecked():
            if not self.deviceTypeTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.deviceTypeTextBrowser.toPlainText())
            requiredDrivers.append('ModelType')
        if self.analyticsDriverCheckBox_2.isChecked():
            if not self.analyticsDriverTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.analyticsDriverTextBrowser.toPlainText())
            requiredDrivers.append('EdgeAnalytics')
        if self.firmwareCheckBox_2.isChecked():
            if not self.firmwareTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.firmwareTextBrowser.toPlainText())
            requiredDrivers.append('Firmware')
        if self.channelCheckBox_2.isChecked():
            if not self.channelsTextBrowser.toPlainText() == 'nan':
                requiredDifference.append(self.channelsTextBrowser.toPlainText())
            requiredDrivers.append('Channels')

        #Set working drivers
        if self.videoDriver1CheckBox.isChecked():
            workingDrivers.append(self.videoDriver1TextBrowser.toPlainText())
        if self.videoDriver2CheckBox.isChecked():
            workingDrivers.append(self.videoDriver2TextBrowser.toPlainText())
        if self.videoDriver3CheckBox.isChecked():
            workingDrivers.append(self.videoDriver3TextBrowser.toPlainText())
        if self.IODriverCheckBox.isChecked():
            workingDrivers.append(self.IODriverTextBrowser.toPlainText())
        if self.LPRDriverCheckBox.isChecked():
            workingDrivers.append(self.LPRDriverTextBrowser.toPlainText())
        if self.eventDriverCheckBox.isChecked():
            workingDrivers.append(self.eventsDriverTextBrowser.toPlainText())
        if self.edgeRecordingDriverCheckBox.isChecked():
            workingDrivers.append(self.edgeRecordingTextBrowser.toPlainText())
        if self.PTZDriverCheckBox.isChecked():
            workingDrivers.append(self.PTZDriverTextBrowser.toPlainText())
        if self.deviceTypeCheckBox.isChecked():
            workingDrivers.append(self.deviceTypeTextBrowser.toPlainText())
        if self.analyticsDriverCheckBox.isChecked():
            workingDrivers.append(self.analyticsDriverTextBrowser.toPlainText())
        if self.firmwareCheckBox.isChecked():
            workingDrivers.append(self.firmwareTextBrowser.toPlainText())
        if self.channelCheckBox.isChecked():
            workingDrivers.append(self.channelsTextBrowser.toPlainText())

        print ("Working Drivers: {}".format(workingDrivers))
        print ("Required Difference: {}".format(requiredDifference))

        for dictitem in dict_from_csv:
            flag = 'flag ok'

            if not all(drivers in str(dictitem.values()) for drivers in workingDrivers):
                flag = 'model not ok'
            if any(drivers in str(dictitem.values()) for drivers in requiredDifference):
                flag = 'model not ok'
            for driver in requiredDrivers:
                if str(dictitem[driver]) == 'nan':
                    flag = 'model not ok'
            if flag == 'flag ok':
                suggestedModels.append(dictitem['Model'])


        print (suggestedModels)
        #Populate Manufacturer ComboBox
        self.modelComboBox_2.addItems(suggestedModels)
        #Set Manufacturer List as editable and searchable
        self.modelComboBox_2.setEditable(True)
        self.modelComboBox_2.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        #Set completer
        self.modelComboBox_2.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    def loadSuggestedModels(self):
        #Clear Drivers ComboBox
        self.videoDriver1TextBrowser_2.clear()
        self.videoDriver2TextBrowser_2.clear()
        self.videoDriver3TextBrowser_2.clear()
        self.IODriverTextBrowser_2.clear()
        self.PTZDriverTextBrowser_2.clear()
        self.LPRDriverTextBrowser_2.clear()
        self.edgeRecordingTextBrowser_2.clear()
        self.analyticsDriverTextBrowser_2.clear()
        self.eventsDriverTextBrowser_2.clear()
        self.deviceTypeTextBrowser_2.clear()
        self.firmwareTextBrowser_2.clear()
        self.channelsTextBrowser_2.clear()
        #Find Model
        for dictitem in dict_from_csv:
            if dictitem['Model'] == str(self.modelComboBox_2.currentText()):
              #Load Drivers
              self.videoDriver1TextBrowser_2.setText(str(dictitem['VideoDriver1']))
              self.videoDriver2TextBrowser_2.setText(str(dictitem['VideoDriver2']))
              self.videoDriver3TextBrowser_2.setText(str(dictitem['VideoDriver3']))
              self.IODriverTextBrowser_2.setText(str(dictitem['DriverIO']))
              self.PTZDriverTextBrowser_2.setText(str(dictitem['DriverPTZ']))
              self.LPRDriverTextBrowser_2.setText(str(dictitem['EdgeLPR']))
              self.edgeRecordingTextBrowser_2.setText(str(dictitem['EdgeRecording']))
              self.analyticsDriverTextBrowser_2.setText(str(dictitem['EdgeAnalytics']))
              self.eventsDriverTextBrowser_2.setText(str(dictitem['EventDriver']))
              self.deviceTypeTextBrowser_2.setText(str(dictitem['ModelType']))
              self.firmwareTextBrowser_2.setText(str(dictitem['Firmware']))
              self.channelsTextBrowser_2.setText(str(dictitem['Channels']))

    def clearEverything(self):

        self.videoDriver1CheckBox.setChecked(False)
        self.videoDriver2CheckBox.setChecked(False)
        self.videoDriver3CheckBox.setChecked(False)
        self.IODriverCheckBox.setChecked(False)
        self.LPRDriverCheckBox.setChecked(False)
        self.eventDriverCheckBox.setChecked(False)
        self.edgeRecordingDriverCheckBox.setChecked(False)
        self.PTZDriverCheckBox.setChecked(False)
        self.deviceTypeCheckBox.setChecked(False)
        self.analyticsDriverCheckBox.setChecked(False)
        self.firmwareCheckBox.setChecked(False)
        self.channelCheckBox.setChecked(False)
        self.videoDriver1CheckBox_2.setChecked(False)
        self.videoDriver2CheckBox_2.setChecked(False)
        self.videoDriver3CheckBox_2.setChecked(False)
        self.IODriverCheckBox_2.setChecked(False)
        self.LPRDriverCheckBox_2.setChecked(False)
        self.eventDriverCheckBox_2.setChecked(False)
        self.edgeRecordingDriverCheckBox_2.setChecked(False)
        self.PTZDriverCheckBox_2.setChecked(False)
        self.deviceTypeCheckBox_2.setChecked(False)
        self.analyticsDriverCheckBox_2.setChecked(False)
        self.firmwareCheckBox_2.setChecked(False)
        self.channelCheckBox_2.setChecked(False)
        self.videoDriver1CheckBox.setEnabled(True)
        self.videoDriver2CheckBox.setEnabled(True)
        self.videoDriver3CheckBox.setEnabled(True)
        self.IODriverCheckBox.setEnabled(True)
        self.LPRDriverCheckBox.setEnabled(True)
        self.eventDriverCheckBox.setEnabled(True)
        self.edgeRecordingDriverCheckBox.setEnabled(True)
        self.PTZDriverCheckBox.setEnabled(True)
        self.deviceTypeCheckBox.setEnabled(True)
        self.analyticsDriverCheckBox.setEnabled(True)
        self.firmwareCheckBox.setEnabled(True)
        self.channelCheckBox.setEnabled(True)
        self.videoDriver1CheckBox_2.setEnabled(True)
        self.videoDriver2CheckBox_2.setEnabled(True)
        self.videoDriver3CheckBox_2.setEnabled(True)
        self.IODriverCheckBox_2.setEnabled(True)
        self.LPRDriverCheckBox_2.setEnabled(True)
        self.eventDriverCheckBox_2.setEnabled(True)
        self.edgeRecordingDriverCheckBox_2.setEnabled(True)
        self.PTZDriverCheckBox_2.setEnabled(True)
        self.deviceTypeCheckBox_2.setEnabled(True)
        self.analyticsDriverCheckBox_2.setEnabled(True)
        self.firmwareCheckBox_2.setEnabled(True)
        self.channelCheckBox_2.setEnabled(True)


    def setupUi(self, MainWindow):
        global icon
        global manufacturerComboBox
        global modelComboBox
        global modelComboBox_2
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(727, 647)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(727, 647))
        MainWindow.setMaximumSize(QtCore.QSize(727, 647))
        MainWindow.setBaseSize(QtCore.QSize(727, 647))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/icone.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LogoLabel = QtWidgets.QLabel(self.centralwidget)
        self.LogoLabel.setGeometry(QtCore.QRect(320, -10, 161, 131))
        self.LogoLabel.setObjectName("LogoLabel")
        self.manufacturerComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.manufacturerComboBox.setGeometry(QtCore.QRect(140, 170, 211, 21))
        self.manufacturerComboBox.setObjectName("manufacturerComboBox")
        self.manufacturerComboBox.currentIndexChanged.connect(self.loadModels)
        self.modelComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.modelComboBox.setGeometry(QtCore.QRect(140, 200, 211, 21))
        self.modelComboBox.setObjectName("modelComboBox")
        self.modelComboBox.currentIndexChanged.connect(self.loadDrivers)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 170, 81, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 200, 81, 21))
        self.label_2.setObjectName("label_2")
        self.videoDriver1TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.videoDriver1TextBrowser.setGeometry(QtCore.QRect(140, 230, 211, 21))
        self.videoDriver1TextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver1TextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver1TextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.videoDriver1TextBrowser.setObjectName("videoDriver1TextBrowser")
        self.videoDriverLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoDriverLabel.setGeometry(QtCore.QRect(20, 230, 71, 16))
        self.videoDriverLabel.setObjectName("videoDriverLabel")
        self.videoDriverLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.videoDriverLabel_2.setGeometry(QtCore.QRect(20, 260, 71, 16))
        self.videoDriverLabel_2.setObjectName("videoDriverLabel_2")
        self.videoDriver2TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.videoDriver2TextBrowser.setGeometry(QtCore.QRect(140, 260, 211, 21))
        self.videoDriver2TextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver2TextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver2TextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.videoDriver2TextBrowser.setObjectName("videoDriver2TextBrowser")
        self.videoDriverLabel_3 = QtWidgets.QLabel(self.centralwidget)
        self.videoDriverLabel_3.setGeometry(QtCore.QRect(20, 290, 71, 16))
        self.videoDriverLabel_3.setObjectName("videoDriverLabel_3")
        self.videoDriver3TextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.videoDriver3TextBrowser.setGeometry(QtCore.QRect(140, 290, 211, 21))
        self.videoDriver3TextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver3TextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver3TextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.videoDriver3TextBrowser.setObjectName("videoDriver3TextBrowser")
        self.IODriverLabel = QtWidgets.QLabel(self.centralwidget)
        self.IODriverLabel.setGeometry(QtCore.QRect(20, 320, 71, 16))
        self.IODriverLabel.setObjectName("IODriverLabel")
        self.IODriverTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.IODriverTextBrowser.setGeometry(QtCore.QRect(140, 320, 211, 21))
        self.IODriverTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.IODriverTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.IODriverTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.IODriverTextBrowser.setObjectName("IODriverTextBrowser")
        self.PTZDriverLabel = QtWidgets.QLabel(self.centralwidget)
        self.PTZDriverLabel.setGeometry(QtCore.QRect(20, 350, 71, 16))
        self.PTZDriverLabel.setObjectName("PTZDriverLabel")
        self.PTZDriverTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.PTZDriverTextBrowser.setGeometry(QtCore.QRect(140, 350, 211, 21))
        self.PTZDriverTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PTZDriverTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PTZDriverTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.PTZDriverTextBrowser.setObjectName("PTZDriverTextBrowser")
        self.analyticsDriverTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.analyticsDriverTextBrowser.setGeometry(QtCore.QRect(140, 440, 211, 21))
        self.analyticsDriverTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.analyticsDriverTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.analyticsDriverTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.analyticsDriverTextBrowser.setObjectName("analyticsDriverTextBrowser")
        self.LPRDriverTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.LPRDriverTextBrowser.setGeometry(QtCore.QRect(140, 380, 211, 21))
        self.LPRDriverTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.LPRDriverTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.LPRDriverTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.LPRDriverTextBrowser.setObjectName("LPRDriverTextBrowser")
        self.LPRDriverLabel = QtWidgets.QLabel(self.centralwidget)
        self.LPRDriverLabel.setGeometry(QtCore.QRect(20, 380, 71, 16))
        self.LPRDriverLabel.setObjectName("LPRDriverLabel")
        self.analyticsDriverLabel = QtWidgets.QLabel(self.centralwidget)
        self.analyticsDriverLabel.setGeometry(QtCore.QRect(20, 440, 71, 16))
        self.analyticsDriverLabel.setObjectName("analyticsDriverLabel")
        self.eventsDriverTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.eventsDriverTextBrowser.setGeometry(QtCore.QRect(140, 470, 211, 21))
        self.eventsDriverTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eventsDriverTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eventsDriverTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.eventsDriverTextBrowser.setObjectName("eventsDriverTextBrowser")
        self.edgeRecordingTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.edgeRecordingTextBrowser.setGeometry(QtCore.QRect(140, 410, 211, 21))
        self.edgeRecordingTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.edgeRecordingTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.edgeRecordingTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.edgeRecordingTextBrowser.setObjectName("edgeRecordingTextBrowser")
        self.deviceTypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.deviceTypeLabel.setGeometry(QtCore.QRect(20, 500, 71, 16))
        self.deviceTypeLabel.setObjectName("deviceTypeLabel")
        self.eventDriverLabel = QtWidgets.QLabel(self.centralwidget)
        self.eventDriverLabel.setGeometry(QtCore.QRect(20, 470, 71, 16))
        self.eventDriverLabel.setObjectName("eventDriverLabel")
        self.deviceTypeTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.deviceTypeTextBrowser.setGeometry(QtCore.QRect(140, 500, 211, 21))
        self.deviceTypeTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.deviceTypeTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.deviceTypeTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.deviceTypeTextBrowser.setObjectName("deviceTypeTextBrowser")
        self.EdgeRecordingDriverLabel = QtWidgets.QLabel(self.centralwidget)
        self.EdgeRecordingDriverLabel.setGeometry(QtCore.QRect(20, 410, 111, 16))
        self.EdgeRecordingDriverLabel.setObjectName("EdgeRecordingDriverLabel")
        self.firmwareTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.firmwareTextBrowser.setGeometry(QtCore.QRect(140, 530, 211, 21))
        self.firmwareTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.firmwareTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.firmwareTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.firmwareTextBrowser.setObjectName("firmwareTextBrowser")
        self.firmwareLabel = QtWidgets.QLabel(self.centralwidget)
        self.firmwareLabel.setGeometry(QtCore.QRect(20, 530, 71, 16))
        self.firmwareLabel.setObjectName("firmwareLabel")
        self.videoDriver1CheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.videoDriver1CheckBox.setGeometry(QtCore.QRect(370, 230, 16, 17))
        self.videoDriver1CheckBox.setText("")
        self.videoDriver1CheckBox.setObjectName("videoDriver1CheckBox")
        self.videoDriver1CheckBox.stateChanged.connect(self.checkBoxControl)
        self.videoDriver2CheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.videoDriver2CheckBox.setGeometry(QtCore.QRect(370, 260, 16, 17))
        self.videoDriver2CheckBox.setText("")
        self.videoDriver2CheckBox.setObjectName("videoDriver2CheckBox")
        self.videoDriver2CheckBox.stateChanged.connect(self.checkBoxControl)
        self.videoDriver3CheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.videoDriver3CheckBox.setGeometry(QtCore.QRect(370, 290, 16, 17))
        self.videoDriver3CheckBox.setText("")
        self.videoDriver3CheckBox.setObjectName("videoDriver3CheckBox")
        self.videoDriver3CheckBox.stateChanged.connect(self.checkBoxControl)
        self.IODriverCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.IODriverCheckBox.setGeometry(QtCore.QRect(370, 320, 16, 17))
        self.IODriverCheckBox.setText("")
        self.IODriverCheckBox.setObjectName("IODriverCheckBox")
        self.IODriverCheckBox.stateChanged.connect(self.checkBoxControl)
        self.LPRDriverCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.LPRDriverCheckBox.setGeometry(QtCore.QRect(370, 380, 16, 17))
        self.LPRDriverCheckBox.setText("")
        self.LPRDriverCheckBox.setObjectName("LPRDriverCheckBox")
        self.LPRDriverCheckBox.stateChanged.connect(self.checkBoxControl)
        self.eventDriverCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.eventDriverCheckBox.setGeometry(QtCore.QRect(370, 470, 16, 17))
        self.eventDriverCheckBox.setText("")
        self.eventDriverCheckBox.setObjectName("eventDriverCheckBox")
        self.eventDriverCheckBox.stateChanged.connect(self.checkBoxControl)
        self.edgeRecordingDriverCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.edgeRecordingDriverCheckBox.setGeometry(QtCore.QRect(370, 410, 16, 17))
        self.edgeRecordingDriverCheckBox.setText("")
        self.edgeRecordingDriverCheckBox.setObjectName("edgeRecordingDriverCheckBox")
        self.edgeRecordingDriverCheckBox.stateChanged.connect(self.checkBoxControl)
        self.PTZDriverCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.PTZDriverCheckBox.setGeometry(QtCore.QRect(370, 350, 16, 17))
        self.PTZDriverCheckBox.setText("")
        self.PTZDriverCheckBox.setObjectName("PTZDriverCheckBox")
        self.PTZDriverCheckBox.stateChanged.connect(self.checkBoxControl)
        self.deviceTypeCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.deviceTypeCheckBox.setGeometry(QtCore.QRect(370, 500, 16, 17))
        self.deviceTypeCheckBox.setText("")
        self.deviceTypeCheckBox.setObjectName("deviceTypeCheckBox")
        self.deviceTypeCheckBox.stateChanged.connect(self.checkBoxControl)
        self.analyticsDriverCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.analyticsDriverCheckBox.setGeometry(QtCore.QRect(370, 440, 16, 17))
        self.analyticsDriverCheckBox.setText("")
        self.analyticsDriverCheckBox.setObjectName("analyticsDriverCheckBox")
        self.analyticsDriverCheckBox.stateChanged.connect(self.checkBoxControl)
        self.firmwareCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.firmwareCheckBox.setGeometry(QtCore.QRect(370, 530, 16, 17))
        self.firmwareCheckBox.setText("")
        self.firmwareCheckBox.setObjectName("firmwareCheckBox")
        self.firmwareCheckBox.stateChanged.connect(self.checkBoxControl)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 130, 391, 491))
        self.groupBox.setObjectName("groupBox")
        self.currentWorkingLabel = QtWidgets.QLabel(self.groupBox)
        self.currentWorkingLabel.setGeometry(QtCore.QRect(340, 10, 51, 16))
        self.currentWorkingLabel.setObjectName("currentWorkingLabel")
        self.channelsTextBrowser = QtWidgets.QTextBrowser(self.groupBox)
        self.channelsTextBrowser.setGeometry(QtCore.QRect(130, 430, 211, 21))
        self.channelsTextBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.channelsTextBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.channelsTextBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.channelsTextBrowser.setObjectName("channelsTextBrowser")
        self.channelsLabel = QtWidgets.QLabel(self.groupBox)
        self.channelsLabel.setGeometry(QtCore.QRect(10, 430, 71, 16))
        self.channelsLabel.setObjectName("channelsLabel")
        self.channelCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.channelCheckBox.setGeometry(QtCore.QRect(360, 430, 16, 17))
        self.channelCheckBox.setObjectName("channelCheckBox")
        self.channelCheckBox.stateChanged.connect(self.checkBoxControl)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(10, 460, 181, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.driverConsultor)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(204, 460, 161, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.clearEverything)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(420, 130, 281, 491))
        self.groupBox_2.setObjectName("groupBox_2")
        self.modelComboBox_2 = QtWidgets.QComboBox(self.groupBox_2)
        self.modelComboBox_2.setGeometry(QtCore.QRect(10, 70, 211, 21))
        self.modelComboBox_2.setObjectName("modelComboBox_2")
        self.modelComboBox_2.currentIndexChanged.connect(self.loadSuggestedModels)
        self.currentWorkingLabel_2 = QtWidgets.QLabel(self.groupBox_2)
        self.currentWorkingLabel_2.setGeometry(QtCore.QRect(210, 10, 51, 16))
        self.currentWorkingLabel_2.setObjectName("currentWorkingLabel_2")
        self.videoDriver1TextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.videoDriver1TextBrowser_2.setGeometry(QtCore.QRect(10, 100, 211, 21))
        self.videoDriver1TextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver1TextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver1TextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.videoDriver1TextBrowser_2.setObjectName("videoDriver1TextBrowser_2")
        self.videoDriver2TextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.videoDriver2TextBrowser_2.setGeometry(QtCore.QRect(10, 130, 211, 21))
        self.videoDriver2TextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver2TextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver2TextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.videoDriver2TextBrowser_2.setObjectName("videoDriver2TextBrowser_2")
        self.videoDriver3TextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.videoDriver3TextBrowser_2.setGeometry(QtCore.QRect(10, 160, 211, 21))
        self.videoDriver3TextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver3TextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.videoDriver3TextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.videoDriver3TextBrowser_2.setObjectName("videoDriver3TextBrowser_2")
        self.IODriverTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.IODriverTextBrowser_2.setGeometry(QtCore.QRect(10, 190, 211, 21))
        self.IODriverTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.IODriverTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.IODriverTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.IODriverTextBrowser_2.setObjectName("IODriverTextBrowser_2")
        self.PTZDriverTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.PTZDriverTextBrowser_2.setGeometry(QtCore.QRect(10, 220, 211, 21))
        self.PTZDriverTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PTZDriverTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PTZDriverTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.PTZDriverTextBrowser_2.setObjectName("PTZDriverTextBrowser_2")
        self.LPRDriverTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.LPRDriverTextBrowser_2.setGeometry(QtCore.QRect(10, 250, 211, 21))
        self.LPRDriverTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.LPRDriverTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.LPRDriverTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.LPRDriverTextBrowser_2.setObjectName("LPRDriverTextBrowser_2")
        self.edgeRecordingTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.edgeRecordingTextBrowser_2.setGeometry(QtCore.QRect(10, 280, 211, 21))
        self.edgeRecordingTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.edgeRecordingTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.edgeRecordingTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.edgeRecordingTextBrowser_2.setObjectName("edgeRecordingTextBrowser_2")
        self.analyticsDriverTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.analyticsDriverTextBrowser_2.setGeometry(QtCore.QRect(10, 310, 211, 21))
        self.analyticsDriverTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.analyticsDriverTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.analyticsDriverTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.analyticsDriverTextBrowser_2.setObjectName("analyticsDriverTextBrowser_2")
        self.eventsDriverTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.eventsDriverTextBrowser_2.setGeometry(QtCore.QRect(10, 340, 211, 21))
        self.eventsDriverTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eventsDriverTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eventsDriverTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.eventsDriverTextBrowser_2.setObjectName("eventsDriverTextBrowser_2")
        self.deviceTypeTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.deviceTypeTextBrowser_2.setGeometry(QtCore.QRect(10, 370, 211, 21))
        self.deviceTypeTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.deviceTypeTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.deviceTypeTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.deviceTypeTextBrowser_2.setObjectName("deviceTypeTextBrowser_2")
        self.firmwareTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.firmwareTextBrowser_2.setGeometry(QtCore.QRect(10, 400, 211, 21))
        self.firmwareTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.firmwareTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.firmwareTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.firmwareTextBrowser_2.setObjectName("firmwareTextBrowser_2")
        self.channelsTextBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.channelsTextBrowser_2.setGeometry(QtCore.QRect(10, 430, 211, 21))
        self.channelsTextBrowser_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.channelsTextBrowser_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.channelsTextBrowser_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.channelsTextBrowser_2.setObjectName("channelsTextBrowser_2")
        self.channelCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.channelCheckBox_2.setGeometry(QtCore.QRect(230, 430, 16, 17))
        self.channelCheckBox_2.setObjectName("channelCheckBox_2")
        self.channelCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.firmwareCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.firmwareCheckBox_2.setGeometry(QtCore.QRect(230, 400, 16, 17))
        self.firmwareCheckBox_2.setText("")
        self.firmwareCheckBox_2.setObjectName("firmwareCheckBox_2")
        self.firmwareCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.eventDriverCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.eventDriverCheckBox_2.setGeometry(QtCore.QRect(230, 340, 16, 17))
        self.eventDriverCheckBox_2.setText("")
        self.eventDriverCheckBox_2.setObjectName("eventDriverCheckBox_2")
        self.eventDriverCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.analyticsDriverCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.analyticsDriverCheckBox_2.setGeometry(QtCore.QRect(230, 310, 16, 17))
        self.analyticsDriverCheckBox_2.setText("")
        self.analyticsDriverCheckBox_2.setObjectName("analyticsDriverCheckBox_2")
        self.analyticsDriverCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.videoDriver1CheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.videoDriver1CheckBox_2.setGeometry(QtCore.QRect(230, 100, 16, 17))
        self.videoDriver1CheckBox_2.setText("")
        self.videoDriver1CheckBox_2.setObjectName("videoDriver1CheckBox_2")
        self.videoDriver1CheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.deviceTypeCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.deviceTypeCheckBox_2.setGeometry(QtCore.QRect(230, 370, 16, 17))
        self.deviceTypeCheckBox_2.setText("")
        self.deviceTypeCheckBox_2.setObjectName("deviceTypeCheckBox_2")
        self.deviceTypeCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.LPRDriverCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.LPRDriverCheckBox_2.setGeometry(QtCore.QRect(230, 250, 16, 17))
        self.LPRDriverCheckBox_2.setText("")
        self.LPRDriverCheckBox_2.setObjectName("LPRDriverCheckBox_2")
        self.LPRDriverCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.videoDriver3CheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.videoDriver3CheckBox_2.setGeometry(QtCore.QRect(230, 160, 16, 17))
        self.videoDriver3CheckBox_2.setText("")
        self.videoDriver3CheckBox_2.setObjectName("videoDriver3CheckBox_2")
        self.videoDriver3CheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.IODriverCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.IODriverCheckBox_2.setGeometry(QtCore.QRect(230, 190, 16, 17))
        self.IODriverCheckBox_2.setText("")
        self.IODriverCheckBox_2.setObjectName("IODriverCheckBox_2")
        self.IODriverCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.PTZDriverCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.PTZDriverCheckBox_2.setGeometry(QtCore.QRect(230, 220, 16, 17))
        self.PTZDriverCheckBox_2.setText("")
        self.PTZDriverCheckBox_2.setObjectName("PTZDriverCheckBox_2")
        self.PTZDriverCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.edgeRecordingDriverCheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.edgeRecordingDriverCheckBox_2.setGeometry(QtCore.QRect(230, 280, 16, 17))
        self.edgeRecordingDriverCheckBox_2.setText("")
        self.edgeRecordingDriverCheckBox_2.setObjectName("edgeRecordingDriverCheckBox_2")
        self.edgeRecordingDriverCheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.videoDriver2CheckBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.videoDriver2CheckBox_2.setGeometry(QtCore.QRect(230, 130, 16, 17))
        self.videoDriver2CheckBox_2.setText("")
        self.videoDriver2CheckBox_2.setObjectName("videoDriver2CheckBox_2")
        self.videoDriver2CheckBox_2.stateChanged.connect(self.checkBoxControl)
        self.fileselectbutton = QtWidgets.QPushButton(self.centralwidget)
        self.fileselectbutton.setGeometry(QtCore.QRect(90, 60, 75, 23))
        self.fileselectbutton.setObjectName("fileselectbutton")
        self.fileselectbutton.clicked.connect(self.selectFile)
        self.loadTableLabel = QtWidgets.QLabel(self.centralwidget)
        self.loadTableLabel.setGeometry(QtCore.QRect(16, 60, 68, 23))
        self.loadTableLabel.setObjectName("loadTableLabel")
        self.tableStatusIndicator = QtWidgets.QLabel(self.centralwidget)
        self.tableStatusIndicator.setGeometry(QtCore.QRect(100, 100, 71, 16))
        self.tableStatusIndicator.setObjectName("tableStatusIndicator")
        self.tableStatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.tableStatusLabel.setGeometry(QtCore.QRect(10, 100, 81, 16))
        self.tableStatusLabel.setObjectName("tableStatusLabel")
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.LogoLabel.raise_()
        self.manufacturerComboBox.raise_()
        self.modelComboBox.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.videoDriver1TextBrowser.raise_()
        self.videoDriverLabel.raise_()
        self.videoDriverLabel_2.raise_()
        self.videoDriver2TextBrowser.raise_()
        self.videoDriverLabel_3.raise_()
        self.videoDriver3TextBrowser.raise_()
        self.IODriverLabel.raise_()
        self.IODriverTextBrowser.raise_()
        self.PTZDriverLabel.raise_()
        self.PTZDriverTextBrowser.raise_()
        self.analyticsDriverTextBrowser.raise_()
        self.LPRDriverTextBrowser.raise_()
        self.LPRDriverLabel.raise_()
        self.analyticsDriverLabel.raise_()
        self.eventsDriverTextBrowser.raise_()
        self.edgeRecordingTextBrowser.raise_()
        self.deviceTypeLabel.raise_()
        self.eventDriverLabel.raise_()
        self.deviceTypeTextBrowser.raise_()
        self.EdgeRecordingDriverLabel.raise_()
        self.firmwareTextBrowser.raise_()
        self.firmwareLabel.raise_()
        self.videoDriver1CheckBox.raise_()
        self.videoDriver2CheckBox.raise_()
        self.videoDriver3CheckBox.raise_()
        self.IODriverCheckBox.raise_()
        self.LPRDriverCheckBox.raise_()
        self.eventDriverCheckBox.raise_()
        self.edgeRecordingDriverCheckBox.raise_()
        self.PTZDriverCheckBox.raise_()
        self.deviceTypeCheckBox.raise_()
        self.analyticsDriverCheckBox.raise_()
        self.firmwareCheckBox.raise_()
        self.fileselectbutton.raise_()
        self.loadTableLabel.raise_()
        self.tableStatusIndicator.raise_()
        self.tableStatusLabel.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Digifort Driver Consult"))
        self.LogoLabel.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/logo/png.png\"/></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Manufacturer"))
        self.label_2.setText(_translate("MainWindow", "Model"))
        self.videoDriverLabel.setText(_translate("MainWindow", "Video Driver 1"))
        self.videoDriverLabel_2.setText(_translate("MainWindow", "Video Driver 2"))
        self.videoDriverLabel_3.setText(_translate("MainWindow", "Video Driver 3"))
        self.IODriverLabel.setText(_translate("MainWindow", "IO Driver"))
        self.PTZDriverLabel.setText(_translate("MainWindow", "PTZ Driver"))
        self.LPRDriverLabel.setText(_translate("MainWindow", "LPR Driver"))
        self.analyticsDriverLabel.setText(_translate("MainWindow", "Analytics Driverr"))
        self.deviceTypeLabel.setText(_translate("MainWindow", "Device Type"))
        self.eventDriverLabel.setText(_translate("MainWindow", "Events Driver"))
        self.EdgeRecordingDriverLabel.setText(_translate("MainWindow", "Edge Recording Driver"))
        self.firmwareLabel.setText(_translate("MainWindow", "Firmware"))
        self.groupBox.setTitle(_translate("MainWindow", "Tested Model"))
        self.currentWorkingLabel.setText(_translate("MainWindow", " Working"))
        self.channelsLabel.setText(_translate("MainWindow", "Channels"))
        self.channelCheckBox.setText(_translate("MainWindow", "Channels"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.pushButton_2.setText(_translate("MainWindow", "Clear"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Suggested model"))
        self.currentWorkingLabel_2.setText(_translate("MainWindow", "Search for"))
        self.channelCheckBox_2.setText(_translate("MainWindow", "Channels"))
        self.fileselectbutton.setText(_translate("MainWindow", "..."))
        self.loadTableLabel.setText(_translate("MainWindow", "Load Table"))
        self.tableStatusIndicator.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">UNLOADED</span></p></body></html>"))
        self.tableStatusLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:10pt;\">Table Status</span></p></body></html>"))
import logo_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
