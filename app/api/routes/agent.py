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

    async def stream() -> AsyncGenerator[str, None]:
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

    try:
        if request.request.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The request cannot be empty",
            )

        return StreamingResponse(
            stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
