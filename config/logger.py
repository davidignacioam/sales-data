import os

from pydantic import BaseModel

from config.config import SERVICE


LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")
LOGGER_NAME: str = SERVICE


class LogConfig(BaseModel):

    """Logging configuration to be set for the server"""

    if not os.path.isdir("./logs"):
        os.mkdir("./logs")
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default_formatter": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", '
            + '"thread": "%(threadName)s", "component": "%(module)s",'
            + '"service": "%(name)s", "payload": %(message)s}',
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    }
    handlers = {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "level": LOG_LEVEL,
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "default_formatter",
            "level": LOG_LEVEL,
            "filename": f"./logs/{LOGGER_NAME}.log",
            "mode": "a",
            "encoding": "utf-8",
        },
    }
    loggers = {
        LOGGER_NAME: {
            "handlers": ["stream_handler", "file_handler"],
            "level": LOG_LEVEL,
            "propagate": False,
        }
    }
