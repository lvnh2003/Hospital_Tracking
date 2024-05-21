import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QEvent, QTimer

class UpdateForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.train_id = None
        # load ui from ui folder
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("Update Form")

        self.centralWidget().installEventFilter(self)  # Giả sử label nằm trong centralWidget
        # Thêm các phần tử giao diện và xử lý sự kiện ở đây (nếu cần)
        # Sự kiện click + ẩn button
        self.initUI()

        self.show()

    def initUI(self):
        self.buttons = []
        self.labels = []
        for i in range(1, 7):
            button = getattr(self, f'btn_Start_{i}')
            button.clicked.connect(self.start_clicked)
            button.hide()
            self.buttons.append(button)
            
            label = getattr(self, f'label_{i}')
            label.installEventFilter(self)
            self.labels.append(label)

        self.timers = [QTimer(self) for _ in range(6)]
        for timer in self.timers:
            timer.setSingleShot(True)
            timer.timeout.connect(self.hide_buttons)

    def eventFilter(self, obj, event):
        for i, label in enumerate(self.labels):
            if obj is label:
                if event.type() == QEvent.Enter:
                    self.buttons[i].show()  
                    self.timers[i].stop() 
                elif event.type() == QEvent.Leave:
                    self.timers[i].start(20) # delay trước khi ẩn nút
        return super().eventFilter(obj, event)

    def hide_buttons(self):
        for button in self.buttons:
            button.hide()

    def start_clicked(self):
        print("Start button clicked!")
        # Add your start button functionality here
       
    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_form = UpdateForm()
    sys.exit(app.exec_())
