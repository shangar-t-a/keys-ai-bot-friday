"""Logging Module for Friday."""

# Standard Library
import os
from pathlib import Path
from typing import Annotated, Literal
import logging
from logging.handlers import RotatingFileHandler

# Third Party Library
from dotenv import load_dotenv
from colorlog import ColoredFormatter


# Load Environment Variables
load_dotenv()


class CustomLogger:
    """
    Custom Logger for Friday AI Personal Assistant.

    Attributes:
        name (str): Name of the Logger.
        log_level (Annotated[log_levels, str]): Log Level.
        logger (logging.Logger): Logger Object.
    """

    log_levels = Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __new__(cls, *args, **kwargs):
        """Create a new instance of the Logger. Return the Logger Object created from CustomLogger when initialized."""
        instance = super(CustomLogger, cls).__new__(cls)
        instance.__init__(*args, **kwargs)
        return instance.logger

    def __init__(self, name: str = "friday", log_level: Annotated[log_levels, str] = "DEBUG") -> None:
        """
        Initialize the CustomLogger.

        Args:
            name (str): Name of the Logger (Default: "friday").
            log_level (Annotated[log_levels, str]): Log Level (Default: "DEBUG").
        """
        self.name = name
        self.log_level = log_level

        log_dir = os.getenv("FRIDAY_LOG_DIR")
        if log_dir and Path(log_dir).exists():
            log_path = Path(log_dir) / f"{name}.log"
        else:
            default_log_dir = Path(__file__).parent.parent.parent / ".friday_cache" / "logs"
            if not default_log_dir.exists():
                default_log_dir.mkdir(parents=True, exist_ok=True)
            log_path = Path(__file__).parent.parent.parent / ".friday_cache" / "logs" / f"{name}.log"

        self.logger = self.__create_logger(log_path=log_path)

    def __create_logger(self, log_path: Path) -> logging.Logger:
        """
        Create and configure the logger.

        Include Console and Rotating File Handlers. Color Logging for Console. Plain Logging for File. The Log File
        will be rotated when it reaches 10KB and will keep the last 5 logs.

        Args:
            log_path (Path): Valid Path to the Log File.
        Returns:
            logging.Logger: Logger Object.
        """
        plain_log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        color_log_format = "%(log_color)s" + plain_log_format
        log_file_max_size = 100 * 1024
        log_file_max_backup = 5

        # Create Logger
        logger = logging.getLogger(self.name)
        logger.setLevel(self.log_level)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)

        # Create a color logging format
        color_formatter = ColoredFormatter(color_log_format)
        console_handler.setFormatter(color_formatter)

        # Create a rotating file handler
        rot_file_handler = RotatingFileHandler(log_path, maxBytes=log_file_max_size, backupCount=log_file_max_backup)
        rot_file_handler.setLevel(self.log_level)

        # Create a basic logging format
        plain_formatter = logging.Formatter(plain_log_format)
        rot_file_handler.setFormatter(plain_formatter)

        # Set the handlers
        logger.addHandler(rot_file_handler)
        logger.addHandler(console_handler)

        return logger


if __name__ == "__main__":
    logger = CustomLogger(name="friday", log_level="DEBUG")
    logger.debug("Friday Logger Initialized...")
    logger.info("Friday Logger Initialized...")
    logger.warning("Friday Logger Initialized...")
    logger.error("Friday Logger Initialized...")
    logger.critical("Friday Logger Initialized...")
