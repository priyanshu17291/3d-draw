from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout
)
from PyQt5.QtCore import Qt

# ──────────────── Project Imports ────────────────
import Styles.colors as cl
from Utils.IconUtils import GetIcon

class IconCard(QWidget):
    def __init__(self,icon_path,size,header_text,description_text):
        super().__init__()
        self.icon_path = icon_path
        self.size_ = size
        self.header_text = header_text
        self.description_text = description_text
        self.setup_ui()


    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.icon = GetIcon(self.icon_path,self.size_)
        self.icon.setFixedWidth(int(self.size_+0.2*self.size_))


        self.text = QWidget()
        self.text.setStyleSheet("border:none;outline:none")
        self.textLayout = QVBoxLayout()
        self.textLayout.setSpacing(0)

        self.header = QLabel(self.header_text)
        self.header.setStyleSheet("color:white;font-size:16px;font-weight:600;border:none;outline:none")


        self.description = QLabel(self.description_text)
        self.description.setStyleSheet(f"color:{cl.SYS_FG2};font-size:14px;font-weight:500;border:none;outline:none")

        self.textLayout.addStretch(1)
        self.textLayout.addWidget(self.header)
        self.textLayout.addSpacing(3)
        self.textLayout.addWidget(self.description)
        self.textLayout.addStretch(1)

        self.text.setLayout(self.textLayout)

        layout.addWidget(self.icon,Qt.AlignVCenter)
        layout.addWidget(self.text,Qt.AlignVCenter)

        self.setLayout(layout)


class SiteInfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(2,2,2,2)
 


        infoIconsDict = {
            "Status : ": ["assets/statusicon60.png", "Online"],
            "System Time : ": ["assets/timeicon60.png", "May 17th 2025"],
            "Name : ": ["assets/nameicon60.png", "SPPL Admin"],
            "Network : ": ["assets/networkicon60.png", "172.18.0.7"],
            "Total Sensors : ": ["assets/sensoricon60.png", "1"],
            "Total Alarms : ": ["assets/alarmicon60.png", "0"],
            "Total Channels : ": ["assets/channelicon60.png", "3"],
            "Total No.of Users : ": ["assets/usericon60.png", "100"],
            "Last Triggered : ": ["assets/triggericon60.png", "None"],
            "Last Schedule : ": ["assets/scheduleicon60.png", "None"],
            "Ring Buffer Since : ": ["assets/buffericon60.png", "14/05/2025 10:00 a.m"],
            "Latitude & Longitude Schedule : ": ["assets/mapmarkericon60.png", "N/A"],
            "System Up-Time : ": ["assets/stopwatchicon60.png", "Year"],
            "Voyager Up-Time : ": ["assets/stopwatchicon60.png", "2 months"],
            "Description : ": ["assets/descriptionicon60.png", "N/A"],
            "Public Description : ": ["assets/publicicon60.png", "N/A"],
        }

        keys_list = list(infoIconsDict.keys())
        values_list = list(infoIconsDict.values())

        index = 0
        for i in range(8):
            for j in range(2):
                header = keys_list[index]
                icon_path = values_list[index][0]
                description = values_list[index][1]

                card = IconCard(icon_path, 50, header, description)
                layout.addWidget(card, i, j)
                index += 1


        self.setLayout(layout)
        self.setStyleSheet(f"background-color:{cl.SYS_BG5};border:1px solid {cl.SYS_BD2}")