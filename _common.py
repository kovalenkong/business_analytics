import logging
import os
import sys


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv('LOGLEVEL', logging.DEBUG))
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(
        logging.Formatter('[%(levelname)s] %(asctime)s %(pathname)s: %(message)s (process ID: %(process)d)')
    )
    logger.addHandler(handler)
    return logger
