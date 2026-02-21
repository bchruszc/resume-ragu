"""Prompt construction and context injection for AI interactions."""

import json
import logging
from pathlib import Path

from app.models import Profile, ChatMessage

logger = logging.getLogger(__name__)

# Cache for system prompt (loaded once from disk)
_system_prompt_cache: str | None = None


def load_system_prompt() -> str:
    """
    Load the system prompt from file.

    Caches after first read for performance.

    Returns:
        System prompt text
    """
    global _system_prompt_cache

    if _system_prompt_cache is not None:
        return _system_prompt_cache

    prompt_path = Path(__file__).parent.parent / "prompts" / "resume_system.txt"

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            _system_prompt_cache = f.read()
        logger.info("Loaded system prompt from disk")
        return _system_prompt_cache
    except Exception as e:
        logger.error(f"Failed to load system prompt: {e}")
        raise


def build_messages(
    profile: Profile, conversation: list[ChatMessage]
) -> tuple[str, list[dict]]:
    """
    Build system prompt with profile context and format messages for AI client.

    Args:
        profile: User's career profile
        conversation: List of chat messages

    Returns:
        Tuple of (system_prompt_with_context, formatted_messages)
    """
    # Load base system prompt
    base_prompt = load_system_prompt()

    # Serialize profile to JSON for context injection
    profile_json = profile.model_dump(by_alias=True)
    profile_str = json.dumps(profile_json, indent=2)

    # Inject profile data into system prompt
    system_prompt = f"""{base_prompt}

# User's Career Profile Data

<profile>
{profile_str}
</profile>

Use this career data to generate resume content. Reference specific accomplishments, jobs, skills, and projects as needed.
"""

    # Format conversation messages for AI client
    formatted_messages = [
        {"role": msg.role, "content": msg.content} for msg in conversation
    ]

    logger.info(
        f"Built prompt with {len(conversation)} messages and profile data "
        f"({len(profile.jobs)} jobs, {len(profile.accomplishments)} accomplishments)"
    )

    return system_prompt, formatted_messages
