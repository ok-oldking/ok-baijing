from autoui.scene.FeatureScene import FindFeatureScene


class MainScene(FindFeatureScene):
    main_screen_mission = None
    main_screen_schedule = None
    main_screen_cafe = None

    def detect(self, frame):
        self.main_screen_mission = self.find_one("main_screen_mission")
        self.main_screen_schedule = self.find_one("main_screen_schedule")
        self.main_screen_cafe = self.find_one("main_screen_cafe")
        return self.main_screen_mission is not None and self.main_screen_schedule is not None and self.main_screen_cafe is not None and self.find_one(
            "close_event") is None and self.find_one("main_screen_loading") is None
