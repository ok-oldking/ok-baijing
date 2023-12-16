import threading
import time
import cv2
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.save.SaveMethodBase import SaveMethodBase
from pynput import keyboard, mouse

class SaveByKeyPress(SaveMethodBase):

    def __init__(self, method : "CaptureMethodBase", capture_key = "c"):
        super().__init__(method) 
        self.capture_key = capture_key
        listener = keyboard.Listener(on_release=self.on_key_release)
        listener.start()

    def on_key_release(self, key):
        print(f'Key {key} released')
        try:
            if key.char == self.capture_key:
                print(f'is capture_key call save()')
                self.save()
            elif key.char == 'x':
                self.stop()
                return False
        except AttributeError as e:
            print(f'AttributeError {e} key {key} released')