from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox , QTabWidget,QTableWidget,QTableWidgetItem,QStackedWidget,QPushButton,QHeaderView,QDateEdit,QCalendarWidget,QLineEdit,
    
)   
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor,QIcon
from PyQt5.QtCore import Qt, QPointF,QDate,QSize

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
from Components.RingBufferTab import RingBuffer
from Components.ManualRecTab import ManualRecordings
from Components.ScheduleEventsTab import ScheduleEvents
import Styles.styles as styles
import Styles.colors as cl
from Utils.IconUtils import GetIcon
from qfluentwidgets import ComboBox , setTheme, Theme, setThemeColor , FastCalendarPicker

class RecordingsPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color:{cl.SYS_BG5};border:1px solid {cl.SYS_BD2}")

        layout = QVBoxLayout()
        layout.setContentsMargins(1,1,1,1)
        layout.setSpacing(0)

        self.tabs = QWidget()
        self.tabs.setStyleSheet("border:none;")
        tabs_layout = QHBoxLayout()

        self.ringBufferTab = QLabel(" Ring Buffer ")
        self.manualRecTab = QLabel(" Manual Recordings ")
        self.scheduleEventsTab = QLabel(" Schedule Events ")

        self.ringBufferTab.setAlignment(Qt.AlignHCenter)
        self.manualRecTab.setAlignment(Qt.AlignHCenter)
        self.scheduleEventsTab.setAlignment(Qt.AlignHCenter)

        self.ringBufferTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG1};border:none;outline:none;border-bottom:1px solid white}}")
        self.manualRecTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")
        self.scheduleEventsTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")

        self.ringBufferTab.setCursor(Qt.PointingHandCursor)
        self.manualRecTab.setCursor(Qt.PointingHandCursor)
        self.scheduleEventsTab.setCursor(Qt.PointingHandCursor)

        self.ringBufferTab.mousePressEvent = self.showRingBuffer
        self.manualRecTab.mousePressEvent = self.showManualRec
        self.scheduleEventsTab.mousePressEvent = self.showScheduleEvents

        tabs_layout.addWidget(self.ringBufferTab,0,Qt.AlignVCenter)
        tabs_layout.addWidget(self.manualRecTab,0,Qt.AlignVCenter)
        tabs_layout.addWidget(self.scheduleEventsTab,0,Qt.AlignVCenter)
        tabs_layout.addStretch(1)

        self.tabs.setLayout(tabs_layout)
        self.tabs.setStyleSheet("border:none;outline:none")

        self.content = QStackedWidget()
        self.ringBufferPanel = RingBuffer()
        self.manualRecPanel = ManualRecordings()
        self.schedulePanel = ScheduleEvents()
        self.content.addWidget(self.ringBufferPanel)
        self.content.addWidget(self.manualRecPanel)
        self.content.addWidget(self.schedulePanel)
        self.content.setCurrentWidget(self.ringBufferPanel)

        layout.addWidget(self.tabs)
        layout.addWidget(self.content)
        # layout.addStretch(1)
        self.setLayout(layout)

    def showRingBuffer(self,event):
        self.ringBufferTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG1};border:none;outline:none;border-bottom:1px solid white}}")
        self.manualRecTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")
        self.scheduleEventsTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")
        self.content.setCurrentWidget(self.ringBufferPanel)

    def showManualRec(self,event):
        self.ringBufferTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")
        self.manualRecTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG1};border:none;outline:none;border-bottom:1px solid white}}")
        self.scheduleEventsTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")
        self.content.setCurrentWidget(self.manualRecPanel)

    def showScheduleEvents(self,event):
        self.ringBufferTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")
        self.manualRecTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG2};border:none;outline:none}}")
        self.scheduleEventsTab.setStyleSheet(f"QLabel{{font-size:14px;font-weight:600;color:{cl.SYS_FG1};border:none;outline:none;border-bottom:1px solid white}}")
        self.content.setCurrentWidget(self.schedulePanel)
        