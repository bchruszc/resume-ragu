"""HTTP routes for AI chat interactions."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.ai.client import AIClient, AnthropicClient
from app.models import ChatRequest, ChatResponse
from app.services import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


# Dependency for AI client (allows tests to inject MockAIClient)
def get_ai_client() -> AIClient:
    """Get AI client instance."""
    return AnthropicClient()


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    ai_client: Annotated[AIClient, Depends(get_ai_client)],
) -> ChatResponse:
    """
    Generate resume content via AI chat.

    The frontend maintains conversation history and sends the full message array
    with each request. The backend is stateless.
    """
    message, usage = await chat_service.generate_resume(
        user_id=request.user_id,
        messages=request.messages,
        ai_client=ai_client,
    )

    return ChatResponse(message=message, usage=usage)
