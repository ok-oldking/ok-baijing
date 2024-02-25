from autoui.scene.FeatureScene import FeatureScene


class MainScene(FeatureScene):
    main_screen_mission = None

    def detect(self, frame):
        self.main_screen_mission = self.find_one(frame, "main_screen_mission")
        return self.main_screen_mission is not None
