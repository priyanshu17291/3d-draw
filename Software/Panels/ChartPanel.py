# ──────────────── Qt Imports ────────────────
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
from Utils.IconUtils import GetIcon
import Styles.styles as styles
import Styles.colors as cl

import random

def create_line_chart():
    # Generate random data
    series = QLineSeries()
    for x in range(300):
        y = random.randint(0, 300)
        series.append(QPointF(x, y))

    series.setColor(QColor("deepskyblue"))

    # Create chart
    chart = QChart()
    chart.addSeries(series)
    chart.createDefaultAxes()
    chart.setBackgroundBrush(QColor("#000000"))
    chart.setContentsMargins(0, 0, 0, 0)
    chart.setBackgroundRoundness(0)
    chart.legend().hide()

    # Remove chart margins
    chart.layout().setContentsMargins(0, 0, 0, 0)

    # Chart view
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    chart_view.setMinimumHeight(150)

    return chart_view


class ChartPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.paused = False

    
    def setup_ui(self):
        # self.setStyleSheet(f"border:1px solid {cl.SYS_BD1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)



        self.header = QLabel("Channel Plot : S10001/x")
        self.header.setStyleSheet(styles.text_style2)

        toolbar = QWidget()
        toolbar_layout = QHBoxLayout()


        channel_label = QLabel("Select Channel : ")
        channel_label.setStyleSheet(styles.text_style1)
        self.axisCombo = QComboBox()
        self.axisCombo.currentTextChanged.connect(self.toggleAxis)
        self.axisCombo.setStyleSheet(styles.combo_style1)
        self.axisCombo.addItems(["x-axis","y-axis","z-axis"])
        self.axisCombo.setFixedWidth(200)

        self.crosshair_icon = GetIcon("assets/crosshairicon24.png",24)
        self.pause_play_icon =GetIcon("assets/paunseicon24.png",24)
        self.move_icon = GetIcon("assets/moveicon24.png",24)
        self.zoomin_icon = GetIcon("assets/zoominicon24.png",24)
        self.zoomout_icon = GetIcon("assets/zoomouticon24.png",24)
        self.settings_icon = GetIcon("assets/settings2icon24.png",24)
        self.data_icon = GetIcon("assets/databaseicon24.png",24)
        self.download_icon = GetIcon("assets/downloadicon24.png",24)
        self.reset_icon = GetIcon("assets/reseticon24.png",24)

        self.pause_play_icon.mousePressEvent = self.togglePausePlay


        toolbar_layout.addWidget(channel_label)
        toolbar_layout.addSpacing(5)
        toolbar_layout.addWidget(self.axisCombo)
        toolbar_layout.addStretch(1)
        toolbar_layout.addWidget(self.pause_play_icon,0)
        toolbar_layout.addWidget(self.crosshair_icon,0)
        toolbar_layout.addWidget(self.move_icon,0)
        toolbar_layout.addWidget(self.zoomin_icon,0)
        toolbar_layout.addWidget(self.zoomout_icon,0)
        toolbar_layout.addWidget(self.settings_icon,0)
        toolbar_layout.addWidget(self.data_icon,0)
        toolbar_layout.addWidget(self.download_icon,0)
        toolbar_layout.addWidget(self.reset_icon,0)
        
        

        toolbar.setLayout(toolbar_layout)
        toolbar.setStyleSheet("background-color:black")


        layout.addWidget(self.header,0)
        layout.addWidget(toolbar)
        for _ in range(1):
            layout.addWidget(create_line_chart())

        

        self.setLayout(layout)


    def togglePausePlay(self, event):
        if not self.paused:
            self.pause_play_icon.setPixmap(QPixmap("assets/playicon24.png"))
            self.paused = True
        else:
            self.pause_play_icon.setPixmap(QPixmap("assets/paunseicon24.png"))
            self.paused = False

    def toggleAxis(self,text):
        current_header = self.header.text()
        axis = ""
        if text == "x-axis":axis = "x"
        elif text == "y-axis":axis = "y"
        elif text == "z-axis":axis = "z"
        self.header.setText(current_header[0:len(current_header)-1]+axis)

        print(axis)