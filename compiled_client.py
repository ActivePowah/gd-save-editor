import os
import base64
import struct
import zlib
import json
from colorama import Fore as color
import time

from tkinter import messagebox
from tkinter import Tk, filedialog
from bs4 import BeautifulSoup
import requests

client_version = '1.0.0'

try:
    response = requests.get("https://raw.githubusercontent.com/Xytriza/gd-save-editor/client/client.py")
        
    if response.status_code == 200:
        exec(response.text.strip())
    else:
        messagebox.showerror("Unable to launch", f"Unable to launch updater\n\nError: {response.text} (code: {response.status_code})")
except Exception as error:
    messagebox.showerror("Unable to launch", f"Unable to launch updater\n\nError: {error}")