from typing_extensions import override

from autoui.scene.Scene import Scene
from autoui.task.FindFeatureTask import FindFindFeatureTask
from autoui.task.TaskExecutor import TaskExecutor
from blue_archive.scene.MainScene import MainScene
from blue_archive.scene.QuestScene import QuestScene


class DailyTask(FindFindFeatureTask):

    @override
    def run_frame(self):
        if self.is_scene(MainScene):
            print(f"DailyTask:click mission")
            self.click_box(self.scene.main_screen_mission)
            scene, frame = self.wait_scene(QuestScene)
            print(f"DailyTask:changed to QuestScene")

    def do_schedule(self, executor: TaskExecutor, scene: Scene):
        pass
