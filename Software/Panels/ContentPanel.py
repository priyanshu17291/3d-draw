from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox , QStackedWidget
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
from Panels.ChartPanel import ChartPanel
from Panels.SiteInfoPanel import SiteInfoPanel
from Panels.RecordingsPanel import RecordingsPanel
import Styles.styles as styles
import Styles.colors as cl


class ContentPanel(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1};border:1px solid {cl.SYS_BD1}")

        self.siteInfoPanel = SiteInfoPanel()
        self.chartPanel = ChartPanel()
        self.recordingsPanel = RecordingsPanel()

        self.addWidget(self.siteInfoPanel)
        self.addWidget(self.chartPanel)
        self.addWidget(self.recordingsPanel)

        self.setCurrentWidget(self.siteInfoPanel)

    

