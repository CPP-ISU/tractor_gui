# main.py
import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
from gui.main_window import MainWindow

app = QApplication(sys.argv)

splash_pix = QPixmap("V1.0.0.png")

if splash_pix.isNull():
    print("❌ Splash image failed to load. Make sure 'Front Cy-Allis.png' exists in this directory.")
    sys.exit(1)

splash = QSplashScreen(splash_pix)
splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
splash.show()

screen_geometry = app.primaryScreen().geometry()
splash_size = splash_pix.size()
splash.move(
    (screen_geometry.width() - splash_size.width()) // 2,
    (screen_geometry.height() - splash_size.height()) // 2
)

app.processEvents()

def launch_main():
    window = MainWindow()
    window.showFullScreen()
    splash.finish(window)

QTimer.singleShot(5000, launch_main)

sys.exit(app.exec_())
