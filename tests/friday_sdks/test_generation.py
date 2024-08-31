"""Test Friday SDKs for generation."""

# Third Party Library
import pytest

# Project Library
from friday.sdk.model import GoogleAIModel
from friday.sdk.generation import GoogleAIGeneration


class TestGeneration:
    """Test Friday SDKs for generation."""

    def setup_class(self):
        """Set up the test class."""
        self.model = GoogleAIModel()
        self.ai_generation = GoogleAIGeneration(genai_model=self.model)

    def test_generation_config(self):
        """Test generation configuration."""
        config = GoogleAIGeneration.generation_config()

        assert config.candidate_count == 1
        assert config.max_output_tokens == 1000
        assert config.temperature == 0.5

    @pytest.mark.parametrize(
        "prompt",
        [
            "What is the meaning of life?",
        ],
    )
    def test_generate_content(self, prompt):
        """Test generate content."""
        response = self.ai_generation.generate_content(prompt=prompt)
        print(f"Response: {response.response.strip()}, Response Object: {response.response_object}")

        assert response.response is not None
        assert response.response_object is not None

    @pytest.mark.parametrize(
        "prompt",
        [
            "What is the meaning of life?",
        ],
    )
    def test_generation_with_generation_config(self, prompt):
        """Test generation with generation configuration."""
        config = GoogleAIGeneration.generation_config(candidate_count=1, max_output_tokens=10, temperature=0.7)

        response = self.ai_generation.generate_content(prompt=prompt, generation_config=config)
        response_token_count = response.response_object.usage_metadata.candidates_token_count

        assert response_token_count <= 10
