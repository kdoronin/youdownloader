#!/usr/bin/env python3
import os
import sys
import urllib.request
import zipfile
import shutil

def download_ffmpeg():
    """Download and setup ffmpeg for the current platform"""
    if sys.platform == 'win32':
        # URL for Windows ffmpeg
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        zip_path = "ffmpeg.zip"
        
        print("Downloading ffmpeg for Windows...")
        urllib.request.urlretrieve(url, zip_path)
        
        print("Extracting ffmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("ffmpeg_temp")
        
        # Create resources directory if it doesn't exist
        os.makedirs("resources", exist_ok=True)
        
        # Copy ffmpeg.exe to resources
        ffmpeg_exe = os.path.join("ffmpeg_temp", "ffmpeg-master-latest-win64-gpl", "bin", "ffmpeg.exe")
        shutil.copy2(ffmpeg_exe, os.path.join("resources", "ffmpeg.exe"))
        
        # Cleanup
        os.remove(zip_path)
        shutil.rmtree("ffmpeg_temp")
        
        print("ffmpeg has been installed successfully!")
    else:
        print("This script is intended for Windows only.")
        print("For macOS, please install ffmpeg using Homebrew: brew install ffmpeg")

if __name__ == "__main__":
    download_ffmpeg() 