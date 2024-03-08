import numpy as np
from PySide6.QtCore import Signal, QObject


class Communicate(QObject):
    frame = Signal(np.ndarray)
    log = Signal(int, str)


communicate = Communicate()
