#%%
import openai
import sys
import logging
from config import config
from tenacity import retry, stop_after_attempt
from tenacity import wait_random_exponential, before_sleep_log

#%%
# Extract API keys
openai_api_key = config['OPENAI']['token']
openai_org_id = config['OPENAI']['org_id']
if not len(openai_api_key):
    print("Please set OPENAI_API_KEY. Exiting...")
    sys.exit(1)

openai.api_key  = openai_api_key
openai.organization = openai_org_id
openai.api_base = "https://api.openai.com/v1" 

#%%
# get completion from gpt-3.5-turbo-0613 model
# since gpt-3.5-turbo-0613 model is not supported anymore, the model name is left as gpt-3.5-turbo, which currently points to gpt-3.5-turbo-0125
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6), before_sleep=before_sleep_log(logging.getLogger(__name__), logging.DEBUG))
def get_completion_from_gpt(prompt, model="gpt-3.5-turbo"):
    logging.info(f"Querying GPT with model = " + str(model) + " and prompt = " + str(prompt))
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {"role": "user", "content": prompt}
    ]
  
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2, # this is the degree of randomness of the model's output
    )
    logging.info(response.choices[0].message["content"])
    return response.choices[0].message["content"]
#%%
def get_statistics_from_tenacity():
    logging.info("Retry statistics from Tenacity:")
    logging.info(get_completion_from_gpt.retry.statistics)
    print(get_completion_from_gpt.retry.statistics)


# %%
