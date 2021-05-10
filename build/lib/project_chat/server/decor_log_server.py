import server.server_log_config
import logging
from functools import wraps
import inspect
logger = logging.getLogger('server')


def log_client(func):
    @wraps(func)
    def deco(*args, **kwargs):
        st = inspect.stack()

        logger.debug(f"Сообщение от клиента. вызвана из функции {st[1].function}")
        return func(*args, **kwargs)

    return deco

def log_msg(func):
    @wraps(func)
    def deco(*args, **kwargs):
        st = inspect.stack()
        logger.debug(f"Ответ клиенту от сервера. вызвана из функции {st[1].function} ")
        return func(*args, **kwargs)
    return deco




def log_auth(func):
    @wraps(func)
    def deco(*args, **kwargs):
        st = inspect.stack()
        logger.debug(f"Аунтификация. вызвана из функции {st[1].function}")
        return func(*args, **kwargs)
    return deco

