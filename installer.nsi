!include "MUI2.nsh"

Name "VDSU"
OutFile "VDSU installer.exe"
Unicode True

;Default installation folder
InstallDir "$DESKTOP\VDSU"

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "C:\Users\Emacser\Desktop\python\VVDS\License.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

;Request application privileges for Windows Vista
RequestExecutionLevel user

Section "Python 3.8"
  SetOutPath "$INSTDIR"

  File resources\PythonInstaller.exe
  ExecWait "$INSTDIR\PythonInstaller.exe PrependPath=1"
SectionEnd

Section "Python Virtual Environment"
  SetOutPath "$INSTDIR"

  File install_environment.exe
  File requirements.txt

  ExecWait $INSTDIR\install_environment.exe
SectionEnd

Section "Openssl 1.1.1"
  SetOutPath "$INSTDIR"

  File resources\OpensslInstaller.exe
  ExecWait $INSTDIR\OpensslInstaller.exe
SectionEnd

Section "VVDS"
  SetOutPath "$INSTDIR"

  File License.txt
  File credentials.json
  File ValheimSaveFileUpdater.py
  File MainUI.py
  File ConfiguresUI.py
  File main.py
  File VVDS.exe

  WriteUninstaller $INSTDIR\Uninstall.exe
SectionEnd

Section Uninstall
    RMDIR /r "$INSTDIR"
SectionEnd

Function .onInit
    InitPluginsDir
    File /oname=$PLUGINSDIR\splash.bmp resources\splash.bmp

    advsplash::show 1000 600 400 -1 $PLUGINSDIR\splash

    Pop $0

    Delete $PLUGINSDIR\splash.bmp
FunctionEnd