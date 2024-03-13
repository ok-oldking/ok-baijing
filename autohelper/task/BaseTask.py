from autohelper.feature.Box import Box
from autohelper.logging.Logger import get_logger
from autohelper.task.TaskExecutor import TaskExecutor


class BaseTask:
    executor: TaskExecutor
    _done = False

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.name = self.__class__.__name__
        self.success_count = 0
        self.error_count = 0
        self.enabled = True
        self.running = False
        self.config = {}

    def run_frame(self):
        pass

    def is_scene(self, scene):
        return isinstance(self.executor.current_scene, scene)

    def click(self, x, y):
        self.executor.reset_scene()
        self.executor.interaction.click(x, y)

    def click_relative(self, x, y):
        self.executor.reset_scene()
        self.executor.interaction.click_relative(x, y)

    def click_box(self, box: Box, relative_x=0.5, relative_y=0.5):
        self.executor.reset_scene()
        self.executor.interaction.click_box(box, relative_x, relative_y)

    def wait_scene(self, scene_type=None, time_out=0, pre_action=None, post_action=None):
        return self.executor.wait_scene(scene_type, time_out, pre_action, post_action)

    def sleep(self, timeout):
        self.executor.sleep(timeout)

    @property
    def done(self):
        return self._done

    def set_done(self, done=True):
        self._done = done

    def send_key(self, key, down_time=0.02):
        self.executor.interaction.send_key(key, down_time)

    def wait_until(self, condition, time_out=0, pre_action=None, post_action=None):
        return self.executor.wait_condition(condition, time_out, pre_action, post_action)

    def next_frame(self):
        return self.executor.next_frame()

    @property
    def scene(self):
        return self.executor.current_scene

    @property
    def frame(self):
        return self.executor.frame
