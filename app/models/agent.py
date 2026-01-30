from enum import StrEnum

from pydantic import BaseModel


class AgentRequest(BaseModel):
    """
    Represents a request to the agent, which contains the question to be answered in natural language.
    """

    request: str


class AgentResponseType(StrEnum):
    """
    Represents the type of response from the agent.
    """

    ERROR = "error"
    MESSAGE = "message"


ENTITY_SYSTEM: str = "system"


class AgentMessage(BaseModel):
    """
    Represents a message from the agent, which contains the message to the user.
    """

    entity: str
    message: str


class AgentResponse(BaseModel):
    """
    Represents a response from the agent, which contains the response to the request in natural language.
    """

    type: AgentResponseType
    detail: AgentMessage

    def to_stream_response_data(self) -> str:
        """
        Convert the stream response to a data string.
        """

        return f"data: {self.model_dump_json()}\n\n"
