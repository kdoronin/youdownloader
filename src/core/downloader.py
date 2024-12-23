import os
import re
from PyQt6.QtCore import QThread, pyqtSignal
import yt_dlp
from src.core.utils import get_ffmpeg_path

class DownloaderThread(QThread):
    """Thread for downloading videos without freezing the GUI"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    info_retrieved = pyqtSignal(dict)
    formats_retrieved = pyqtSignal(list)

    def __init__(self, url, save_path, selected_height=None):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.selected_height = selected_height
        self.info = None
        self.custom_title = None

    def get_video_info(self):
        """Retrieve video information without downloading"""
        try:
            print("Starting video info retrieval...")
            ffmpeg_location = get_ffmpeg_path()
            
            if not os.path.exists(ffmpeg_location):
                self.finished.emit(False, f"Error: ffmpeg not found at {ffmpeg_location}")
                return
                
            if not os.access(ffmpeg_location, os.X_OK):
                try:
                    os.chmod(ffmpeg_location, 0o755)
                except Exception as e:
                    self.finished.emit(False, f"Error: Could not make ffmpeg executable: {str(e)}")
                    return

            print("Initializing yt-dlp options...")
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'ffmpeg_location': os.path.dirname(ffmpeg_location),
            }

            print("Creating yt-dlp instance...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("Extracting video info...")
                info = ydl.extract_info(self.url, download=False)
                print("Video info extracted successfully")
                
                # Store only necessary info
                self.info = {
                    'title': info.get('title', ''),
                    'formats': info.get('formats', []),
                    'url': self.url
                }
                
                self.info_retrieved.emit(self.info)

                print("Processing available formats...")
                available_heights = set()
                
                # Get all available heights from formats with h264 codec
                for f in info['formats']:
                    if (f.get('vcodec', '').startswith('avc1') or  # h264 codec
                        f.get('vcodec', '').startswith('h264')):
                        height = f.get('height', 0)
                        if height:
                            available_heights.add(height)
                            print(f"Found format: {height}p - {f.get('vcodec', 'N/A')}")

                # Sort heights in descending order
                heights = sorted(list(available_heights), reverse=True)
                print(f"Available heights: {heights}")
                self.formats_retrieved.emit(heights)
                print("Format processing completed")
                self.finished.emit(True, "Video information retrieved successfully")

        except Exception as e:
            print(f"Error during video info retrieval: {str(e)}")
            self.finished.emit(False, f"Error: {str(e)}")

    def run(self):
        try:
            if not self.info:
                self.get_video_info()
                return

            ffmpeg_location = get_ffmpeg_path()
            
            if not os.path.exists(ffmpeg_location):
                self.finished.emit(False, f"Error: ffmpeg not found at {ffmpeg_location}")
                return
                
            if not os.access(ffmpeg_location, os.X_OK):
                try:
                    os.chmod(ffmpeg_location, 0o755)
                except Exception as e:
                    self.finished.emit(False, f"Error: Could not make ffmpeg executable: {str(e)}")
                    return
            
            format_spec = f'bestvideo[height={self.selected_height}][vcodec^=avc]+bestaudio[ext=m4a]/best[height<={self.selected_height}][vcodec^=avc]' if self.selected_height else 'bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/best[vcodec^=avc]'
            
            # Use custom title if available
            output_template = os.path.join(self.save_path, '%(title)s.%(ext)s')
            if self.custom_title:
                output_template = os.path.join(self.save_path, f"{self.custom_title}.%(ext)s")
            
            ydl_opts = {
                'format': format_spec,
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'outtmpl': output_template,
                'merge_output_format': 'mp4',
                'ffmpeg_location': os.path.dirname(ffmpeg_location),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                
            self.finished.emit(True, "Download completed successfully!")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent = d.get('_percent_str', '0%').replace('%', '').strip()
                # Remove ANSI color codes if present
                percent = re.sub(r'\x1b\[[0-9;]*m', '', percent)
                self.progress.emit(f"Downloading: {percent}%")
            except:
                self.progress.emit("Downloading...")
        elif d['status'] == 'finished':
            self.progress.emit('Processing downloaded file...') 