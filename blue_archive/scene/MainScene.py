from autoui.scene.FeatureScene import FindFeatureScene


class MainScene(FindFeatureScene):
    main_screen_mission = None

    def detect(self, frame):
        self.main_screen_mission = self.find_one(frame, "main_screen_mission")
        return self.main_screen_mission is not None and self.find_one(frame, "close_event") is None
