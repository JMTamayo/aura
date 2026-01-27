from fastapi import APIRouter, Depends
from app.api.security.api_key import get_api_key

from app.models.agent import AgentResponse, AgentRequest


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

    return AgentResponse(answer="TODO")
