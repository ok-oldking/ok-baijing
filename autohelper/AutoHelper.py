import threading
import time
from typing import Dict, Any

from autohelper.capture.HwndWindow import HwndWindow
from autohelper.feature.FeatureSet import FeatureSet
from autohelper.gui.App import App
from autohelper.interaction.ADBInteraction import ADBBaseInteraction
from autohelper.interaction.Win32Interaction import Win32Interaction
from autohelper.logging.Logger import get_logger, config_logger
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
        config_logger(config)
        logger.info(f"initializing {self.__class__.__name__}, config: {config}")
        self.debug = config.get("debug", False)
        self.exit_event = threading.Event()
        if config['interaction'] == 'adb' or config['capture'] == 'adb':
            self.init_adb()
        self.init_hwnd(config.get('capture_window_title'), self.exit_event)
        if config['capture'] == 'adb':
            from autohelper.capture.adb.ADBCaptureMethod import ADBCaptureMethod
            self.capture = ADBCaptureMethod(self.device_manager)
        else:
            from autohelper.capture.windows.WindowsGraphicsCaptureMethod import WindowsGraphicsCaptureMethod
            self.capture = WindowsGraphicsCaptureMethod(self.hwnd)
        if config['interaction'] == 'adb':
            self.interaction = ADBBaseInteraction(self.device_manager, self.capture)
        else:
            self.init_hwnd(config['capture_window_title'], self.exit_event)
            self.interaction = Win32Interaction(self.capture)

        if config.get('coco_feature_folder') is not None:
            coco_feature_folder = config.get('coco_feature_folder')
            self.feature_set = FeatureSet(coco_feature_folder,
                                          default_horizontal_variance=config.get('default_horizontal_variance', 0),
                                          default_vertical_variance=config.get('default_vertical_variance', 0),
                                          default_threshold=config.get('default_threshold', 0))

        self.task_executor = TaskExecutor(self.capture, interaction=self.interaction, exit_event=self.exit_event,
                                          tasks=config['tasks'], scenes=config['scenes'], feature_set=self.feature_set)

        if config['use_gui']:
            if config.get('debug'):
                overlay = True
            else:
                overlay = False
            app = App(config.get('gui_title'), config.get('gui_icon'), config['tasks'], overlay, self.hwnd,
                      self.exit_event)
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
                self.exit_event.set()
                logger.info("Keyboard interrupt received, exiting script.")
            finally:
                # Clean-up code goes here (if any)
                # This block ensures that the script terminates gracefully,
                # releasing resources or performing necessary clean-up operations.
                logger.info("Script has terminated.")

    def wait_task(self):
        while not self.exit_event.is_set():
            time.sleep(1)

    def init_hwnd(self, window_title, exit_event):
        if window_title and self.hwnd is None:
            if self.device_manager is not None and self.device_manager.device is not None:
                self.hwnd = HwndWindow(window_title, exit_event, self.device_manager.width, self.device_manager.height)
            else:
                self.hwnd = HwndWindow(window_title, exit_event)

    def init_adb(self):
        if self.device_manager is None:
            from autohelper.capture.adb.DeviceManager import DeviceManager
            self.device_manager = DeviceManager()
