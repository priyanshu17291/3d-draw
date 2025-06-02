import Styles.colors as cl

input_style1 = f"""
QLineEdit {{
    background-color: #545454;
    color: {cl.SYS_FG1};
    border: 1px solid #666666;
    border-radius: 4px;
    padding: 5px;
}}

QLineEdit::placeholder {{
    color: #bbbbbb;
}}

QLineEdit:hover {{
    border: 1px solid #888888;
}}
"""

button_style1=f"""
QPushButton{{
    background-color:{cl.SYS_TH_BG1};
    color:#ffffff;
    border:1px solid {cl.SYS_TH_BD1};
    border-radius:5px;
    font-size:14px;
    font-weight:600;

}}

QPushButton:hover{{
    background-color:{cl.SYS_TH_BGH1};
}}
"""

button_style2=f"""
QPushButton{{
    background-color:{cl.SYS_BG3};
    color:#ffffff;
    border:1px solid {cl.SYS_BD1};
    border-radius:5px;
    font-size:14px;
    font-weight:600;

}}

QPushButton:hover{{
    background-color:{cl.SYS_BG4};
}}
"""

button_style3=f"""
QPushButton{{
    background-color:#a81800;
    color:#ffffff;
    border:1px solid #ff7f69;
    border-radius:5px;
    font-size:14px;
    font-weight:600;

}}

QPushButton:hover{{
    background-color:#751100;
}}
"""

header_style1=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:28px;
    font-weight:600;
}}
"""

header_style2=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:28px;
    font-weight:400;
}}
"""


text_style1=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:14px;
    font-weight:500;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""

text_style2=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:16px;
    font-weight:500;
}}
"""

text_style3=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:12px;
    font-weight:500;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""

splitter_style1=f"""
QSplitter::handle {{
    background-color: {cl.SYS_BG2};
}}
"""


iconbtn_style1=f"""
QPushButton{{
    border:none;
    color:white;
    outline:none;
    font-size:14px;
    font-weight:500;
    padding-left:5px;
    text-align:left;
    margin:3px;
}}
"""

combo_style1 = f"""
QComboBox {{
    background-color: transparent;
    border: 1px solid #3B3B3B;
    color: white;
    padding: 6px;
    border-radius: 4px;
    font-size: 13px;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    background-color: transparent;
}}

QComboBox::down-arrow {{
    image: url(assets/downtriangle24.png);  /* Optional custom arrow */
    width: 12px;
    height: 12px;
}}

QComboBox QAbstractItemView {{
    background-color: #2B2B2B;
    color: white;
    padding: 0px;
    margin: 0px;
    border: 1px solid #3B3B3B;
    selection-background-color: #505050;
    selection-color: white;

    /* Most important */
    outline: none;
    show-decoration-selected: 1;
}}
"""


infotext_style1=f"""
QLabel{{
    color : {cl.SYS_FG2};
    font-size : 14px;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""



table_style1=f"""
QTableWidget{{
    color:white;
}}
QHeaderView::section{{
    color:white;
    font-weight:600;
    background-color:{cl.SYS_BG1};
    font-size:12px;
    outline:none;
    border:none;
    border-right:1px solid {cl.SYS_BD1};
}}


QTableWidget {{
    gridline-color: #444444;
    alternate-background-color: #2e2e2e;
}}
"""

table_style2=f"""
QTableWidget{{
    color:white;
}}
QHeaderView::section{{
    color:white;
    font-weight:500;
    background-color:{cl.SYS_BG2};
    font-size:11px;
    outline:none;
    border:none;
    border-right:1px solid {cl.SYS_BD1};
}}


QTableWidget {{
    gridline-color: #444444;
    alternate-background-color: #2e2e2e;
    font-size:10px;
}}
"""

date_style1=f"""
QDateEdit{{
    background-color: #2e2e2e;
    color: white;
    border: 1px solid #555;
    padding: 4px;
}}
"""


scrollbar_style = f"""
QScrollBar:vertical {{
    border: none;
    background: #2c2c2c;
    width: 10px;
    margin: 0px 0px 0px 0px;
}}

QScrollBar::handle:vertical {{
    background: #5e5e5e;
    min-height: 20px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background: #787878;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    border: none;
    background: #2c2c2c;
    height: 10px;
    margin: 0px 0px 0px 0px;
}}

QScrollBar::handle:horizontal {{
    background: #5e5e5e;
    min-width: 20px;
    border-radius: 5px;
}}

QScrollBar::handle:horizontal:hover {{
    background: #787878;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""


dock_style1= f"""
QDockWidget {{
    background-color: {cl.SYS_BG4};
    color: white;
    font-weight: bold;
    border: 1px solid {cl.SYS_BD1};
}}

QDockWidget::title {{
    background-color: {cl.SYS_BG5};
    border:1px solid {cl.SYS_BD3};
    padding: 4px;
}}
"""

panel_style1=f"""
QWidget{{
    background-color:{cl.SYS_BG1};
    border-left:1px solid {cl.SYS_BD3};
    border-right:1px solid {cl.SYS_BD3};
    border-bottom:1px solid {cl.SYS_BD3};
}}
"""

