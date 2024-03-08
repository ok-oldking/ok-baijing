from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from autoui.gui.Communicate import communicate


class InfoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        # Connect the custom signal to the slot that updates the values
        communicate.fps.connect(self.update_fps)
        communicate.scene.connect(self.update_scene)
        communicate.frame_time.connect(self.update_frame_time)

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.scene_widget = QLabel()
        self.layout.addWidget(self.scene_widget)
        self.update_scene("None")

        self.fps_widget = QLabel()
        self.layout.addWidget(self.fps_widget)
        self.update_fps(0)

        self.frame_time_widget = QLabel()
        self.layout.addWidget(self.frame_time_widget)
        self.update_frame_time(0)

        self.layout.addStretch()

    def update_fps(self, fps):
        self.fps_widget.setText(f"FPS: {fps}")

    def update_frame_time(self, fps):
        self.frame_time_widget.setText(f"FrameTime: {fps}")

    def update_scene(self, scene):
        self.scene_widget.setText(f"Scene: {scene}")
