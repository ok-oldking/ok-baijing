import threading
import time
from typing import List

from autoui.capture.WindowsGraphicsCaptureMethod import CaptureMethodBase
from autoui.scene.Scene import Scene


class TaskExecutor:
    tasks = []
    scenes: List[Scene] = []
    last_frame = None
    current_scene: Scene = None

    def __init__(self, method: CaptureMethodBase, target_fps=10):
        self.method = method
        self.target_delay = 1.0 / target_fps
        self.thread = threading.Thread(target=self.execute)
        self.exit_event = threading.Event()
        self.thread.start()
        self.capture_thread = threading.Thread(target=self.capture_frame)
        self.capture_thread.start()
        # self.frame = None    

    def capture_frame(self):
        while not self.exit_event.is_set():
            start = time.time()
            frame = self.method.get_frame()
            if frame is not None:
                if hasattr(self.tasks[0].interaction.overlay, "draw_image"):
                    self.tasks[0].interaction.overlay.draw_image(frame)
                self.last_frame = frame
                self.detect_scene(frame)
                self.wait_fps(start)

    def wait_fps(self, start):
        cost = time.time() - start
        if cost < self.target_delay:
            # print(f"TaskExecutor:cost {cost} lower than target {self.target_delay}, sleeping")
            self.exit_event.wait(self.target_delay - cost)

    def next_frame(self):
        while not self.exit_event.is_set():
            frame = self.last_frame
            self.last_frame = None
            if frame is not None:
                return frame

    def execute(self):
        print(f"execute")
        while not self.exit_event.is_set():
            start = time.time()
            if self.current_scene is not None:
                frame = self.last_frame
                for task in self.tasks:
                    if self.last_frame is not None:
                        frame = self.last_frame
                    self.last_frame = None
                    if frame is not None:
                        task.run_frame(self, self.current_scene, frame)
                print(f"frame time {time.time() - start}")
            self.wait_fps(start)

    def detect_scene(self, frame):
        if self.current_scene is not None:
            # detect the last scene optimistically
            if self.current_scene.detect(frame):
                return
        for scene in self.scenes:
            if scene != self.current_scene:
                if scene.detect(frame):
                    self.current_scene = scene
                    print(f"scene changed {scene.__class__.__name__}")
                    return

    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):
        self.thread.join()
