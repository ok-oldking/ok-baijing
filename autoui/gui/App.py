import sys

from PySide6.QtCore import QTranslator, QLocale, QSize
from PySide6.QtWidgets import QApplication, QStyleFactory

from autoui.gui.MainWindow import MainWindow


class App:
    def __init__(self, exit_event):
        super().__init__()
        self.exit_event = exit_event
        self.app = QApplication(sys.argv)
        self.ex = MainWindow(exit_event=self.exit_event)

    def start(self):
        self.app.setStyle(QStyleFactory.create("Fusion"))
        screen = self.app.primaryScreen()
        size = screen.size()

        # Calculate half the screen size
        half_screen_width = size.width() / 2
        half_screen_height = size.height() / 2

        # Resize the window to half the screen size

        locale = QLocale.system().name()
        translator = QTranslator(self.app)
        if translator.load(f"your_application_{locale}", "path/to/translations"):
            self.app.installTranslator(translator)
        else:
            print(f"No translation available for {locale}, falling back to English/default.")
        size = QSize(half_screen_width, half_screen_height)
        self.ex.resize(size)
        self.ex.setMinimumSize(size)

        # Optional: Move the window to the center of the screen
        self.ex.move(half_screen_width / 2, half_screen_height / 2)
        translator = QTranslator(self.app)
        self.ex.show()
        sys.exit(self.app.exec())
