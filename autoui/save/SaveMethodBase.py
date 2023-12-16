import threading
import cv2
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase

class SaveMethodBase:

    def __init__(self, method : "CaptureMethodBase"):
        self.method = method
        self.i = 1
        self.thread = threading.Thread(target=self.run)
        self.thread.start()        
        self.exit_event = threading.Event()

    def save(self):
        frame, err = self.method.get_frame()
        print(f"self.save {frame is not None} {err}")
        if frame is not None:
            filename = f"images/{self.i}.jpg"
            self.i += 1
            # Save the image
            cv2.imwrite(filename, frame)
    
    def run(self):
        print("Thread started")
        while not self.exit_event.is_set():
            # Do some work here
            print("Thread is running...")
            self.exit_event.wait(1)  # Wait for 1 second or until the event is set
        print("Thread exiting")
    
    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):        
        self.thread.join()
