import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
# add filemode="w" to overwrite

logger = logging.getLogger("client")

formatter = logging.Formatter("%(asctime)s - %(levelname)s -%(module)s- %(message)s ")
# create the logging file handler
path_log = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'log\\client.log')
fh = logging.FileHandler(path_log, encoding='utf-8')

fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)