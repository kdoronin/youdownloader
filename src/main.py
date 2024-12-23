import sys
import os
from PyQt6.QtWidgets import QApplication

# Add debug information
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")
print("Attempting to import MainWindow...")

try:
    from src.gui.main_window import MainWindow
    print("MainWindow imported successfully")
except Exception as e:
    print(f"Error importing MainWindow: {str(e)}")
    print(f"Exception type: {type(e)}")
    import traceback
    traceback.print_exc()

def main():
    try:
        print("Creating QApplication...")
        app = QApplication(sys.argv)
        print("Creating MainWindow...")
        window = MainWindow()
        print("Showing window...")
        window.show()
        print("Starting event loop...")
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 