import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QEvent, QThread, pyqtSignal, pyqtSlot
import cv2
import numpy as np

class ThreadClass(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)
    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index
        self.ThreadActive = False

    def run(self):
        Capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not Capture.isOpened():
            print(f"Error: Camera index {self.camera_index} could not be opened.")
            return

        Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        Capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.ThreadActive = True
        while self.ThreadActive:
            ret, frame_cap = Capture.read()
            if ret:
                self.ImageUpdate.emit(frame_cap)
        Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.quit()

class UpdateForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.train_id = None
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("Hospital Home")
        self.labels = [self.camera_1, self.camera_2, self.camera_3, self.camera_4, self.camera_5, self.camera_6]
        self.start_buttons = [self.btn_Start_1, self.btn_Start_2, self.btn_Start_3, self.btn_Start_4, self.btn_Start_5, self.btn_Start_6]
        self.centralWidget().installEventFilter(self)
        self.workers = [None] * len(self.labels)

        for i, btn in enumerate(self.start_buttons):
            btn.clicked.connect(lambda _, x=i: self.start_clicked(x))
            btn.hide()

        for label in self.labels:
            label.installEventFilter(self)

        self.show()

    def eventFilter(self, obj, event):
        if event.type() in [QEvent.Enter, QEvent.Leave]:
            for i, label in enumerate(self.labels):
                if obj is label:
                    if event.type() == QEvent.Enter:
                        self.start_buttons[i].show()
                    elif event.type() == QEvent.Leave:
                        self.start_buttons[i].hide()
        return super().eventFilter(obj, event)

    def start_clicked(self, num):
        if self.workers[num] is None:
            self.workers[num] = ThreadClass(camera_index=0)
            self.workers[num].ImageUpdate.connect(lambda image, x=num: self.opencv_emit(image, x))
            self.workers[num].start()

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

    def closeEvent(self, event):
        for worker in self.workers:
            if worker is not None:
                worker.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_form = UpdateForm()
    sys.exit(app.exec_())