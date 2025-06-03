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


#System Imports
import os
import sys
import platform
# Only import Mac-specific modules if on macOS
if platform.system() == 'Darwin':
    import objc
    from AppKit import NSApp, NSAppearance
    os.environ['QT_MAC_WANTS_LAYER'] = '1'



class DynamicInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPPL India")
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        self.toolbar = Toolbar()  
        self.setMenuWidget(self.toolbar)

        sensorInfoDock = QDockWidget("Sensor Info",self)
        sensorInfoDock.setWidget(SensorInfoPanel())
        sensorInfoDock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea,sensorInfoDock)

        self.contentDock = QDockWidget("Site Info",self)
        self.content = ContentPanel()
        self.contentDock.setWidget(self.content)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.contentDock)

        self.splitDockWidget(sensorInfoDock,self.contentDock,Qt.Horizontal)

        alarmsDock = QDockWidget("Alarms",self)
        alarmsDock.setWidget(AlarmPanel())
        alarmsDock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea,alarmsDock)

        triggersDock = QDockWidget("Triggers",self)
        triggersDock.setWidget(TriggerPanel())
        triggersDock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea,triggersDock)

        self.splitDockWidget(alarmsDock,triggersDock,Qt.Vertical)

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [sensorInfoDock, self.contentDock, alarmsDock],
            [int(self.width() * 0.2), int(self.width() * 0.6), int(self.width() * 0.2)],
            Qt.Horizontal
        ))

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [alarmsDock, triggersDock],
            [int(self.height() * 0.5), int(self.height() * 0.5)],
            Qt.Vertical
        ))



        self.toolbar.infoBtn.mousePressEvent = self.showSiteInfo
        self.toolbar.systemBtn.mousePressEvent = self.showChartPanel
        self.toolbar.recordingsBtn.mousePressEvent = self.showRecordingsPanel


        self.setDockNestingEnabled(True)
        self.showMaximized()
        self.close()

    def showChartPanel(self,event):
        self.content.setCurrentWidget(self.content.chartPanel)
        self.chart_in_view = True
        self.contentDock.setWindowTitle("System")
        
    
    def showSiteInfo(self,event):
        self.content.setCurrentWidget(self.content.siteInfoPanel)
        self.chart_in_view = False
        self.contentDock.setWindowTitle("Site Info")
    
    def showRecordingsPanel(self,event):
        self.content.setCurrentWidget(self.content.recordingsPanel)
        self.chart_in_view = False
        self.contentDock.setWindowTitle("Recordings")


