import logging
import os
import sys
import inspect
from collections import deque
from pathlib import Path
from datetime import datetime
from logging.handlers import QueueHandler


class ColoredFormatter(logging.Formatter):
    """
    Formatter that adds ANSI colors to console log records.
    """

    COLORS = {
        logging.DEBUG: "\033[34m",  # BLUE
        logging.INFO: "\033[32m",  # GREEN
        logging.WARNING: "\033[38;5;214m",  # ORANGE
        logging.ERROR: "\033[31m",  # RED
        logging.CRITICAL: "\033[1;31m",  # BOLD RED
    }
    MODULE_COLOR = "\033[38;5;45m"  # Neon blue

    def format(self, record):
        """
        Format a log record with colored level and module names.
        """

        RESET = "\033[0m"
        color = self.COLORS.get(record.levelno, RESET)
        record.levelname = f"{color}{record.levelname}{RESET}"
        record.module = f"{self.MODULE_COLOR}{record.module}{RESET}"
        format_string = "| %(levelname)s | [PID:%(process)d]  %(module)s: - %(message)s"
        formatter = logging.Formatter(format_string)
        return formatter.format(record)


class Initial_Logger:
    """
    Early-process logger used before the full ESPADA logger is configured.
    """

    _instance = None
    _buffer = deque(maxlen=1000)  
    
    def __new__(cls):
        """
        Return the singleton early logger instance.
        """

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup()
        return cls._instance
    
    def _setup(self):
        """
        Configure the early console logger.
        """

        self.logger = logging.getLogger("initial_espada_logger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColoredFormatter()) 
        self.logger.addHandler(handler)
    
    def _log(self, level, msg):
        """
        Log a message and keep it in the early-message buffer.
        """

        self.logger.log(level, msg)
        self._buffer.append((level, msg, datetime.now()))
    
    def debug(self, msg): self._log(logging.DEBUG, msg)
    def info(self, msg): self._log(logging.INFO, msg)
    def warning(self, msg): self._log(logging.WARNING, msg)
    def error(self, msg): self._log(logging.ERROR, msg)
    def critical(self, msg): self._log(logging.CRITICAL, msg)
    
    def get_buffer(self):
        """
        Return buffered messages collected before full logger setup.
        """

        return list(self._buffer)
    
    def clear_buffer(self):
        """
        Clear buffered early messages.
        """

        self._buffer.clear()


RAW_LEVEL = 15
logging.addLevelName(RAW_LEVEL, "RAW")

class CustomFormatter(logging.Formatter):
    """
    Formatter that leaves RAW log records undecorated.
    """

    def format(self, record):
        """
        Format RAW records as plain messages and all other records normally.
        """

        if record.levelno == RAW_LEVEL:
            return record.getMessage()
        return super().format(record)


class Logger:
    """
    Shared ESPADA logger wrapper for console, file, and raw log output.
    """

    # This singleton pattern is redundant
    _logger_instance = None
    _log_queue = None
    _log_path = None

    @classmethod
    def setup_logger(
        cls, output_dir=None, log_path="espada.log", 
        clear_logs=False, queue=None, early_buffer=None, debug_mode=False
    ):
        """
        Configure the shared ESPADA logger.

        Parameters
        ----------
        output_dir : pathlib.Path, optional
            Base directory where log files are written.
        log_path : str or pathlib.Path, optional
            Requested log path relative to output_dir, unless it is an accepted absolute path.
        clear_logs : bool, optional
            Remove previous log files in the selected log directory.
        queue : multiprocessing.Queue, optional
            Queue used by worker processes to forward log records.
        early_buffer : list, optional
            Reserved for early logger records.
        debug_mode : bool, optional
            Enable DEBUG level logging when true.
        """
        
        _ = early_buffer

        logger = logging.getLogger("espada_logger")
        logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

        if log_path is None or log_path == '':
            log_path = "log_dir/espada.log"

        timestamp = datetime.now().strftime("%d%m%y_%H%M%S")
        log_path_obj = Path(log_path).expanduser()

        warning_messages = []

    ##############################################################################################
        if log_path_obj.is_absolute():
            try:
                abs_output_dir = output_dir.resolve()
                abs_log_path = log_path_obj.resolve()
                
                if abs_output_dir in abs_log_path.parents:
                    final_log_path = log_path_obj
                else:
                    final_log_path = output_dir / "log_dir/espada.log"
                    warning_messages.append(
                        f"The absolute path '{log_path_obj}' is outside of output_dir. "
                        f"Using default path: {final_log_path}"
                    )
            
            except Exception as e:
                final_log_path = output_dir / "log_dir/espada.log"
                warning_messages.append(
                    f"Error processing absolute path: {e}. "
                    f"Using default path: {final_log_path}"
                )
                

        else:
            final_log_path = output_dir / log_path_obj
        

        timestamp = datetime.now().strftime("%d%m%y_%H%M%S")
        original_stem = final_log_path.stem
        new_stem = f"raw_{original_stem}_{timestamp}"
        final_log_path = final_log_path.with_name(new_stem).with_suffix(final_log_path.suffix)

        # Clear existing logs if requested
        if clear_logs:
            # Remove older logs of the same type
            log_dir = final_log_path.parent
            #base_name = original_path.stem.split('_')[0]  
            #{base_name}_
            pattern = f"*{final_log_path.suffix}"
            
            
            for old_log in log_dir.glob(pattern):
                if old_log != final_log_path:  # Keep the new file
                    try:
                        old_log.unlink()
                    except Exception as e:
                        warning_messages.append(f"Error deleting {old_log}: {e}")

        if not final_log_path.exists():
            final_log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(final_log_path, 'w') as file:
                file.write("")
    ##############################################################################################
        
        file_handler = logging.FileHandler(final_log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG if debug_mode else RAW_LEVEL)
        file_handler.setFormatter(
            CustomFormatter(
                "%(asctime)s | %(levelname)s | [PID:%(process)d] %(module)s: - %(message)s"
            )
        )
        # ColoredFormatter writes ANSI codes that do not fit the plain .log format.
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
        console_handler.setFormatter(ColoredFormatter())
        if not debug_mode:
            console_handler.addFilter(lambda record: record.levelno >= logging.INFO)

        
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._logger_instance = logger
        cls._log_queue = queue
        cls._log_path = final_log_path

    ##############################################################################################

        # Dump Initial_Logger buffer to file
        early_logger = Initial_Logger()
        early_buffer = early_logger.get_buffer()
        
        for level, msg, dt in early_buffer:
            record = logging.LogRecord(
                name="espada_logger",
                level=level,
                pathname="",
                lineno=0,
                msg=msg,
                args=(),
                exc_info=None
            )
            record.module = "init"  # Generic module for early messages
            record.created = dt.timestamp()  
            
            file_handler.handle(record)

        early_logger.clear_buffer()

        # Issue accumulated warnings during setup
        for msg in warning_messages:
            logger.warning(msg)


    @classmethod
    def get_logger(
        cls, output_dir=None, log_path="espada.log", clear_logs=False, queue=None, debug_mode=False
    ):
        """
        Return the configured logger, creating it if needed.
        """
        
        if cls._logger_instance is None:
            cls.setup_logger(
                output_dir, log_path=log_path, clear_logs=clear_logs, 
                queue=queue, debug_mode=debug_mode
                )
        return cls._logger_instance
    

    @classmethod
    def raw(cls, message):
        """
        Add a raw message to the terminal and log file.
        """

        if cls._logger_instance is not None:
            cls._logger_instance.log(RAW_LEVEL, message)
        else:
            print("PUUFF")
    

    @classmethod
    def echo(cls, message):
        """
        Write a plain text message directly to the console 
        and to the log file.
        """
        # Console
        print(message)
        
        # Log file (raw write)
        if cls._logger_instance is not None:
            for handler in cls._logger_instance.handlers:
                if isinstance(handler, logging.FileHandler):
                    try:
                        # Write additional plain text
                        handler.stream.write(message + '\n')
                        handler.stream.flush()
                    except Exception:
                        pass  # If it fails, it simply doesn't write to the file


    @classmethod
    def log_to_file(cls, level, message):
        """
        Write a message only to the log file using the standard log format.
        """

        if cls._logger_instance is not None:
            frame = inspect.currentframe().f_back
            module_name = frame.f_globals.get("__name__", "Unknown module")
            # Keep only the file name, not the full module path.
            module_name = os.path.basename(module_name.split(".")[-1])

            record = cls._logger_instance.makeRecord(
                cls._logger_instance.name, 
                level, fn=None, lno=0, msg=message, args=None, 
                exc_info=None
            )
            record.module = module_name

            for handler in cls._logger_instance.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.handle(record)
                    handler.flush()


    @classmethod
    def get_log_filename(cls):
        """Returns the name of the associated log file."""
        if cls._log_path:
            return cls._log_path.resolve()
        return None
