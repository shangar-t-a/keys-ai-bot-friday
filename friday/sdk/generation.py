"""Generation SDKs for Friday built from Google Generative AI."""

# Standard Library
from typing import Annotated, Optional
from dataclasses import dataclass

# Project Library
from friday.utilities.exceptions import FridayBaseException
from friday.sdk.model import GoogleAIModel

# Type hints
from google.generativeai.generative_models import ChatSession
from google.generativeai.types.generation_types import GenerateContentResponse
from google.generativeai import GenerationConfig, protos


class FridayGenerationError(FridayBaseException):
    """Friday Generation Error in the SDK."""


@dataclass
class FridayResponse:
    """Friday Response for the Generation SDK."""

    response: str
    response_object: Optional[GenerateContentResponse] = None

    def __str__(self) -> str:
        """Return the response as a string."""
        return f"Response: {self.response.strip()}"


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

    @staticmethod
    def generation_config(
        candidate_count: int = 1, max_output_tokens: int = 1000, temperature: float = 0.5
    ) -> GenerationConfig:
        """
        Create a generation configuration for the model.

        Args:
            candidate_count (int, optional): Number of candidates to generate. Defaults to 1.
            max_output_tokens (int, optional): Maximum number of tokens to generate. Defaults to 1000.
            temperature (float, optional): Temperature for generation. Defaults to 0.5. Range: [0.0, 1.0].

        Returns:
            GenerationConfig: Generation configuration for the model.
        """
        return GenerationConfig(
            candidate_count=candidate_count,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )

    def generate_content(
        self, prompt: str, *, generation_config: Optional[GenerationConfig] = generation_config()
    ) -> FridayResponse:
        """
        Generate content using the configured model.

        Args:
            prompt (str): Prompt for generating content.
            generation_config (Optional[GenerationConfig]): Generation configuration for the model.
                Defaults to GoogleAIGeneration.generation_config().

        Returns:
            FridayResponse: Response from the model for the prompt.
        """
        response: GenerateContentResponse = self.__model.generate_content(prompt, generation_config=generation_config)
        return FridayResponse(response=response.text, response_object=response)

    def start_new_chat(self) -> ChatSession:
        """
        Start a new chat session with Friday using google generativeai ChatSession.

        Returns:
            ChatSession: Chat session created with Friday using google generativeai ChatSession.
        """
        return self.__model.start_chat(history=[])

    def send_chat_message(
        self, chat: ChatSession, message: str, generation_config: Optional[GenerationConfig] = generation_config()
    ) -> FridayResponse:
        """
        Send a message to the chat session with Friday and get the response from the chat session.

        Args:
            chat (ChatSession): Chat session created with Friday.
            message (str): Message to be sent to the chat session.
            generation_config (Optional[GenerationConfig]): Generation configuration for the model.
                Defaults to GoogleAIGeneration.generation_config().

        Returns:
            FridayResponse: Response from the chat session for the message.
        """
        response: GenerateContentResponse = chat.send_message(message, generation_config=generation_config)
        return FridayResponse(response=response.text, response_object=response)

    def get_chat_history(self, chat: ChatSession) -> list[str]:
        """
        Get chat history from the chat session with Friday and return the chat history as a dictionary with role as
        key and message as value.

        Args:
            chat (ChatSession): Chat session created with Friday using google generativeai ChatSession.

        Returns:
            list[str]: Chat history from the chat session with Friday.
        """
        return [f"{message.role}: {message.parts[0].text}" for message in chat.history]

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
    # Test the Generation SDK
    model = GoogleAIModel()
    ai_gen = GoogleAIGeneration(genai_model=model)
    print(ai_gen)

    # Test Generate Content
    if True:
        generation_config = ai_gen.generation_config(candidate_count=1, max_output_tokens=15, temperature=0.5)
        gen_response = ai_gen.generate_content(
            prompt="Who is the president of the United States?", generation_config=generation_config
        )
        print(f"Response: {gen_response.response.strip()}, Response Object: {gen_response.response_object}")

    # Test Chat Session
    if True:
        chat = ai_gen.start_new_chat()
        chat_response = ai_gen.send_chat_message(chat=chat, message="There are 5 apples in a basket.")
        print(f"Chat Response: {chat_response.response.strip()}")
        chat_response = ai_gen.send_chat_message(chat=chat, message="How many apples are there?")
        print(f"Chat Response: {chat_response.response.strip()}")
        print(f"Chat History:\n{ai_gen.get_chat_history(chat=chat)}")
        print(f"Token Count: {ai_gen._count_tokens(text=chat.history)}")
