from ValheimSaveFileUpdater import ValheimSaveFileUpdater, TerrariaSaveFileUpdater
import sys
import os

import configparser

from MainUI import MainUI
from ConfiguresUI import ConfiguresUI

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, \
    QFileDialog

GAMEPRESET_VALHEIM = 0
GAMEPRESET_MINECRAFT = 1
GAMEPRESET_TERRARIA = 2
GAMEPRESET_DIABLO2 = 3

BACKUPSTYLE_TIME = 0
BACKUPSTYLE_OLD = 1
BACKUPSTYLE_NOBACKUP = 2


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
        'worldname': "None",
        'drivefolderid': "None",
        'gamepreset': 0,
        'savefilepath': default_path,
        'backupstyle': BACKUPSTYLE_TIME,
        'minimizetosystemtrayonclose': 0
    }

    return config


def config_file_exists():
    return os.path.exists("config.ini")


def create_config_file_if_not_exists():
    config = configparser.ConfigParser()
    if not config_file_exists():
        with open("config.ini", "w", encoding="cp949") as config_file:
            config = get_default_config()
            config.write(config_file)


class ConfiguresWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = ConfiguresUI()
        self.ui.setupUi(self)

        self.ui.SelectSaveFilePathButton.clicked.connect(
            self.select_save_file_path)

        create_config_file_if_not_exists()

        self.config = configparser.ConfigParser()

        with open("config.ini", "r", encoding="utf-8") as config_file:
            self.config.read_file(config_file)
            self.ui.WorldNameEdit.setText(
                self.config['General']['worldname'])
            self.ui.GamePresetComboBox.setCurrentIndex(
                int(self.config['General']['gamepreset']))
            self.ui.DriveFolderIDEdit.setText(
                self.config['General']['drivefolderid'])
            self.ui.SaveFilePathEdit.setText(
                self.config['General']['savefilepath'])

            backup_style = int(self.config['General']['backupstyle'])
            self.ui.TimeRadioButton.setChecked(backup_style == BACKUPSTYLE_TIME)
            self.ui.OldRadioButton.setChecked(backup_style == BACKUPSTYLE_OLD)
            self.ui.NoBackupRadioButton.setChecked(backup_style == BACKUPSTYLE_NOBACKUP)

            self.ui.TrayCheckBox.setChecked(
                bool(int(self.config['General']['minimizetosystemtrayonclose'])))

    def select_save_file_path(self):
        self.ui.SaveFilePathEdit.setText(QFileDialog.getExistingDirectory(
            self, "Select Save File Directory"))

    def closeEvent(self, event):
        self.config['General']['worldname'] = self.ui.WorldNameEdit.text()
        self.config['General']['gamepreset'] = str(self.ui.GamePresetComboBox.currentIndex())
        self.config['General']['drivefolderid'] = self.ui.DriveFolderIDEdit.text()
        self.config['General']['savefilepath'] = self.ui.SaveFilePathEdit.text()
        self.config['General']['backupstyle'] = str( \
            self.ui.TimeRadioButton.isChecked() * BACKUPSTYLE_TIME + \
            self.ui.OldRadioButton.isChecked() * BACKUPSTYLE_OLD + \
            self.ui.NoBackupRadioButton.isChecked() * BACKUPSTYLE_NOBACKUP)

        self.config['General']['minimizetosystemtrayonclose'] = \
            str(int(self.ui.TrayCheckBox.isChecked()))

        with open("config.ini", "w", encoding="utf-8") as config_file:
            self.config.write(config_file)

        event.accept()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = MainUI()
        self.ui.setupUi(self)

        self.ui.UpdateLocalFileButton.clicked.connect(self.update_local)
        self.ui.UpdateDriveFileButton.clicked.connect(self.update_drive)
        self.ui.AutoUpdateCheckBox.stateChanged.connect(self.toggle_auto_update)
        self.ui.actionConfigures.triggered.connect(self.open_configures)

        create_config_file_if_not_exists()

        self.config = configparser.ConfigParser()

        with open("config.ini", "r", encoding="utf-8") as config_file:
            self.config.read_file(config_file)
            self.auto_update = self.config['Main']['autoupdate']
            self.world_name = self.config['General']['worldname']
            self.game_preset = int(self.config['General']['gamepreset'])
            self.drive_folder_id = self.config['General']['drivefolderid']
            self.save_file_path = self.config['General']['savefilepath']
            self.backup_style = self.config['General']['backupstyle']

            if self.game_preset == GAMEPRESET_VALHEIM:
                self.save_file_updater = ValheimSaveFileUpdater(
                    "credentials.json",
                    self.drive_folder_id,
                    self.save_file_path,
                    self.world_name)
            elif self.game_preset == GAMEPRESET_TERRARIA:
                self.save_file_updater = TerrariaSaveFileUpdater(
                    "credentials.json",
                    self.drive_folder_id,
                    self.save_file_path,
                    self.world_name)

    def open_configures(self):
        self._configures_widget = ConfiguresWidget()
        self._configures_widget.show()

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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
