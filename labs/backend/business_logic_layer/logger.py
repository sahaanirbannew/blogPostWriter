import logging
import os
import datetime
import traceback

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Get today's date for log filename
log_filename = os.path.join(LOG_DIR, f"{datetime.date.today()}.log")

# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Capture all log levels
    format="%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | Line: %(lineno)d | %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

logger = logging.getLogger(__name__)

def log_exception(exc):
    """Logs an exception with traceback."""
    logger.error("Exception occurred: %s", traceback.format_exc())