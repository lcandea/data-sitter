import logging
import logging.config
from os import environ

from dotenv import load_dotenv


load_dotenv()

DEFAULT_LEVEL = "INFO"
VALID_LOG_LEVEL = ["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]
LOG_LEVEL = environ.get("LOG_LEVEL", DEFAULT_LEVEL)

if LOG_LEVEL not in VALID_LOG_LEVEL:
    LOG_LEVEL = DEFAULT_LEVEL


def configure_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "[%(asctime)s] %(name)s [%(levelname)s] %(funcName)s - %(filename)s:%(lineno)d - %(message)s"
                },
            },
            "handlers": {
                "default": {
                    "level": LOG_LEVEL,
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",  # Use standard output
                },
            },
            "loggers": {"": {"handlers": ["default"], "level": LOG_LEVEL, "propagate": True}},  # root logger
        }
    )

configure_logging()

def get_logger(name: str):
    return logging.getLogger(name)
