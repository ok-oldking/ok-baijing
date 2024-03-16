from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget, QVBoxLayout

from autohelper.gui.Communicate import communicate
from autohelper.gui.debug.FrameWidget import FrameWidget
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class Communicate(QObject):
    speak = Signal(str)


class OverlayWindow(QWidget):
    def __init__(self, exit_event):
        super().__init__()
        self.exit_event = exit_event
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint)  # Make the window frameless
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowTransparentForInput, True)
        self.setWindowFlag(Qt.Tool)
        self.visible = False
        communicate.window.connect(self.update_overlay)
        layout = QVBoxLayout(self)
        # Create a child widget, in this case, a QLabel
        childWidget = FrameWidget(parent=self)

        # Add the child widget to the layout
        layout.addWidget(childWidget)

        # Set the layout on the parent widget
        self.setLayout(layout)

    def update_overlay(self, visible, x, y, border, title_height, width, height, scaling):
        logger.debug(f'update_overlay: {visible}')
        self.visible = visible
        self.setGeometry(x + border, y + title_height, width, height)
        self.update()

    def paintEvent(self, event):
        if self.visible:
            painter = QPainter(self)

            # Set up the painter to draw the border
            pen = QPen(QColor(255, 0, 0, 255))  # Solid red color for the border
            pen.setWidth(5)  # Set the border width
            painter.setPen(pen)

            # Draw the border around the widget
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
