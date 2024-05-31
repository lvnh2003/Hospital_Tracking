import torch
from ultralytics import YOLO
# get device for run program if gpu exist use gpu and else use cpu
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class FallDetect():
    def __init__(self, conf):
        self.conf = conf
        # base on model trained
        self.model = YOLO('./best.pt').float().to(device)

    def detect(self, frame):
        results = self.model(frame, conf=self.conf, verbose=False)
        return results[0] if len(results) > 0 else None
