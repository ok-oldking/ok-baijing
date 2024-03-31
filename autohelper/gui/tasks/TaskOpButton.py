from PySide6.QtCore import Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton

from autohelper.gui.Communicate import communicate
from autohelper.logging.Logger import get_logger
from autohelper.task.BaseTask import BaseTask

logger = get_logger(__name__)


class TaskOpButton(QPushButton):
    def __init__(self, row, task: BaseTask):
        super().__init__("Enable")
        self.row = row
        self.task = task
        self.setCheckable(True)
        self.clicked.connect(self.toggle_text)
        communicate.task.connect(self.update_task)
        self.update_task(row, task)

    def update_task(self, row, task: BaseTask):
        if row == self.row:
            if task.enabled:
                self.setText("Enable")
            else:
                self.setText("Disable")

    @Slot()
    def toggle_text(self):
        if self.isChecked():
            self.task.enable()
        else:
            self.task.disable()

    def start_animation(self):
        self.animation.setStartValue(QColor(0, 0, 0))
        self.animation.setEndValue(QColor(255, 255, 255))
        self.animation.setDuration(1000)
        self.animation.start()
