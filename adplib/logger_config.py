import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[34m",  # BLUE
        logging.INFO: "\033[32m",   # GREEN
        logging.WARNING: "\033[38;5;214m",  # ORANGE
        logging.ERROR: "\033[31m",  # RED
        logging.CRITICAL: "\033[1;31m",  # BOLD RED
    }
    MODULE_COLOR = "\033[38;5;45m"  # Neon blue

    def format(self, record):
        RESET = "\033[0m"
        color = self.COLORS.get(record.levelno, RESET)
        record.levelname = f"{color}{record.levelname}{RESET}"
        record.module = f"{self.MODULE_COLOR}{record.module}{RESET}"
        format_string = "| %(levelname)s | %(module)s: - %(message)s"
        formatter = logging.Formatter(format_string)
        return formatter.format(record)

def setup_logger(name="ColoredLogger", level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Evita duplicar handlers
        logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)
    return logger
