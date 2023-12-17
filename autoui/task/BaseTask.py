import threading
from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase

class BaseTask:

    paused = False

    def __init__(self, method : CaptureMethodBase, wait_time = 1):
        self.method = method
        self.wait_time = wait_time
        self.thread = threading.Thread(target=self.execute)        
        self.exit_event = threading.Event()   
        self.thread.start()         
    
    def execute(self):
        try:
            while not self.exit_event.is_set():
                if not self.paused:
                    self.run()
                self.exit_event.wait(self.wait_time)  # Wait for 1 second or until the event is set
        except KeyboardInterrupt:
            print("Received Ctrl+C... Initiating shutdown.")
            self.exit_event.set()

    def run(self):
        pass

    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):        
        self.thread.join()

