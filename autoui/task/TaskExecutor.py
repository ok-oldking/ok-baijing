import threading
import time
from cv2.typing import MatLike
from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase

class TaskExecutor:

    tasks = []
    last_frame = None

    def __init__(self, method : CaptureMethodBase, target_fps = 10):
        self.method = method
        self.thread = threading.Thread(target=self.execute)        
        self.exit_event = threading.Event()   
        self.thread.start()  
        self.capture_thread = threading.Thread(target=self.capture_frame)        
        self.capture_thread.start() 
        self.target_delay = 1.0/target_fps   
        # self.frame = None    
    
    def capture_frame(self):
        while not self.exit_event.is_set():
            start = time.time()
            frame = self.method.get_frame()                    
            if frame is not None:
               if hasattr(self.tasks[0].interaction.overlay,"draw_image"):
                    self.tasks[0].interaction.overlay.draw_image(frame) 
               self.last_frame = frame
            # else:
            #     print("TaskExecutor.capture_frame:frame is null")    # frame.close()            
            cost = time.time() - start
            if cost < self.target_delay:
                # print(f"TaskExecutor:cost {cost} lower than target {self.target_delay}, sleeping")
                self.exit_event.wait(self.target_delay - cost)
            elif self.exit_event.is_set():
                print(f"TaskExecutor: exit_event")
                return

    def execute(self):
        print(f"execute")
        while not self.exit_event.is_set():
            frame = self.last_frame
            self.last_frame = None
            if frame is not None:                     
                for task in self.tasks:
                    task.run_frame(frame)
                    if self.last_frame is not None:
                        # print("new frame arrived break to next frame")
                        break            
   
    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):        
        self.thread.join()

