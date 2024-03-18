import threading
import time
import traceback

from autohelper.capture.BaseCaptureMethod import BaseCaptureMethod
from autohelper.gui.Communicate import communicate
from autohelper.interaction.BaseInteraction import BaseInteraction
from autohelper.logging.Logger import get_logger
from autohelper.scene.Scene import Scene
from autohelper.stats.StreamStats import StreamStats

logger = get_logger(__name__)


class TaskExecutor:
    current_scene: Scene | None = None
    last_scene: Scene | None = None
    frame_stats = StreamStats()
    _frame = None
    paused = True
    ocr = None

    def __init__(self, method: BaseCaptureMethod, interaction: BaseInteraction, target_fps=10,
                 wait_until_timeout=10, wait_until_before_delay=1, wait_until_check_delay=1,
                 exit_event=threading.Event(), tasks=[], scenes=[], feature_set=None, ocr=None):
        self.interaction = interaction
        self.feature_set = feature_set
        self.wait_until_check_delay = wait_until_check_delay
        self.wait_until_before_delay = wait_until_before_delay
        self.method = method
        self.wait_scene_timeout = wait_until_timeout
        self.target_delay = 1.0 / target_fps
        self.exit_event = exit_event
        self.ocr = ocr
        self.tasks = tasks
        self.scenes = scenes
        for scene in self.scenes:
            scene.executor = self
            scene.feature_set = self.feature_set
        for task in self.tasks:
            task.executor = self
            task.feature_set = self.feature_set
        self.thread = threading.Thread(target=self.execute)
        self.thread.start()

    def wait_fps(self, start):
        cost = time.time() - start
        if cost < self.target_delay:
            self.sleep(self.target_delay - cost)

    def next_frame(self):
        self.reset_scene()
        start = time.time()
        while not self.exit_event.is_set():
            self._frame = self.method.get_frame()
            if self._frame is not None:
                communicate.frame.emit(self._frame)
                return self._frame
            time.sleep(0.01)
            if time.time() - start > self.wait_scene_timeout:
                return None

    @property
    def frame(self):
        if self._frame is None:
            return self.next_frame()
        else:
            return self._frame

    def sleep(self, timeout):
        """
        Sleeps for the specified timeout, checking for an exit event every 100ms, with adjustments to prevent oversleeping.

        :param timeout: The total time to sleep in seconds.
        """
        self.frame_stats.add_sleep(timeout)
        end_time = time.time() + timeout
        while True:
            if self.exit_event.is_set():
                logger.info("Exit event set. Exiting early.")
                return
            remaining = end_time - time.time()
            if remaining <= 0:
                return
            time.sleep(min(0.1, remaining))  # Sleep for 100ms or the remaining time, whichever is smaller

    def wait_scene(self, scene_type, time_out, pre_action, post_action):
        return self.wait_condition(lambda: self.detect_scene(scene_type), time_out, pre_action, post_action)

    def wait_condition(self, condition, time_out, pre_action, post_action):
        self.sleep(self.wait_until_before_delay)
        start = time.time()
        if time_out == 0:
            time_out = self.wait_scene_timeout
        while not self.exit_event.is_set():
            self.reset_scene()
            if pre_action is not None:
                pre_action()
            self._frame = self.next_frame()
            if self._frame is not None:
                result = condition()
                self.add_frame_stats()
                result_str = list_or_obj_to_str(result)
                if result:
                    logger.debug(f"found result {result_str}")
                    self.sleep(self.wait_until_check_delay)
                    return result
            if post_action is not None:
                post_action()
            self.wait_fps(start)
            if time.time() - start > time_out:
                logger.info(f"wait_until timeout {condition} {time_out} seconds")
                break
        return None

    def reset_scene(self):
        self._frame = None
        self.last_scene = self.current_scene
        self.current_scene = None

    def execute(self):
        logger.info(f"start execute")
        while not self.exit_event.is_set():
            self._frame = self.next_frame()
            start = time.time()
            if self._frame is not None:
                self.detect_scene()
                task_executed = 0
                for task in self.tasks:
                    if task.done:
                        continue
                    task.running = True
                    communicate.tasks.emit()
                    try:
                        result = task.run_frame()
                        if result is not None:
                            if result:
                                task.success_count += 1
                            else:
                                task.error_count += 1
                    except Exception as e:
                        traceback.print_exc()
                        stack_trace_str = traceback.format_exc()
                        logger.error(f"{task.name} exception: {e}, traceback: {stack_trace_str}")
                        task.error_count += 1
                    task.running = False
                    communicate.tasks.emit()
                    processing_time = time.time() - start
                    task_executed += 1
                    if processing_time > 0.2:
                        logger.debug(
                            f"{task.__class__.__name__} taking too long get new frame {processing_time} {task_executed} {len(self.tasks)}")
                        self.next_frame()
                        start = time.time()
                self.add_frame_stats()
            self.wait_fps(start)

    def add_frame_stats(self):
        self.frame_stats.add_frame()
        mean = self.frame_stats.mean()
        if mean > 0:
            communicate.frame_time.emit(mean)
            communicate.fps.emit(round(1000 / mean))
            scene = "None"
            if self.current_scene is not None:
                scene = self.current_scene.name or self.current_scene.__class__.__name__
            communicate.scene.emit(scene)

    def latest_scene(self):
        return self.current_scene or self.last_scene

    def detect_scene(self, scene_type=None):
        latest_scene = self.latest_scene()
        if latest_scene is not None:
            # detect the last scene optimistically
            if latest_scene.detect(self._frame):
                self.current_scene = latest_scene
                return latest_scene
        for scene in self.scenes:
            if scene_type is not None and not isinstance(scene, scene_type):
                continue
            if scene != latest_scene:
                if scene.detect(self._frame):
                    self.current_scene = scene
                    logger.debug(f"TaskExecutor: scene changed {scene.__class__.__name__}")
                    return scene
        if self.current_scene is not None:
            logger.debug(f"TaskExecutor: scene changed to None")
            self.current_scene = None
        return self.current_scene

    def stop(self):
        self.exit_event.set()

    def wait_until_done(self):
        self.thread.join()


def list_or_obj_to_str(val):
    if val is not None:
        if isinstance(val, list):
            return ', '.join(str(obj) for obj in val)
        else:
            return str(val)
    else:
        return None
