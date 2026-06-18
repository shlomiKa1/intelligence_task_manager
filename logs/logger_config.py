from config import LOGS_FILE
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOGS_FILE, encoding="utf-8")]
)

logger = logging.getLogger(__name__)