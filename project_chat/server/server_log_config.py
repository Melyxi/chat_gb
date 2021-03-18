# from logging.handlers import TimedRotatingFileHandler
import logging as logging
from logging.handlers import TimedRotatingFileHandler
# add filemode="w" to overwrite
import os

logger = logging.getLogger("server")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
# create the logging file handler
path_log = os.path.join(os.getcwd(), 'log\\server.log')



rotation_logging_handler = TimedRotatingFileHandler(path_log, when='d', interval=1, backupCount=5, encoding='utf-8')

rotation_logging_handler.setFormatter(formatter)

rotation_logging_handler.setLevel(logging.DEBUG)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
#logger.addHandler(fh)
logger.addHandler(rotation_logging_handler)
logger.setLevel(logging.DEBUG)



