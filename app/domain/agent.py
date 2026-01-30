from enum import StrEnum
from typing import AsyncGenerator

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from app.config.conf import CONFIG
from app.models.agent import (
    ENTITY_SYSTEM,
    AgentMessage,
    AgentRequest,
    AgentResponse,
    AgentResponseType,
)
from app.models.prompts import PromptBuilder

GREETING_PROMPT_FILE_PATH = "app/domain/prompts/greeting.md"
SYSTEM_PROMPT_FILE_PATH = "app/domain/prompts/system.md"


class AgentState(MessagesState):
    """
    Represents the state of the agent to be used in the workflow.
    """

    user_query: str


class Nodes(StrEnum):
    """
    Represents the implemented nodes of the workflow.
    """

    GREETING = "Greet the user"
    AGENT = "Aura agent"


class Aura:
    """
    The Aura agent.
    """

    prompt_builder: PromptBuilder
    llm: BaseChatModel
    workflow: CompiledStateGraph

    def __init__(self):
        prompt_builder = PromptBuilder(
            GREETING_PROMPT_FILE_PATH, SYSTEM_PROMPT_FILE_PATH
        )

        llm = init_chat_model(
            model=CONFIG.LLM_MODEL,
            model_provider=CONFIG.LLM_PROVIDER,
            temperature=CONFIG.LLM_TEMPERATURE,
            api_key=CONFIG.LLM_API_KEY.get_secret_value(),
        )

        workflow = (
            StateGraph(AgentState)
            .add_node(Nodes.GREETING, self.greeting_node)
            .add_node(Nodes.AGENT, self.agent_node)
            .add_edge(Nodes.GREETING, Nodes.AGENT)
            .add_edge(Nodes.AGENT, END)
            .set_entry_point(Nodes.GREETING)
            .compile()
        )

        self.prompt_builder = prompt_builder
        self.llm = llm
        self.workflow = workflow

    def get_prompt_builder(self) -> PromptBuilder:
        """
        Get the prompt builder, used to build the prompts for the LLM.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            PromptBuilder: The prompt builder.
        """

        return self.prompt_builder

    def get_llm(self) -> BaseChatModel:
        """
        Get the LLM, used to generate the responses.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            BaseChatModel: The LLM.
        """

        return self.llm

    def get_workflow(self) -> CompiledStateGraph:
        """
        Get the agent workflow

        Arguments:
            None: The function does not take any arguments.

        Returns:
            CompiledStateGraph: The agent workflow.
        """

        return self.workflow

    async def greeting_node(self, state: AgentState) -> Command:
        """
        The greeting node of the workflow, when the LLM starts to answer the user's query.

        Arguments:
            state [AgentState]: The state of the agent.

        Returns:
            Command[Literal[Nodes.AGENT]]: The command to the next node.
        """

        response: AIMessage = await self.get_llm().ainvoke(
            self.get_prompt_builder().greeting_prompt(
                state["user_query"],
            )
        )

        return Command(goto=Nodes.AGENT, update={"messages": [response]})

    async def agent_node(self, state: AgentState) -> Command:
        """
        The agent node of the workflow, when the LLM thinks to answer the user's query.

        Arguments:
            state [AgentState]: The state of the agent.

        Returns:
            AgentState: The state of the agent.
        """

        response: AIMessage = await self.get_llm().ainvoke(
            self.get_prompt_builder().user_query_prompt(
                state["user_query"],
            )
        )

        return Command(goto=END, update={"messages": [response]})

    async def stream(
        self, request: AgentRequest
    ) -> AsyncGenerator[AgentResponse, None]:
        """
        Stream the response from the agent.

        Arguments:
            request [AgentRequest]: The request containing the question to be answered.

        Returns:
            AsyncGenerator[AgentResponse, None]: The response from the agent as an asynchronous generator.
        """

        state = {
            "user_query": request.request,
            "messages": self.get_prompt_builder().user_query_prompt(request.request),
        }

        try:
            async for chunk in self.get_workflow().astream(state, stream_mode="values"):
                msg = chunk["messages"][-1]
                yield AgentResponse(
                    type=AgentResponseType.MESSAGE,
                    detail=AgentMessage(
                        entity=msg.type,
                        message=msg.content,
                    ),
                )

        except Exception as e:
            yield AgentResponse(
                type=AgentResponseType.ERROR,
                detail=AgentMessage(
                    entity=ENTITY_SYSTEM,
                    message=str(e),
                ),
            )
