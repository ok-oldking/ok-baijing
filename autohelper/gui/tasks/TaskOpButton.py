from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton

from autohelper.logging.Logger import get_logger
from autohelper.task.BaseTask import BaseTask

logger = get_logger(__name__)


class TaskOpButton(QPushButton):
    def __init__(self, task: BaseTask):
        super().__init__("Enable")
        self.setCheckable(True)
        self.clicked.connect(self.toggle_text)
        self.task = task

    def update_task(self, task: BaseTask):
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
        communicate.tasks.emit()
