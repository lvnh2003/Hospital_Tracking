import cv2
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

from detect_utils import FallDetect
from func import Function_TXT

fall_detect = FallDetect(conf=0.7)
func_txt = Function_TXT()
# class thread để gửi frame cho label
class ThreadClassDetect(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)
    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index
        self.ThreadActive = False
        self.fall_detect = fall_detect
        self.cameras = func_txt.getCameras()

    def run(self):
        Capture = cv2.VideoCapture(self.cameras[self.camera_index])
        if not Capture.isOpened():
            print(f"Error: Camera index {self.camera_index} could not be opened.")
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
                annotated_frame = results.plot() if results else frame_cap
                self.ImageUpdate.emit(annotated_frame)
        Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.quit()

class ThreadClass(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)
    def __init__(self, camera):
        super().__init__()
        self.ThreadActive = False
        self.camera = camera

    def run(self):
        Capture = cv2.VideoCapture(self.camera)

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
        self.terminate()
