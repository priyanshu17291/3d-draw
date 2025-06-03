# ──────────────── Qt Imports ────────────────
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox , QSizePolicy , QStackedWidget , QApplication ,QMainWindow , QDockWidget , QTextEdit  )
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor , QGuiApplication,QPalette
from PyQt5.QtCore import Qt, QPointF , QTimer

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
from Components.Toolbar import Toolbar

from Panels.ChartPanel import ChartPanel
from Panels.AlarmsPanel import AlarmPanel
from Panels.TriggerPanel import TriggerPanel
from Panels.SiteInfoPanel import SiteInfoPanel
from Panels.RecordingsPanel import RecordingsPanel
from Panels.SensorInfoPanel import SensorInfoPanel
from Panels.ContentPanel import ContentPanel
from Panels.LoginPanel import LoginPanel

import Styles.styles as styles
import Styles.colors as cl

class LoginWindow(QMainWindow):
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

        self.loginPanel = LoginPanel()

        self.setCentralWidget(self.loginPanel)