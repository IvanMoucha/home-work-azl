import logging
import os


class LoggingSingleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LoggingSingleton, cls).__new__(cls)
            cls.set_for_environment()

        return cls.instance

    @staticmethod
    def set_for_environment():
        if "ENVIRONMENT" in os.environ and os.environ["ENVIRONMENT"] in ['test', 'prod']:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.DEBUG)
        if logging.getLogger().hasHandlers():
            for handler in logging.getLogger().handlers:
                handler.setFormatter(
                    logging.Formatter('[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t[%(name)s:%(lineno)s]\t%(message)s\n', '%Y-%m-%dT%H:%M:%S'))

logger = LoggingSingleton()

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name=name)
