# YouTube Downloader

A cross-platform desktop application for downloading YouTube videos in the highest available quality. The application supports downloading videos in Full HD (1080p) and higher resolutions while ensuring codec compatibility with your operating system.

## Features

- Simple and intuitive graphical user interface
- Downloads videos in the highest available quality (1080p or better)
- Ensures codec compatibility (H.264/AVC for maximum compatibility)
- Shows video information before download (title, resolution, file size)
- Progress bar with download status
- Allows selecting custom download location
- Cross-platform support (macOS, Windows, Linux)
- No additional software required - works out of the box

## Installation

### Using Pre-built Binaries

#### macOS
1. Download the latest `YouTubeDownloader.dmg` from the releases page
2. Open the DMG file
3. Drag the YouTube Downloader app to your Applications folder
4. Launch it from Applications or Launchpad

#### Windows
1. Download the latest `YouTubeDownloader.exe` from the releases page
2. Run the installer
3. Launch the application from the Start menu

#### Linux
1. Download the latest `YouTubeDownloader.AppImage` from the releases page
2. Make it executable: `chmod +x YouTubeDownloader.AppImage`
3. Run the application: `./YouTubeDownloader.AppImage`

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtubedownloader.git
cd youtubedownloader
```

2. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
# Run GUI version
python youtube_downloader_gui.py

# Run command-line version
python youtube_downloader.py <youtube_url>
```

## Building from Source

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- Platform-specific build tools:
  - macOS: Xcode Command Line Tools
  - Windows: Visual Studio Build Tools
  - Linux: build-essential package

### Building Steps

1. Install build dependencies:
```bash
pip install -r requirements.txt
```

2. Generate application icon (macOS only):
```bash
mkdir icon.iconset
convert icon.svg -resize 16x16 icon.iconset/icon_16x16.png
convert icon.svg -resize 32x32 icon.iconset/icon_32x32.png
convert icon.svg -resize 64x64 icon.iconset/icon_64x64.png
convert icon.svg -resize 128x128 icon.iconset/icon_128x128.png
convert icon.svg -resize 256x256 icon.iconset/icon_256x256.png
convert icon.svg -resize 512x512 icon.iconset/icon_512x512.png
iconutil -c icns icon.iconset
```

3. Build the application:

#### macOS
```bash
# Build .app bundle
pyinstaller youtube_downloader.spec

# Create DMG installer
dmgbuild -s dmg_settings.py "YouTube Downloader" YouTubeDownloader.dmg
```

#### Windows
```bash
pyinstaller youtube_downloader.spec
```

#### Linux
```bash
pyinstaller youtube_downloader.spec
```

The compiled applications will be available in the `dist` directory.

## Usage

1. Launch the application
2. Paste a YouTube video URL into the input field
3. (Optional) Change the download location using the "Browse" button
4. Click "Download"
5. Wait for the download to complete
6. Find your downloaded video in the selected location

## Command Line Usage

You can also use the command-line version:

```bash
python youtube_downloader.py https://www.youtube.com/watch?v=VIDEO_ID
```

## Technical Details

The application uses:
- `yt-dlp` for video downloading
- `PyQt6` for the graphical interface
- H.264/AVC codec for maximum compatibility
- MP4 container format

Video format preferences:
1. 1080p or higher resolution
2. H.264/AVC codec
3. MP4 container
4. Best available audio quality

## Troubleshooting

### Common Issues

1. **"ffmpeg is not installed" Error**
   - This error occurs when trying to download high-quality videos without ffmpeg installed
   - After installing ffmpeg, restart the application

2. **Video Not Playing**
   - Make sure your media player supports H.264/AVC codec
   - Try VLC media player which supports most video formats

3. **Download Fails**
   - Check your internet connection
   - Verify the video URL is correct and accessible
   - Make sure you have write permissions in the download directory
   - Ensure ffmpeg is properly installed and accessible from PATH

4. **Application Won't Start**
   - Ensure you have the latest version
   - Try reinstalling the application
   - Check system requirements
   - Verify all dependencies are installed

### Getting Help

If you encounter any issues:
1. Check the Troubleshooting section above
2. Look for similar issues in the Issues section
3. Create a new issue with:
   - Your operating system and version
   - Application version
   - Error message or description
   - Steps to reproduce the problem

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the YouTube download functionality
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework 