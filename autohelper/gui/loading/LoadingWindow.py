from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from autohelper.gui.Communicate import communicate


class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Loading...')
        self.setGeometry(100, 100, 200, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.Tool)
        layout = QVBoxLayout()

        self.label = QLabel('Loading, please wait...')
        layout.addWidget(self.label)
        communicate.loading_progress.connect(self.update_progress)
        self.setLayout(layout)
        self.update_progress("Loading, please wait...")

    def update_progress(self, message):
        self.label.setText(message)
