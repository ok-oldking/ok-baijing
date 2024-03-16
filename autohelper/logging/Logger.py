import logging
import os
import traceback
from logging.handlers import TimedRotatingFileHandler

from autohelper.gui.Communicate import communicate


class CommunicateHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_message = self.format(record)
        communicate.log.emit(record.levelno, log_message)


formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s %(message)s')
communicate_handler = CommunicateHandler()
communicate_handler.setFormatter(formatter)


def get_substring_from_last_dot_exclusive(s):
    # Find the last occurrence of "."
    last_dot_index = s.rfind(".")
    # If there's no ".", return an empty string or the original string based on your need
    if last_dot_index == -1:
        return ""  # or return s to return the whole string if there's no dot
    # Slice the string from just after the last "." to the end
    return s[last_dot_index + 1:]


root = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
root.addHandler(console_handler)


def config_logger(config):
    if config.get('debug'):
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)

    root.addHandler(communicate_handler)

    if config.get('log_file'):
        ensure_dir_for_file(config['log_file'])

        os.makedirs("logs", exist_ok=True)
        # File handler with rotation
        file_handler = TimedRotatingFileHandler(config['log_file'], when="midnight", interval=1,
                                                backupCount=7)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)  # File handler level
        root.addHandler(file_handler)


class Logger:
    def __init__(self, name):
        # Initialize the logger with the name of the subclass
        self.logger = root
        self.name = name

    def debug(self, message):
        self.logger.debug(f"{self.name}:{message}")

    def info(self, message):
        self.logger.info(f"{self.name}:{message}")

    def warning(self, message):
        self.logger.warning(f"{self.name}:{message}")

    def error(self, message, exception=None):
        if exception is not None:
            traceback.print_exc()
            stack_trace_str = traceback.format_exc()
        else:
            stack_trace_str = ""
        self.logger.error(f"{self.name}:{message} {stack_trace_str}")

    def critical(self, message):
        self.logger.critical(f"{self.name}:{message}")


def get_logger(name):
    return Logger(name)


def ensure_dir_for_file(file_path):
    # Extract the directory from the file path
    directory = os.path.dirname(file_path)

    # Check if the directory exists
    if not os.path.exists(directory):
        # If the directory does not exist, create it (including any intermediate directories)
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        print(f"Directory already exists: {directory}")
