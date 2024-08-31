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
        model_name (str): Supported model name from Google Generative AI. Default: "gemini-1.5-flash".
        system_instruction (str): System instruction for the model. Default: None.
    """

    __supported_models: list[Model] = None

    @classmethod
    def get_supported_models(cls) -> list[Model]:
        """
        List supported models from Google Generative AI.

        Returns:
            list[Model]: List of supported models from Google Generative AI.
        """
        if not cls.__supported_models:
            cls.__supported_models = list(genai.list_models())
        return cls.__supported_models

    def __init__(
        self, model_name: Optional[str] = "gemini-1.5-flash", system_instruction: Optional[str] = None
    ) -> None:
        """
        Generators for Google Generative AI.

        Args:
            model_name (Optional[str]): Supported model name from Google Generative AI (default: "gemini-1.5-flash").
            system_instruction (Optional[str]): System instruction for the model (default: None).
        """
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.logger = CustomLogger(name="friday")

        # Load API key from the environment variables
        self.__api_key = os.getenv("GOOGLE_API_KEY")
        if not self.__api_key:
            raise FridayModelCreationError(
                message="API Key not found in the environment variables...", logger=self.logger
            )

        self.__supported_models: list[Model] = GoogleAIModel.supported_models()
        self._configure()

    @staticmethod
    def supported_models() -> list[Model]:
        """
        List supported models from Google Generative AI.

        Returns:
            list[Model]: List of supported models from Google Generative AI.
        """
        return [model.name for model in GoogleAIModel.get_supported_models()]

    @staticmethod
    def supported_generation_models() -> list[Model]:
        """
        List supported generation methods from Google Generative AI.

        Returns:
            list[Model]: List of supported generation methods from Google Generative AI.
        """
        return [
            model.name
            for model in GoogleAIModel.get_supported_models()
            if "generateContent" in model.supported_generation_methods
        ]

    def _configure(self) -> None:
        """
        Configure Friday with Google Generative AI. Once configured, the model can be accessed using the `model`
        attribute.
        """
        genai.configure(api_key=self.__api_key)
        self.model: GenerativeModel = genai.GenerativeModel(
            model_name=self.model_name, system_instruction=self.system_instruction
        )

    def __str__(self) -> str:
        """String representation of the GoogleAIModel."""
        return f"GoogleAIModel:\n{self.model}"


if __name__ == "__main__":
    google_model = GoogleAIModel()
    print(str(google_model))
    print(GoogleAIModel.supported_models())
    print(GoogleAIModel.supported_generation_models())
    print(google_model.model)
