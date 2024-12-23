import sys
import os

def get_ffmpeg_path():
    """Get the path to bundled ffmpeg"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        if sys.platform == 'darwin':
            # macOS app bundle
            if 'Contents/MacOS' in sys.executable:
                # We're inside an app bundle, use the Resources directory
                bundle_dir = os.path.abspath(os.path.join(os.path.dirname(sys.executable), '..', 'Resources'))
            else:
                # Fallback to executable directory
                bundle_dir = os.path.dirname(sys.executable)
            ffmpeg_path = os.path.join(bundle_dir, 'resources', 'ffmpeg')
        else:
            # Windows/Linux executable
            bundle_dir = os.path.dirname(sys.executable)
            ffmpeg_name = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'
            ffmpeg_path = os.path.join(bundle_dir, 'resources', ffmpeg_name)
    else:
        # Running in development
        ffmpeg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'ffmpeg')
    
    # Debug information
    print(f"Executable path: {sys.executable}")
    print(f"Bundle directory: {bundle_dir if getattr(sys, 'frozen', False) else 'Not bundled'}")
    print(f"ffmpeg path: {ffmpeg_path}")
    print(f"ffmpeg exists: {os.path.exists(ffmpeg_path)}")
    print(f"ffmpeg is executable: {os.access(ffmpeg_path, os.X_OK) if os.path.exists(ffmpeg_path) else False}")
    
    return ffmpeg_path 