from distutils.util import strtobool
import logging
import logging.handlers
from os import getenv
from sys import stdout

logger = logging.getLogger('discord')

if strtobool(getenv("DEBUG", "False")):
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

if strtobool(getenv("FILE_LOGGER", "True")):
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename='discord.log',
        when='midnight',
        interval=1,
        encoding='utf-8',
        utc=False,
        backupCount=7,
    )
else:
    file_handler = None

if strtobool(getenv("STDOUT_LOGGER", "True")):
    stdout_handler = logging.StreamHandler(stream=stdout)
else:
    stdout_handler = None

if file_handler is not None or stdout_handler is not None:
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

if file_handler is not None:
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

if stdout_handler is not None:
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)