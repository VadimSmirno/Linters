import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(levelname)s] %(filename)s:%(lineno)d - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
