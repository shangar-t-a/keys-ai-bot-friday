"""Friday Model Definition."""

# Standard Library
import os
from typing import Optional

# Third Party Library
from dotenv import load_dotenv
import google.generativeai as genai

# Project Library
from friday.utilities.logger import CustomLogger
from friday.utilities.exceptions import FridayBaseException

# Type hints
from google.generativeai.generative_models import GenerativeModel
from google.generativeai.protos import Model


load_dotenv()


class FridayModelCreationError(FridayBaseException):
    """Friday Model Creation Error."""


class GoogleAIModel:
    """
    Google Generative AI Model Configuration for Friday.

    Expected Environment Variables:
    - `GOOGLE_API_KEY`: Google API Key for Generative AI.

    Attributes:
        model (GenerativeModel): Generative Model from Google Generative AI.
    """

    def __init__(self) -> None:
        """Generators for Google Generative AI."""
        # Load API key from the environment variables
        self.logger = CustomLogger(name="friday")

        self.__api_key = os.getenv("GOOGLE_API_KEY")
        if not self.__api_key:
            raise FridayModelCreationError(
                message="API Key not found in the environment variables...", logger=self.logger
            )

        self.__supported_models: list[Model] = list(genai.list_models())

        self.configure()

    @property
    def supported_models(self) -> list:
        """
        List supported models from Google Generative AI.

        Returns:
            list: List of supported models from Google Generative AI.
        """
        return [model.name for model in self.__supported_models]

    @property
    def supported_generation_models(self) -> list:
        """
        List supported generation methods from Google Generative AI.

        Returns:
            list: List of supported generation methods from Google Generative AI.
        """
        return [
            model.name for model in self.__supported_models if "generateContent" in model.supported_generation_methods
        ]

    def configure(self, model_name: Optional[str] = "gemini-1.5-flash") -> None:
        """
        Configure Friday with Google Generative AI. Once configured, the model can be accessed using the `model`
        attribute.

        Args:
            model_name (Optional[str]): Supported model name from Google Generative AI (default: "gemini-1.5-flash").
        """
        genai.configure(api_key=self.__api_key)
        self.model: GenerativeModel = genai.GenerativeModel(model_name)

    def __str__(self) -> str:
        """String representation of the GoogleAIModel."""
        return f"GoogleAIModel:\n{self.model}"


if __name__ == "__main__":
    google_model = GoogleAIModel()
    print(str(google_model))
    print(google_model.supported_models)
    print(google_model.supported_generation_models)
    google_model.configure()
    print(google_model.model)
