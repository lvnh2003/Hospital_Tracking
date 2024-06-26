import datetime

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import numpy as np
from playsound import playsound
import threading
from Model.DetectFallingModel import FallDetect
from Controller.FunctionQueryTXTFile import Function_TXT
from Components.NotifyMessage import NotifyMessage

fall_detect = FallDetect(conf=0.7)
func_txt = Function_TXT()
from Controller.SendPush import sendMessage, uploadImageToImgur
from concurrent.futures import ThreadPoolExecutor

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
        with ThreadPoolExecutor(max_workers=2) as executor:
            while self.ThreadActive:
                ret, frame_cap = Capture.read()
                if ret:
                    results = self.fall_detect.detect(frame_cap)
                    # phát hiện có người ngã
                    if results:
                        sound_thread = threading.Thread(target=self.playWarningSound)
                        sound_thread.start()
                        cv2.putText(frame_cap, "Fall detect!!!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                        # gửi thông báo sau mỗi 15s, tránh spam
                        if (self.last_alert is None) or (
                                (datetime.datetime.utcnow() - self.last_alert).total_seconds() > self.alert_telegram_each):
                            self.last_alert = datetime.datetime.utcnow()
                           # cv2.imwrite("img.jpg", frame_cap)
                            results.save('./img.jpg')
                            # thực hiện việc đăng hình ảnh và gửi thông báo
                            executor.submit(self.handle_alert, "./img.jpg", self.camera_index + 1)

                    annotated_frame = results.plot() if results else frame_cap
                    self.ImageUpdate.emit(annotated_frame)
        Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.quit()

    def playWarningSound(self):
         playsound('./resources/warning.wav')

    def handle_alert(self, image_path, camera_index):
        try:
            # Upload ảnh lên Imgur
            url = uploadImageToImgur(image_path)
            # Send a notification
            sendMessage(camera_index, url)
        except Exception as e:
            print(f"An error occurred while handling alert: {e}")

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
