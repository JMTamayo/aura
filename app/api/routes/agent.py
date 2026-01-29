from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse

from app.models.agent import AgentResponse, AgentRequest, AgentStreamError
from app.domain.agent import Aura
from app.api.security.api_key import get_api_key

aura: Aura = Aura()

agent_router: APIRouter = APIRouter(
    prefix="/aura",
    tags=["Agent"],
)


@agent_router.post(
    path="/",
    dependencies=[Depends(get_api_key)],
    response_model=AgentResponse,
)
def make_a_question_to_aura(
    request: AgentRequest,
) -> AgentResponse:
    """
    Interact with Aura, the agent, wich helps you to manage your ecosystem by solving questions in natural language.
    """

    try:
        response: AgentResponse = aura.ask(request)
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@agent_router.post(
    path="/stream",
    dependencies=[Depends(get_api_key)],
)
async def stream_a_question_to_aura(
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
            yield AgentStreamError(detail=str(e)).to_stream_response_data()

    try:
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
