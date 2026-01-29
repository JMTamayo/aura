import json

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

    type: str
    response: str

    def to_stream_response_data(self) -> str:
        """
        Convert the stream response to a data string.
        """

        return f"data: {self.model_dump_json()}\n\n"


class AgentError(Exception):
    """
    Represents an error in the response from the agent.
    """

    detail: str

    def __init__(self, detail: str):
        self.detail = detail

    def to_stream_response_data(self) -> str:
        """
        Convert the stream error to a data string.
        """

        obj = {"detail": self.detail}
        return f"data: {json.dumps(obj)}\n\n"
