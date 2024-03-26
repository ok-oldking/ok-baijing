from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

from autohelper.gui.Communicate import communicate
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class LoadingWindow(QWidget):
    def __init__(self, app, exit_event):
        super().__init__()
        self.app = app
        self.exit_event = exit_event
        self.initUI()
        self.closed_by_finish_loading = False

    def initUI(self):
        self.setWindowTitle('Loading...')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.Tool)
        layout = QVBoxLayout()

        self.label = QLabel('Loading, please wait...')
        self.label.setAlignment(Qt.AlignCenter)  # Center the label
        layout.addWidget(self.label)
        communicate.loading_progress.connect(self.update_progress)
        self.setLayout(layout)
        self.update_progress("Loading, please wait...")

    def update_progress(self, message):
        self.label.setText(message)

    def close(self):
        self.closed_by_finish_loading = True
        super().close()

    def closeEvent(self, event):
        if self.closed_by_finish_loading:
            super().closeEvent(event)
        else:
            # Create a message box that asks the user if they really want to close the window
            reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.exit_event.set()
                event.accept()
                self.app.quit()
                logger.info("Window closed")  # Place your code here
            else:
                event.ignore()
