# Semantic Log Parsing Project

## Overview
This project aims to perform semantic log parsing using language models like GPT3.5-turbo, qwen2.5-code, deepseek-coder-v2 and codegemma to evaluate the parsing quality through various metrics such as Edit Distance, Rouge-L, BLEU and Cosine similarity scores. The system can convert unstructured log messages into a more structured format, making analysing the underlying semantics of log entries easier.

## Project Structure
The repository contains several Python files and notebooks, each responsible for a different part of the log parsing process:

- **gpt_model.py**:  This script contains functions interacting with OpenAI's GPT model. It includes retry mechanisms for handling API errors and retrieving model completions.

- **config.py**: This handles the project's configuration settings. It parses a configuration file (`config.ini`) to extract API keys and other necessary settings.

- **format_output.py**: This script formats the output from the language models. It includes functions for saving results in different formats (e.g., JSON, CSV) and formatting the strings to be more readable.

- **semantic_log_parsing.ipynb & syntactic_log_parsing.ipynb**: These Jupyter notebooks provide an interactive environment for running evaluations and experiments on log parsing and model interactions.

## Installation
You will need Python 3.7+ and some additional dependencies to run this project locally.

1. **Clone the repository**:
   ```sh
   git clone https://github.com/navneetsharma13/semantic_log_parsing.git
   cd semantic_log_parsing
   ```

2. **Install dependencies**:
   Create a virtual environment and install the required packages using:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Configuration**:
   Create a `config.ini` file and add API keys for OpenAI and Claude services:
   ```ini
   [OPENAI]
   token = YOUR_OPENAI_API_KEY
   org_id = YOUR_OPENAI_ORG_ID
   proj_id = YOUR_OPENAI_PROJECT_ID

   [CLAUDE]
   token = YOUR_CLAUDE_API_KEY
   ```

## Usage
1. **Format Log Messages**:
   You can use `format_output.py` to format log outputs and save them in different formats like CSV or JSON for easier analysis:
   ```sh
   python format_output.py
   ```

2. **Interact with Language Models**:
   Use either `olamma.py` or `gpt_model.py` to interact with language models and parse your log messages:
   ```sh
   python claude.py
   python gpt_model.py
   ``

## File Descriptions
- **ollama.py**: Contains the function `get_completion_from_ollama()` which queries locally hosted open-sourced LLMs for parsing logs.
- **gpt_model.py**: Implements `get_completion_from_gpt()` to interact with OpenAI's GPT-3.5 Turbo model.
- **config.py**: Reads API keys from `config.ini`.
- **format_output.py**: Formats model responses and provides functionalities to save outputs in various formats.
- **log_parisng_evaluation.py**: Loads log messages and evaluate the predictions using sci-kit-learn metrics.
- **ground_truth_corrected_by_Khan2022.txt & log_messages_corrected.txt**: These contain sample ground truth and parsed log messages used for evaluation.

## Contributing
Feel free to open issues and contribute to improving this project. Please fork the repository and create a pull request for any feature addition or bug fix.

## Contact
Please contact [Navneet Sharma](mailto:sharma.navneet092@gmail.com).

## License
This project is licensed under the MIT License. See the LICENSE file for details.

