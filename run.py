import sys
import os
import ctypes
from WordBook import WordBook
from PySide6.QtWidgets import (QApplication, QDockWidget, QGraphicsView, QGridLayout,
    QMainWindow, QMenuBar, QSizePolicy, QStatusBar, QComboBox,
    QWidget)
from qt_material import apply_stylesheet
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if __name__ == "__main__":
    os.environ['QT_PLUGIN_PATH'] = r'E:\Qt\Tools\QtDesignStudio\qt6_design_studio_reduced_version\plugins'
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'E:\Qt\Tools\QtDesignStudio\qt6_design_studio_reduced_version\plugins\platforms'
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    app = QApplication(sys.argv)
    cc = WordBook()
    cc.show()
    def on_exit():
        if cc.worker.isRunning():
            cc.worker.quit()
            cc.worker.wait()
        if cc.internet.isRunning():
            cc.internet.quit()
            cc.internet.wait()
    app.aboutToQuit.connect(on_exit)
    sys.exit(app.exec())