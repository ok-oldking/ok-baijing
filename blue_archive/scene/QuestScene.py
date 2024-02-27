from autoui.scene.FeatureScene import FindFeatureScene


class QuestScene(FindFeatureScene):
    mission_scene_mission = None
    mission_get_reward_gray = None
    mission_get_reward_yellow = None

    def detect(self, frame):
        self.mission_scene_mission = self.find_one("mission_scene_mission")
        if self.mission_scene_mission is None:
            return False
        self.mission_get_reward_gray = self.find_one("mission_get_reward_gray")
        self.mission_get_reward_yellow = self.find_one("mission_get_reward_yellow")
        print(f"QuestScene : {self.mission_get_reward_gray} {self.mission_get_reward_yellow}")
        return True
