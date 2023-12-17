import threading
import cv2
import os
from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.save.PostProcessor import PostProcessor

class SaveMethodBase:

    def __init__(self, method : CaptureMethodBase, image_processor:PostProcessor = None):
        self.method = method
        self.image_processor = image_processor
        self.i = 1
        self.thread = threading.Thread(target=self.run)
        self.dir = "images"
        # Check if the directory exists, and create it if it doesn't
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)        
        self.thread.start()        
        self.exit_event = threading.Event()

    def save(self):
        frame, err = self.method.get_frame()
        print(f"self.save {frame is not None} {err}")        
        if frame is not None:
            if self.image_processor is not None:
                self.image_processor.process(frame)
            filename = f"{self.dir}/{self.i}.jpg"
            self.i += 1
            # Save the image
            cv2.imwrite(filename, frame)
    
    def run(self):
        print("Thread started")
        while not self.exit_event.is_set():
            # Do some work here
            # print("Thread is running...")
            self.exit_event.wait(1)  # Wait for 1 second or until the event is set
        print("Thread exiting")
    
    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):        
        self.thread.join()

