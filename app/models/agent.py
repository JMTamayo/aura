from pydantic import BaseModel


class AgentRequest(BaseModel):
    """
    Represents a request to the agent, which contains the question to be answered in natural language.
    """

    question: str


class AgentResponse(BaseModel):
    """
    Represents a response from the agent, which contains the answer to the question in natural language.
    """

    answer: str
