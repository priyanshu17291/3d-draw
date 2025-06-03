#System Imports
import os
import sys

###MAC ONLY###
os.environ['QT_MAC_WANTS_LAYER'] = '1'
##############

#Qt Imports
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QGuiApplication



#Custom Imports
from Panels.LoginPanel import LoginPanel
from Panels.MainPanel import MainPanel
from Panels.LaunchPanel import LaunchPanel
from Styles import colors as cl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPPL India")
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        width, height = 600, 500
        self.resize(width, height)

        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2
        self.move(x, y)

        # loginPanel = LoginPanel(self)
        # self.setCentralWidget(loginPanel)

        mainPanel = MainPanel()
        self.setCentralWidget(mainPanel)
        self.showMaximized()

    
    def showLaunchScreen(self):
        start_geom = self.geometry()
        screen = QGuiApplication.primaryScreen()
        screen_geom = screen.availableGeometry()

        new_width, new_height = 900, 600
        new_x = start_geom.x() - (new_width - start_geom.width()) // 2
        new_y = start_geom.y() - (new_height - start_geom.height()) // 2

        new_x = max(screen_geom.left(), min(new_x, screen_geom.right() - new_width))
        new_y = max(screen_geom.top(), min(new_y, screen_geom.bottom() - new_height))

        end_geom = QRect(new_x, new_y, new_width, new_height)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(start_geom)
        self.animation.setEndValue(end_geom)
        self.animation.start()

        self.animation.finished.connect(lambda: self.setCentralWidget(LaunchPanel(self)))

    
    def showMainPanel(self):
        self.sensorInfoPanel = MainPanel()
        self.setCentralWidget(self.sensorInfoPanel)
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

