import logging
import os
from logging.handlers import RotatingFileHandler

LOG_LEVEL = logging.DEBUG

# Create a log directory if it does not exist
LOG_DIR = 'log'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file settings
LOG_FILE = os.path.join(LOG_DIR, 'main.log')
MAX_LOG_SIZE = 1024 * 1024
BACKUP_COUNT = 10

# Create a rotating file handler
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
)

file_handler.setLevel(LOG_LEVEL)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# Create a formatter with timestamps
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Create a logger
logger = logging.getLogger('getTheCat')
logger.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Function to use the logger
def get_logger():
    return logger

# Example usage
if __name__ == "__main__":
    log = get_logger()
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
