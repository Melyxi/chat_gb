import project_chat.client.client_log_config
import logging
import json
from functools import wraps

import inspect
logger = logging.getLogger('client')

def log_auth_client(func):
    @wraps(func)
    def deco(*args, **kwargs):
        st = inspect.stack()
        f = func(*args, **kwargs)
        logger.debug(f"Сообщение от сервера: {f}")
        return func(*args, **kwargs)

    return deco

def log_msg_client(func):
    @wraps(func)
    def deco(*args, **kwargs):
        st = inspect.stack()
        try:
            f = func(*args, **kwargs)
            f = json.loads(f.decode('utf-8'))
            logger.debug(f"Сообщение отправлено {f}. вызвана из функции {st[1].function}")
            return func(*args, **kwargs)

        except BaseException as e:
            logger.exception(f"Сообщение не отправлено. вызвана из функции {st[1].function}")
    return deco

def log_server_code(func):
    @wraps(func)
    def deco(*args, **kwargs):
        st = inspect.stack()
        try:
            f = func(*args, **kwargs)

            logger.debug(f'Сообщение от сервера {f}. вызвана из функции {st[1].function}')
            return func(*args, **kwargs)

        except BaseException as e:
            logger.exception(f"Сообщение не отправлено. вызвана из функции {st[1].function}")
    return deco

