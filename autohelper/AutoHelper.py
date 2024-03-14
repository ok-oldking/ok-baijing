import threading
import time
from typing import Dict, Any

from autohelper.capture.HwndWindow import HwndWindow
from autohelper.capture.adb.ADBCaptureMethod import ADBCaptureMethod
from autohelper.capture.adb.DeviceManager import DeviceManager
from autohelper.feature.FeatureSet import FeatureSet
from autohelper.gui.App import App
from autohelper.interaction.ADBInteraction import ADBBaseInteraction
from autohelper.interaction.Win32Interaction import Win32Interaction
from autohelper.logging.Logger import get_logger
from autohelper.task.TaskExecutor import TaskExecutor

logger = get_logger(__name__)


class AutoHelper:
    executor: TaskExecutor
    adb = None
    adb_device = None
    feature_set = None
    hwnd = None
    device_manager = None

    def __init__(self, config: Dict[str, Any]):
        logger.config(config)
        logger.info(f"initializing {self.__class__.__name__}, config: {config}")
        exit_event = threading.Event()

        if config['capture'] == 'adb':
            self.init_adb()
            self.capture = ADBCaptureMethod(self.device_manager)
        else:
            from autohelper.capture.windows.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
            self.init_hwnd(config['capture_window_title'], exit_event)
            self.capture = WindowsGraphicsCaptureMethod(self.hwnd)
        if config['interaction'] == 'adb':
            self.init_adb()
            self.interaction = ADBBaseInteraction(self.device_manager, self.capture)
        else:
            self.init_hwnd(config['capture_window_title'], exit_event)
            self.interaction = Win32Interaction(self.capture)

        if config['coco_feature_folder'] is not None:
            coco_feature_folder = config['coco_feature_folder']
            self.feature_set = FeatureSet(coco_feature_folder,
                                          default_horizontal_variance=config.get('default_horizontal_variance', 0),
                                          default_vertical_variance=config.get('default_vertical_variance', 0),
                                          default_threshold=config.get('default_threshold', 0))

        self.task_executor = TaskExecutor(self.capture, interaction=self.interaction, exit_event=exit_event,
                                          tasks=config['tasks'], scenes=config['scenes'], feature_set=self.feature_set)

        if config['use_gui']:
            app = App(config.get('gui_title'), config.get('gui_icon'), config['tasks'], exit_event)
            app.start()
        else:
            try:
                # Starting the task in a separate thread (optional)
                # This allows the main thread to remain responsive to keyboard interrupts
                task_thread = threading.Thread(target=self.wait_task())
                task_thread.start()

                # Wait for the task thread to end (which it won't, in this case, without an interrupt)
                task_thread.join()
            except KeyboardInterrupt:
                exit_event.set()
                logger.info("Keyboard interrupt received, exiting script.")
            finally:
                # Clean-up code goes here (if any)
                # This block ensures that the script terminates gracefully,
                # releasing resources or performing necessary clean-up operations.
                logger.info("Script has terminated.")

    @staticmethod
    def wait_task():
        while True:
            time.sleep(1)

    def init_hwnd(self, window_title, exit_event):
        if self.hwnd is None:
            self.hwnd = HwndWindow(window_title, exit_event)

    def init_adb(self):
        if self.device_manager is None:
            self.device_manager = DeviceManager()
