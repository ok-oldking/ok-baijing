from autoui.task.TaskExecutor import TaskExecutor


class AutoUI:
    executor: TaskExecutor

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
