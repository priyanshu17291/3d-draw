# ──────────────── Qt Imports ────────────────
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox , QSizePolicy , QStackedWidget , QTabWidget , QDockWidget
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton

from Panels.ChartPanel import ChartPanel
from Panels.AlarmsPanel import AlarmPanel
from Panels.TriggerPanel import TriggerPanel
from Panels.SiteInfoPanel import SiteInfoPanel
from Panels.RecordingsPanel import RecordingsPanel

import Styles.styles as styles
import Styles.colors as cl


# ──────────────── Standard Library ────────────────
import random


class MainPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.chart_in_view = True
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(f"background-color:{cl.SYS_BD1}")
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)


        #Header
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0,0,0,0)
        header_layout.setSpacing(0)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/sppl-logo-white.png"))
        self.logo.setFixedSize(50, 50)
        self.logo.setStyleSheet("margin:5px")
        self.logo.setScaledContents(True)

        self.logoLabel1 = QLabel("SPPL India")
        self.logoLabel1.setStyleSheet(styles.text_style2+";QLabel{font-weight:600}")
 

        self.addSensorBtn = VerticalIconTextButton("assets/addicon30.png","Add Sensor")
        self.systemSettingsBtn = VerticalIconTextButton("assets/settingsicon30.png","Settings")
        self.devicesBtn = VerticalIconTextButton("assets/devicesicon30.png","Devices")
        self.recordingsBtn = VerticalIconTextButton("assets/graphicon30.png","Recordings")
        self.logsBtn = VerticalIconTextButton("assets/logicon30.png","Logs")
        self.infoBtn = VerticalIconTextButton("assets/infoicon30.png","Site Info")
        self.systemBtn = VerticalIconTextButton("assets/systemicon30.png","System")
        self.accountBtn = VerticalIconTextButton("assets/accounticon30.png","Account")



        line1 = SeparatorLine(color=f"{cl.SYS_SEP1}", orientation="V", length=60, thickness=1)
        line2 = SeparatorLine(color=f"{cl.SYS_SEP1}", orientation="V", length=60, thickness=1)

        header_layout.addSpacing(10)
        header_layout.addWidget(self.logo,Qt.AlignVCenter)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.logoLabel1,Qt.AlignVCenter)

        header_layout.addWidget(self.addSensorBtn,Qt.AlignVCenter)
        header_layout.addWidget(self.devicesBtn,Qt.AlignVCenter)
        header_layout.addWidget(self.recordingsBtn,Qt.AlignVCenter)
        
        header_layout.addWidget(line1,Qt.AlignVCenter)

        header_layout.addWidget(self.systemSettingsBtn,Qt.AlignVCenter)
        header_layout.addWidget(self.systemBtn,Qt.AlignVCenter)
        header_layout.addWidget(self.infoBtn,Qt.AlignVCenter)
        header_layout.addWidget(line2,Qt.AlignVCenter)

        header_layout.addWidget(self.logsBtn,Qt.AlignVCenter)
        header_layout.addWidget(self.accountBtn,Qt.AlignVCenter)
        
        


        header.setLayout(header_layout)
        header.setFixedHeight(70)
        header.setStyleSheet(f"background-color:{cl.SYS_BG6}")

        #Main
        # main = QWidget()

        sensorInfoDock = QDockWidget(self,"Sensor Info")
        sensorInfoDock.setFloating(False)







        layout.addWidget(header)
        # layout.addWidget(main)

        layout.setSpacing(5)
        self.setLayout(layout)


    def toggleSensor(self,text):
        if self.chart_in_view:
            self.chartPanel.header.setText("Channel Plot : "+text + "/x")
            self.chartPanel.axisCombo.setCurrentIndex(0)

    def showChartPanel(self,event):
        self.content.setCurrentWidget(self.chartPanel)
        self.chart_in_view = True
        self.toggleSensor(self.sensorCombo.currentText())
    
    def showSiteInfo(self,event):
        self.content.setCurrentWidget(self.siteInfoPanel)
        self.chart_in_view = False
    
    def showRecordingsPanel(self,event):
        self.content.setCurrentWidget(self.recordingsPanel)
        self.chart_in_view = False

    