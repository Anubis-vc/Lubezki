import logging
import logging.config
import sys
from typing import Dict, Any


def setup_logging(log_level: str = "INFO") -> None:
    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": sys.stdout,
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "app": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "sqlalchemy": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    # Apply the configuration
    logging.config.dictConfig(config)


def setup_production_logging(log_level: str = "INFO") -> None:
    """Set up logging optimized for production environments.
    Uses JSON format for easy parsing by log aggregation systems.
    """
    setup_logging(log_level=log_level)


def setup_development_logging(log_level: str = "DEBUG") -> None:
    """Set up logging optimized for development environments.
    Uses human-readable format for easier local debugging.
    """
    setup_logging(log_level=log_level)
