import logging
import logging.handlers
from .config import LOGGER_FILE, LOGGER_ERROR_FILE


# 获取日志器
def init_logging(verbose=1, logger_name=None):
    """
    1.获取日志器
    2.设置日志级别
    3.获取处理器
    4.设置处理器级别
    5.文件打印格式
    6.添加处理器到日志器
    """
    formatter = logging.Formatter(
        ("[%(asctime)s %(filename)s:%(lineno)s] - %(message)s "))

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if verbose > 0 else logging.INFO)

    rf_handler = logging.handlers.TimedRotatingFileHandler(
        LOGGER_FILE, encoding='utf-8')
    rf_handler.setFormatter(formatter)

    f_handler = logging.FileHandler(LOGGER_ERROR_FILE, encoding='utf-8')
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(formatter)

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)

    return logger


logger = init_logging()
