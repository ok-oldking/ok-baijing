from typing_extensions import override

from autoui.task.FindFeatureTask import FindFindFeatureTask
from blue_archive.scene.MainScene import MainScene


class DailyTask(FindFindFeatureTask):

    @override
    def run_frame(self):
        if self.is_scene(MainScene):
            print(f"DailyTask:schedule")
            self.do_schedule()

    def do_schedule(self):
        self.click_box(self.scene.main_screen_schedule)
        rewards = self.wait_until(lambda: self.find_one("schedule_scene_reward", 0.1, 0.5))
        print(f"DailyTask:do_schedule schedule_scene_reward {rewards}")
        self.click_box(rewards)
