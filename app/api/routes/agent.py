from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from app.models.agent import AgentResponse, AgentRequest
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
