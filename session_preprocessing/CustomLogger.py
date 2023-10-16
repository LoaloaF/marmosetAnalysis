import os
import logging
import config
import datetime

class CustomLogger:
    """
    A customizable logger class that simplifies Python logging.

    Usage:
    - Create an instance with a desired name and optional log file directory.
    - Use the provided methods to log messages at different levels.
    - Call the 'spacer' method to insert a separator line in the log.

    Attributes:
    - name (str): The name of the logger, typically corresponding to the module or script.
    - logger (logging.Logger): The logger object for logging messages.
    - Default formatters for console and file logging.
    - Spacer formatter for visually separating log entries.
    """

    def __init__(self, name, write_to_directory=None):
        """
        Initialize the logger with the given name and optional log file directory.

        Args:
        - name (str): The name of the logger.
        - write_to_directory (str, optional): The directory where log files will be written.
        """
        # Create a logger with the provided name
        self._name = name
        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(config.LOGGING_LEVEL)

        console_fmt = config.CONSOLE_LOGGING_FMT + config.LOGGING_FMT_MSG
        file_fmt = config.CONSOLE_LOGGING_FMT + config.LOGGING_FMT_MSG
        self._default_console_fmtr = self._create_formatter(console_fmt)
        self._default_file_fmtr = self._create_formatter(file_fmt)

        self._console_hdlr = self._create_console_logger()
        self._logger.addHandler(self._console_hdlr)

        self._file_hdlr = None
        if write_to_directory is not None:
            self._file_hdlr = self._create_logfile_handler(write_to_directory)
            self._logger.addHandler(self._file_hdlr)
        
    def _create_formatter(self, fmt):
        return logging.Formatter(fmt)
    
    def _create_console_logger(self):
        """
        Set up console logging with the default formatter.
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._default_console_fmtr)
        return console_handler
    
    def _create_logfile_handler(self, write_to_directory):
        """
        Set up file-based logging with the default file formatter.

        Args:
        - write_to_directory (str): The directory where log files will be written.
        """
        try:
            tstamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_fname = f"{tstamp}_{self._name}.log"
            log_fullfname = os.path.join(write_to_directory, log_fname)
            
            file_handler = logging.FileHandler(log_fullfname)
            file_handler.setFormatter(self._default_file_fmtr)
            return file_handler
        
        except FileNotFoundError as e:
            print(f"{e} Won't log to file.")

    def _switch_spacer_fmt(self):
        """
        Toggle between default formatter and spacer formatter for all handlers.
        """
        is_default = self._logger.handlers[0].formatter == self._default_console_fmtr
        if is_default:
            spacer_fmtr = self._create_formatter(config.SPACER_LOGGING_FMT)
            [han.setFormatter(spacer_fmtr) for han in self._logger.handlers]
        else:
            fmts = (self._default_console_fmtr, self._default_file_fmtr)
            [han.setFormatter(fmt) for han, fmt in zip(self._logger.handlers, fmts)]

    def extend_fmt(self, exten):
        console_fmt = config.CONSOLE_LOGGING_FMT + exten + config.LOGGING_FMT_MSG
        file_fmt = config.CONSOLE_LOGGING_FMT + exten + config.LOGGING_FMT_MSG
        self._default_console_fmtr = self._create_formatter(console_fmt)
        self._default_file_fmtr = self._create_formatter(file_fmt)

        self._console_hdlr.setFormatter(self._default_console_fmtr)
        self._file_hdlr.setFormatter(self._default_file_fmtr)

    def spacer(self):
        """
        Insert a separator line in the log to visually separate log entries.
        """
        self._switch_spacer_fmt()
        self._logger.info('')  # log a separator line
        self._switch_spacer_fmt()

    def debug(self, msg):
        """
        Log a debug-level message.

        Args:
        - msg (str): The message to log.
        """
        self._logger.debug(msg)

    def info(self, msg):
        """
        Log an info-level message.

        Args:
        - msg (str): The message to log.
        """
        # self._logger.info(msg)
        self._log_msg(msg, self._logger.info)

    
    def warning(self, msg):
        """
        Log a warning-level message.

        Args:
        - msg (str): The message to log.
        """
        self._log_msg(msg, self._logger.warning)
    
    def error(self, msg):
        """
        Log an error-level message.

        Args:
        - msg (str): The message to log.
        """
        self._logger.error(msg)
    
    def critical(self, msg):
        """
        Log a critical-level message.

        Args:
        - msg (str): The message to log.
        """
        self._logger.critical(msg)

    def _log_msg(self, msg, log_func):
        if isinstance(msg, (list, tuple)):
            log_func("\n\t".join(msg))
        else:
            log_func(msg)



if __name__ == "__main__":
    custom_logger = CustomLogger(__name__, './logs')
    custom_logger.info('This is a regular log message.')
    custom_logger.spacer()
    custom_logger.info('This is another regular log message.')
