import time

from autohelper.config.Config import Config
from autohelper.logging.Logger import get_logger
from autohelper.task.ExecutorOperation import ExecutorOperation

logger = get_logger(__name__)


class BaseTask(ExecutorOperation):
    _done = False

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.name = self.__class__.__name__
        self.success_count = 0
        self.error_count = 0
        self.enabled = True
        self.running = False
        self.config = None
        self.default_config = {}
        self.last_execute_time = 0

    def can_run(self):
        return self.enabled and not self._done

    def load_config(self, folder):
        self.config = Config(self.default_config, folder, self.__class__.__name__)

    def enable(self):
        self.enabled = True
        self.set_done(False)

    def disable(self):
        self.enabled = False

    def get_status(self):
        if not self.enabled:
            return "Disabled"
        elif self.done:
            return "Done"
        elif self.enabled and self.executor.paused:
            return "Paused"
        elif self.running or self.enabled and time.time() - self.last_execute_time < 3:
            return "Running"
        else:
            return "In Queue"

    def run_frame(self):
        pass

    def reset(self):
        self._done = False
        pass

    @property
    def done(self):
        return self._done

    def set_done(self, done=True):
        self._done = done
