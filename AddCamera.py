import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

from NotifyMessage import NotifyMessage
from ThreadClass import ThreadClass
from FunctionQueryTXTFile import Function_TXT


class AddCamera(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AddCamera, self).__init__(parent)
        # load ui from ui folder
        uic.loadUi("camera_setting.ui", self)
        self.setWindowTitle("Add Camera")
        self.ipAddress.setStyleSheet("background-color:white;color: black")
        self.setStyleSheet("background-color: #DDDDDD;color: black")
        # show video button
        self.parent = parent
        self.checkBtn.clicked.connect(self.checkCameraIsAvailable)
        self.updateBtn.setText("Add")
        self.updateBtn.clicked.connect(self.addCamera)
        self.close_btn.clicked.connect(self.closeWindow)

        self.func_txt = Function_TXT()
        self.linkIsTrue = False
        self.link = None
        # tạo ra thread để check được method isRunning()
        self.ThreadActiveCamera = ThreadClass(camera=0)
        self.show()

    # Kiểm tra IP của camera có chuẩn ( tòn tại hay không )
    def checkCameraIsAvailable(self):
        self.link = self.ipAddress.toPlainText()
        if len(self.link) > 255:
            print("Camera IP Address of character is too long")
            return
        # change value video_capture
        if self.ThreadActiveCamera.isRunning():
            self.ThreadActiveCamera.stop()
        # Tạo thread mới ở camera mới
        self.ThreadActiveCamera = ThreadClass(camera=self.link)
        self.ThreadActiveCamera.ImageUpdate.connect(self.opencv_emit)
        self.ThreadActiveCamera.start()
    @pyqtSlot(np.ndarray)
    def opencv_emit(self, Image):
        original = self.cvt_cv_qt(Image)
        self.camera_preview.setPixmap(original)
        self.camera_preview.setScaledContents(True)

    def cvt_cv_qt(self, Image):
        rgb_img = cv2.cvtColor(src=Image, code=cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        cvt2QtFormat = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(cvt2QtFormat)
        return pixmap

    def addCamera(self):
        # if self.linkIsTrue:
        # thêm link mới vào file cameras.txt
        self.link = self.ipAddress.toPlainText()
        if len(self.link) > 255:
            print("Camera IP Address of character is too long")
            return
        NotifyMessage("Add new camera successfully")
        self.func_txt.addCamera(self.link)
        self.parent.updateCameraList()
        self.ThreadActiveCamera.stop()
        self.close()

    def closeWindow(self):
        if self.ThreadActiveCamera is not None:
            self.ThreadActiveCamera.stop()
        self.close()

    def closeEvent(self, event):
        if self.ThreadActiveCamera is not None:
            self.ThreadActiveCamera.stop()
        event.accept()
