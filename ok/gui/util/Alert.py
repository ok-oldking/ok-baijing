from PySide6.QtWidgets import QMessageBox

import ok


def show_alert(title, message):
    # Create a QMessageBox
    msg = QMessageBox()

    # Set the title and message
    msg.setWindowTitle(title)
    msg.setText(message)

    msg.setWindowIcon(ok.gui.app.icon)

    # Add a confirm button
    msg.setStandardButtons(QMessageBox.Ok)

    # Show the message box
    msg.exec()
