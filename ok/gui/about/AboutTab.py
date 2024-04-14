from PySide6.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class AboutTab(QWidget):
    def __init__(self, text=""):
        super().__init__()
        layout = QVBoxLayout()

        # Create a QTextEdit instance
        text_edit = QTextEdit()
        text_edit.setHtml(text)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)

        # Set the layout on the widget
        self.setLayout(layout)
