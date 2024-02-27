import threading
import time

from autoui.capture.windows.WindowsGraphicsCaptureMethod import BaseCaptureMethod
from autoui.interaction.BaseInteraction import BaseInteraction
from autoui.scene.Scene import Scene
from autoui.stats.StreamStats import StreamStats


class TaskExecutor:
    current_scene: Scene | None = None
    frame_stats = StreamStats()

    def __init__(self, method: BaseCaptureMethod, interaction: BaseInteraction, overlay=None, target_fps=10,
                 wait_scene_timeout=10,
                 exit_event=threading.Event(), tasks=[], scenes=[]):
        self.interaction = interaction
        self.method = method
        self.wait_scene_timeout = wait_scene_timeout
        self.target_delay = 1.0 / target_fps
        self.thread = threading.Thread(target=self.execute)
        self.exit_event = exit_event
        self.thread.start()
        self.overlay = overlay
        self.tasks = tasks
        self.scenes = scenes
        for task in self.tasks:
            task.executor = self

    def wait_fps(self, start):
        cost = time.time() - start
        if cost < self.target_delay:
            # print(f"TaskExecutor:cost {cost} lower than target {self.target_delay}, sleeping")
            self.sleep(self.target_delay - cost)

    def next_frame(self):
        while not self.exit_event.is_set():
            frame = self.method.get_frame()
            if frame is not None:
                return frame

    def sleep(self, timeout):
        """
        Sleeps for the specified timeout, checking for an exit event every 100ms, with adjustments to prevent oversleeping.

        :param timeout: The total time to sleep in seconds.
        """
        start_time = time.time()
        end_time = start_time + timeout
        self.frame_stats.add_sleep(timeout)
        while time.time() < end_time:
            if self.exit_event.is_set():
                print("Exit event set. Exiting early.")
                return
            remaining = end_time - time.time()
            time.sleep(min(0.1, remaining))  # Sleep for 100ms or the remaining time, whichever is smaller

    def wait_scene(self, scene_type, time_out=0):
        self.current_scene = None
        start = time.time()
        if time_out == 0:
            time_out = self.wait_scene_timeout
        while not self.exit_event.is_set():
            frame = self.method.get_frame()
            if frame is not None:
                scene = self.detect_scene(frame, scene_type)
                self.add_frame_stats()
                if scene is not None:
                    return scene, frame
            self.wait_fps(start)
            if time.time() - start > time_out:
                print(f"TaskExecutor: wait_scene timeout {scene_type} {time_out} seconds")
                break
        return None, None

    def reset_scene(self):
        self.current_scene = None

    def execute(self):
        print(f"TaskExecutor: start execute")
        try:
            while not self.exit_event.is_set():
                frame = self.method.get_frame()
                start = time.time()
                if frame is not None:
                    self.detect_scene(frame)
                    # print(f"detect_scene: {self.current_scene.__class__.__name__} {(time.time() - start)}")
                    if self.current_scene is not None:
                        task_executed = 0
                        for task in self.tasks:
                            task.run_frame()
                            processing_time = time.time() - start
                            task_executed += 1
                            if processing_time > 0.2:
                                print(
                                    f"{task.__class__.__name__} taking too long skip to next frame {processing_time} {task_executed} {len(self.tasks)}")
                                self.add_frame_stats()
                                break
                    self.add_frame_stats()
                self.wait_fps(start)
        except Exception as e:
            # Handle the exception or store it for later use
            print(f"TaskExecutor Thread Exception : {e}")
            self.exit_event.set()

    def add_frame_stats(self):
        if self.overlay:
            self.frame_stats.add_frame()
            mean = self.frame_stats.mean()
            if mean > 0:
                # print(f"frame_stats.mean(): {mean}, fps:{round(1000 / mean)}")
                self.overlay.draw_text("fps", 0.3, 0.01,
                                       f"Scene:{self.current_scene.__class__.__name__} FrameTime:{mean}, FPS:{round(1000 / mean)}")

    def detect_scene(self, frame, scene_type=None):
        if self.current_scene is not None:
            # detect the last scene optimistically
            if self.current_scene.detect(frame):
                return
        for scene in self.scenes:
            if scene_type is not None and isinstance(scene, scene_type) == False:
                continue
            if scene != self.current_scene:
                if scene.detect(frame):
                    self.current_scene = scene
                    print(f"TaskExecutor: scene changed {scene.__class__.__name__}")
                    return scene
        if self.current_scene is not None:
            print(f"TaskExecutor: scene changed to None")
            self.current_scene = None
        return self.current_scene

    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):
        self.thread.join()
