from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, QPoint
class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QPixmap()
        self.position = QPoint(0, 0)
        self.scale = 1.0
        self.last_pos = QPoint(0, 0)
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.position, self.image.scaled(self.image.size() * self.scale))
    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.scale += delta * 0.1
        if self.scale < 0.1:
            self.scale = 0.1
        self.update()
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.position += QPoint(event.position().x() - self.last_pos.x(), event.position().y() - self.last_pos.y())
            self.last_pos = event.position()
            self.update()
    def mousePressEvent(self, event):
        self.last_pos = event.position()