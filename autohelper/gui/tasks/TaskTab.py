from typing import List

from PySide6.QtGui import QColor, QBrush
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
        self.labels = ['Name', 'Enabled', 'Running', 'Success', 'Error', 'Done']
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
            # self.table_widget.setItem(row, 0, QTableWidgetItem(task.name))
            if task.enabled:
                enabled = "Enabled"
            else:
                enabled = "Disabled"
            self.table_widget.item(row, 1).setText(enabled)
            if task.running:
                self.table_widget.item(row, 2).setBackground(QColor("green"))
                running = "Yes"
            else:
                running = "No"
                self.table_widget.item(row, 2).setBackground(QBrush())
            self.table_widget.item(row, 2).setText(running)
            self.table_widget.item(row, 3).setText(str(task.success_count))
            self.table_widget.item(row, 4).setText(str(task.error_count))
            if task.done:
                done = "Yes"
            else:
                done = "No"
            self.table_widget.item(row, 5).setText(done)
            # self.table_widget.setItem(row, 1, QTableWidgetItem(enabled))
            # self.table_widget.setItem(row, 2, QTableWidgetItem(str(task.success_count)))
            # self.table_widget.setItem(row, 3, QTableWidgetItem(str(task.error_count)))
            #
            # self.table_widget.setItem(row, 4, QTableWidgetItem(done))
