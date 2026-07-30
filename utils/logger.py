"""
Sentinel — Logger Utility
Provides structured logging for the enterprise support platform.
"""
import sys
from pathlib import Path
from loguru import logger as _loguru_logger

from config.openai_config import openai_settings

# Remove default logger
_loguru_logger.remove()

# Console handler with color
_loguru_logger.add(
    sys.stdout,
    level=openai_settings.LOG_LEVEL,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> — "
        "<level>{message}</level>"
    ),
)


def setup_logger(name: str) -> "logger":
    """Return a bound logger with module name context."""
    return _loguru_logger.bind(name=name)
