"""Input validation and safety guardrails for AI interactions."""

import logging
import re

from app.config import settings
from app.errors import ValidationError
from app.models import ChatMessage

logger = logging.getLogger(__name__)

# Maximum message length (characters)
MAX_MESSAGE_LENGTH = 10000

# Common prompt injection patterns to detect and sanitize
INJECTION_PATTERNS = [
    r"ignore all previous instructions",
    r"disregard all previous",
    r"you are now",
    r"your new instructions",
    r"system:",
    r"</system>",
    r"<system>",
    r"assistant:",
    r"</assistant>",
    r"<assistant>",
]


def validate_message(content: str) -> str:
    """
    Validate and sanitize a single message.

    Args:
        content: Message content to validate

    Returns:
        Validated (possibly sanitized) message content

    Raises:
        ValidationError: If message exceeds length limit
    """
    # Check length
    if len(content) > MAX_MESSAGE_LENGTH:
        raise ValidationError(
            f"Message exceeds maximum length of {MAX_MESSAGE_LENGTH} characters"
        )

    # Basic sanitization: detect common prompt injection patterns
    original = content
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            # Replace suspicious patterns with harmless text
            content = re.sub(pattern, "[filtered]", content, flags=re.IGNORECASE)

    if content != original:
        logger.warning(
            f"Message sanitized: removed potential prompt injection patterns"
        )

    return content


def validate_conversation(messages: list[ChatMessage]) -> list[ChatMessage]:
    """
    Validate a full conversation.

    Enforces MAX_CONVERSATION_TURNS limit and validates each message.

    Args:
        messages: List of chat messages

    Returns:
        Validated (possibly truncated) message list
    """
    max_turns = settings.MAX_CONVERSATION_TURNS

    # Truncate to most recent N turns if exceeded
    if len(messages) > max_turns:
        logger.warning(
            f"Conversation exceeds {max_turns} turns, truncating to most recent messages"
        )
        messages = messages[-max_turns:]

    # Validate each message
    validated = []
    for msg in messages:
        sanitized_content = validate_message(msg.content)
        validated.append(
            ChatMessage(role=msg.role, content=sanitized_content)
        )

    return validated
