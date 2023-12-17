import threading
import time
import cv2
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase

class SaveByInterval:

    def __init__(self, method : "CaptureMethodBase", interval = 1):
        self.interval = interval
        self.method = method

    def save(self):
        for i in range(5):
            print(f"Log message {i}")
            frame, err = self.method.get_frame()
            if frame is not None:
                filename = f"images/{i}.jpg"
                # Save the image
                cv2.imwrite(filename, frame)
            time.sleep(1)
        self.method.close()
        print("Thread completed its execution.")

    def wait_until_done(self):
        # thread = threading.Thread(target=self.save)
        # thread.start()
        # thread.join()
        pass
