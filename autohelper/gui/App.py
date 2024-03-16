import sys

from PySide6.QtCore import QTranslator, QLocale, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

from autohelper.capture.HwndWindow import HwndWindow
from autohelper.gui.MainWindow import MainWindow
from autohelper.gui.overlay.OverlayWindow import OverlayWindow
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class App:
    def __init__(self, title="AutoUI", icon=None, tasks=None, overlay=False, hwnd_window: HwndWindow = None,
                 exit_event=None):
        super().__init__()
        self.exit_event = exit_event
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow(tasks, exit_event=self.exit_event)
        self.main_window.setWindowTitle(title)  # Set the window title here
        if icon is not None:
            self.main_window.setWindowIcon(QIcon(icon))
        if overlay:
            self.overlay_window = OverlayWindow(hwnd_window)

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
            logger.debug(f"No translation available for {locale}, falling back to English/default.")
        size = QSize(half_screen_width, half_screen_height)
        self.main_window.resize(size)
        self.main_window.setMinimumSize(size)

        # Optional: Move the window to the center of the screen
        self.main_window.move(half_screen_width / 2, half_screen_height / 2)
        translator = QTranslator(self.app)
        self.main_window.show()
        sys.exit(self.app.exec())
