"""
logger.py - Centralized logger configuration for Snackstack
"""
import logging
import sys

LOG_FORMAT = "%(asctime)s | %(name)-28s | %(levelname)-7s | %(message)s"
DATE_FORMAT = "%H:%M:%S"

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a named logger with consistant stream handler"""
    logger = logging.getLogger()

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter =  logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    # logger.disabled = True
    return logger
