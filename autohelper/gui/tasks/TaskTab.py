from typing import List

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem

from autohelper.gui.Communicate import communicate
from autohelper.logging.Logger import get_logger
from autohelper.task.BaseTask import BaseTask

logger = get_logger(__name__)


class TaskTab(QWidget):
    def __init__(self, tasks: List[BaseTask]):
        super().__init__()

        self.mainLayout = QHBoxLayout(self)
        self.setLayout(self.mainLayout)
        self.tasks = tasks
        # Top row setup with horizontal splitter
        self.table_widget = QTableWidget()
        self.labels = ['Name', 'Status']
        self.table_widget.setRowCount(len(tasks))  # Adjust the row count to match the number of attributes
        self.table_widget.setColumnCount(len(self.labels))  # Name and Value
        self.table_widget.setHorizontalHeaderLabels(self.labels)
        self.create_table()
        self.update_table()
        communicate.tasks.connect(self.update_table)
        self.mainLayout.addWidget(self.table_widget)

    def create_table(self):
        for row, task in enumerate(self.tasks):
            for i in range(len(self.labels)):
                self.table_widget.setItem(row, i, QTableWidgetItem())

    def update_table(self):
        for row, task in enumerate(self.tasks):
            self.table_widget.item(row, 0).setText(task.name)
            status = task.get_status()
            self.table_widget.item(row, 1).setText(status)
            if status == "Running":
                self.table_widget.item(row, 1).setBackground(QColor("green"))
            elif status == "Disabled":
                self.table_widget.item(row, 1).setBackground(QColor("red"))
            else:
                self.table_widget.item(row, 1).setBackground(QColor(0, 0, 0, 0))
