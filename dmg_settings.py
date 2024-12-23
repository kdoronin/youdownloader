import os.path
import plistlib

application = defines.get('app', 'dist/YouTube Downloader.app')
appname = os.path.basename(application)

def icon_from_app(app_path):
    plist_path = os.path.join(app_path, 'Contents', 'Info.plist')
    if os.path.exists(plist_path):
        with open(plist_path, 'rb') as f:
            plist = plistlib.load(f)
        if 'CFBundleIconFile' in plist:
            icon_name = plist['CFBundleIconFile']
            if not icon_name.endswith('.icns'):
                icon_name += '.icns'
            return os.path.join(app_path, 'Contents', 'Resources', icon_name)

format = defines.get('format', 'UDBZ')
size = defines.get('size', '1G')
files = [application]
symlinks = {'Applications': '/Applications'}
badge_icon = 'icon.icns'
icon_locations = {
    appname: (140, 120),
    'Applications': (500, 120)
}
background = 'builtin-arrow'
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
sidebar_width = 180
window_rect = ((100, 100), (640, 280))
default_view = 'icon-view'
show_icon_preview = False
include_icon_view_settings = True
include_list_view_settings = False
arrange_by = None
grid_offset = (0, 0)
grid_spacing = 100
scroll_position = (0, 0)
label_pos = 'bottom'
text_size = 16
icon_size = 128 