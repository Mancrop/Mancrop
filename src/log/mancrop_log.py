import logging
import logging.config

# 定义日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 'file': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'filename': 'app.log',
        #     'formatter': 'detailed'
        # },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


def log_init(path: str | None = None):
    logging.config.dictConfig(LOGGING_CONFIG)
    if path is not None:
        try:
            handler = logging.FileHandler(path)
            handler.set_name("file")
            handler.setFormatter(logging.Formatter(LOGGING_CONFIG['formatters']['detailed']['format']))
            logging.getLogger('').addHandler(handler)
        except Exception:
            pass
