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
git clone https://github.com/yourusername/nlie-api-text-analysis.git
cd nlie-api-text-analysis

# Install dependencies
pip install -r requirements.txt
```

## Configuration
This project requires a `config.yml` file (not included) to store API keys and secrets. You need to create this file in the root directory with the following structure:

```yaml
api_keys:
  xai: "your_xai_api_key"
  sonar: "your_sonar_api_key"
  chatgpt: "your_chatgpt_api_key"
  claude: "your_claude_api_key"
```

⚠️ **Note:** Do not share or commit your API keys to the repository.

## Usage
```sh
python main.py --input text_file.txt
```
This will process the text file and output results for sentiment analysis, NER, and text classification.

## Contributing
Feel free to fork this repository, submit issues, or make pull requests for improvements.

## License
MIT License © [Your Name](https://github.com/yourusername)
