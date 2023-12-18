import win32api
import win32con
import win32gui
import time
from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.overlay.BaseOverlay import BaseOverlay
from autoui.feature.Box import Box
from typing import List

class BaseTask:

    def __init__(self, interaction):
        self.interaction = interaction
    
    def run_frame(self, frame):
        pass

    

