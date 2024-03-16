import numpy as np
from PySide6.QtCore import Signal, QObject


class Communicate(QObject):
    frame = Signal(np.ndarray)
    log = Signal(int, str)
    fps = Signal(int)
    frame_time = Signal(int)
    scene = Signal(str)
    draw_box = Signal(str, list)
    tasks = Signal()
    window = Signal(int, int, int, int, int, int, int, float)


communicate = Communicate()
