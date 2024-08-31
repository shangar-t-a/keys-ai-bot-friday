"""Friday - AI Personal Assistant. Main module."""

# Third Party Library
from dotenv import load_dotenv
from pathlib import Path

# Project Library
from friday.utilities.logger import CustomLogger
from friday.utilities.exceptions import FridayBaseException
from friday.sdk.model import GoogleAIModel, FridayModelCreationError
from friday.sdk.generation import GoogleAIGeneration, FridayGenerationError


# Load Environment Variables
load_dotenv()


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


def main():
    """Main function for Friday AI Personal Assistant."""
    friday = Friday()
    response = friday.google_ai_generation.generate_content(prompt="Who are you?")
    print(response)
    friday_chat = friday.google_ai_generation.start_new_chat()

    while True:
        try:
            user_input = input("You: ")
            try:
                response = friday.google_ai_generation.send_chat_message(chat=friday_chat, message=user_input)
            except FridayGenerationError as err:
                print(f"Friday: Failed to send message to the chat session with Friday...")
                print(f"Error: {err}")
                continue
            print(f"Friday: {response.response}")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
