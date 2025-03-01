import openai

def get_sentiment_analysis(api_key, headline):
    """
    Analyzes the sentiment of a given headline using OpenAI's GPT model.

    Parameters:
        api_key (str): Your OpenAI API key.
        headline (str): The news headline to analyze.

    Returns:
        dict: A dictionary containing sentiment percentages for positive, neutral, and negative.
    """
    openai.api_key = api_key

    # Define the prompt with the conditioning statements
    prompt = """You are a financial sentiment analyzer. Your task is to analyze the sentiment of financial headlines 
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
        # Make the API request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return the response content
        sentiment_result = response['choices'][0]['message']['content']
        return sentiment_result

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace with your OpenAI API key
    api_key = ""

    # Input news headline
    headline = "Tesla Reports Record Q4 Earnings, Beating Analyst Expectations."

    print(f"Headline for analysis: {headline}")

    # Get sentiment analysis
    result = get_sentiment_analysis(api_key, headline)

    if result:
        print("Sentiment Analysis Result:")
        print(result)
