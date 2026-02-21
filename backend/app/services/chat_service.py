"""Business logic for AI chat interactions."""

import logging
import time

from app.ai.client import AIClient
from app.ai import guardrails, prompts
from app.models import ChatMessage
from app.services import profile_service

logger = logging.getLogger(__name__)


async def generate_resume(
    user_id: str, messages: list[ChatMessage], ai_client: AIClient
) -> tuple[ChatMessage, dict[str, int]]:
    """
    Generate resume content using AI.

    Args:
        user_id: The user ID
        messages: Conversation history
        ai_client: AI client to use for generation

    Returns:
        Tuple of (assistant ChatMessage, usage dict with token counts)

    Raises:
        NotFoundError: If profile not found
        AIServiceError: If AI generation fails
    """
    start_time = time.time()

    # Load user profile
    profile = profile_service.get_profile(user_id)
    logger.info(f"Loaded profile for user {user_id}: {len(profile.jobs)} jobs, "
                f"{len(profile.accomplishments)} accomplishments")

    # Validate conversation
    validated_messages = guardrails.validate_conversation(messages)
    logger.info(f"Validated {len(validated_messages)} messages for user {user_id}")

    # Build system prompt with profile context
    system_prompt, formatted_messages = prompts.build_messages(
        profile, validated_messages
    )

    # Generate AI response
    response = await ai_client.generate(system_prompt, formatted_messages)

    elapsed = time.time() - start_time

    # Create response message
    assistant_message = ChatMessage(role="assistant", content=response.content)

    logger.info(
        f"Generated resume for user {user_id}: "
        f"input_tokens={response.usage['input_tokens']}, "
        f"output_tokens={response.usage['output_tokens']}, "
        f"elapsed={elapsed:.2f}s"
    )

    return assistant_message, response.usage
