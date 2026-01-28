from enum import StrEnum
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from app.models.prompts import PromptBuilder
from app.models.agent import AgentRequest, AgentResponse
from app.config.conf import CONFIG


SYSTEM_PROMPT_FILE_PATH = "app/domain/prompts/system.md"


class AgentState(MessagesState):
    """
    Represents the state of the agent to be used in the workflow.
    """

    pass


class Nodes(StrEnum):
    """
    Represents the implemented nodes of the workflow.
    """

    AGENT = "Aura agent"


class Aura:
    """
    The Aura agent.
    """

    prompt_builder: PromptBuilder
    llm: BaseChatModel
    workflow: CompiledStateGraph

    def __init__(self):
        prompt_builder = PromptBuilder(SYSTEM_PROMPT_FILE_PATH)

        llm = init_chat_model(
            model=CONFIG.LLM_MODEL,
            model_provider=CONFIG.LLM_PROVIDER,
            temperature=CONFIG.LLM_TEMPERATURE,
            api_key=CONFIG.LLM_API_KEY.get_secret_value(),
        )

        graph_builder = StateGraph(AgentState)

        graph_builder.add_node(Nodes.AGENT, self.agent_node)

        graph_builder.add_edge(Nodes.AGENT, END)

        graph_builder.set_entry_point(Nodes.AGENT)

        workflow = graph_builder.compile()

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

    def agent_node(self, state: AgentState) -> AgentState:
        """
        The agent node of the workflow, when the LLM thinks to answer the user's query.

        Arguments:
            state [AgentState]: The state of the agent.

        Returns:
            AgentState: The state of the agent.
        """

        response: AIMessage = self.get_llm().invoke(
            self.get_prompt_builder().user_query_prompt(
                str(state["messages"][-1].content),
            )
        )

        state["messages"].append(response)

        return state

    def ask(self, request: AgentRequest) -> AgentResponse:
        """
        Ask a question to the agent.

        Arguments:
            request [AgentRequest]: The request containing the question to be answered.

        Returns:
            AgentResponse: The response from the agent.
        """

        state = {
            "messages": self.get_prompt_builder().user_query_prompt(request.request),
        }

        try:
            agent_response: dict[str, Any] = self.get_workflow().invoke(state)
            return AgentResponse(response=agent_response["messages"][-1].content)

        except Exception:
            raise Exception(
                "A server error occurred while answering the question. Contact the administrator."
            )
