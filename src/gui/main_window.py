import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLineEdit, QPushButton, QLabel, QProgressBar,
                            QFileDialog, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from src.core.downloader import DownloaderThread
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.setMinimumWidth(600)
        self.available_heights = []
        self.video_info = None
        self.setup_ui()

    def clean_youtube_url(self, url):
        """Remove playlist parameters from YouTube URL"""
        # Extract video ID
        video_id_match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11}).*', url)
        if video_id_match:
            video_id = video_id_match.group(1)
            return f'https://www.youtube.com/watch?v={video_id}'
        return url

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL here")
        url_layout.addWidget(self.url_input)
        
        # Check formats button
        self.check_formats_button = QPushButton("Check Available Formats")
        self.check_formats_button.clicked.connect(self.check_formats)
        url_layout.addWidget(self.check_formats_button)
        
        # Quality selection
        quality_layout = QHBoxLayout()
        self.quality_combo = QComboBox()
        self.quality_combo.setEnabled(False)
        quality_layout.addWidget(QLabel("Select Resolution:"))
        quality_layout.addWidget(self.quality_combo)
        
        # Title input section
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("File name:"))
        self.title_input = QLineEdit()
        self.title_input.setEnabled(False)
        title_layout.addWidget(self.title_input)
        
        # Download location section
        location_layout = QHBoxLayout()
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Download location")
        self.location_input.setText(os.path.expanduser("~/Downloads"))
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_location)
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(self.browse_button)

        # Download button
        self.download_button = QPushButton("Download")
        self.download_button.setFixedHeight(40)
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setEnabled(False)

        # Info labels
        self.resolution_label = QLabel()
        self.size_label = QLabel()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label = QLabel()

        # Add widgets to layout
        layout.addLayout(url_layout)
        layout.addLayout(quality_layout)
        layout.addLayout(title_layout)
        layout.addLayout(location_layout)
        layout.addWidget(self.download_button)
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.size_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)

        # Add stretcher at the bottom
        layout.addStretch()

    def check_formats(self):
        url = self.clean_youtube_url(self.url_input.text().strip())
        save_path = self.location_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL")
            return

        if not save_path:
            QMessageBox.warning(self, "Error", "Please select a download location")
            return

        # Disable UI while checking formats
        self.url_input.setEnabled(False)
        self.check_formats_button.setEnabled(False)
        self.location_input.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.quality_combo.setEnabled(False)
        self.title_input.setEnabled(False)
        self.quality_combo.clear()
        self.title_input.clear()

        # Reset progress
        self.progress_bar.setValue(0)
        self.progress_label.setText("Fetching video information...")

        # Create and start info thread
        self.thread = DownloaderThread(url, save_path)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.check_formats_finished)
        self.thread.info_retrieved.connect(self.show_video_info)
        self.thread.formats_retrieved.connect(self.update_formats)
        self.thread.start()

    def update_formats(self, heights):
        self.available_heights = heights
        self.quality_combo.clear()
        
        for height in heights:
            self.quality_combo.addItem(f"{height}p", height)

    def check_formats_finished(self, success, message):
        # Re-enable UI
        self.url_input.setEnabled(True)
        self.check_formats_button.setEnabled(True)
        self.location_input.setEnabled(True)
        self.browse_button.setEnabled(True)
        
        if success:
            self.quality_combo.setEnabled(True)
            self.download_button.setEnabled(True)
            self.title_input.setEnabled(True)
            # Reset progress only on success
            self.progress_bar.setValue(0)
            self.progress_label.setText("Ready to download")
        else:
            # Reset all UI elements on error
            self.quality_combo.setEnabled(False)
            self.download_button.setEnabled(False)
            self.title_input.setEnabled(False)
            self.quality_combo.clear()
            self.title_input.clear()
            self.progress_bar.setValue(0)
            self.progress_label.setText("")
            QMessageBox.warning(self, "Error", message)

    def browse_location(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Location")
        if folder:
            self.location_input.setText(folder)

    def start_download(self):
        url = self.clean_youtube_url(self.url_input.text().strip())
        save_path = self.location_input.text().strip()
        selected_height = self.quality_combo.currentData()
        custom_title = self.title_input.text().strip()

        if not url or not save_path or not selected_height:
            QMessageBox.warning(self, "Error", "Please select video resolution")
            return

        if not self.video_info:
            QMessageBox.warning(self, "Error", "Please check formats first")
            return

        if not custom_title:
            QMessageBox.warning(self, "Error", "Please enter a file name")
            return

        # Disable input while downloading
        self.url_input.setEnabled(False)
        self.check_formats_button.setEnabled(False)
        self.location_input.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.quality_combo.setEnabled(False)
        self.title_input.setEnabled(False)

        # Reset progress
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting download...")

        # Create and start download thread
        self.thread = DownloaderThread(url, save_path, selected_height)
        self.thread.info = self.video_info
        self.thread.custom_title = custom_title
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()

    def show_video_info(self, info):
        self.video_info = info
        # Set default title in the input field
        self.title_input.setText(info['title'])

    def update_progress(self, progress_text):
        if "Downloading:" in progress_text and "%" in progress_text:
            try:
                percentage = float(progress_text.split('%')[0].split(':')[1].strip())
                self.progress_bar.setValue(int(percentage))
            except:
                pass
        self.progress_label.setText(progress_text)

    def download_finished(self, success, message):
        # Re-enable input
        self.url_input.setEnabled(True)
        self.check_formats_button.setEnabled(True)
        self.location_input.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.download_button.setEnabled(True)
        self.quality_combo.setEnabled(True)
        self.title_input.setEnabled(True)

        if success:
            QMessageBox.information(self, "Success", message)
            self.url_input.clear()
            self.quality_combo.clear()
            self.title_input.clear()
            self.quality_combo.setEnabled(False)
            self.download_button.setEnabled(False)
            self.title_input.setEnabled(False)
            self.video_info = None
        else:
            QMessageBox.warning(self, "Error", message)

        # Reset progress
        self.progress_bar.setValue(0)
        self.progress_label.setText("")
        self.resolution_label.setText("")
        self.size_label.setText("") 