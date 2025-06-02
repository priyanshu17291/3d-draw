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
from Panels.SAControlPanel import SAControlPanel
from Panels.SAWorkPanel import SAWorkPanel
from Panels.SAStatusPanel import SAStatusPanel

from Utils.IconUtils import GetIcon

import Styles.styles as styles
import Styles.colors as cl


#System Imports
import os
import sys
######MAC ONLY######
import objc
from AppKit import NSApp, NSAppearance
####################

###MAC ONLY###
os.environ['QT_MAC_WANTS_LAYER'] = '1'
##############


class SignalAnalysisMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(1,1,1,1)

        self.tabsPanel = QWidget()
        self.tabsPanel_layout = QHBoxLayout()
        self.tabsPanel_layout.setSpacing(15)
        self.tabsPanel_layout.setContentsMargins(8,8,8,0)

        self.homeLabel = self.getTabLabel("    Home    ",True)
        self.analysisLabel = self.getTabLabel("    Analysis    ")
        self.modelLabel = self.getTabLabel("    Model    ")
        self.viewLabel = self.getTabLabel("    View   ")
        self.helpLabel = self.getTabLabel("    Help    ")

        self.homeLabel.mousePressEvent = self.showHome
        self.analysisLabel.mousePressEvent = self.showAnalysis
        self.modelLabel.mousePressEvent = self.showModel
        self.viewLabel.mousePressEvent = self.showView
        self.helpLabel.mousePressEvent = self.showHelp

        self.tabsPanel_layout.addWidget(self.homeLabel)
        self.tabsPanel_layout.addWidget(self.analysisLabel)
        self.tabsPanel_layout.addWidget(self.modelLabel)
        self.tabsPanel_layout.addWidget(self.viewLabel)
        self.tabsPanel_layout.addWidget(self.helpLabel)
        self.tabsPanel_layout.addStretch(1)

        self.tabsPanel.setFixedHeight(30)
        self.tabsPanel.setLayout(self.tabsPanel_layout)

        self.ribbonTab = QStackedWidget()

        self.homeRibbon = QWidget()
        self.homeRibbon.setStyleSheet(f"background-color:{cl.SYS_BG3}")
        self.homeRibbon_layout = QHBoxLayout()
        self.homeRibbon_layout.setSpacing(0)
        self.homeRibbon_layout.setContentsMargins(0,0,0,5)
        self.setupHomeRibbon()
        self.homeRibbon.setLayout(self.homeRibbon_layout)

        self.analysisRibbon = QWidget()
        self.analysisRibbon.setStyleSheet(f"background-color:{cl.SYS_BG3}")
        self.analysisRibbon_layout = QHBoxLayout()
        self.analysisRibbon_layout.addWidget(QLabel("ANALYSIS"))
        self.analysisRibbon.setLayout(self.analysisRibbon_layout)

        self.modelRibbon = QWidget()
        self.modelRibbon.setStyleSheet(f"background-color:{cl.SYS_BG3}")
        self.modelRibbon_layout = QHBoxLayout()
        self.modelRibbon_layout.addWidget(QLabel("MODEL"))
        self.modelRibbon.setLayout(self.modelRibbon_layout)

        self.viewRibbon = QWidget()
        self.viewRibbon.setStyleSheet(f"background-color:{cl.SYS_BG3}")
        self.viewRibbon_layout = QHBoxLayout()
        self.viewRibbon_layout.addWidget(QLabel("VIEW"))
        self.viewRibbon.setLayout(self.viewRibbon_layout)

        self.helpRibbon = QWidget()
        self.helpRibbon.setStyleSheet(f"background-color:{cl.SYS_BG3}")
        self.helpRibbon_layout = QHBoxLayout()
        self.helpRibbon_layout.addWidget(QLabel("HELP"))
        self.helpRibbon.setLayout(self.helpRibbon_layout)

        self.ribbonTab.addWidget(self.homeRibbon)
        self.ribbonTab.addWidget(self.analysisRibbon)
        self.ribbonTab.addWidget(self.modelRibbon)
        self.ribbonTab.addWidget(self.viewRibbon)
        self.ribbonTab.addWidget(self.helpRibbon)

        self.ribbonTab.setCurrentWidget(self.homeRibbon)




        layout.addWidget(self.tabsPanel)
        layout.addWidget(self.ribbonTab)
        layout.addStretch(1)

        self.setLayout(layout)
    


    
    def showHome(self,event=None):
        tabList = [self.homeLabel,self.analysisLabel,self.modelLabel,self.viewLabel,self.helpLabel]
        for tab in tabList:
            if tab == self.homeLabel:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG3};font-size:14px;font-weight:500;color:white;border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
            else:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG1};font-size:14px;font-weight:500;color:{cl.SYS_FG2};border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")

        self.ribbonTab.setCurrentWidget(self.homeRibbon)   

    def showAnalysis(self,event=None):
        tabList = [self.homeLabel,self.analysisLabel,self.modelLabel,self.viewLabel,self.helpLabel]
        for tab in tabList:
            if tab == self.analysisLabel:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG3};font-size:14px;font-weight:500;color:white;border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
            else:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG1};font-size:14px;font-weight:500;color:{cl.SYS_FG2};border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
        self.ribbonTab.setCurrentWidget(self.analysisRibbon)          
        
    def showModel(self,event=None):
        tabList = [self.homeLabel,self.analysisLabel,self.modelLabel,self.viewLabel,self.helpLabel]
        for tab in tabList:
            if tab == self.modelLabel:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG3};font-size:14px;font-weight:500;color:white;border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
            else:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG1};font-size:14px;font-weight:500;color:{cl.SYS_FG2};border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
        self.ribbonTab.setCurrentWidget(self.modelRibbon)      


    def showView(self,event=None):
        tabList = [self.homeLabel,self.analysisLabel,self.modelLabel,self.viewLabel,self.helpLabel]
        for tab in tabList:
            if tab == self.viewLabel:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG3};font-size:14px;font-weight:500;color:white;border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
            else:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG1};font-size:14px;font-weight:500;color:{cl.SYS_FG2};border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
        self.ribbonTab.setCurrentWidget(self.viewRibbon)   

    def showHelp(self,event=None):
        tabList = [self.homeLabel,self.analysisLabel,self.modelLabel,self.viewLabel,self.helpLabel]
        for tab in tabList:
            if tab == self.helpLabel:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG3};font-size:14px;font-weight:500;color:white;border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
            else:
                tab.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG1};font-size:14px;font-weight:500;color:{cl.SYS_FG2};border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
        self.ribbonTab.setCurrentWidget(self.helpRibbon)     


    def setupHomeRibbon(self):
        self.newFileBtn = VerticalIconTextButton("assets/newfileicon30.png","New File",hover_bg=cl.SYS_BG3) 
        self.openFileBtn = VerticalIconTextButton("assets/openicon30.png","Open",hover_bg=cl.SYS_BG3) 
        self.saveFileBtn = VerticalIconTextButton("assets/saveicon30.png","Save",hover_bg=cl.SYS_BG3) 
        self.closeFileBtn = VerticalIconTextButton("assets/closeicon30.png","Close",hover_bg=cl.SYS_BG3) 
        self.downloadFileBtn = VerticalIconTextButton("assets/downloadicon30.png","Download",hover_bg=cl.SYS_BG3) 

        self.homeRibbon_layout.addWidget(self.newFileBtn)
        self.homeRibbon_layout.addWidget(self.openFileBtn)
        self.homeRibbon_layout.addWidget(self.downloadFileBtn)
        self.homeRibbon_layout.addWidget(self.saveFileBtn)
        self.homeRibbon_layout.addWidget(self.closeFileBtn)
        self.homeRibbon_layout.addStretch(1)
        
        
        
        


    def getTabLabel(self,label_:str,active=False):
        label = QLabel(label_)
        label.setAlignment(Qt.AlignHCenter)
        if active:
            label.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG3};font-size:14px;font-weight:500;color:white;border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
        else:
            label.setStyleSheet(f"QLabel{{background-color:{cl.SYS_BG1};font-size:14px;font-weight:500;color:{cl.SYS_FG2};border:none;outline:none;border-top-left-radius:7px;border-top-right-radius:7px}}")
        label.setCursor(Qt.PointingHandCursor)

        return label
        



class SignalAnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Analysis")
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        width, height = 1100, 700
        self.resize(width, height)

        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2
        self.move(x, y)

        self.setup_ui()

        controlDock = QDockWidget("Control Panel",self)
        self.controlPanel = SAControlPanel()
        controlDock.setWidget(self.controlPanel)
        self.addDockWidget(Qt.LeftDockWidgetArea,controlDock)

        workSpaceDock = QDockWidget("WorkSpace",self)
        self.workPanel = SAWorkPanel()
        workSpaceDock.setWidget(self.workPanel)
        self.addDockWidget(Qt.RightDockWidgetArea,workSpaceDock)

        statusDock = QDockWidget("Status",self)
        self.statusPanel = SAStatusPanel()
        statusDock.setWidget(self.statusPanel)
        self.addDockWidget(Qt.RightDockWidgetArea,statusDock)

        # Stack statusDock BELOW workSpaceDock (vertically)
        self.splitDockWidget(workSpaceDock, statusDock, Qt.Vertical)

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [controlDock, workSpaceDock],
            [self.width() * 0.3, self.width() * 0.7],
            Qt.Horizontal
        ))

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [workSpaceDock, statusDock],
            [self.height() * 0.75, self.height() * 0.25],
            Qt.Vertical
        ))

    def setup_ui(self):
        self.signalAnalysisMenu = SignalAnalysisMenu()

        self.setMenuWidget(self.signalAnalysisMenu)



