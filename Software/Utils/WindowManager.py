# ──────────────── Project Imports ────────────────
from Windows.DynamicInfoWindow import DynamicInfoWindow
from Windows.LoginWindow import LoginWindow
from Windows.LaunchWindow import LaunchWindow
from Windows.SignalAnalysisWindow import SignalAnalysisWindow

import Styles.styles as styles
import Styles.colors as cl



class WindowManager:
    def __init__(self):
        self.loginWindow = LoginWindow()
        self.launchWindow = LaunchWindow()
        self.dynamicInfoWindow = DynamicInfoWindow()
        self.signalAnalysisWindow = SignalAnalysisWindow()

        self.loginWindow.loginPanel.button.clicked.connect(self.showLaunchWindow)
        self.launchWindow.launchPanel.card3.mousePressEvent = self.showDynamicInfoWindow
        self.launchWindow.launchPanel.logout_btn.mousePressEvent = self.showLoginWindow
        self.dynamicInfoWindow.toolbar.signalBtn.mousePressEvent = self.showSignalAnalysisWindow
        self.dynamicInfoWindow.toolbar.exitBtn.mousePressEvent = self.showLaunchWindow

        self.currentWindow = self.loginWindow

    def showLoginWindow(self,event = None):
        self.currentWindow.close()
        self.loginWindow.show()
        self.currentWindow = self.loginWindow

    def showLaunchWindow(self,event = None):
        self.currentWindow.close()
        self.launchWindow.show()
        self.currentWindow = self.launchWindow
        

    def showDynamicInfoWindow(self,event=None):
        self.currentWindow.close()
        self.dynamicInfoWindow.showMaximized()
        self.currentWindow = self.dynamicInfoWindow
    
    def showSignalAnalysisWindow(self,event=None):
        self.signalAnalysisWindow.show()

    
