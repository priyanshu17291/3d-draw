# ──────────────── Qt Imports ────────────────
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox , QSizePolicy , QStackedWidget , QApplication ,QMainWindow , QDockWidget , QTextEdit  )
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor , QGuiApplication,QPalette,QFont
from PyQt5.QtCore import Qt, QPointF , QTimer
from qfluentwidgets import ComboBox , setTheme, Theme, setThemeColor , SwitchButton

# ──────────────── Project Imports ────────────────
from Windows.DynamicInfoWindow import DynamicInfoWindow
from Windows.LoginWindow import LoginWindow
from Windows.LaunchWindow import LaunchWindow
from Windows.SignalAnalysisWindow import SignalAnalysisWindow

import Styles.styles as styles
import Styles.colors as cl

from Utils.WindowManager import WindowManager


#System Imports
import os
import sys
import platform
# Only import Mac-specific modules if on macOS
if platform.system() == 'Darwin':
    import objc
    from AppKit import NSApp, NSAppearance
    os.environ['QT_MAC_WANTS_LAYER'] = '1'




if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    ######MAC ONLY######
    NSApp.setAppearance_(NSAppearance.appearanceNamed_("NSAppearanceNameDarkAqua"))
    ####################

    app.setStyleSheet(styles.dock_style1)
    # app.setFont(QFont("Helvetica Neue"))
    setThemeColor(cl.SYS_TH_BG1, save=False)

    # dynamicInfoWindow = DynamicInfoWindow()
    # dynamicInfoWindow.show()

    signalAnalysisWindow = SignalAnalysisWindow()
    signalAnalysisWindow.show()

    # windowManager = WindowManager()
    # windowManager.showLoginWindow()

    sys.exit(app.exec_())

