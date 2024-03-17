from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QThread, Signal
import time
class Worker(QThread):
    current_time = Signal(str)
    def run(self):
    	while True:
	        current_datetime = time.ctime()
	        self.current_time.emit(current_datetime)
	        time.sleep(1)