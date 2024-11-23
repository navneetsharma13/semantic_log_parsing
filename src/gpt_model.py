# %%
import openai
import sys
import logging
from config import config
from tenacity import retry, stop_after_attempt
from tenacity import wait_random_exponential, before_sleep_log

# %%
# Extract API keys
openai_api_key = config['OPENAI']['token']
openai_org_id = config['OPENAI']['org_id']

if not openai_api_key:
    print("Please set OPENAI_API_KEY. Exiting...")
    sys.exit(1)

# Set API key for OpenAI
openai.api_key = openai_api_key
# Only set the organization ID if it is needed
if openai_org_id:
    openai.organization = openai_org_id

# You might want to comment out this line unless you're explicitly using a custom endpoint
# openai.api_base = "https://api.openai.com/v1"

# %%
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6), before_sleep=before_sleep_log(logging.getLogger(__name__), logging.DEBUG))
def get_completion_from_gpt(prompt, model="gpt-3.5-turbo"):
    logging.info(f"Querying GPT with model = {model} and prompt = {prompt}")
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2  # Adjust for the randomness of the output
        )
        content = response.choices[0].message.content
        logging.info(content)
        return content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        raise e  # Retry via tenacity

# %%
def get_statistics_from_tenacity():
    logging.info("Retry statistics from Tenacity:")
    logging.info(get_completion_from_gpt.retry.statistics)
    print(get_completion_from_gpt.retry.statistics)


# %%
