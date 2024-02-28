from typing_extensions import override

from blue_archive.scene.MainScene import MainScene
from blue_archive.task.BaseBaTaskask import BaseBaTask


class DailyScheduleTask(BaseBaTask):
    target_max_hearts = 3
    cycle_time = 0

    @override
    def run_frame(self):
        if self.is_scene(MainScene):
            print(f"DailyTask:schedule")
            self.click_box(self.scene.main_screen_schedule)
            schedule_scene_reward = self.wait_until(lambda: self.find_one("schedule_scene_reward", 0.1, 0.5))
            if schedule_scene_reward is None:
                return False
            self.click_box(schedule_scene_reward)
            while self.do_schedule():
                pass

    def do_schedule(self):
        self.cycle_time += 1
        if self.cycle_time % 10 == 0:
            self.target_max_hearts -= 1
            if self.target_max_hearts == 0:
                print(f"DailyTask: can't find any with hearts, probably a bug")
                return False

        choose_schedule_scene_all = self.wait_until(lambda: self.find_one("choose_schedule_scene_all", 0.1, 0.5))
        if choose_schedule_scene_all is None:
            return False

        self.click_relative(0.99, 0.5)

        choose_schedule_scene_all = self.wait_until(lambda: self.find_one("choose_schedule_scene_all", 0.1, 0.5))
        if choose_schedule_scene_all is None:
            return False

        self.click_box(choose_schedule_scene_all)

        hearts = self.wait_until(lambda: self.find("schedule_scene_heart", 1, 0.8, 0.9), time_out=3)

        box, count = find_most_hearts(hearts)
        if count < self.target_max_hearts:
            print(f"DailyTask: can't find any with target hearts {count} < {self.target_max_hearts}, skip to next")
            self.go_back()
            return True
        self.click_box(box)

        schedule_start_screen_start = self.wait_until(lambda: self.find_one("schedule_start_screen_start"))
        if schedule_start_screen_start is None:
            return False
        self.click_box(schedule_start_screen_start)

        # click the center of the screen until we get an ok button
        dialog_ok = self.wait_until(
            lambda: self.find_one("reward_get_ok", 0.5, 0.5) or self.find_one("dialog_ok_schedule", 0.5, 0.5),
            time_out=15, post_action=lambda: (self.sleep(1), self.click_relative(0.5, 0.5)))
        if dialog_ok is None:
            return False
        if dialog_ok.name == "reward_get_ok":
            print(f"schedule exhausted all")
            self.done = True
            self.go_home()
            return False

        self.click_box(dialog_ok)

        all_schedule_screen_close = self.wait_until(lambda: self.find_one("all_schedule_screen_close"))
        if all_schedule_screen_close is None:
            return False

        # True means continue the loop
        return True


def find_most_hearts(boxes):
    if boxes is None or len(boxes) == 0:
        return None, 0
    """
       find the box with most hearts
       """
    max_width = boxes[0].width * 10
    current_start = boxes[0]
    current_hearts = 1
    max_hearts = 1
    max_box = boxes[0]

    for box in boxes[1:]:
        distance = box.x + box.width - current_start.x
        if max_width > distance > 0:
            current_hearts += 1
            if current_hearts > max_hearts:
                max_box = current_start
                max_hearts = current_hearts
        else:
            current_start = box
            current_hearts = 1

    print(f"find_most_hearts size {max_hearts} {max_box}")

    return max_box, max_hearts
