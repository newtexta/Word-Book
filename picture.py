from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QFile, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QDesktopServices)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy, QStyleFactory,
    QSpacerItem, QWidget, QFileDialog, QScrollArea, QMessageBox)
from PictureUI import Ui_Dialog
from PIL import Image
from PIL import ImageGrab
import pytesseract
import PictureIdentification
import os
import cv2
import numpy as np
from qt_material import apply_stylesheet
class picture_ocr(QDialog,Ui_Dialog):
    def __init__(self):
        super(picture_ocr,self).__init__()
        self.setupUi(self)
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        id_secret_path = d + "/resource/Identification.txt"
        icon_path = d + "/resource/OCR.png"
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        with open(id_secret_path,"r") as f:
            all_ = f.readlines()
            APP_ID = all_[0][3:-1]
            APP_SECRET = all_[1][7:-1]
        if bool(APP_ID) and bool(APP_SECRET):
            self.lineEdit.setText(APP_ID)
            self.lineEdit_2.setText(APP_SECRET)
        self.radioButton.setChecked(True)
        self.radioButton_3.setChecked(True)
        self.radioButton_6.setChecked(True)
        self.radioButton_5.setEnabled(False)
        self.pushButton_2.clicked.connect(self.OCR_run_basic)
        self.radioButton_6.setEnabled(False)
        self.radioButton_7.setEnabled(False)
        self.radioButton_5.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.radioButton_2.toggled.connect(self._setEnabled_1)
        self.radioButton.toggled.connect(self._setEnabled_2)
        self.pushButton.clicked.connect(self.open_picture)
        self.pushButton_3.clicked.connect(self.jump_website)
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.theme)
        self.timer1.start(1000)
    def theme(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        theme_path = d + "/resource/Theme.txt"
        with open(theme_path,"r") as f:
            selected_text = f.read()
        if selected_text == "default_theme":
            fusion_style = QStyleFactory.create("Fusion")
            self.setStyle(fusion_style)
        else:
            apply_stylesheet(self, theme=selected_text)
        with open(theme_path,"w") as f:
            f.write(selected_text)
    def open_picture(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Image File', '', 'Image Files (*.png *.jpg *.jpeg)')
        file_path_ = QFile(file_path)
        if file_path and file_path_.exists():
            self.lineEdit_3.setText(file_path)
            self.widget_3.image = QPixmap(file_path)
            self.widget_3.update()
            img2 = cv2.imread(file_path)
            gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
            lines = cv2.HoughLinesP(thresh, 1, np.pi/90,300, minLineLength=500, maxLineGap=500)
            cv2.waitKey(0)
            a = os.path.abspath('.')
            b = a.split("\\")
            c = tuple(b)
            d = '/'.join(c)
            file = d + "/resource/temp.png"
            cv2.imwrite(file,thresh)
    def _setEnabled_1(self):
        self.radioButton_5.setEnabled(True)
        self.radioButton_5.setChecked(True)
        self.radioButton_3.setEnabled(False)
        self.radioButton_4.setEnabled(False)
        self.radioButton_6.setEnabled(True)
        self.radioButton_7.setEnabled(True)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
    def _setEnabled_2(self):
        self.radioButton_5.setEnabled(False)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setEnabled(True)
        self.radioButton_4.setEnabled(True)
        self.radioButton_6.setEnabled(False)
        self.radioButton_7.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
    def OCR_run_basic(self):
        a = os.path.abspath('.')
        b = a.split("\\")
        c = tuple(b)
        d = '/'.join(c)
        T_T = d + "/resource/TempText.txt"
        file_path = self.lineEdit_3.text()
        file_path_ = QFile(file_path)
        if file_path and file_path_.exists():
            if self.radioButton.isChecked():
                file = d + "/resource/temp.png"
                if self.radioButton_3.isChecked():
                    text = pytesseract.image_to_string(Image.open(file),lang="eng")
                    with open(T_T,"w") as file:
                        file.writelines(text)
                    reply = QMessageBox.information(self,u'消息',u'识别完成！',QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        pass
                if self.radioButton_4.isChecked():
                    text = pytesseract.image_to_string(Image.open(file),lang="chi_sim")
                    with open(T_T,"w") as file:
                        file.writelines(text)
                    reply = QMessageBox.information(self,u'消息',u'识别完成！',QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        pass
            elif self.radioButton_2.isChecked():
                a = os.path.abspath('.')
                b = a.split("\\")
                c = tuple(b)
                d = '/'.join(c)
                id_secret_path = d + "/resource/Identification.txt"
                if self.radioButton_6.isChecked():
                    results = PictureIdentification.basic_identification_standard(file_path)
                    id_ = self.lineEdit.text()
                    secret_ = self.lineEdit_2.text()
                    text_in = "ID=" + id_ + "\n" + "SECRET=" + secret_ + "\n" + accurate_time + "\n" + standard_time
                    with open(id_secret_path,"w") as ff:
                        ff.write(text_in)
                    with open(T_T,"w") as file:
                        for dict_ in results:
                            text_line = dict_["words"]
                            file.write(text_line)
                            file.write("\n")
                    reply = QMessageBox.information(self,u'消息',u'识别完成！',QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        pass
                if self.radioButton_7.isChecked():
                    results = PictureIdentification.basic_identification_high(file_path)
                    id_ = self.lineEdit.text()
                    secret_ = self.lineEdit_2.text()
                    text_in = "ID=" + id_ + "\n" + "SECRET=" + secret_ + "\n" + accurate_time + "\n" + standard_time
                    with open(id_secret_path,"w") as ff:
                        ff.write(text_in)
                    with open(T_T,"w") as file:
                        for dict_ in results:
                            text_line = dict_["words"]
                            file.write(text_line)
                            file.write("\n")
                    reply = QMessageBox.information(self,u'消息',u'识别完成！',QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        pass
            else:
                reply = QMessageBox.warning(self,u'警告',u'请选择识别方式！',QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    pass
        else:
            reply = QMessageBox.warning(self,u'警告',u'请先打开图片再识别！',QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                pass
    def jump_website(self):
        url = QUrl('https://console.bce.baidu.com/#/index/overview')  # 指定要跳转的链接
        QDesktopServices.openUrl(url)