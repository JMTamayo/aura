from pathlib import Path
from typing import List

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage


class PromptBuilder:
    """
    A prompts builder for the email agent.
    """

    greeting_base_prompt: SystemMessage
    system_base_prompt: SystemMessage

    def __init__(self, greeting_prompt_file_path: str, system_prompt_file_path: str):
        try:
            greeting_prompt: str = Path(greeting_prompt_file_path).read_text(
                encoding="utf-8"
            )

        except FileNotFoundError:
            raise ValueError(
                f"Greeting prompt file not found: {greeting_prompt_file_path}"
            )

        try:
            system_prompt: str = Path(system_prompt_file_path).read_text(
                encoding="utf-8"
            )

        except FileNotFoundError:
            raise ValueError(f"System prompt file not found: {system_prompt_file_path}")

        self.greeting_base_prompt = SystemMessage(content=greeting_prompt)
        self.system_base_prompt = SystemMessage(content=system_prompt)

    def _get_greeting_prompt(self) -> SystemMessage:
        """
        Get the greeting base prompt.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            SystemMessage: The greeting base prompt.
        """

        return self.greeting_base_prompt

    def _get_system_base_prompt(self) -> SystemMessage:
        """
        Get the system base prompt.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            SystemMessage: The system base prompt.
        """

        return self.system_base_prompt

    def greeting_prompt(self, user_query: str) -> List[AnyMessage]:
        max_query_words = 10
        user_query_truncated = " ".join(user_query.strip().split()[:max_query_words])

        human_message = HumanMessage(
            content=f"The first {max_query_words} words of the user's query are: {user_query_truncated}"
        )

        prompt: List[AnyMessage] = [
            self._get_greeting_prompt(),
            human_message,
        ]

        return prompt

    def user_query_prompt(
        self,
        user_query: str,
    ) -> List[AnyMessage]:
        """
        Build a prompt to ask the user's query.

        Arguments
            user_query [str]: The user's query.

        Returns:
            List[AnyMessage]: The prompt to ask the user's query.
        """

        human_message: HumanMessage = HumanMessage(
            content=user_query.strip(),
        )

        prompt: List[AnyMessage] = [self._get_system_base_prompt(), human_message]

        return prompt
