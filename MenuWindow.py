import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QDialog
from PyQt5 import uic
from PyQt5.QtCore import QEvent, QThread, pyqtSignal, pyqtSlot, QTimer, Qt
import cv2
import numpy as np

from AddCamera import AddCamera
from EditCamera import EditCamera
from NotifyMessage import NotifyMessage
from ThreadClass import ThreadClass
from FunctionQueryTXTFile import Function_TXT
from DeleteConfirm import DeleteConfirmationDialog

func_txt = Function_TXT()


class CameraLabel(QLabel):
    def __init__(self, parent=None):
        super(CameraLabel, self).__init__(parent)
        self.cameras = func_txt.getCameras()
        self.parent = parent

    # sự kiện click vào từng camera
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for label in self.parent.camera_labels:
                label.setStyleSheet(
                    "padding-left:20;border: None; background-color: transparent; color: white; border-radius: 8")

            self.setStyleSheet("background-color: white;color: black;padding-left:20; border-radius: 8")
            clicked_label_index = self.parent.camera_labels.index(self)
            self.parent.camera_active = clicked_label_index
            # nếu thread camera đã chạy rồi thì stop
            if self.parent.ThreadActiveCamera.isRunning():
                self.parent.ThreadActiveCamera.stop()

            # Tạo thread mới ở camera mới
            self.parent.ThreadActiveCamera = ThreadClass(camera=self.cameras[clicked_label_index])
            self.parent.ThreadActiveCamera.ImageUpdate.connect(self.parent.opencv_emit)
            self.parent.ThreadActiveCamera.start()


class MenuWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.camera_labels = None
        uic.loadUi("menuwindow.ui", self)
        self.cameras = func_txt.getCameras()
        self.camera_active = 0
        self.ThreadActiveCamera = ThreadClass(camera=self.cameras[0])
        self.ThreadActiveCamera.ImageUpdate.connect(self.opencv_emit)
        self.ThreadActiveCamera.start()
        self.initUI()
        self.editBtn.clicked.connect(self.editCamera)
        self.addBtn.clicked.connect(lambda: AddCamera(self))
        self.deleteBtn.clicked.connect(self.showDeleteConfirmation)
        self.show()

    def initUI(self):
        if self.camera_labels is None:
            self.camera_labels = []
        else:
            self.clear_layout(self.verticalLayout)
            self.camera_labels = []
        for i in range(len(self.cameras)):
            label = CameraLabel(self)
            label.setText(f"Camera {i + 1}")
            label.setStyleSheet(
                "padding-left:20;border: None; background-color: transparent; color: white; border-radius: 8")
            label.setObjectName(f"camera_{i + 1}")
            self.camera_labels.append(label)
            setattr(self, f"camera_{i + 1}", label)
            self.verticalLayout.addWidget(label)
        if self.camera_labels:
            self.camera_1.setStyleSheet("background-color: white;color: black;padding-left:20; border-radius: 8")



    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())
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

    def editCamera(self):
        EditCamera(self)
        self.ThreadActiveCamera.stop()

    def updateCameraList(self):
        self.cameras = func_txt.getCameras()
        self.initUI()
        self.parent.updateCameraList()

    def showDeleteConfirmation(self):
        dialog = DeleteConfirmationDialog()
        if dialog.exec_() == QDialog.Accepted:
            func_txt.deleteCamera(self.camera_active)
            NotifyMessage("Delete camera successfully")
            self.updateCameraList()

    def closeEvent(self, event):
        if self.ThreadActiveCamera is not None:
            self.ThreadActiveCamera.stop()
        event.accept()
