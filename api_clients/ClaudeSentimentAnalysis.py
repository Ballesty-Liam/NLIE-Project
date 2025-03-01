import json
from anthropic import Anthropic


class FinancialSentimentAnalyzer:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def analyze_sentiment(self, headline):
        # System prompt to condition Claude's behavior
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
            # Make the API call to Claude
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Analyze the sentiment of this financial headline: {headline}"
                    }
                ]
            )

            # Parse the response content as JSON
            result = json.loads(response.content[0].text)
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


def main():
    # Replace with your actual API key
    api_key = ""

    # Initialize the analyzer
    analyzer = FinancialSentimentAnalyzer(api_key)

    # Example headlines
    headlines = [
        "Tesla Reports Record Q4 Earnings, Beating Analyst Expectations",
        "Meta Announces 10% Workforce Reduction Amid Cost-Cutting Measures",
        "Apple Maintains Market Position Despite Industry-Wide Chip Shortage"
    ]

    # Analyze each headline
    for headline in headlines:
        print(f"\nAnalyzing: {headline}")
        result = analyzer.analyze_sentiment(headline)

        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("\nSentiment Breakdown:")
            print(f"Positive: {result['sentiment']['positive']}%")
            print(f"Neutral: {result['sentiment']['neutral']}%")
            print(f"Negative: {result['sentiment']['negative']}%")
            print(f"\nExplanation: {result['explanation']}")


if __name__ == "__main__":
    main()