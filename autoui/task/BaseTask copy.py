import threading
from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.overlay.BaseOverlay import BaseOverlay

class TaskExecutor:

    tasks = []

    def __init__(self, method : CaptureMethodBase, overlay:BaseOverlay = None, wait_time = 1):
        self.method = method
        self.overlay = overlay
        self.wait_time = wait_time
        self.thread = threading.Thread(target=self.execute)        
        self.exit_event = threading.Event()   
        self.thread.start()         
    
    def execute(self):
        print(f"execute")
        while not self.exit_event.is_set():
            print(f"execute1")
            if not self.paused:
                print(f"execute2")
                self.run()
                print(f"execute3")
            self.exit_event.wait(self.wait_time)  # Wait for 1 second or until the event is set

    def run(self):
        pass

    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):        
        self.thread.join()

