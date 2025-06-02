from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox , QTabWidget,QTableWidget,QTableWidgetItem,QStackedWidget,QPushButton,QHeaderView,QDateEdit,QCalendarWidget,QLineEdit,
    
)   
from PyQt5.QtCore import QDate,QSize

# ──────────────── Project Imports ────────────────
import Styles.styles as styles
import Styles.colors as cl
from Utils.IconUtils import GetIcon
from qfluentwidgets import  FastCalendarPicker

class RingBuffer(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(1,1,1,1)
        layout.setSpacing(0)

        head_labels = ["File Name","From","To","Duration","Status","Download","Actions"]
        self.table = QTableWidget()
        self.table.setColumnCount(len(head_labels))
        self.table.setHorizontalHeaderLabels(head_labels)

        for i in range(20):
            self.addRecord([f"10000_{i}.json", "10:00", "10:30", "30 min", "Completed"])


        self.table.setStyleSheet(styles.table_style1+styles.scrollbar_style)
        self.table.horizontalHeader().setFixedHeight(40)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 160)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(6, 160)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.horizontalHeader().setStretchLastSection(False)

        fromWidget = QWidget()
        fromWidget.setFixedHeight(70)
        fromWidget.setStyleSheet("border:none;outline:none")
        fromWidget_layout = QHBoxLayout()

        from_label = QLabel("From Date : ")
        from_label.setStyleSheet(styles.text_style1)
        date_picker = FastCalendarPicker()
        # date_picker.setCalendarPopup(True)
        date_picker.setDate(QDate.currentDate()) 
        # date_picker.setStyleSheet(styles.date_style1)

        fromWidget_layout.addWidget(from_label)
        fromWidget_layout.addWidget(date_picker)
        fromWidget_layout.addStretch(1)

        fromWidget.setLayout(fromWidget_layout)

        layout.addWidget(fromWidget)
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

        download_widget = QWidget()
        download_widget_layout = QHBoxLayout()
        download_widget_layout.setSpacing(4)
        download_widget_layout.setContentsMargins(8,8,8,8)
        raw_btn = QPushButton("Raw")
        ascii_btn = QPushButton("ASCII")
        raw_btn.setStyleSheet(styles.button_style2+";height:35px")
        ascii_btn.setStyleSheet(styles.button_style2+";height:35px")
        download_widget_layout.addWidget(raw_btn)
        download_widget_layout.addWidget(ascii_btn)
        download_widget.setLayout(download_widget_layout)

        actions_widget = QWidget()
        actions_widget_layout = QHBoxLayout()
        actions_widget_layout.setSpacing(4)
        actions_widget_layout.setContentsMargins(8,8,8,8)
        preview_btn = QPushButton("Preview")
        analyse_btn = QPushButton("Analyse")
        preview_btn.setStyleSheet(styles.button_style1+";height:35px")
        analyse_btn.setStyleSheet(styles.button_style1+";height:35px")
        actions_widget_layout.addWidget(preview_btn)
        actions_widget_layout.addWidget(analyse_btn)
        actions_widget.setLayout(actions_widget_layout)

        self.table.setCellWidget(row, 5, download_widget)
        self.table.setCellWidget(row, 6, actions_widget)

        self.table.resizeColumnsToContents()
