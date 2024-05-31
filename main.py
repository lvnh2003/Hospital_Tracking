import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import QEvent, pyqtSlot,QTimer
import cv2
import numpy as np
from ThreadClass import ThreadClassDetect
from MenuWindow import MenuWindow
from FunctionQueryTXTFile import Function_TXT

func_txt = Function_TXT()
class HomeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.train_id = None
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("Hospital Home")
        self.labels = [self.camera_1, self.camera_2, self.camera_3, self.camera_4, self.camera_5, self.camera_6]
        self.start_buttons = [self.btn_Start_1, self.btn_Start_2, self.btn_Start_3, self.btn_Start_4, self.btn_Start_5, self.btn_Start_6]
        self.cameras = func_txt.getCameras()
        # Sự kiện click + ẩn button
        self.initUI()
        self.show()
    # init ui các camera và sự kiện camera
    def initUI(self):
        self.centralWidget().installEventFilter(self)
        self.ThreadActiveCamera = [None] * len(self.labels)

        for i, btn in enumerate(self.start_buttons):
            btn.clicked.connect(lambda _, x=i: self.start_camera(x))
            btn.hide()

        for label in self.labels:
            label.installEventFilter(self)
        self.centralWidget().installEventFilter(self)  # Giả sử label nằm trong centralWidget
        self.timers = [QTimer(self) for _ in range(6)]
        for timer in self.timers:
            timer.setSingleShot(True)
            timer.timeout.connect(self.hide_buttons)

    def eventFilter(self, obj, event):
        if event.type() in [QEvent.Enter, QEvent.Leave]:
            for i, label in enumerate(self.labels):
                if obj is label:
                    if event.type() == QEvent.Enter:
                        # kiểm tra số camera đó được thêm chưa
                        if (i+1) > len(self.cameras):
                            self.start_buttons[i].setText("New Camera")
                        self.start_buttons[i].show()
                        self.timers[i].stop()
                    elif event.type() == QEvent.Leave:
                        self.timers[i].start(20) # delay trước khi ẩn nút
        return super().eventFilter(obj, event)

    def start_camera(self, num):
        if(num+1) > len(self.cameras):
            # mở thêm camera
            self.menuWindow = MenuWindow(self)
            self.menuWindow.show()
            return
        if self.ThreadActiveCamera[num] is None:
            self.start_buttons[num].setText("Stop")
            self.ThreadActiveCamera[num] = ThreadClassDetect(camera_index=num)
            self.ThreadActiveCamera[num].ImageUpdate.connect(lambda image, x=num: self.opencv_emit(image, x))
            self.ThreadActiveCamera[num].start()
        # sự kiện stop camera
        else:
            self.ThreadActiveCamera[num].stop()
            self.ThreadActiveCamera[num] = None
            self.start_buttons[num].setText("Start")
    #  gửi tin dạng Image đến cho Qlabel
    @pyqtSlot(np.ndarray, int)
    def opencv_emit(self, Image, camera_index):
        original = self.cvt_cv_qt(Image)
        self.labels[camera_index].setPixmap(original)
        self.labels[camera_index].setScaledContents(True)

    def cvt_cv_qt(self, Image):
        rgb_img = cv2.cvtColor(src=Image, code=cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        cvt2QtFormat = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(cvt2QtFormat)
        return pixmap

    def hide_buttons(self):
        for button in self.start_buttons:
            button.hide()
    def closeEvent(self, event):
        for threadCamera in self.ThreadActiveCamera:
            if threadCamera is not None:
                threadCamera.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_form = HomeWindow()
    sys.exit(app.exec_())
