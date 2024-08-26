"""Friday - AI Personal Assistant. Main module."""

# Third Party Library
from dotenv import load_dotenv

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

    def _setup_google_ai_model(self) -> GoogleAIModel:
        """Setup Google Generative AI Model."""
        try:
            return GoogleAIModel()
        except FridayModelCreationError as err:
            self.logger.error("Failed to create Google AI Model for Friday.")
            raise FridayInitializationError(
                message="Failed to create Google AI Model for Friday...", logger=self.logger
            ) from err

    def _setup_google_ai_generation(self) -> GoogleAIGeneration:
        """Setup Google Generative AI Generation."""
        try:
            return GoogleAIGeneration(self.google_ai_model)
        except FridayGenerationError as err:
            self.logger.error("Failed to create Google AI Generation for Friday.")
            raise FridayInitializationError(
                message="Failed to create Google AI Generation for Friday...", logger=self.logger
            ) from err


if __name__ == "__main__":
    friday = Friday()
    response = friday.google_ai_generation.generate_content(prompt="Who are you?")
    print(response)
