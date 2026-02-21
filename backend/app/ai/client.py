"""AI client interface and Anthropic implementation."""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

from anthropic import Anthropic, APIError, AuthenticationError, RateLimitError

from app.config import settings
from app.errors import AIServiceError

logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    """Response from AI generation."""

    content: str
    model: str
    usage: dict[str, int]  # input_tokens, output_tokens


class AIClient(ABC):
    """Abstract AI client interface."""

    @abstractmethod
    async def generate(
        self, system_prompt: str, messages: list[dict], model: str | None = None
    ) -> AIResponse:
        """
        Generate AI response.

        Args:
            system_prompt: System prompt to set context
            messages: List of message dicts with 'role' and 'content'
            model: Optional model override (uses default if not provided)

        Returns:
            AIResponse with content, model, and usage info

        Raises:
            AIServiceError: If generation fails
        """
        pass


class AnthropicClient(AIClient):
    """Anthropic Claude implementation of AIClient."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize Anthropic client.

        Args:
            api_key: Anthropic API key (defaults to settings.ANTHROPIC_API_KEY)
        """
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.default_model = settings.MODEL_NAME
        logger.info(f"Initialized Anthropic client with model {self.default_model}")

    async def generate(
        self, system_prompt: str, messages: list[dict], model: str | None = None
    ) -> AIResponse:
        """
        Generate response using Anthropic Claude.

        Args:
            system_prompt: System prompt
            messages: Message history
            model: Optional model override

        Returns:
            AIResponse

        Raises:
            AIServiceError: If API call fails
        """
        model_to_use = model or self.default_model

        try:
            start_time = time.time()

            response = self.client.messages.create(
                model=model_to_use,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
            )

            elapsed = time.time() - start_time

            # Extract usage info
            usage = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }

            # Extract text content
            content = ""
            for block in response.content:
                if block.type == "text":
                    content += block.text

            logger.info(
                f"AI generation completed: model={model_to_use}, "
                f"input_tokens={usage['input_tokens']}, "
                f"output_tokens={usage['output_tokens']}, "
                f"elapsed={elapsed:.2f}s"
            )

            return AIResponse(content=content, model=model_to_use, usage=usage)

        except AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            raise AIServiceError("AI service authentication failed")
        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise AIServiceError("AI service rate limit exceeded, please try again later")
        except APIError as e:
            logger.error(f"API error: {e}")
            raise AIServiceError(f"AI service error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during AI generation: {e}")
            raise AIServiceError(f"Unexpected AI service error: {str(e)}")
