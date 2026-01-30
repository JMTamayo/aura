from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.api.security.api_key import get_api_key
from app.domain.agent import Aura
from app.models.agent import (
    ENTITY_SYSTEM,
    AgentMessage,
    AgentRequest,
    AgentResponse,
    AgentResponseType,
)

aura: Aura = Aura()

agent_router: APIRouter = APIRouter(
    prefix="/aura",
    tags=["Agent"],
)


async def stream(request: AgentRequest) -> AsyncGenerator[str, None]:
    """
    Stream the response from the agent.

    Arguments:
        request [AgentRequest]: The request containing the question to be answered.

    Returns:
        AsyncGenerator[str, None]: The response from the agent as an asynchronous generator.
    """

    try:
        async for response in aura.stream(request):
            yield response.to_stream_response_data()

    except Exception as e:
        yield AgentResponse(
            type=AgentResponseType.ERROR,
            detail=AgentMessage(
                entity=ENTITY_SYSTEM,
                message=str(e),
            ),
        ).to_stream_response_data()


@agent_router.post(
    path="/",
    dependencies=[Depends(get_api_key)],
)
async def ask(
    request: AgentRequest,
) -> StreamingResponse:
    """
    Stream the response from the agent as Server-Sent Events (SSE). Each event is a JSON object.
    """

    try:
        if request.request.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The request cannot be empty",
            )

        return StreamingResponse(
            stream(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
