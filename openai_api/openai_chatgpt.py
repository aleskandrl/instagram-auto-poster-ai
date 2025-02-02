import openai
from openai import OpenAI
import openai

class BaseChatClient:
    """Abstract base class for a ChatGPT client."""

    def send_message(self, prompt):
        raise NotImplementedError("This method should be overridden in a subclass.")

    def chat(self, message):
        raise NotImplementedError("This method should be overridden in a subclass.")


class OpenAIChatClient(BaseChatClient):
    """Implementation of ChatGPT client using OpenAI API."""

    def __init__(self, api_key, openai_api_settings="Default"):
        openai.api_key = api_key
        self.client = OpenAI(api_key=api_key)

        configuration=openai_api_settings
        if configuration=="Default":
            default_settings = {
                "model": "gpt-4",
                "role": "You are default assistant",
                "max_tokens": 100,  # Adjust the response length
                "temperature": 0.7,  # Adjust creativity (0.0-1.0)
                "n": 1  # Number of responses
            }
            configuration = default_settings

        self.model = configuration["model"]  # Model name
        self.role = configuration["role"]  # Set pre-prompt
        self.max_tokens = configuration["max_tokens"]  # Adjust the response length
        self.temperature = configuration["temperature"]  # Adjust creativity (0.0-1.0)
        self.n = configuration["n"]  # Number of responses

    def send_message(self, prompt):
        """Send a message to ChatGPT and return the response."""
        try:
            # Create a request to the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.role},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,  # Adjust the response length
                temperature=self.temperature,  # Adjust creativity (0.0-1.0)
                n=self.n  # Number of responses
            )
            if response.choices and response.choices[0].message:
                assistant_answer = response.choices[0].message.content
            # Extract and return the response text
            return assistant_answer
        except Exception as e:
            return f"Error: {str(e)}"

    def chat(self, message):
        """Interact with ChatGPT for a conversation."""
        return self.send_message(message)


class EmptyChatClient(BaseChatClient):
    """Dummy implementation of a ChatGPT client with no functionality."""

    def send_message(self, prompt):
        """Empty implementation that does nothing."""
        return ""

    def chat(self, message):
        """Empty implementation that does nothing."""
        return self.send_message(message)


# Factory function to choose the client
def create_chat_client(use_openai, api_key=None, openai_api_settings="Default"):
    """
    Factory to create either an OpenAIChatClient or EmptyChatClient.

    Parameters:
    use_openai (bool): Whether to use the OpenAI client or the empty client.
    api_key (str): API key for OpenAI (required if use_openai is True).
    model (str): Model name (default is "gpt-4").

    Returns:
    BaseChatClient: An instance of OpenAIChatClient or EmptyChatClient.
    """
    if use_openai:
        print("ChatGPT in use")
        if not api_key:
            raise ValueError("API key is required when use_openai is True.")
        return OpenAIChatClient(api_key=api_key, openai_api_settings=openai_api_settings)
    else:
        print("ChatGPT not in use")
        return EmptyChatClient()


# Example usage
from configuration import OPENAI_API_SETTINGS,OPENAI_API_KEY

if __name__ == "__main__":
    # Example usage
    use_openai = False  # Set to False to disable OpenAI functionality
    api_key = OPENAI_API_KEY  # Provide your API key if using OpenAI

    client = create_chat_client(use_openai, api_key=api_key)

    response = client.chat("What.")
    print(response)
