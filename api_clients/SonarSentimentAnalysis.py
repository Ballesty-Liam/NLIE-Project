import os
import json
import requests

class OpenAIClient:
    def __init__(self, api_key, base_url="https://api.perplexity.ai"):
        """
        Initialize the OpenAIClient with an API key and base URL.

        Parameters:
            api_key (str): Your API key for authentication.
            base_url (str): The base URL for the API. Defaults to the provided API endpoint.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(self, model, messages):
        """
        Send a request to the ChatCompletion endpoint.

        Parameters:
            model (str): The model to use, e.g., "grok-2-latest".
            messages (list): A list of messages in the chat format.

        Returns:
            dict: The response from the API.
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    @staticmethod
    def parse_response(response):
        """
        Parse the API response to extract sentiment and explanation.

        Parameters:
            response (dict): The raw response from the API.

        Returns:
            dict: A simplified JSON object with sentiment and explanation.
        """
        try:
            content = response['choices'][0]['message']['content']
            # First try to parse as JSON
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, clean the string and try again
                content = content.replace('\n', '').replace('\\', '').strip()
                if content.startswith('"') and content.endswith('"'):
                    content = content[1:-1]
                parsed_content = json.loads(content)

            return {
                "sentiment": parsed_content["sentiment"],
                "explanation": parsed_content["explanation"]
            }
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing response: {e}")

# Example usage
if __name__ == "__main__":
    SONAR_API_KEY = ""

    # Create the client
    client = OpenAIClient(
        api_key=SONAR_API_KEY,
        base_url="https://api.perplexity.ai"
    )

    system_prompt = """You are a financial sentiment analyzer. Your task is to analyze the sentiment of financial headlines 
            and provide a percentage breakdown across three categories: positive, neutral, and negative. The percentages should 
            sum to 100%. Consider the following in your analysis:

            - Impact on stock price/company value
            - Market reaction
            - Industry implications
            - Overall business health indicators

            Respond only with a JSON object in this exact format:
            {
                "sentiment": {
                    "positive": float,
                    "neutral": float,
                    "negative": float
                },
                "explanation": "Brief explanation of the analysis"
            }"""


    # Example chat request
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What is the sentiment of the headline: 'Tesla Reports Record Q4 Earnings, Beating Analyst Expectations'?"}
    ]

    # Make the request
    response = client.chat_completion(model="sonar", messages=messages)
    print(response)
    content = response['choices'][0]['message']['content']
    # Remove the code block markers
    clean_content = content.replace('```json\n', '').replace('\n```', '')
    result = json.loads(clean_content)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("\nSentiment Breakdown:")
        print(f"Positive: {result['sentiment']['positive']}%")
        print(f"Neutral: {result['sentiment']['neutral']}%")
        print(f"Negative: {result['sentiment']['negative']}%")
        print(f"\nExplanation: {result['explanation']}")
