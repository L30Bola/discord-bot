import logging
import logging.handlers

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.handlers.TimedRotatingFileHandler(
    filename='discord.log',
    when='midnight',
    interval=1,
    encoding='utf-8',
    utc=False,
    backupCount=7,  # Rotate through 7 files
)

dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)