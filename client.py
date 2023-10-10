import os
import base64
import struct
import zlib
import json
from colorama import Fore as color
import time
try:
    import psutil
except ModuleNotFoundError:
    pass
# modules not included in 1.0.0

from tkinter import messagebox
from tkinter import Tk, filedialog
from bs4 import BeautifulSoup
import requests

try:
    try:
        response = requests.get('https://github.com/Xytriza/gd-save-editor/releases/latest')

        if response.status_code == 200:
            version = BeautifulSoup(response.text, "html.parser").find("h1", {"data-view-component": "true"}).text.strip()
            comment = BeautifulSoup(response.text, "html.parser").find("div", {"data-pjax": "true", "data-test-selector": "body-content", "data-view-component": "true", "class": "markdown-body my-3"}).text.strip()
        else:
            version = 'n/a'
            comment = 'n/a'
    except:
        version = 'n/a'
        comment = 'n/a'

    #client_version is not defined here, it's defined in the compiled version (https://github.com/Xytriza/gd-save-editor/blob/client/compiled_client.py)

    if version != 'n/a' and version != client_version:
        messagebox.showwarning("Update required", f"GD Save Editor requires an update\n\nYour version: {client_version}\nLatest version: {version}\nUpdate Includes: {comment}\n\nPress \"OK\" to update")
        window = Tk()
        window.withdraw()

        default_file_name = "GD Save Editor.exe"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".exe",
            filetypes=[("Executable Files", "*.exe")],
            initialfile=default_file_name
        )

        window.destroy()

        if save_path:
            try:
                print("Downloading update")
                response = requests.get(f"https://github.com/Xytriza/gd-save-editor/releases/latest/download/gd-save-editor.exe")
                os.system("cls")

                if response.status_code == 200:
                    try:
                        with open(save_path, 'wb') as file:
                            file.write(response.content)
                            messagebox.showinfo("Update downloaded successfully", f"Run the file that has been downloaded to your computer at {save_path} to use the update.")
                    except Exception as error:
                        messagebox.showerror("Error while downloading update", f"There was an error while attempting to download the file.\n\nIf you are attempting to save the file to a running program, please try closing the program or temporaily save the file with a different name\n\nError: {error}")
                else:
                    messagebox.showerror("Error while downloading update    ", f"There was an error while attempting to download the file.\n\nError: {response.text} (code: {response.status_code})\n\nPlease try again or contact us at cryfxreal@gmail.com for info on how to fix this issue.")
            except:
                messagebox.showerror("Error while downloading update", "There was an error while attempting to download the file.\n\nPlease try again or contact us at cryfxreal@gmail.com for info on how to fix this issue.")
        else:
            messagebox.showerror("Error while downloading update", "There was an error while attempting to download the file.\n\nPlease try again or contact us at cryfxreal@gmail.com for info on how to fix this issue.")
    else:
        try:
            response = requests.get("https://raw.githubusercontent.com/Xytriza/gd-save-editor/main/gd-save-editor.py")
                    
            if response.status_code == 200:
                exec(response.text.strip())
            else:
                messagebox.showerror("Unable to launch", f"Unable to launch GD Save Editor\n\nError: {response.text} (code: {response.status_code})")
        except Exception as error:
            messagebox.showerror("GD Save Editor has Crashed", f"GD Save Editor has crashed\n\nError: {error}")
except Exception as error:
    messagebox.showerror("Unable to launch", f"Unable to launch updater\n\nError: {error}")