# utils/logger.py
import logging
import sys

class Logger:
    @staticmethod
    def setup_logger(name="NudamuLogger"):
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
