import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class DeleteConfirmationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Confirmation")
        self.setGeometry(800, 500, 300, 100)

        # Tạo layout chính
        layout = QVBoxLayout()

        # Tạo và thêm nhãn vào layout
        label = QLabel("Are you sure you want to delete x?")
        layout.addWidget(label)

        # Tạo layout cho các nút
        button_layout = QHBoxLayout()

        # Tạo và thêm nút Đồng ý
        confirm_button = QPushButton("Yes")
        confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(confirm_button)

        # Tạo và thêm nút Hủy
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        # Thêm layout các nút vào layout chính
        layout.addLayout(button_layout)

        self.setLayout(layout)