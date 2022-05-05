from helpers import call_pycode_method

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def log(log_level, log_type, message):
    if log_level.upper() not in LOG_LEVELS:
        raise ValueError('log_level must be one of {}'.format(LOG_LEVELS))

    call_pycode_method(
        method='telegramlog',
        data=dict(
            log_level=log_level,
            log_type=log_type,
            message=message,
        ),
    )


def debug(log_type, message):
    log(log_level='DEBUG', log_type=log_type, message=message)


def info(log_type, message):
    log(log_level='INFO', log_type=log_type, message=message)


def warning(log_type, message):
    log(log_level='WARNING', log_type=log_type, message=message)


def error(log_type, message):
    log(log_level='ERROR', log_type=log_type, message=message)


def critical(log_type, message):
    log(log_level='CRITICAL', log_type=log_type, message=message)
