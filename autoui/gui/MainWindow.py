from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QMessageBox, QTabWidget

from autoui.gui.TabTitles import TabContent
from autoui.gui.debug.DebugTab import DebugTab


class Communicate(QObject):
    speak = Signal(str)


class MainWindow(QTabWidget):
    def __init__(self, exit_event):
        super().__init__()
        self.exit_event = exit_event
        self.initUI()
        self.setWindowTitle("Close Event Example")
        self.setTabPosition(QTabWidget.West)
        # self.setTabBar(QTabBar())
        self.comm = Communicate()
        self.comm.speak.connect(self.say_hello)

    def initUI(self):
        debug_tab = DebugTab()

        self.addTab(TabContent("Home"), "Home")
        self.addTab(debug_tab, "Debug")
        # ... Add other tabs similarly

        # Styling the tabs and content if needed, for example:
        self.setStyleSheet("""
                    QTabWidget::tab-bar {
                        alignment: center;
                    }
                    QTabBar::tab {
                        background: #333;
                        color: white;
                        border-radius: 5px;
                        padding: 10px;
                    }
                    QTabBar::tab:selected {
                        background: #555;
                        font-weight: bold;
                    }
                    QWidget {
                        background-color: #222;
                        color: #ddd;
                    }
                """)

    @Slot(str)
    def say_hello(self, message):
        print(message)

    def btn_clicked(self):
        self.comm.speak.emit("Hello, PySide6 with parameters!")

    def closeEvent(self, event):
        # Create a message box that asks the user if they really want to close the window
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.exit_event.set()
            event.accept()
            print("Window closed")  # Place your code here
        else:
            event.ignore()
