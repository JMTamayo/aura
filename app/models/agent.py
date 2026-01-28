from pydantic import BaseModel


class AgentRequest(BaseModel):
    """
    Represents a request to the agent, which contains the question to be answered in natural language.
    """

    request: str


class AgentResponse(BaseModel):
    """
    Represents a response from the agent, which contains the response to the request in natural language.
    """

    response: str
