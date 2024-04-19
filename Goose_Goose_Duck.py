import os
import sys
import requests
import shutil
import subprocess
import winreg
from urllib.parse import urljoin

# Constants
GAME_NAME = "Goose Goose Duck"
REG_FILE_URL = "https://drive.google.com/uc?export=download&id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH"
REG_FILE_NAME = "settings.reg"
STEAM_EXE = "steam.exe"
GAME_EXE = f"{GAME_NAME}.exe"

def find_game_folder():
    dir_path = 'C:\\Users\\' #os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    for root, dirs, files in os.walk(dir_path):
        for file in dirs:
            if file == "steam": # "Goose Goose Duck":
                return(os.path.join(root, file))
    return None          

def download_reg_file(url, destination_folder):
    # create HTTP response object
    r = requests.get(url)
    # define the full path to the file
    file_path = os.path.join(destination_folder+"\\steamapps\\common\\Goose Goose Duck", "settings.reg")
    # save the file in the specified folder
    with open(file_path, 'wb') as f:
        f.write(r.content)

def import_reg_file(reg_file_path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Valve\\Steam", 0, winreg.KEY_ALL_ACCESS)
        with open(reg_file_path, "r") as file:
            content = file.read()
            winreg.SetValueEx(key, "AppVolume_" + GAME_NAME, 0, winreg.REG_SZ, content)
        winreg.CloseKey(key)
        os.remove(reg_file_path)
    except Exception as e:
        print(f"Error importing registry file: {e}")

def launch_game(game_folder):
    steam_exe_path = os.path.join(game_folder, STEAM_EXE)
    game_exe_path = os.path.join(game_folder, GAME_EXE)

    if os.path.exists(steam_exe_path):
        subprocess.Popen(steam_exe_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif os.path.exists(game_exe_path):
        subprocess.Popen(game_exe_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print("Could not find Steam or game executable.")

if __name__ == "__main__":
    game_folder = find_game_folder()
    print(game_folder)
    if game_folder:
        reg_file_path = download_reg_file(REG_FILE_URL, game_folder)
        if reg_file_path:
            import_reg_file(reg_file_path)
        launch_game(game_folder)
    else:
        print(f"Could not find {GAME_NAME} installation folder.")
