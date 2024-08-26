"""Generation SDKs for Friday built from Google Generative AI."""

# Standard Library
from typing import Annotated

# Project Library
from friday.utilities.exceptions import FridayBaseException
from friday.sdk.model import GoogleAIModel

# Type hints
from google.generativeai.generative_models import ChatSession
from google.generativeai.types.generation_types import GenerateContentResponse
from google.generativeai import protos


class FridayGenerationError(FridayBaseException):
    """Friday Generation Error in the SDK."""


class GoogleAIGeneration:
    """
    Generation SDK for Friday built from Google Generative AI.

    Attributes:
        genai_model (GoogleAIModel): Google Generative AI Model Configuration for Friday.
    """

    def __init__(self, genai_model: GoogleAIModel) -> None:
        """
        Generators for Google Generative AI.

        Args:
            model (GoogleAIModel): Google Generative AI Model Configuration for Friday.
        """
        self.__model = genai_model.model

    def generate_content(self, prompt: str) -> str:
        """
        Generate content using the configured model.

        Args:
            prompt (str): Prompt for generating content.

        Returns:
            str: Generated content.
        """
        content: GenerateContentResponse = self.__model.generate_content(prompt)
        return content.text

    def start_new_chat(self) -> ChatSession:
        """
        Start a new chat session with Friday using google generativeai ChatSession.

        Returns:
            ChatSession: Chat session created with Friday using google generativeai ChatSession.
        """
        return self.__model.start_chat(history=[])

    def send_chat_message(self, chat: ChatSession, message: str) -> str:
        """
        Send a message to the chat session with Friday and get the response from the chat session.

        Args:
            chat (ChatSession): Chat session created with Friday.
            message (str): Message to be sent to the chat session.

        Returns:
            str: Response from the chat session.
        """
        response: GenerateContentResponse = chat.send_message(message)
        return response.text

    def get_chat_history(self, chat: ChatSession) -> dict:
        """
        Get chat history from the chat session with Friday and return the chat history as a dictionary with role as
        key and message as value.

        Args:
            chat (ChatSession): Chat session created with Friday using google generativeai ChatSession.

        Returns:
            dict: Chat history from the chat session as a dictionary with role as key and message as value.
        """
        return {message.role: message.parts[0].text for message in chat.history}

    def _count_tokens(self, text: str | Annotated[list[protos.Content], ChatSession.history]) -> int:
        """
        Count the number of tokens in the text or chat history.

        Args:
            text (str | Annotated[list[protos.Content], ChatSession.history]): Text or chat history to count the tokens.

        Returns:
            int: Number of tokens in the text or chat history.
        """
        return self.__model.count_tokens(text)

    def __str__(self):
        return f"Friday - Keys' AI Personal Assistant Generation with model: {self.__model.model_name}"


if __name__ == "__main__":
    model = GoogleAIModel()
    ai_gen = GoogleAIGeneration(genai_model=model)
    print(ai_gen)
    print(ai_gen.generate_content(prompt="Who is the president of the United States?").strip())
    chat = ai_gen.start_new_chat()
    print(ai_gen.send_chat_message(chat=chat, message="What is the capital of India?").strip())
    print(ai_gen.get_chat_history(chat=chat))
    print(ai_gen._count_tokens(text=chat.history))
