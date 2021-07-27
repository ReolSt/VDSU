# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\GUI\options.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(634, 330)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 621, 311))
        self.tabWidget.setObjectName("tabWidget")
        self.General = QtWidgets.QWidget()
        self.General.setObjectName("General")
        self.groupBox = QtWidgets.QGroupBox(self.General)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 591, 71))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 171, 41))
        self.label.setObjectName("label")
        self.DriveFolderIDEdit = QtWidgets.QLineEdit(self.groupBox)
        self.DriveFolderIDEdit.setGeometry(QtCore.QRect(210, 30, 351, 21))
        self.DriveFolderIDEdit.setObjectName("DriveFolderIDEdit")
        self.groupBox_2 = QtWidgets.QGroupBox(self.General)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 100, 591, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.SaveFilePathEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.SaveFilePathEdit.setGeometry(QtCore.QRect(210, 30, 291, 21))
        self.SaveFilePathEdit.setReadOnly(True)
        self.SaveFilePathEdit.setObjectName("SaveFilePathEdit")
        self.SelectSaveFilePathButton = QtWidgets.QPushButton(self.groupBox_2)
        self.SelectSaveFilePathButton.setGeometry(QtCore.QRect(520, 30, 41, 21))
        self.SelectSaveFilePathButton.setObjectName("SelectSaveFilePathButton")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 91, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 101, 16))
        self.label_3.setObjectName("label_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton.setGeometry(QtCore.QRect(220, 70, 71, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_2.setGeometry(QtCore.QRect(350, 70, 71, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_3.setGeometry(QtCore.QRect(470, 70, 81, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.groupBox_4 = QtWidgets.QGroupBox(self.General)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 210, 591, 71))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 201, 41))
        self.label_5.setObjectName("label_5")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_2.setGeometry(QtCore.QRect(250, 25, 21, 31))
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.tabWidget.addTab(self.General, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Google Drive Preference"))
        self.label.setText(_translate("Form", "Save File Folder ID (see URL)"))
        self.groupBox_2.setTitle(_translate("Form", "Local File Preference"))
        self.SelectSaveFilePathButton.setText(_translate("Form", "..."))
        self.label_2.setText(_translate("Form", "Save File Path"))
        self.label_3.setText(_translate("Form", "Backup File Style"))
        self.radioButton.setText(_translate("Form", "Time"))
        self.radioButton_2.setText(_translate("Form", ".old"))
        self.radioButton_3.setText(_translate("Form", "No Backup"))
        self.groupBox_4.setTitle(_translate("Form", "Background "))
        self.label_5.setText(_translate("Form", "Minimize to system tray on close"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.General), _translate("Form", "General"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

