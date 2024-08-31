"""Exceptions for the friday Module."""

from friday.utilities import logger


class FridayBaseException(Exception):
    """
    Friday Base Exception.

    Attributes:
        message (str): Message for the exception.
        logger (logger.CustomLogger): Logger for the exception.
    """

    def __init__(self, message: str = "Friday Base Exception...", logger: logger.CustomLogger = None) -> None:
        """
        Initialize Friday Base Exception.

        Args:
            message (str, optional): Message for the exception. Defaults to "Friday Base Exception...".
            logger (logger.CustomLogger, optional): Logger for the exception. Defaults to None.
        """
        self.message = message
        self.logger = logger
        super().__init__(self.message)
        if logger:
            logger.error(message)
