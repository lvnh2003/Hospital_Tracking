import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

class UpdateForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.train_id = None
        # load ui from ui folder
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("Update Form")

        # Thêm các phần tử giao diện và xử lý sự kiện ở đây (nếu cần)

        self.show()

    def closeEvent(self, event):
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    update_form = UpdateForm()
    sys.exit(app.exec_())
