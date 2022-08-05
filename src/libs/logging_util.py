
__all__ = ['configure_logger']

import logging
from typing import Any, Mapping

COLOR_GRAY = "\x1b[38;20m"
COLOR_BLUE = "\x1b[34;20m"
COLOR_YELLOW = "\x1b[33;20m"
COLOR_RED = "\x1b[31;20m"
COLOR_BOLD_RED = "\x1b[31;1m"
COLOR_END = "\x1b[0m"

def _col(col, msg):
    return f"{col}{msg}{COLOR_END}"

def configure_logger(logger:logging.Logger, level_name="DEBUG", log_color:str=COLOR_GRAY):
    # Check logger level
    invalid_lvl = not level_name in logging._nameToLevel
    if(invalid_lvl): 
        invalid_name = level_name
        level_name = "DEBUG"

    # Set logger level
    level = logging._nameToLevel[level_name]
    logger.setLevel(level)

    # Create stream handeler with level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(custom_formatter(log_color = log_color))

    # Add handeler to logger
    logger.addHandler(ch)

    # Check if overode level name
    if(invalid_lvl):
        raise Exception(f"Invalid Log Level name, \"{invalid_name}\", given for configuration.")


class custom_formatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None, log_color:str = COLOR_GRAY):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        self._log_color = log_color
        
        log_name = _col(log_color, '%(name)s')
        self._formats = {
            logging.DEBUG:    f"(%(asctime)s)[{log_name}][{_col(COLOR_BLUE, '%(levelname)s')}] %(message)s (%(filename)s:%(lineno)d)",
            logging.INFO:     f"(%(asctime)s)[{log_name}][{_col(COLOR_GRAY, '%(levelname)s')}] %(message)s",
            logging.WARNING:  f"(%(asctime)s)[{log_name}][{_col(COLOR_YELLOW, '%(levelname)s')}] %(message)s (%(filename)s:%(lineno)d)",
            logging.ERROR:    f"(%(asctime)s)[{log_name}][{_col(COLOR_RED, '%(levelname)s')}] %(message)s (%(filename)s:%(lineno)d)",
            logging.CRITICAL: f"(%(asctime)s)[{log_name}][{_col(COLOR_BOLD_RED, '%(levelname)s')}] %(message)s",
        }

    def format(self, record):
        log_fmt = self._formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
