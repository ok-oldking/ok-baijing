import threading
import time
from typing import List

from autoui.capture.WindowsGraphicsCaptureMethod import BaseCaptureMethod
from autoui.scene.Scene import Scene


class TaskExecutor:
    tasks = []
    scenes: List[Scene] = []
    current_scene: Scene | None = None

    def __init__(self, method: BaseCaptureMethod, target_fps=10, exit_event=threading.Event()):
        self.method = method
        self.target_delay = 1.0 / target_fps
        self.thread = threading.Thread(target=self.execute)
        self.exit_event = exit_event
        self.thread.start()

    def wait_fps(self, start):
        cost = time.time() - start
        if cost < self.target_delay:
            # print(f"TaskExecutor:cost {cost} lower than target {self.target_delay}, sleeping")
            self.exit_event.wait(self.target_delay - cost)

    def next_frame(self):
        while not self.exit_event.is_set():
            frame = self.method.get_frame()
            if frame is not None:
                return frame

    def execute(self):
        print(f"execute")
        while not self.exit_event.is_set():
            start = time.time()
            frame = self.method.get_frame()
            if frame is not None:
                self.detect_scene(frame)
                if self.current_scene is not None:
                    task_executed = 0
                    for task in self.tasks:
                        task.run_frame(self, self.current_scene, frame)
                        processing_time = time.time() - start
                        task_executed += 1
                        if processing_time > 0.2:
                            print(
                                f"{task.__class__.__name__} taking too long skip to next frame {processing_time} {task_executed} {len(self.tasks)}")
                            break
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
                    print(f"TaskExecutor: scene changed {scene.__class__.__name__}")
                    return
        if self.current_scene is not None:
            print(f"TaskExecutor: scene changed to None")
            self.current_scene = None

    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):
        self.thread.join()
