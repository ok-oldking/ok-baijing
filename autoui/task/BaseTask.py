from autoui.feature.Box import Box
from autoui.task.TaskExecutor import TaskExecutor


class BaseTask:
    executor: TaskExecutor
    done = False

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

    def send_key(self, key, down_time=0.02):
        self.executor.interaction.send_key(key, down_time)

    def wait_until(self, condition, time_out=0, pre_action=None, post_action=None):
        return self.executor.wait_until(condition, time_out, pre_action, post_action)

    def next_frame(self):
        return self.executor.next_frame()

    @property
    def scene(self):
        return self.executor.current_scene

    @property
    def frame(self):
        return self.executor.frame
