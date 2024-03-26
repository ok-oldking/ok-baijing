import sys

from PySide6.QtCore import QTranslator, QLocale, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStyleFactory

from autohelper.capture.HwndWindow import HwndWindow
from autohelper.gui.Communicate import communicate
from autohelper.gui.MainWindow import MainWindow
from autohelper.gui.loading.LoadingWindow import LoadingWindow
from autohelper.gui.overlay.OverlayWindow import OverlayWindow
from autohelper.logging.Logger import get_logger

logger = get_logger(__name__)


class App:
    def __init__(self,
                 exit_event=None):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setStyle(QStyleFactory.create("Fusion"))
        self.overlay = False
        self.hwnd_window = None
        self.loading_window = None
        self.overlay_window = None
        self.main_window = None
        self.exit_event = exit_event
        communicate.init.connect(self.on_init)

    def show_loading(self):
        self.loading_window = LoadingWindow(self, self.exit_event)
        size = self.size_relative_to_screen(width=0.2, height=0.2)
        self.loading_window.resize(size)
        self.loading_window.setMinimumSize(size)
        self.center_window(self.loading_window)
        self.loading_window.show()

    def center_window(self, window):
        screen = self.app.primaryScreen()
        size = screen.size()
        # Calculate half the screen size
        half_screen_width = size.width() / 2
        half_screen_height = size.height() / 2

        window.move(half_screen_width / 2, half_screen_height / 2)

    def set(self, overlay=False, hwnd_window: HwndWindow = None, title="AutoUI", icon=None, tasks=None):
        self.tasks = tasks
        self.title = title
        self.icon = icon
        self.hwnd_window = hwnd_window
        self.overlay = overlay

    def on_init(self, done, message):
        if done:
            self.show_main_window()
        else:
            self.loading_window.update_progress(message)

    def show_main_window(self):
        self.loading_window.close()
        self.main_window = MainWindow(self.tasks, exit_event=self.exit_event)
        self.main_window.setWindowTitle(self.title)  # Set the window title here
        if self.icon is not None:
            self.main_window.setWindowIcon(QIcon(self.icon))
        if self.overlay and self.hwnd_window is not None:
            self.overlay_window = OverlayWindow(self.hwnd_window)

        locale = QLocale.system().name()
        translator = QTranslator(self.app)
        if translator.load(QLocale(), "myapp", "_", ":/i18n"):
            self.app.installTranslator(translator)
        else:
            logger.debug(f"No translation available for {locale}, falling back to English/default.")

        size = self.size_relative_to_screen(width=0.5, height=0.5)
        self.main_window.resize(size)
        self.main_window.setMinimumSize(size)

        # Optional: Move the window to the center of the screen

        self.main_window.show()

    def size_relative_to_screen(self, width, height):
        screen = self.app.primaryScreen()
        size = screen.size()
        # Calculate half the screen size
        half_screen_width = size.width() * width
        half_screen_height = size.height() * height
        # Resize the window to half the screen size
        size = QSize(half_screen_width, half_screen_height)
        return size

    def exec(self):
        sys.exit(self.app.exec())

    def quit(self):
        self.app.quit()
