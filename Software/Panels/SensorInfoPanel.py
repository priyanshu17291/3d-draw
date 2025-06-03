from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox,QStyleFactory
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF,QSize
from qfluentwidgets import ComboBox , setTheme, Theme, setThemeColor

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
import Styles.styles as styles
import Styles.colors as cl


class SensorInfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(styles.panel_style1)
        layout = QVBoxLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(0)

        # sensorLabel = QLabel("Sensor :")
        # sensorLabel.setStyleSheet(styles.text_style2+";border:none;outline:none;")
        # sensorLabel.setFixedSize(200,30)

        self.sensorCombo = ComboBox()
        # self.sensorCombo.setStyleSheet("background-color:black")
        setTheme(Theme.DARK)
        self.sensorCombo.addItems(["S10001","S20023","S31020"])
        self.sensorCombo.setFixedHeight(30)

        sensorInfoText = """
Status : Streaming

Channels : 3

Digital Outputs : N/A

SMS Alarming : N/A

Interface : Eth

Time Sync : DigiSync

Firmware : 3.1.9.62

Error : 0

Time : 15.05.25 - 10.23.57

Last Boot : N/A

Voltage : 23.28
"""
        sensorInfoLabel = QLabel(sensorInfoText)
        sensorInfoLabel.setStyleSheet(styles.infotext_style1)


        # layout.addWidget(sensorLabel,Qt.AlignHCenter)
        layout.addWidget(self.sensorCombo,Qt.AlignHCenter)
        layout.addWidget(sensorInfoLabel,0)
        layout.addStretch(1)

        self.setLayout(layout)
        setThemeColor(cl.SYS_TH_BG1, save=False)

        self.setLayout(layout)