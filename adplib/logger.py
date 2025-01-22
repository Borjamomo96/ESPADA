import logging
import os
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[34m",  # BLUE
        logging.INFO: "\033[32m",  # GREEN
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



class Initial_Logger:
    _logger_instance = None  # Variable de clase para almacenar la instancia del logger

    @classmethod
    def initial_setup_logger(cls):
        
        if cls._logger_instance is None:
            logger = logging.getLogger("initial_adpalmap_logger")
            logger.setLevel(logging.INFO)

            # Configuración básica (solo consola)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(ColoredFormatter())

            if logger.hasHandlers():
                logger.handlers.clear()

            logger.addHandler(console_handler)

            cls._logger_instance = logger


    @classmethod
    def get_initial_logger(cls):
        
        if cls._logger_instance is None:
            cls.initial_setup_logger()
        return cls._logger_instance
    
class Logger:
    _logger_instance = None

    @classmethod
    def setup_logger(cls, log_path="adpalmap.log", clear_logs=False):
        
        """Configura el logger si no está configurado."""
        if cls._logger_instance is None:
            logger = logging.getLogger("adpalmap_logger")
            logger.setLevel(logging.INFO)
            
            log_path = Path(log_path)

            # Limpiar el archivo de logs si es necesario
            
            if clear_logs and log_path.exists():
                
                with open(log_path, 'w') as file:
                    file.write("")

            if not log_path.exists():
                log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(log_path, 'w') as file:
                    file.write("")

            
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(module)s: - %(message)s"))
            #file_handler.setFormatter(ColoredFormatter()) #Para añadir al archivo .log este formato no lo entiende bien. 
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(ColoredFormatter())

            
            if logger.hasHandlers():
                logger.handlers.clear()

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

            cls._logger_instance = logger


    @classmethod
    def get_logger(cls, log_path="adpalmap.log", clear_logs=False ):
        
        if cls._logger_instance is None:
            cls.setup_logger(log_path=log_path, clear_logs=clear_logs)
        return cls._logger_instance
    
    @classmethod
    def raw(cls, message):
        """Añade un mensaje sin formato al archivo .log."""
        if cls._logger_instance is not None:
            for handler in cls._logger_instance.handlers:
                if isinstance(handler, logging.StreamHandler) or isinstance(handler, logging.FileHandler):  
                    handler.stream.write(message + "\n")
                    handler.flush()
    


    


