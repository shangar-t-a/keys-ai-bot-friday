"""Friday - AI Personal Assistant. Main module."""

# Standard Library
from pathlib import Path
from typing import Literal

# Third Party Library
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Project Library
from friday.utilities.logger import CustomLogger
from friday.utilities.exceptions import FridayBaseException
from friday.sdk.model import GoogleAIModel, FridayModelCreationError
from friday.sdk.generation import GoogleAIGeneration, FridayGenerationError


# Load Environment Variables
load_dotenv()

# Constants
CHAT_USER_FOREGROUND_COLOR = Fore.MAGENTA
CHAT_FRIDAY_FOREGROUND_COLOR = Fore.CYAN
CHAT_ERROR_FOREGROUND_COLOR = Fore.RED
CHAT_COLOR_STYLE = Style.BRIGHT


class FridayInitializationError(FridayBaseException):
    """Friday Initialization Error."""


class Friday:
    """Friday - AI Personal Assistant."""

    def __init__(self):
        """Initialize Friday AI Personal Assistant."""
        self.logger = CustomLogger(name="friday")
        self.google_ai_model = self._setup_google_ai_model()
        self.google_ai_generation = self._setup_google_ai_generation()

    def _system_instruction(self) -> str:
        """
        Return the system instruction for Friday.

        Returns:
            str: System instruction for Friday.
        """
        system_instruction_file = Path(__file__).parent / "assets" / "system_message.yaml"
        with open(system_instruction_file, "r") as file:
            system_instruction = file.read()

        return system_instruction

    def _setup_google_ai_model(self) -> GoogleAIModel:
        """
        Setup Google Generative AI Model.

        Returns:
            GoogleAIModel: Google Generative AI Model for Friday.
        """
        try:
            return GoogleAIModel(model_name="gemini-1.5-flash", system_instruction=self._system_instruction())
        except FridayModelCreationError as err:
            self.logger.error("Failed to create Google AI Model for Friday.")
            raise FridayInitializationError(
                message="Failed to create Google AI Model for Friday...", logger=self.logger
            ) from err

    def _setup_google_ai_generation(self) -> GoogleAIGeneration:
        """
        Setup Google Generative AI Generation.

        Returns:
            GoogleAIGeneration: Google Generative AI Generation for Friday.
        """
        try:
            return GoogleAIGeneration(self.google_ai_model)
        except FridayGenerationError as err:
            self.logger.error("Failed to create Google AI Generation for Friday.")
            raise FridayInitializationError(
                message="Failed to create Google AI Generation for Friday...", logger=self.logger
            ) from err


def console_chat_color_formatter(message: str, role: Literal["User", "Friday", "Error"]) -> str:
    """
    Format the message for the console chat.

    Args:
        message (str): Message to format.
        role (Literal["User", "Friday"]): Role of the message sender.

    Returns:
        str: Formatted message for the console chat.
    """
    if role == "User":
        return f"{CHAT_USER_FOREGROUND_COLOR}{CHAT_COLOR_STYLE}You: {message}{Style.RESET_ALL}"
    elif role == "Friday":
        return f"{CHAT_FRIDAY_FOREGROUND_COLOR}{CHAT_COLOR_STYLE}Friday: {message}{Style.RESET_ALL}"
    elif role == "Error":
        return f"{CHAT_ERROR_FOREGROUND_COLOR}{CHAT_COLOR_STYLE}Error: {message}{Style.RESET_ALL}"


def main():
    """Main function for Friday AI Personal Assistant."""
    friday = Friday()
    init()
    response = friday.google_ai_generation.generate_content(prompt="Who are you?")
    print(console_chat_color_formatter(response.response.strip(), role="Friday"))
    friday_chat = friday.google_ai_generation.start_new_chat()

    while True:
        try:
            user_input = input(f"{CHAT_USER_FOREGROUND_COLOR}{CHAT_COLOR_STYLE}You: ")
            try:
                response = friday.google_ai_generation.send_chat_message(chat=friday_chat, message=user_input)
            except FridayGenerationError as err:
                print(
                    console_chat_color_formatter(
                        "Friday: Failed to send message to the chat session with Friday...", role="Error"
                    )
                )
                print(console_chat_color_formatter(f"Error: {err}", role="Error"))
                continue
            print(console_chat_color_formatter(response.response.strip(), role="Friday"))
        except KeyboardInterrupt:
            response = friday.google_ai_generation.generate_content(prompt="Good Bye!")
            print("\n" + console_chat_color_formatter(response.response.strip(), role="Friday"))
            break


if __name__ == "__main__":
    main()
