import cv2
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from Components.NotifyMessage import NotifyMessage
from ThreadClass import ThreadClass
from Controller.FunctionQueryTXTFile import Function_TXT
class EditCamera(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(EditCamera, self).__init__(parent)
        # load ui from ui folder
        uic.loadUi("camera_setting.ui", self)
        self.setWindowTitle("Edit Camera")
        self.ipAddress.setStyleSheet("background-color:white;color: black")
        self.setStyleSheet("background-color: #DDDDDD;color: black")
        # show video button
        self.parent = parent
        self.checkBtn.clicked.connect(self.checkCameraIsAvailable)
        self.updateBtn.clicked.connect(self.updateCamera)
        self.close_btn.clicked.connect(self.closeWindow)

        self.func_txt = Function_TXT()
        self.link = None
        print(self.parent.camera_active)
        # tạo ra thread để hiển thị camera, lấy gá trị của camera đang phát bên menuwindow để hiển thị
        self.ThreadActiveCamera = ThreadClass(camera=self.parent.cameras[self.parent.camera_active])
        self.ThreadActiveCamera.ImageUpdate.connect(self.opencv_emit)
        self.ThreadActiveCamera.start()
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
    def updateCamera(self):
        self.link = self.ipAddress.toPlainText()
        if len(self.link) > 255:
            print("Camera IP Address of character is too long")
            return
        NotifyMessage("Update camera successfully")
        # self.parent.__init__()
        index = self.parent.camera_active
        self.func_txt.replaceCamera(index, self.link)
        self.parent.updateCameraList()
        self.ThreadActiveCamera.stop()
        self.close()
        print("Update success")

    def closeWindow(self):
        self.ThreadActiveCamera.stop()
        self.close()
    def closeEvent(self, event):
         if self.ThreadActiveCamera is not None:
             self.ThreadActiveCamera.stop()
         event.accept()