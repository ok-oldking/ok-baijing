from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QTableWidget, QToolTip


class TooltipTableWidget(QTableWidget):

    def __init__(self, width_percentages=None):
        super().__init__()
        self.verticalHeader().setVisible(False)
        self.width_percentages = width_percentages

    def setItem(self, row, column, item):
        super().setItem(row, column, item)

    def resizeEvent(self, event):
        if self.width_percentages is not None:
            width = self.width() - self.verticalScrollBar().width()
            for i, percentage in enumerate(self.width_percentages):
                self.setColumnWidth(i, int(width * percentage))
        super().resizeEvent(event)

    def viewportEvent(self, event):
        if event.type() == QEvent.ToolTip:
            pos = event.pos()
            item = self.itemAt(pos)
            if item:
                if self.visualItemRect(item).width() < self.fontMetrics().horizontalAdvance(item.text()):
                    QToolTip.showText(event.globalPos(), item.text(), self)
                else:
                    QToolTip.hideText()
                return True
        return super().viewportEvent(event)
