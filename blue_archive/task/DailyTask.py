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

        schedule_scene_reward = self.wait_until(lambda: self.find_one("schedule_scene_reward", 0.1, 0.5))
        if schedule_scene_reward is None:
            return False
        self.click_box(schedule_scene_reward)

        choose_schedule_scene_all = self.wait_until(lambda: self.find_one("choose_schedule_scene_all", 0.1, 0.5))
        if choose_schedule_scene_all is None:
            return False
        self.click_box(choose_schedule_scene_all)

        hearts = self.wait_until(lambda: self.find("schedule_scene_heart", 1, 0.8, 0.5))
        if hearts is None:
            return False
        max_hearts = find_most_hearts(hearts, hearts[0].width * 10)
        self.click_box(max_hearts)

        schedule_start_screen_start = self.wait_until(lambda: self.find_one("schedule_start_screen_start"))
        if schedule_start_screen_start is None:
            return False
        self.click_box(schedule_start_screen_start)

        return True


def find_most_hearts(boxes, max_width):
    """
       find the box with most hearts
       """
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

    return max_box
