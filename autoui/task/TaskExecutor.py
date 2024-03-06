import threading
import time
import traceback

from autoui.capture.windows.WindowsGraphicsCaptureMethod import BaseCaptureMethod
from autoui.interaction.BaseInteraction import BaseInteraction
from autoui.scene.Scene import Scene
from autoui.stats.StreamStats import StreamStats


class TaskExecutor:
    current_scene: Scene | None = None
    last_scene: Scene | None = None
    frame_stats = StreamStats()
    frame = None

    def __init__(self, method: BaseCaptureMethod, interaction: BaseInteraction, overlay=None, target_fps=10,
                 wait_until_timeout=10, wait_until_before_delay=1, wait_until_check_delay=1,
                 exit_event=threading.Event(), tasks=[], scenes=[]):
        self.interaction = interaction
        self.wait_until_check_delay = wait_until_check_delay
        self.wait_until_before_delay = wait_until_before_delay
        self.method = method
        self.wait_scene_timeout = wait_until_timeout
        self.target_delay = 1.0 / target_fps
        self.exit_event = exit_event
        self.overlay = overlay
        self.tasks = tasks
        self.scenes = scenes
        for scene in self.scenes:
            scene.executor = self
        for task in self.tasks:
            task.executor = self
        self.thread = threading.Thread(target=self.execute)
        self.thread.start()

    def wait_fps(self, start):
        cost = time.time() - start
        if cost < self.target_delay:
            # print(f"TaskExecutor:cost {cost} lower than target {self.target_delay}, sleeping")
            self.sleep(self.target_delay - cost)

    def next_frame(self):
        self.reset_scene()
        start = time.time()
        while not self.exit_event.is_set():
            self.frame = self.method.get_frame()
            if self.frame is not None:
                return self.frame
            time.sleep(0.01)
            if time.time() - start > self.wait_scene_timeout:
                return None

    def sleep(self, timeout):
        """
        Sleeps for the specified timeout, checking for an exit event every 100ms, with adjustments to prevent oversleeping.

        :param timeout: The total time to sleep in seconds.
        """
        self.frame_stats.add_sleep(timeout)
        end_time = time.time() + timeout
        while True:
            if self.exit_event.is_set():
                print("Exit event set. Exiting early.")
                return
            remaining = end_time - time.time()
            if remaining <= 0:
                return
            time.sleep(min(0.1, remaining))  # Sleep for 100ms or the remaining time, whichever is smaller

    def wait_scene(self, scene_type, time_out, pre_action, post_action):
        return self.wait_condition(lambda: self.detect_scene(scene_type), time_out, pre_action, post_action)

    def wait_condition(self, condition, time_out, pre_action, post_action):
        self.reset_scene()
        self.sleep(self.wait_until_before_delay)
        start = time.time()
        if time_out == 0:
            time_out = self.wait_scene_timeout
        while not self.exit_event.is_set():
            if pre_action is not None:
                pre_action()
            self.frame = self.next_frame()
            if self.frame is not None:
                result = condition()
                self.add_frame_stats()
                # print(f"TaskExecutor: wait_until {result}")
                if is_not_empty(result):
                    print(f"TaskExecutor: found result {result}")
                    self.sleep(self.wait_until_check_delay)
                    return result
            if post_action is not None:
                post_action()
            self.wait_fps(start)
            if time.time() - start > time_out:
                print(f"TaskExecutor: wait_until timeout {condition} {time_out} seconds")
                break
        return None

    def reset_scene(self):
        self.frame = None
        self.last_scene = self.current_scene
        self.current_scene = None

    def execute(self):
        print(f"TaskExecutor: start execute")
        try:
            while not self.exit_event.is_set():
                self.frame = self.next_frame()
                start = time.time()
                if self.frame is not None:
                    self.detect_scene()
                    # print(f"detect_scene: {self.current_scene.__class__.__name__} {(time.time() - start)}")
                    if self.current_scene is not None:
                        task_executed = 0
                        for task in self.tasks:
                            if task.done:
                                continue
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
            traceback.print_exc()
            self.exit_event.set()

    def add_frame_stats(self):
        if self.overlay:
            self.frame_stats.add_frame()
            mean = self.frame_stats.mean()
            if mean > 0:
                # print(f"frame_stats.mean(): {mean}, fps:{round(1000 / mean)}")
                self.overlay.draw_text("fps", 0.3, 0.01,
                                       f"Scene:{self.current_scene.__class__.__name__} FrameTime:{mean}, FPS:{round(1000 / mean)}")

    def latest_scene(self):
        return self.current_scene or self.last_scene

    def detect_scene(self, scene_type=None):
        latest_scene = self.latest_scene()
        if latest_scene is not None:
            # detect the last scene optimistically
            if latest_scene.detect(self.frame):
                self.current_scene = latest_scene
                return
        for scene in self.scenes:
            if scene_type is not None and isinstance(scene, scene_type) == False:
                continue
            if scene != latest_scene:
                if scene.detect(self.frame):
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


def is_not_empty(val):
    if isinstance(val, list):
        return len(val) > 0
    return val is not None
