import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QEvent

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
        self.btn_Start_1.clicked.connect(self.start_clicked)
        self.btn_Start_1.hide()
        self.label_1.installEventFilter(self)

        self.btn_Start_2.clicked.connect(self.start_clicked)
        self.btn_Start_2.hide()
        self.label_2.installEventFilter(self)

        self.btn_Start_3.clicked.connect(self.start_clicked)
        self.btn_Start_3.hide()
        self.label_3.installEventFilter(self)

        self.btn_Start_4.clicked.connect(self.start_clicked)
        self.btn_Start_4.hide()
        self.label_4.installEventFilter(self)

        self.btn_Start_5.clicked.connect(self.start_clicked)
        self.btn_Start_5.hide()
        self.label_5.installEventFilter(self)

        self.btn_Start_6.clicked.connect(self.start_clicked)
        self.btn_Start_6.hide()
        self.label_6.installEventFilter(self)

        self.show()

    def eventFilter(self, obj, event):
        if obj is self.label_1:
            if event.type() == QEvent.Enter:
                self.btn_Start_1.show()  # Show the button when mouse enters the widget
            elif event.type() == QEvent.Leave:
                self.btn_Start_1.hide()  # Hide the button when mouse leaves the widget
        elif obj is self.label_2:
            if event.type() == QEvent.Enter:
                self.btn_Start_2.show()  # Show the button when mouse enters the widget
            elif event.type() == QEvent.Leave:
                self.btn_Start_2.hide()  # Hide the button when mouse leaves the widget
        elif obj is self.label_3:
            if event.type() == QEvent.Enter:
                self.btn_Start_3.show()  # Show the button when mouse enters the widget
            elif event.type() == QEvent.Leave:
                self.btn_Start_3.hide()  # Hide the button when mouse leaves the widget
        elif obj is self.label_4:
            if event.type() == QEvent.Enter:
                self.btn_Start_4.show()  # Show the button when mouse enters the widget
            elif event.type() == QEvent.Leave:
                self.btn_Start_4.hide()  # Hide the button when mouse leaves the widget
        elif obj is self.label_5:
            if event.type() == QEvent.Enter:
                self.btn_Start_5.show()  # Show the button when mouse enters the widget
            elif event.type() == QEvent.Leave:
                self.btn_Start_5.hide()  # Hide the button when mouse leaves the widget
        elif obj is self.label_6:
            if event.type() == QEvent.Enter:
                self.btn_Start_6.show()  # Show the button when mouse enters the widget
            elif event.type() == QEvent.Leave:
                self.btn_Start_6.hide()  # Hide the button when mouse leaves the widget
        return super().eventFilter(obj, event)

    def start_clicked(self):
        print("Start button clicked!")
        # Add your start button functionality here
       
    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_form = UpdateForm()
    sys.exit(app.exec_())
