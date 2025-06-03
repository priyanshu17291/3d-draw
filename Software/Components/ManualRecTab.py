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
import Styles.styles as styles
import Styles.colors as cl
from Utils.IconUtils import GetIcon
from qfluentwidgets import ComboBox , setTheme, Theme, setThemeColor , FastCalendarPicker

class ManualRecordings(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(1,1,1,1)
        layout.setSpacing(0)

        head_labels = ["ID","Name","Description","From","To","Duration","Status","Download","Actions"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(head_labels))
        self.table.setHorizontalHeaderLabels(head_labels)

        for i in range(20):
            self.addRecord([f"id_{i}",f"name_{i}" ,"","10:00", "10:30", "30 min", "Completed"])

        self.table.setStyleSheet(styles.table_style1+styles.scrollbar_style)
        self.table.horizontalHeader().setFixedHeight(40)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        config_widget = QWidget()
        config_widget.setFixedHeight(70)
        config_widget_layout = QHBoxLayout()

        duration_input = QLineEdit()
        duration_input.setPlaceholderText("Duration")
        duration_input.setStyleSheet(styles.input_style1)
        duration_input.setFixedSize(80,25)

        description_input = QLineEdit()
        description_input.setPlaceholderText("Description")
        description_input.setStyleSheet(styles.input_style1)
        description_input.setFixedSize(200,25)

        startrec_btn = QPushButton("Start Recording")
        startrec_btn.setStyleSheet(styles.button_style1)
        startrec_btn.setFixedSize(150,25)

        config_widget_layout.addWidget(duration_input)
        config_widget_layout.addWidget(description_input)
        config_widget_layout.addWidget(startrec_btn)
        config_widget_layout.addStretch(1)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)
        self.table.setColumnWidth(7, 160)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.Fixed)
        self.table.setColumnWidth(8, 200)
        self.table.horizontalHeader().setStretchLastSection(False)
 

        config_widget.setLayout(config_widget_layout)
        config_widget.setStyleSheet("border:none;outline:none")

        layout.addWidget(config_widget)
        layout.addWidget(self.table)
        self.setLayout(layout)
        

    def addRecord(self,data:list):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setRowHeight(row,60)

        self.table.setItem(row, 0, QTableWidgetItem(data[0]))
        self.table.setItem(row, 1, QTableWidgetItem(data[1]))
        self.table.setItem(row, 2, QTableWidgetItem(data[2]))
        self.table.setItem(row, 3, QTableWidgetItem(data[3]))
        self.table.setItem(row, 4, QTableWidgetItem(data[4]))
        self.table.setItem(row, 5, QTableWidgetItem(data[5]))
        self.table.setItem(row, 6, QTableWidgetItem(data[6]))



        download_widget = QWidget()
        download_widget_layout = QHBoxLayout()
        download_widget_layout.setSpacing(4)
        download_widget_layout.setContentsMargins(8,8,8,8)
        raw_btn = QPushButton("")
        raw_btn.setIcon(QIcon("assets/rawicon25.png"))
        raw_btn.setIconSize(QSize(25,25))
        ascii_btn = QPushButton("")
        ascii_btn.setIcon(QIcon("assets/ascicon25.png"))
        ascii_btn.setIconSize(QSize(25,25))
        pdf_btn = QPushButton("")
        pdf_btn.setIcon(QIcon("assets/pdficon25.png"))
        pdf_btn.setIconSize(QSize(25,25))
        raw_btn.setStyleSheet(styles.button_style2+";height:35px")
        ascii_btn.setStyleSheet(styles.button_style2+";height:35px")
        pdf_btn.setStyleSheet(styles.button_style2+";height:35px")
        download_widget_layout.addWidget(raw_btn)
        download_widget_layout.addWidget(ascii_btn)
        download_widget_layout.addWidget(pdf_btn)
        download_widget.setLayout(download_widget_layout)

        actions_widget = QWidget()
        actions_widget_layout = QHBoxLayout()
        actions_widget_layout.setSpacing(4)
        actions_widget_layout.setContentsMargins(8,8,8,8)
        preview_btn = QPushButton("Preview")
        analyse_btn = QPushButton("Analyse")
        delete_btn = QPushButton("")
        delete_btn.setIcon(QIcon("assets/binicon25.png"))
        delete_btn.setIconSize(QSize(20,20))
        delete_btn.setFixedWidth(30)
        preview_btn.setStyleSheet(styles.button_style1+";height:35px")
        analyse_btn.setStyleSheet(styles.button_style1+";height:35px")
        delete_btn.setStyleSheet(styles.button_style2+";height:35px")
        actions_widget_layout.addWidget(preview_btn)
        actions_widget_layout.addWidget(analyse_btn)
        actions_widget_layout.addWidget(delete_btn)
        actions_widget.setLayout(actions_widget_layout)

        self.table.setCellWidget(row, 7, download_widget)
        self.table.setCellWidget(row, 8, actions_widget)

        self.table.resizeColumnsToContents()
