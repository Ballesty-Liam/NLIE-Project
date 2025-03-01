# NLIE API-Based Text Analysis

## Overview
This project implements **Natural Language Information Extraction (NLIE)** using four major API calls:

- **xAI**
- **Sonar**
- **ChatGPT**
- **Claude**

The system performs **Sentiment Analysis**, **Named Entity Recognition (NER)**, and **Text Classification** by leveraging these external AI services. Additionally, it integrates **explainable AI (xAI)** methodologies to enhance model transparency and interpretability.

## Features
- **Multi-API Analysis:** Uses four distinct APIs for NLP tasks.
- **Sentiment Analysis:** Determines the sentiment of given text inputs.
- **Named Entity Recognition (NER):** Identifies entities such as names, organizations, and locations.
- **Text Classification:** Categorizes text into predefined classes.
- **Explainable AI (xAI) Support:** Provides insights into model predictions.

## Setup & Installation
### Prerequisites
- Python 3.8+
- Required libraries (listed in `requirements.txt`)
- API access keys for xAI, Sonar, ChatGPT, and Claude

### Installation
```sh
# Clone the repository
git clone https://github.com/yourusername/NLIE-Project.git
cd NLIE-Project

# Install dependencies
pip install -r requirements.txt
```

## Configuration
This project requires a `config.yml` file (not included) to store API keys and secrets. You need to create this file in the root directory with the following structure:

```yaml
# config.yaml

# API Keys and Configuration
api_keys:
  claude:
    key: "YOUR-KEY-HERE"
    model: "claude-3-sonnet-20240229"

  openai:
    key: "YOUR-KEY-HERE"
    model: "gpt-4-turbo-preview"

  sonar:
    key: "YOUR-KEY-HERE"
    base_url: "https://api.perplexity.ai"
    model: "sonar"

  xai:
    key: "YOUR-KEY-HERE"
    model: "grok-2-latest"
    base_url: "https://api.x.ai/v1"

# Model Configuration
model_settings:
  default_temperature: 0.0
  max_tokens: 1000
  timeout: 30  # seconds

# Analysis Types Configuration
analysis_settings:
  sentiment:
    default_categories: ["positive", "neutral", "negative"]

  ner:
    entity_types: ["PERSON", "ORGANIZATION", "LOCATION", "DATE", "MONEY", "MISC"]

  classification:
    confidence_threshold: 0.5
    max_categories: 5

# Output Configuration
output_settings:
  save_directory: "./results"
  file_format: "json"  # or "csv"
  include_timestamp: true
  include_input_text: true
```

⚠️ **Note:** Do not share or commit your API keys to the repository.

## Contributing
Feel free to fork this repository, submit issues, or make pull requests for improvements.

