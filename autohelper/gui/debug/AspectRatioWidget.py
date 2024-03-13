from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy


class AspectRatioWidget(QWidget):
    def __init__(self, child_widget, aspect_ratio=16 / 9, parent=None):
        super(AspectRatioWidget, self).__init__(parent)
        self.aspect_ratio = aspect_ratio
        self.child_widget = child_widget
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(child_widget)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        new_width = h * self.aspect_ratio
        new_height = w / self.aspect_ratio
        if new_height > h:
            self.child_widget.setFixedSize(QSize(new_width, h))
        else:
            self.child_widget.setFixedSize(QSize(w, new_height))
        super().resizeEvent(event)

    def sizeHint(self):
        # Provide a default size hint that respects the aspect ratio
        height = 200  # Default height
        return QSize(int(height * self.aspect_ratio), height)

    def set_ratio(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio
