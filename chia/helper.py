import logging
import os

from logging.handlers import RotatingFileHandler


class Helper:

    @staticmethod
    def init_logger(filename, mode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG, maxBytes=50000, logname='root'):
        logger = logging.getLogger(logname)

        # check if path exists
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path)

        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S");
        handler = RotatingFileHandler(filename, mode=mode, maxBytes=maxBytes, backupCount=2, encoding=None, delay=0)
        handler.setFormatter(formatter)
        handler.setLevel(level)

        logger.setLevel(level)
        logger.addHandler(handler)

        return logger
