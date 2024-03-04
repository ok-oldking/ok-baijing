from typing_extensions import override

from blue_archive.scene.MainScene import MainScene
from blue_archive.task.BaseBaTaskask import BaseBaTask


class DailyCafeTask(BaseBaTask):
    target_max_hearts = 3
    cycle_time = 0

    @override
    def run_frame(self):
        if self.is_scene(MainScene):
            print(f"DailyTask:cafe")

            self.click_box(self.scene.main_screen_cafe)

            dialog_ok = self.wait_until(
                lambda: self.find_one("cafe_gift", 0.5, 0.5) or self.find_one("dialog_ok_center", 0.5, 0.5, 0.9))

            if dialog_ok is None:
                return

            if dialog_ok.name == "dialog_ok_center":
                self.click_box(dialog_ok)

            self.try_invite()

            while self.wait_and_click("cafe_girl_click", 1, 1, 0.5, 1.3, time_out=6):
                pass

            self.go_home()

            self.done = True

    def try_invite(self):
        self.wait_and_click("cafe_invite_ticket", time_out=3) and self.wait_and_click(
            "cafe_invite_blue") and self.wait_and_click(
            "dialog_choice_ok", 0.3, 0.3)
