from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox,QStackedWidget,QTableWidget,QTableWidgetItem,QHeaderView,QPushButton,QLineEdit
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor,QFont
from PyQt5.QtCore import Qt, QPointF,QSize


from qfluentwidgets import ComboBox , setTheme, Theme, setThemeColor , SwitchButton,LineEdit

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
from Components.ToggleText import ToggleText
import Styles.styles as styles
import Styles.colors as cl

from Utils.IconUtils import GetIcon
from Utils.LabelInput import GetLabelLineEdit , GetLabelCombo


class SAControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.sgFilters = {
            "Low-Pass":["CutOff-Frqeuency",'Filter Order'],
            "High-Pass":["CutOff-Frqeuency",'Filter Order'],
            "Band-Pass":["Low Cutoff","High-Cutoff",'Filter Order'],
            "Band-Stop":["Start","End",'Filter Order'],
            "Moving Average":["Window Size"],
            "Median Filter":["Window Size"],
        }
    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(styles.panel_style1)
        layout = QVBoxLayout()
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(0)

        configLabel = QLabel("Analysis Mode")
        configLabel.setStyleSheet(styles.text_style3)

        self.controlCombox = ComboBox()
        self.controlCombox.setFixedHeight(28)
        self.controlCombox.addItems(
            [
            "Signal Conditioning",
            "Frequency Conditioning",
            "Damping Configuration",
            "Auto-Correlation",
            "Cross-Correlation"
            ]
        )

        dfont = self.controlCombox.font()
        dfont.setPointSize(12)
        self.controlCombox.setFont(dfont)
        print(dfont.family())

        self.modeStack = QStackedWidget()
        self.modeStack.setStyleSheet("border:non")
        self.modeStack.setContentsMargins(0,0,0,0)

        self.signalCondMode = QWidget()
        self.signalCondMode.setStyleSheet("border:none")
        self.signalCondMode_layout = QVBoxLayout()
        self.signalCondMode.setContentsMargins(0,0,0,0)
        self.setupSignalCond()
        self.signalCondMode.setLayout(self.signalCondMode_layout)

        self.freqCondMode = QWidget()
        self.freqCondMode.setStyleSheet("border:none")
        self.freqCondMode_layout = QVBoxLayout()
        self.signalCondMode.setContentsMargins(0,0,0,0)
        self.setupFeqCond()
        self.freqCondMode.setLayout(self.freqCondMode_layout)

        self.dampConfMode = QWidget()
        self.dampConfMode.setStyleSheet("border:none")
        self.dampConfMode_layout = QVBoxLayout()
        self.dampConfMode_layout.addWidget(QLabel("dampConfMode"))
        self.dampConfMode.setLayout(self.dampConfMode_layout)

        self.autoCorrMode = QWidget()
        self.autoCorrMode.setStyleSheet("border:none")
        self.autoCorrMode_layout = QVBoxLayout()
        self.autoCorrMode_layout.addWidget(QLabel("autoCorrMode"))
        self.autoCorrMode.setLayout(self.autoCorrMode_layout)

        self.crossCorrMode = QWidget()
        self.crossCorrMode.setStyleSheet("border:none")
        self.crossCorrMode_layout = QVBoxLayout()
        self.crossCorrMode_layout.addWidget(QLabel("crossCorrMode"))
        self.crossCorrMode.setLayout(self.crossCorrMode_layout)

        self.modeStack.addWidget(self.signalCondMode)
        self.modeStack.addWidget(self.freqCondMode)
        self.modeStack.addWidget(self.dampConfMode)
        self.modeStack.addWidget(self.autoCorrMode)
        self.modeStack.addWidget(self.crossCorrMode)

        self.modeStack.setCurrentWidget(self.signalCondMode)

        self.analyseBtn = QPushButton("Analyse")
        self.analyseBtn.setFixedSize(QSize(250,24))
        self.analyseBtn.setStyleSheet(styles.button_style1+";font-weight:500")



        setTheme(Theme.DARK)
        layout.addSpacing(10)
        layout.addWidget(configLabel)
        layout.addSpacing(5)
        layout.addWidget(self.controlCombox)
        layout.addSpacing(10)
        layout.addWidget(self.modeStack)
        layout.addStretch(1)
        layout.addWidget(self.analyseBtn,0,Qt.AlignHCenter)
        layout.addSpacing(20)

        self.controlCombox.currentIndexChanged.connect(self.changeMode)

        

        self.setLayout(layout)

    

    def setupSignalCond(self):
        self.sgdetrendToggle = ToggleText("Detrending",True,styles.text_style3)
        self.sgdecimationToggle = ToggleText("Decimation",True,styles.text_style3)
        self.sgfilterDToggle = ToggleText("Filter Data",True,styles.text_style3)

        filterDPanel = QWidget()
        filterDPanel_layout = QHBoxLayout()
        filterDPanel_layout.setSpacing(5)
        filterDPanel_layout.setContentsMargins(0,0,0,0)

        filterText = QLabel("Filter")
        filterText.setStyleSheet(styles.text_style3)

        filterIcon = GetIcon("assets/filtericon20.png",20)
        filterIcon.setFixedWidth(20)
        self.filterCombo = ComboBox(self)
        self.filterCombo.addItems(
            [
                "Low-Pass",
                "High-Pass",
                "Band-Pass",
                "Band-Stop",
                "Moving Average",
                "Median Filter"
            ]
        )

        self.filterCombo.setFixedHeight(25)
        dfont = self.filterCombo.font()
        dfont.setPointSize(11)
        self.filterCombo.setFont(dfont)
        self.filterCombo.currentTextChanged.connect(self.sgFilterChange)

        filterDPanel_layout.addWidget(filterIcon,0)
        filterDPanel_layout.addWidget(self.filterCombo,1)

        filterDPanel.setLayout(filterDPanel_layout)

        self.sgFilterTable = QTableWidget()
        self.sgFilterTable.setColumnCount(2)
        self.sgFilterTable.setRowCount(2)
        self.sgFilterTable.setHorizontalHeaderLabels(["Parameter","Value"])

        self.sgFilterTable.setItem(0,0,QTableWidgetItem("Cutoff Frequency"))
        self.sgFilterTable.setItem(0,1,QTableWidgetItem(""))

        self.sgFilterTable.setItem(1,0,QTableWidgetItem("Filter Order"))
        self.sgFilterTable.setItem(1,1,QTableWidgetItem(""))

        self.sgFilterTable.setStyleSheet(styles.table_style2)
        self.sgFilterTable.horizontalHeader().setStretchLastSection(True)
        self.sgFilterTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sgFilterTable.verticalHeader().setVisible(False)
        

        self.signalCondMode_layout.addWidget(self.sgdetrendToggle)
        self.signalCondMode_layout.addWidget(self.sgdecimationToggle)
        self.signalCondMode_layout.addWidget(self.sgfilterDToggle)
        self.signalCondMode_layout.addSpacing(25)
        self.signalCondMode_layout.addWidget(filterText)
        self.signalCondMode_layout.addWidget(filterDPanel)
        self.signalCondMode_layout.addSpacing(10)
        self.signalCondMode_layout.addWidget(self.sgFilterTable)
  

        self.signalCondMode_layout.addStretch(1)


    def setupFeqCond(self):

        fftlabel , fftinput = GetLabelLineEdit("FFT Size :","Enter Float")
        splrlabel , splrinput = GetLabelLineEdit("Sampling Rate :","Enter Float")
        windowslabel , windowsddw = GetLabelCombo("Select Window :",["Rectangular","Hanning","Gaussian","Blackman","Kaiser","Flattop"])
        self.fcfftPlotToggle = ToggleText("Show FFT Plot",True,styles.text_style3)

        self.freqCondMode_layout.addWidget(fftlabel)
        self.freqCondMode_layout.addWidget(fftinput)
        self.freqCondMode_layout.addSpacing(5)
        self.freqCondMode_layout.addWidget(splrlabel)
        self.freqCondMode_layout.addWidget(splrinput)
        self.freqCondMode_layout.addSpacing(30)
        self.freqCondMode_layout.addWidget(windowslabel)
        self.freqCondMode_layout.addWidget(windowsddw)
        self.freqCondMode_layout.addSpacing(5)
        self.freqCondMode_layout.addWidget(self.fcfftPlotToggle)
        self.freqCondMode_layout.addStretch(1)
        

    def changeMode(self,index):
        self.modeStack.setCurrentIndex(index)

    def sgFilterChange(self,index):
        self.sgFilterTable.clear()
        self.sgFilterTable.setHorizontalHeaderLabels(["Parameter","Value"])

        print(index)

        parameters = self.sgFilters[index]
        self.sgFilterTable.setRowCount(len(parameters))
        for i in range(0,len(parameters)):
            self.sgFilterTable.setItem(i,0,QTableWidgetItem(parameters[i]))
            self.sgFilterTable.setItem(i,1,QTableWidgetItem(""))
            
