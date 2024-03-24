import logging
from functools import wraps
import time
from datetime import timedelta
import sys
import colorlog

def add_log(func):

    log_colors_config = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    logFormatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(levelname)s][%(asctime)s] %(name)s %(message)s',
        log_colors=log_colors_config
        )

    logger = logging.getLogger(
        f'{func.__module__}.{func.__name__}'
        )
    
    logger.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler(sys.stderr)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    @wraps(func)
    def wrapper(*args, **kwargs):

        logger.info('start...')
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        used = timedelta(seconds=end - start)
        logger.info('done. time used: %s', used)
        return result

    wrapper.logger = logger
    return wrapper