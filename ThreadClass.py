import datetime

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import numpy as np

from DetectFallingModel import FallDetect
from FunctionQueryTXTFile import Function_TXT
from NotifyMessage import NotifyMessage

fall_detect = FallDetect(conf=0.7)
func_txt = Function_TXT()
from SendPush import sendMessage, uploadImageToImgur


# class thread để gửi frame cho label
class ThreadClassDetect(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)

    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index
        self.ThreadActive = False
        self.fall_detect = fall_detect
        self.cameras = func_txt.getCameras()
        self.last_alert = None
        self.alert_telegram_each = 15  # seconds

    def run(self):
        self.cameras = func_txt.getCameras()
        Capture = cv2.VideoCapture(self.cameras[self.camera_index])
        if not Capture.isOpened():
            print(f"Error: Camera could not be opened.")
            return

        Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        Capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.ThreadActive = True
        while self.ThreadActive:
            ret, frame_cap = Capture.read()
            if ret:
                results = self.fall_detect.detect(frame_cap)
                # phát hiện có người ngã
                if results:
                    cv2.putText(frame_cap, "Fall detect!!!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                    # gửi thông báo sau mỗi 15s, tránh spam
                    if (self.last_alert is None) or (
                            (datetime.datetime.utcnow() - self.last_alert).total_seconds() > self.alert_telegram_each):
                        self.last_alert = datetime.datetime.utcnow()
                        cv2.imwrite("img.jpg", frame_cap)
                        # upload ảnh lên imgur
                        url = uploadImageToImgur("./img.jpg")
                        sendMessage(self.camera_index+1, url)

                annotated_frame = results.plot() if results else frame_cap
                self.ImageUpdate.emit(annotated_frame)
        Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.quit()


class ThreadClass(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)
    NotifySignal = pyqtSignal(str)

    def __init__(self, camera):
        super().__init__()
        self.ThreadActive = False
        self.camera = camera
        self.NotifySignal.connect(self.notify_error)

    def run(self):
        Capture = cv2.VideoCapture(self.camera)
        if not Capture.isOpened():
            self.NotifySignal.emit("Invalid Camera IP Address")
            print("Error: Camera could not be opened.")
            self.stop()
            return

        Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        Capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.ThreadActive = True
        while self.ThreadActive:
            ret, frame_cap = Capture.read()
            if ret:
                self.ImageUpdate.emit(frame_cap)
        Capture.release()

    @pyqtSlot(str)
    def notify_error(self, message):
        NotifyMessage(message, 0)

    def stop(self):
        self.ThreadActive = False
        self.quit()
