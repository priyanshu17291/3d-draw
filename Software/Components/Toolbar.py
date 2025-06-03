from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
import Styles.styles as styles
import Styles.colors as cl


class Toolbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/sppl-logo-white.png"))
        self.logo.setFixedSize(50, 50)
        self.logo.setStyleSheet("margin:5px")
        self.logo.setScaledContents(True)

        self.logoLabel1 = QLabel("SPPL India")
        self.logoLabel1.setStyleSheet("QLabel{color:white;font-size:14px;font-weight:600;}")
 

        self.addSensorBtn = VerticalIconTextButton("assets/addicon30.png","Add Sensor")
        self.systemSettingsBtn = VerticalIconTextButton("assets/settingsicon30.png","Settings")
        self.devicesBtn = VerticalIconTextButton("assets/devicesicon30.png","Devices")
        self.signalBtn = VerticalIconTextButton("assets/signalicon30.png","Signals")
        self.recordingsBtn = VerticalIconTextButton("assets/graphicon30.png","Recordings")
        self.logsBtn = VerticalIconTextButton("assets/logicon30.png","Logs")
        self.infoBtn = VerticalIconTextButton("assets/infoicon30.png","Site Info")
        self.systemBtn = VerticalIconTextButton("assets/systemicon30.png","System")
        self.accountBtn = VerticalIconTextButton("assets/accounticon30.png","Account")
        self.exitBtn = VerticalIconTextButton("assets/exiticon30.png","Exit")



        line1 = SeparatorLine(color=f"{cl.SYS_SEP1}", orientation="V", length=60, thickness=1)
        line2 = SeparatorLine(color=f"{cl.SYS_SEP1}", orientation="V", length=60, thickness=1)

        layout.addSpacing(10)
        layout.addWidget(self.logo,Qt.AlignVCenter)
        layout.addSpacing(10)
        layout.addWidget(self.logoLabel1,Qt.AlignVCenter)

        layout.addWidget(self.addSensorBtn,Qt.AlignVCenter)
        layout.addWidget(self.devicesBtn,Qt.AlignVCenter)
        layout.addWidget(self.recordingsBtn,Qt.AlignVCenter)
        
        layout.addWidget(line1,Qt.AlignVCenter)

        layout.addWidget(self.signalBtn,Qt.AlignVCenter)
        layout.addWidget(self.systemSettingsBtn,Qt.AlignVCenter)
        layout.addWidget(self.systemBtn,Qt.AlignVCenter)
        layout.addWidget(self.infoBtn,Qt.AlignVCenter)
        layout.addWidget(line2,Qt.AlignVCenter)

        layout.addWidget(self.exitBtn,Qt.AlignVCenter)
        layout.addWidget(self.logsBtn,Qt.AlignVCenter)
        layout.addWidget(self.accountBtn,Qt.AlignVCenter)
        
        self.setLayout(layout)
        self.setFixedHeight(70)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")  