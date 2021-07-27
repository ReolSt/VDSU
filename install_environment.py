import os

os.system("pip install --upgrade pip")
os.system("pip install virtualenv")

os.system("virtualenv env")
os.system("env\Scripts\pip.exe install -r requirements.txt")