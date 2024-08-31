# Google Generative AI Developer Handbook - Friday - AI Personal Assistant

- [Google Generative AI Developer Handbook - Friday - AI Personal Assistant](#google-generative-ai-developer-handbook---friday---ai-personal-assistant)
  - [Google Gemini API](#google-gemini-api)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Content Generation](#content-generation)
      - [Chat Conversation](#chat-conversation)

## Google Gemini API

- Refer to [Gemini API Python](https://colab.research.google.com/github/google/generative-ai-docs/blob/main/site/en/gemini-api/docs/get-started/python.ipynb#scrollTo=Tce3stUlHN0L)
  to get started with the Google API.

### Installation

- New API key can be generated from the [Google AI Studio](https://aistudio.google.com/app/apikey).
- API can be stored in the `.env` file as `GOOGLE_API_KEY`.
- Python SDK for Google Generative AI can be installed using `pip install google-generativeai`.

### Configuration

- The API key can be configured using the `configure` method.

  ```python
  genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
  ```

- The supported models can be listed using the `list_models` method.

  ```python
  for m in genai.list_models():
      if "generateContent" in m.supported_generation_methods:
          print(m.name)
  ```

- Create the model object using the `GenerativeModel` class. The model name can be passed as an argument.

  ```python
  model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction="Answer the questions.")
  ```

### Content Generation

- Generate content using the `generate_content` method.

  ```python
  content = model.generate_content("What is the color of the sky?")
  print(content.text)
  print(content.prompt_feedback)
  ```

#### Chat Conversation

- Start a chat session using the `start_chat` method and send messages using the `send_message` method.

  ```python
  chat = model.start_chat(history=[])
  response = chat.send_message("How are you?")
  print(response.text)
  ```

- Get the chat history using the `history` attribute. Get role and message using the `role` and `message` attributes.

  ```python
  print(chat.history)
    for message in chat.history:
        print(message.role, message.parts[0].text)
  ```

- Get the token count using the `count_tokens` method. The method accepts text or chat history as input.

  ```python
  print(model.count_tokens("Hello, how are you?"))
  print(model.count_tokens(chat.history))
  ```
