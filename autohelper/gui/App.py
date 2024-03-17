import sys

from PySide6.QtCore import QTranslator, QLocale, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

from autohelper.capture.HwndWindow import HwndWindow
from autohelper.gui.MainWindow import MainWindow
from autohelper.gui.loading.LoadingWindow import LoadingWindow
from autohelper.gui.overlay.OverlayWindow import OverlayWindow
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class App:
    def __init__(self, title="AutoUI", icon=None, tasks=None, overlay=False, hwnd_window: HwndWindow = None,
                 exit_event=None):
        super().__init__()
        self.loading_window = None
        self.overlay_window = None
        self.main_window = None
        self.exit_event = exit_event
        self.app = QApplication(sys.argv)
        self.app.setStyle(QStyleFactory.create("Fusion"))
        self.tasks = tasks
        self.title = title
        self.icon = icon
        self.hwnd_window = hwnd_window
        self.overlay = overlay

    def show_loading(self):
        self.loading_window = LoadingWindow()
        self.loading_window.show()

    def center_window(self, window):
        screen = self.app.primaryScreen()
        size = screen.size()
        # Calculate half the screen size
        half_screen_width = size.width() / 2
        half_screen_height = size.height() / 2

        window.move(half_screen_width / 2, half_screen_height / 2)

    def start(self):
        self.loading_window.close()
        self.main_window = MainWindow(self.tasks, exit_event=self.exit_event)
        self.main_window.setWindowTitle(self.title)  # Set the window title here
        if self.icon is not None:
            self.main_window.setWindowIcon(QIcon(self.icon))
        if self.overlay and self.hwnd_window is not None:
            self.overlay_window = OverlayWindow(self.hwnd_window)

        locale = QLocale.system().name()
        translator = QTranslator(self.app)
        if translator.load(f"your_application_{locale}", "path/to/translations"):
            self.app.installTranslator(translator)
        else:
            logger.debug(f"No translation available for {locale}, falling back to English/default.")

        screen = self.app.primaryScreen()
        size = screen.size()
        # Calculate half the screen size
        half_screen_width = size.width() / 2
        half_screen_height = size.height() / 2

        # Resize the window to half the screen size
        size = QSize(half_screen_width, half_screen_height)
        self.main_window.resize(size)
        self.main_window.setMinimumSize(size)

        # Optional: Move the window to the center of the screen

        self.main_window.show()
        sys.exit(self.app.exec())
