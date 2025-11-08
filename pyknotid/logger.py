"""
Logging configuration for pyknotid.

This module provides a centralized logging setup for the pyknotid package.
Use this instead of print statements for debug and informational output.

Example usage:
    from pyknotid.logger import get_logger

    logger = get_logger(__name__)
    logger.debug("Debug information")
    logger.info("Processing knot...")
    logger.warning("Potential issue detected")
    logger.error("Error occurred")
"""

import logging
import sys
from typing import Optional

# Default log format
DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
SIMPLE_FORMAT = '%(levelname)s: %(message)s'

# Global logger cache
_loggers = {}


def get_logger(name: str = 'pyknotid', level: Optional[int] = None) -> logging.Logger:
    """
    Get or create a logger with the specified name.

    Parameters
    ----------
    name : str
        The name of the logger, typically __name__ from the calling module
    level : int, optional
        The logging level (e.g., logging.DEBUG, logging.INFO)
        If None, uses the environment variable PYKNOTID_LOG_LEVEL or INFO

    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)

    # Only configure if no handlers exist
    if not logger.handlers:
        # Determine log level
        if level is None:
            import os
            level_name = os.environ.get('PYKNOTID_LOG_LEVEL', 'INFO')
            level = getattr(logging, level_name.upper(), logging.INFO)

        logger.setLevel(level)

        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(SIMPLE_FORMAT)
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

    _loggers[name] = logger
    return logger


def set_log_level(level: int, logger_name: Optional[str] = None):
    """
    Set the log level for a specific logger or all pyknotid loggers.

    Parameters
    ----------
    level : int
        The logging level (e.g., logging.DEBUG, logging.INFO)
    logger_name : str, optional
        The name of the logger to configure. If None, sets level for all
        cached loggers
    """
    if logger_name:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)
    else:
        # Set level for all cached loggers
        for logger in _loggers.values():
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)


def configure_logger(
    name: str = 'pyknotid',
    level: int = logging.INFO,
    format_string: str = SIMPLE_FORMAT,
    stream=sys.stdout
) -> logging.Logger:
    """
    Configure a logger with custom settings.

    Parameters
    ----------
    name : str
        The name of the logger
    level : int
        The logging level
    format_string : str
        The format string for log messages
    stream : file-like
        The output stream (default: sys.stdout)

    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add new handler
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    _loggers[name] = logger
    return logger


# Create a default logger for convenience
default_logger = get_logger('pyknotid')
