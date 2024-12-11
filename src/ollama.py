import sys
import logging
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential, before_sleep_log

# Create client for local instance
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required, but unused in this context
)




@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6), before_sleep=before_sleep_log(logging.getLogger(__name__), logging.DEBUG))
def get_completion_from_ollama(prompt, model):
    logging.info(f"Querying Qwen with model = {model} and prompt = {prompt}")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2  # Adjust for the randomness of the output
        )
        content = response.choices[0].message.content
        logging.info(content)
        return content
    except Exception as e:
        logging.error(f"Local API error: {e}")
        raise e  # Retry via tenacity

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    prompt = "Say hello!"
    response = get_completion_from_ollama(prompt)
    print(response)
