import threading
from typing import Dict, Any

import adbutils

from autoui.capture.HwndWindow import HwndWindow
from autoui.capture.adb.ADBCaptureMethod import ADBCaptureMethod
from autoui.capture.windows.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
from autoui.feature.FeatureSet import FeatureSet
from autoui.gui.App import App
from autoui.interaction.ADBInteraction import ADBBaseInteraction
from autoui.interaction.Win32Interaction import Win32Interaction
from autoui.logging.Logger import get_logger
from autoui.task.TaskExecutor import TaskExecutor

logger = get_logger(__name__)


class AutoUI:
    executor: TaskExecutor
    adb = None
    adb_device = None
    feature_set = None
    hwnd = None

    def __init__(self, config: Dict[str, Any]):
        logger.config(config)
        logger.info(f"initializing {self.__class__.__name__}, config: {config}")
        exit_event = threading.Event()

        if config['capture'] == 'adb':
            self.init_adb(config)
            self.capture = ADBCaptureMethod(self.adb_device)
        else:
            self.init_hwnd(config['window_title'], exit_event)
            self.capture = WindowsGraphicsCaptureMethod(self.hwnd)
        if config['interaction'] == 'adb':
            self.init_adb(config)
            self.interaction = ADBBaseInteraction(self.adb_device, self.capture)
        else:
            self.init_hwnd(config['window_title'], exit_event)
            self.interaction = Win32Interaction(self.capture)

        if config['coco_feature_folder'] is not None:
            coco_feature_folder = config['coco_feature_folder']
            self.feature_set = FeatureSet(coco_feature_folder,
                                          default_horizontal_variance=config['default_horizontal_variance'],
                                          default_vertical_variance=config['default_vertical_variance'],
                                          default_threshold=config['default_threshold'])

        self.task_executor = TaskExecutor(self.capture, interaction=self.interaction, exit_event=exit_event,
                                          tasks=config['tasks'], scenes=config['scenes'], feature_set=self.feature_set)
        app = App(exit_event)
        app.start()

    def init_hwnd(self, window_title, exit_event):
        if self.hwnd is None:
            self.hwnd = HwndWindow(window_title, exit_event)

    def init_adb(self, config):
        if self.adb is None:
            self.adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
            self.adb.connect(f"{config['adb_host']}:{config['adb_port']}")
            self.adb_device = self.adb.device()
