
import logging
import logging.handlers as handlers
import logging.config as config
from colorlog import ColoredFormatter


# Define logging formats
file_fmt = (
    '{"time": "%(asctime)s", "level":'
    ' "%(levelname)s", "name": "%(name)s", "source": %(filename)s:%(lineno)d#%(funcName)s, "message": "%(message)s"}')


loggers = {}


class Logger:

    def __init__(self):
        pass

    @staticmethod
    def get_logger(name='root'):
        global loggers

        if "root" not in loggers:
            raise Exception("ERROR - logger not initialized!")

        if name in loggers:
            return loggers[name]

        new_logger = logging.getLogger(name)
        loggers[name] = new_logger

        return new_logger

    @staticmethod
    def init_logger(log_dir):
        if "root" in loggers:
            return

        config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
        })

        # -------- Setup file logger --------
        root_logger = logging.getLogger()
        max_mb = 100
        file_handler = handlers.RotatingFileHandler(log_dir,
                                                    maxBytes=max_mb*1024*1024,
                                                    backupCount=2)
        file_handler.setFormatter(logging.Formatter(file_fmt))

        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)

        # -------- Setup console logger --------
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        console_fmt = '%(asctime)s | %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(name)s%(reset)s ' \
                      '- %(log_color)s%(message)s%(reset)s'

        console_fmtr = ColoredFormatter(
            console_fmt,
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG':    'white',
                'INFO':     'blue',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )

        console.setFormatter(console_fmtr)
        root_logger.addHandler(console)

        # Save root logger to dictionary
        loggers["root"] = root_logger


if __name__ == "__main__":
    Logger.create_logger("my.log")
    Logger.get_logger("app").debug("info")
    Logger.get_logger("app").info("info")
    Logger.get_logger("app").warning("info")
    Logger.get_logger("app").error("info")
    Logger.get_logger("app").critical("info")

