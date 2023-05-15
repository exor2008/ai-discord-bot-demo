import logging
import os

logger = logging.getLogger("AIbot logger")
logger.setLevel(os.environ["LOG_LEVEL"])
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

logger_file = logging.getLogger("AIbot file-logger")
logger_file.setLevel(os.environ["LOG_LEVEL"])
formatter_file = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler_file = logging.StreamHandler(open("log.txt", mode="at"))
handler_file.setFormatter(formatter_file)
logger_file.addHandler(handler_file)
