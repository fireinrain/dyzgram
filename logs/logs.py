import sys
from loguru import logger as loguru_logger
from config import GLONAL_CONFIG as global_config


class Loggin:
    def __init__(self) -> None:
        enable = global_config['logger']['enable']
        if isinstance(enable, str):
            enable = True
        self.enable = enable
        level = global_config['logger']['level']
        if not level or level not in ['debug', 'info']:
            level = 'debug'
        if level == 'debug':
            self.level = "DEBUG"
        else:
            self.level = "INFO"

    def setup_logger(self):
        loguru_logger.remove()
        loguru_logger.add(sink=sys.stdout, level=self.level, colorize=True)
        loguru_logger.add("dyzgram.log", level=self.level, rotation="5 MB", retention=2,
                          colorize=True, encoding="utf-8")  # Output log messages to a file
        return loguru_logger


_loggin = Loggin()
_logger = _loggin.setup_logger()


class GramLogger(object):
    def __init__(self, loggin: Loggin, logger_in):
        self.loggin = loggin
        self.logger = logger_in

    def debug(self, message):
        if self.loggin.enable:
            self.logger.debug(message)

    def info(self, message):
        if self.loggin.enable:
            self.logger.info(message)

    def warning(self, message):
        if self.loggin.enable:
            self.logger.warning(message)

    def error(self, message):
        if self.loggin.enable:
            self.logger.error(message)


logger = GramLogger(_loggin, _logger)
