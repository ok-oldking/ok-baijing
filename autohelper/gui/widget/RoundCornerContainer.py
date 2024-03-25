from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame, QSizePolicy


class RoundCornerContainer(QFrame):
    def __init__(self, title, child=None, parent=None):
        super(RoundCornerContainer, self).__init__(parent)

        # Set the layout
        layout = QVBoxLayout(self)
        self.title_label = QLabel(title)
        self.title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(self.title_label)
        if child is not None:
            child.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            layout.addWidget(child)

        self.setLayout(layout)

        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(2)

        color = self.get_palette_color(QPalette.Base)
        self.setStyleSheet(f"background-color:{color};")

    def get_palette_color(self, palette_color):
        palette = self.palette()
        return color_to_hex(palette.color(palette_color))


def color_to_hex(color):
    """Converts a QColor object to a hex string representation.

    Args:
        color: The QColor object to convert.

    Returns:
        A string representing the hex code of the color (e.g., "#FF0000" for red).
    """
    red = color.red()
    green = color.green()
    blue = color.blue()
    hex_color = f"#{red:02X}{green:02X}{blue:02X}"
    return hex_color

# Usage:
# widget = RoundCornerContainer("Title")
# widget.show()
