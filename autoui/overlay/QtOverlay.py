import sys
from PyQt5 import QtWidgets, QtCore
from typing import List
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.overlay.BaseOverlay import BaseOverlay
from autoui.feature.Box import Box

class QtOverlay(BaseOverlay):
    
    def __init__(self, method: CaptureMethodBase):
        super().__init__()
        self.method = method
        self.uiDict = {}
        self.app = QtWidgets.QApplication(sys.argv)
        # Create a window
        self.window = QtWidgets.QWidget()
        self.window.setWindowTitle("QtOverlay")
        self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput)
        self.window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Create a layout and canvas
        self.layout = QtWidgets.QVBoxLayout()
        self.canvas = QtWidgets.QLabel()
        self.layout.addWidget(self.canvas)
        self.window.setLayout(self.layout)

        # Connect to method's window change listener
        method.add_window_change_listener(self)

    def draw_boxes(self, key: str, boxes: List[Box], outline: str):
        # dpi = 2
        # Clear existing drawings
        self.canvas.clear()
        
        # Reimplement drawing logic here...
        # Note: You'll need to use QPainter for drawing on the QLabel (canvas)

    def window_changed(self, visible, x, y, border, title_height, window_width, window_height):
        print(f"QtOverlay window_changed {round(window_width)}x{round(window_height)}+{round(x)}+{round((y+title_height))}")
        self.window.setGeometry(round(x), round((y + title_height)), round(window_width), round(window_height))
        if visible:
            self.window.show()
        else:
            self.window.hide()

    def start(self):
        self.window.show()
        sys.exit(self.app.exec_())

