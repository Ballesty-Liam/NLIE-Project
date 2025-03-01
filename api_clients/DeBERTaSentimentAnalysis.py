import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import os

"""
DeBERTA-v3 was found on Hugging Face here: https://huggingface.co/mrm8488/deberta-v3-ft-financial-news-sentiment-analysis
More information on its training set can be found here: https://huggingface.co/microsoft/deberta-v3-small
"""

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def analyze_sentiment(text):
    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/deberta-v3-ft-financial-news-sentiment-analysis")
    model = AutoModelForSequenceClassification.from_pretrained(
        "mrm8488/deberta-v3-ft-financial-news-sentiment-analysis")

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    # Get model outputs
    outputs = model(**inputs)

    # Apply softmax to get probabilities
    probabilities = F.softmax(outputs.logits, dim=1)

    # Convert to percentages
    percentages = probabilities[0].tolist()

    # DeBERTa's labels are: ['negative', 'neutral', 'positive']
    sentiments = {
        'negative': round(percentages[0] * 100, 2),
        'neutral': round(percentages[1] * 100, 2),
        'positive': round(percentages[2] * 100, 2)
    }

    return sentiments


# Example usage
if __name__ == "__main__":
    test_sentence = "Tesla Reports Record Q4 Earnings, Beating Analyst Expectations."
    results = analyze_sentiment(test_sentence)

    print(f"Input text: {test_sentence}")
    print("\nSentiment Analysis Results:")
    for sentiment, percentage in results.items():
        print(f"{sentiment.capitalize()}: {percentage}%")