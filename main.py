import os
import requests
import subprocess
import atexit
import tempfile
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle

# Constants
FILE_LIST = [
    {"name": "Steam", "url": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe", "msi": False},
    {"name": "Epic Games", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "msi": True},
    {"name": "Minecraft", "url": "https://launcher.mojang.com/download/MinecraftInstaller.msi", "msi": True},
    {"name": "Oracle Java 17", "url": "https://download.oracle.com/java/17/archive/jdk-17.0.8_windows-x64_bin.msi", "msi": True},
    {"name": "Adoptium Java 17", "url": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/372925194/de257a55-edf1-434b-aca2-9bfe51582b85?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230804%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230804T114230Z&X-Amz-Expires=300&X-Amz-Signature=f6ff2a1e53d7e11f3361907ea686c1080f47f73881d7a45e77accc4d1eb10562&X-Amz-SignedHeaders=host&actor_id=139683653&key_id=0&repo_id=372925194&response-content-disposition=attachment%3B%20filename%3DOpenJDK17U-jdk_x64_windows_hotspot_17.0.8_7.msi&response-content-type=application%2Foctet-stream", "msi": True},
    {"name": "Geforce Experience", "url": "https://us.download.nvidia.com/GFE/GFEClient/3.27.0.112/GeForce_Experience_v3.27.0.112.exe", "msi": False},
    {"name": "Visual C++ Redistribute", "url": "https://aka.ms/vs/17/release/vc_redist.x64.exe", "msi": False},
    {"name": "Qbittorent", "url": "https://download.fosshub.com/Protected/expiretime=1691199675;badurl=aHR0cHM6Ly93d3cuZm9zc2h1Yi5jb20vcUJpdHRvcnJlbnQuaHRtbA==/bcfc73f5ce2a762e9c534ad2ce729885c47d8bcbe0526939cf234111a7cdb712/5b8793a7f9ee5a5c3e97a3b2/648f3f47cf0a39defa2f67a2/qbittorrent_4.5.4_lt20_qt6_x64_setup.exe", "msi": False},
    {"name": "NotePad++", "url": "https://objects.githubusercontent.com/github-production-release-asset-2e65be/33014811/5a74a03e-3fac-418a-8153-b2dce220b5f7?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230804%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230804T114955Z&X-Amz-Expires=300&X-Amz-Signature=bcc668f9aaf309159eea97bf39612725475eebf816258c11fc36f65178498056&X-Amz-SignedHeaders=host&actor_id=139683653&key_id=0&repo_id=33014811&response-content-disposition=attachment%3B%20filename%3Dnpp.8.5.4.Installer.x64.exe&response-content-type=application%2Foctet-stream", "msi": False},
    {"name": "Optimiser", "url": "https://github.com/hellzerg/optimizer/releases/download/15.6/Optimizer-15.6.exe", "msi": False},
    
]

TEMP_DOWNLOAD_DIR = tempfile.mkdtemp(prefix="file_downloader_")
atexit.register(lambda: shutil.rmtree(TEMP_DOWNLOAD_DIR, ignore_errors=True))

# Functions
def download_and_execute(url, file_path, msi):
    try:
        response = requests.get(url)
        with open(file_path, "wb") as file:
            file.write(response.content)
        if msi:
            subprocess.Popen(["msiexec", "/i", file_path, "/passive"], shell=True)
        else:
            subprocess.Popen(file_path, shell=True)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download and execute file: {e}")
        return False

def download_files():
    selected_files = [file for file in FILE_LIST if file["var"].get()]
    if not selected_files:
        messagebox.showwarning("No Selection", "Please select at least one file to download.")
        return

    download_button.config(state=tk.DISABLED)  # Disable the download button during the process

    for file in selected_files:
        file_name = os.path.basename(file["url"])
        file_path = os.path.join(TEMP_DOWNLOAD_DIR, file_name)
        success = download_and_execute(file["url"], file_path, file["msi"])
        if not success:
            break

    download_button.config(state=tk.NORMAL)  # Enable the download button after the process

# GUI
def create_main_window():
    root = tk.Tk()
    root.title("File Downloader")
    root.geometry("600x500")
    root.attributes("-topmost", True)

    # Apply the "equilux" theme
    style = ThemedStyle(root)
    style.set_theme("equilux")

    root.columnconfigure(0, weight=1)  # Make the frame expand to fill the window
    root.rowconfigure(0, weight=1)

    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Select Apps / Games to download:", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10)

    for i, file in enumerate(FILE_LIST, 1):
        file["var"] = tk.BooleanVar()
        file["var"].set(False)
        ttk.Checkbutton(frame, text=file["name"], variable=file["var"]).grid(row=i, column=0, columnspan=2, sticky="w")

    global download_button
    download_button = ttk.Button(frame, text="Download", command=download_files, width=20)
    download_button.grid(row=len(FILE_LIST) + 1, column=0, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
