#Qt Imports
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout ,QHBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

#Styles Import
import Styles.styles as styles
import Styles.colors as cl

#Project Imports
from Components.Header import Header
from Utils.IconUtils import GetIcon


class DashCard(QWidget):
    def __init__(self,icon_path,size_,header_text,description_text):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.icon_path = icon_path
        self.size_ = size_
        self.header_text = header_text
        self.description_text = description_text

        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()

        icon = GetIcon(self.icon_path,self.size_)
        header = QLabel(self.header_text)
        description = QLabel(self.description_text)
        description.setAlignment(Qt.AlignHCenter)

        header.setStyleSheet(f"color:{cl.SYS_FG1};font-size:20px;font-weight:600;border:none;outline:none;")
        description.setStyleSheet(f"""QLabel{{
    color : {cl.SYS_FG3};
    font-size : 15px;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""
)


        layout.addStretch(1)
        layout.addWidget(icon)
        layout.addStretch(1)
        layout.addWidget(header,0,Qt.AlignHCenter)
        layout.addWidget(description,0,Qt.AlignHCenter)
        layout.addStretch(1)

        self.setStyleSheet(f"""
QWidget{{
    background-color : {cl.SYS_BG3};
    border:1px solid {cl.SYS_BD1};                    
}}
""")
        self.setCursor(Qt.PointingHandCursor)
        self.setLayout(layout)



class LaunchPanel(QWidget):
    def __init__(self):
        super().__init__()
        # self.main_window = main_window

        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")
        layout = QVBoxLayout()

        #Header
        header = Header()

        header_text1 = QLabel("Welcome !")
        header_text2 = QLabel("Your Tools are Ready - choose a Workspace to get Started")

        header_text1.setStyleSheet(styles.header_style2+"QLabel{font-size:48px;font-weight:500}")
        header_text2.setStyleSheet(styles.infotext_style1+f"QLabel{{font-size:18px;color:{cl.SYS_FG3}}}")



        #CardContainer
        cardContainer = QWidget()
        cardContainer_layout = QHBoxLayout()

         
        self.card1 = DashCard("assets/structureicon100.png",100,"Structural Assessment","View Detailed Insights\ninto Structural Performance") 
        self.card2 = DashCard("assets/staticicon100.png",100,"Static Monitoring","Review Fixed Diagnostic Data \nfrom out DataBase")
        self.card3 = DashCard("assets/dashboardicon100.png",100,"Dynamic Monitoring","Start Analysing Live Sensor Data \ndirectly from the Cloud") 

        self.card1.setFixedSize(275,275)
        self.card2.setFixedSize(275,275)
        self.card3.setFixedSize(275,275)

        cardContainer_layout.addStretch(1)
        cardContainer_layout.addWidget(self.card1,0,Qt.AlignHCenter) 
        cardContainer_layout.addWidget(self.card2,0,Qt.AlignHCenter)   
        cardContainer_layout.addWidget(self.card3,0,Qt.AlignHCenter)     
        cardContainer_layout.addStretch(1)

        cardContainer.setLayout(cardContainer_layout)


        #Button Container
        buttonContainer = QWidget()
        buttonContainer_layout = QHBoxLayout()

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setFixedSize(175, 35)
        self.logout_btn.setStyleSheet(styles.button_style1)

        self.help_btn = QPushButton("View Documentation")
        self.help_btn.setFixedSize(175, 35)
        self.help_btn.setStyleSheet(styles.button_style2)

        buttonContainer_layout.addStretch(1)
        buttonContainer_layout.addWidget(self.help_btn)
        buttonContainer_layout.addWidget(self.logout_btn)

        buttonContainer.setLayout(buttonContainer_layout)
    

        layout.addWidget(header)
        layout.addSpacing(10)
        layout.addWidget(header_text1,0,Qt.AlignHCenter)
        layout.addWidget(header_text2,0,Qt.AlignHCenter)
        layout.addSpacing(10)
        layout.addWidget(cardContainer)
        layout.addStretch(1)
        layout.addWidget(buttonContainer)

        self.setLayout(layout)


        