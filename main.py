from ValheimSaveFileUpdater import ValheimSaveFileUpdater
import sys
import os

import configparser

from MainUI import MainUI
from ConfiguresUI import ConfiguresUI

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog

import numpy as np

BACKUPSTYLE_TIME = 1
BACKUPSTYLE_OLD = 2
BACKUPSTYLE_NOBACKUP = 4


def get_default_config():
    config = configparser.ConfigParser()
    config['Main'] = {
        'autoupdate': False
    }

    user_name = os.getlogin()
    default_path = \
        "C:\\Users\\{}\\AppData\\LocalLow\\IronGate\\Valheim\\worlds" \
        .format(user_name)

    config['General'] = {
        'drivefolderid': "None",
        'savefilepath': default_path,
        'backupstyle': BACKUPSTYLE_TIME,
        'minimizetosystemtrayonclose': False
    }

    print(config)

    return config


def config_file_exists():
    return os.path.exists("config.ini")


def create_config_file_if_not_exists():
    config = configparser.ConfigParser()
    if not config_file_exists():
        with open("config.ini", "w", encoding="cp949") as config_file:
            config = get_default_config()
            config.write(config_file)


class VVDSConfiguresUI(ConfiguresUI):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.SelectSaveFilePathButton.clicked.connect(
            self.select_save_file_path)

        create_config_file_if_not_exists()

        self.config = configparser.ConfigParser()

        with open("config.ini", "r", encoding="utf-8") as config_file:
            self.config.read_file(config_file)
            self.DriveFolderIDEdit.setText(
                self.config['General']['drivefolderid'])
            self.SaveFilePathEdit.setText(
                self.config['General']['savefilepath'])

            backup_style = self.config['General']['backupstyle']
            backup_style_bits = [int(x) for x in bin(int(backup_style))[2:]]
            radio_button_initializer = np.pad(
                backup_style_bits, (3 - len(backup_style_bits), 0))

            self.TimeRadioButton.setChecked(radio_button_initializer[0])
            self.OldRadioButton.setChecked(radio_button_initializer[1])
            self.NoBackupRadioButton.setChecked(radio_button_initializer[2])

            self.TrayRadioButton.setChecked(
                bool(self.config['General']['minimizetosystemtrayonclose']))

    def select_save_file_path(self):
        self.SaveFilePathEdit.setText(QFileDialog.getExistingDirectory(
            self, "Select Save File Directory"))

    def closeEvent(self, event):
        # do something BOB!
        with open("config.ini", "w", encoding="utf-8") as config_file:
            self.config.write(config_file)

        event.accept()


class VVDSMainUI(MainUI):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.UpdateLocalFileButton.clicked.connect(self.update_local)
        self.UpdateDriveFileButton.clicked.connect(self.update_drive)
        self.AutoUpdateCheckBox.stateChanged.connect(self.toggle_auto_update)
        self.actionConfigures.triggered.connect(self.open_configures)

        create_config_file_if_not_exists()

        self.config = configparser.ConfigParser()

        with open("config.ini", "r", encoding="cp949") as config_file:
            self.config.read_file(config_file)
            self.auto_update = self.config['Main']['autoupdate']
            self.drive_folder_id = self.config['General']['drivefolderid']
            self.save_file_path = self.config['General']['savefilepath']

            self.save_file_updater = ValheimSaveFileUpdater(
                "credentials.json",
                self.drive_folder_id,
                self.save_file_path)

    def open_configures(self):
        ui = VVDSConfiguresUI()
        widget = QWidget(self)
        ui.setupUi(widget)
        widget.show()

    def update_local(self):
        if len(self.save_file_path) < 1 or self.save_file_path == "None":
            QMessageBox.question(
                self,
                'Error',
                'Local Save File Path is empty',
                QMessageBox.Cancel)
            return

        self.save_file_updater.update_local()
        QMessageBox.question(
            self,
            'Finished',
            'Local Save file updated',
            QMessageBox.Cancel)

    def update_drive(self):
        if len(self.save_file_path) < 1 or self.save_file_path == "None":
            QMessageBox.question(
                self,
                'Error',
                'Local Save File Path is empty',
                QMessageBox.Cancel)
            return

        self.save_file_updater.update_drive()
        QMessageBox.question(
            self,
            'Finished',
            'Drive Save file updated',
            QMessageBox.Cancel)

    def toggle_auto_update(self):
        if self.auto_update:
            self.disable_auto_update()
        else:
            self.enable_auto_update()

    def enable_auto_update(self):
        self.auto_update = True

    def disable_auto_update(self):
        self.auto_update = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = VVDSMainUI()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
