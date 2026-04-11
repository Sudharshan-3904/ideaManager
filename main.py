import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles import get_modern_stylesheet

def main():
    app = QApplication(sys.argv)
    
    # Apply modern look & feel
    app.setStyle('Fusion')
    app.setStyleSheet(get_modern_stylesheet())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
