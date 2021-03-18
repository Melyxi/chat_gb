import logging
import os
# add filemode="w" to overwrite

logger = logging.getLogger("client")

formatter = logging.Formatter("%(asctime)s - %(levelname)s -%(module)s- %(message)s ")
# create the logging file handler
path_log = os.path.join(os.getcwd(), 'log\\client.log')
rotation_logging_handler = TimedRotatingFileHandler(path_log, when='h', interval=1, backupCount=5, encoding='utf-8')

rotation_logging_handler.setFormatter(formatter)

rotation_logging_handler.setLevel(logging.DEBUG)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
#logger.addHandler(fh)
logger.addHandler(rotation_logging_handler)
logger.setLevel(logging.DEBUG)