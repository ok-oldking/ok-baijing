from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGridLayout, QSplitter, QTextEdit

from autoui.gui.debug.FrameWidget import FrameWidget
from autoui.gui.debug.LoggerWidget import LoggerWidget


class DebugTab(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        # Top row setup with horizontal splitter
        self.topSplitter = QSplitter(Qt.Horizontal)
        self.topSplitter.setMinimumHeight(300)
        self.leftTextEdit = QTextEdit()
        self.leftTextEdit.setPlainText("Left Pane\nTry resizing me!")
        self.leftTextEdit.setFixedWidth(200)
        self.frame_widget = FrameWidget()
        self.rightTextEdit = FrameWidget()
        self.topSplitter.addWidget(self.leftTextEdit)
        self.topSplitter.addWidget(self.rightTextEdit)

        # Bottom row setup
        self.bottomTextEdit = LoggerWidget()

        # Main splitter to handle top and bottom rows
        self.mainSplitter = QSplitter(Qt.Vertical)
        self.mainSplitter.addWidget(self.topSplitter)
        self.mainSplitter.addWidget(self.bottomTextEdit)

        # Add the main splitter to the layout
        self.mainLayout.addWidget(self.mainSplitter, 0, 0)
