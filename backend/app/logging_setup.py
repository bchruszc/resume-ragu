"""Centralized logging configuration with per-request context."""

import contextvars
import logging

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)
user_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "user_id", default="-"
)

LOG_FORMAT = (
    "%(asctime)s %(levelname)s [%(request_id)s] [%(user_id)s] %(name)s: %(message)s"
)


class ContextFilter(logging.Filter):
    """Injects request_id and user_id from contextvars into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        record.user_id = user_id_var.get()
        return True


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application. Call once at startup."""
    level = getattr(logging, log_level.upper(), logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handler.addFilter(ContextFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)
