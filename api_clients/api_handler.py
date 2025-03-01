from typing import Dict, Any
import json
from anthropic import Anthropic
import openai
import requests
from datetime import datetime
from config_handler import ConfigHandler


class BaseAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError

    def analyze_ner(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError

    def analyze_classification(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError


class ClaudeClient(BaseAPIClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = Anthropic(api_key=api_key)

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
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

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Analyze the sentiment of this text: {text}"
                    }
                ]
            )

            result = json.loads(response.content[0].text)
            result['timestamp'] = datetime.now().isoformat()
            return result

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "sentiment": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            }

    def analyze_ner(self, text: str) -> Dict[str, Any]:
        system_prompt = """You are a Named Entity Recognition system. Analyze the provided text and identify key entities.
        Categorize them into: PERSON, ORGANIZATION, LOCATION, DATE, MONEY, and MISC.

        Respond only with a JSON object in this exact format:
        {
            "entities": [
                {
                    "text": "entity text",
                    "category": "category name",
                    "start": start_index,
                    "end": end_index
                }
            ],
            "summary": "Brief summary of found entities"
        }"""

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Perform NER analysis on this text: {text}"
                    }
                ]
            )

            result = json.loads(response.content[0].text)
            result['timestamp'] = datetime.now().isoformat()
            return result

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "entities": []
            }

    def analyze_classification(self, text: str) -> Dict[str, Any]:
        system_prompt = """You are a text classification system. Analyze the provided text and classify it into relevant categories.
        Provide confidence scores for each category.

        Respond only with a JSON object in this exact format:
        {
            "categories": [
                {
                    "name": "category name",
                    "confidence": float,
                    "explanation": "brief explanation"
                }
            ],
            "dominant_category": "most confident category",
            "summary": "Brief classification summary"
        }"""

        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Classify this text: {text}"
                    }
                ]
            )

            result = json.loads(response.content[0].text)
            result['timestamp'] = datetime.now().isoformat()
            return result

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "categories": []
            }


class SonarClient(BaseAPIClient):
    def __init__(self, api_key: str, base_url: str = "https://api.perplexity.ai"):
        super().__init__(api_key)
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, messages: list) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": "sonar",
            "messages": messages
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
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

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze the sentiment of this text: {text}"}
            ]

            response = self._make_request(messages)
            content = response['choices'][0]['message']['content']
            clean_content = content.replace('```json\n', '').replace('\n```', '')
            result = json.loads(clean_content)
            result['timestamp'] = datetime.now().isoformat()
            return result

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "sentiment": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            }

    # Similar implementation pattern for NER and classification...
    def analyze_ner(self, text: str) -> Dict[str, Any]:
        # Implementation similar to sentiment analysis but with NER prompt
        pass

    def analyze_classification(self, text: str) -> Dict[str, Any]:
        # Implementation similar to sentiment analysis but with classification prompt
        pass


class xAIClient(BaseAPIClient):
    def __init__(self, api_key: str, base_url: str = "https://api.x.ai/v1"):
        super().__init__(api_key)
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, messages: list) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": "grok-2-latest",
            "messages": messages
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
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

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze the sentiment of this text: {text}"}
            ]

            response = self._make_request(messages)
            content = response['choices'][0]['message']['content']
            clean_content = content.replace('```json\n', '').replace('\n```', '')
            result = json.loads(clean_content)
            result['timestamp'] = datetime.now().isoformat()
            return result

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "sentiment": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            }

    # Similar implementation pattern for NER and classification...
    def analyze_ner(self, text: str) -> Dict[str, Any]:
        # Implementation similar to sentiment analysis but with NER prompt
        pass

    def analyze_classification(self, text: str) -> Dict[str, Any]:
        # Implementation similar to sentiment analysis but with classification prompt
        pass


class ChatGPTClient(BaseAPIClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        openai.api_key = api_key
        self.client = openai

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
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

        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the sentiment of this text: {text}"
                    }
                ],
                max_tokens=1000,
                temperature=0
            )

            # The response structure is different from Claude
            result = json.loads(response.choices[0].message.content)
            result['timestamp'] = datetime.now().isoformat()
            return result

        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "sentiment": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                }
            }
    # Similar implementation pattern for NER and classification...
    def analyze_ner(self, text: str) -> Dict[str, Any]:
        # Implementation similar to sentiment analysis but with NER prompt
        pass

    def analyze_classification(self, text: str) -> Dict[str, Any]:
        # Implementation similar to sentiment analysis but with classification prompt
        pass

class APIHandler:
    def __init__(self):
        self.config = ConfigHandler()

        # Initialize clients with config
        self.clients = {
            'Claude': ClaudeClient(
                self.config.get_api_key('claude')
            ),
            'Sonar': SonarClient(
                self.config.get_api_key('sonar'),
                self.config.get_base_url('sonar')
            ),
            'ChatGPT': ChatGPTClient(
                self.config.get_api_key('openai')
            ),
            'xAI': xAIClient(
                self.config.get_api_key('xai'),
                self.config.get_base_url('xai')
            )
        }

    def analyze(self, api_name: str, analysis_type: str, text: str) -> Dict[str, Any]:
        client = self.clients.get(api_name)
        if not client:
            return {"error": f"API client {api_name} not implemented"}

        try:
            if analysis_type == "Sentiment Analysis":
                return client.analyze_sentiment(text)
            elif analysis_type == "Named Entity Recognition":
                return client.analyze_ner(text)
            elif analysis_type == "Text Classification":
                return client.analyze_classification(text)
            else:
                return {"error": f"Unknown analysis type: {analysis_type}"}
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}