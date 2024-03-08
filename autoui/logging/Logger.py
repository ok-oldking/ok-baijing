import logging
from logging.handlers import TimedRotatingFileHandler

from autoui.gui.Communicate import communicate

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# File handler with rotation
file_handler = TimedRotatingFileHandler(f"auto_ui_log.log", when="midnight", interval=1,
                                        backupCount=7)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # File handler level


class CommunicateHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_message = self.format(record)
        communicate.log.emit(record.levelno, log_message)


communicate_handler = CommunicateHandler()
communicate_handler.setFormatter(formatter)


class Logger:
    def __init__(self, name):
        # Initialize the logger with the name of the subclass
        self.logger = logging.getLogger(name)

        # Set the log level
        self.logger.setLevel(logging.DEBUG)  # Or any other level

        # Formatter for the log messages

        self.logger.addHandler(file_handler)
        self.logger.addHandler(communicate_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)  # Console handler level
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


def get_logger(name):
    return Logger(name)
