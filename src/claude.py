import sys
import logging
from pathlib import Path
from config import config
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

logger = logging.getLogger(__name__)

# Extract API key
claude_api_key = config['CLAUDE']['token']
if not len(claude_api_key):
    print("Please set CLAUDE_API_KEY. Exiting...")
    sys.exit(1)

anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=claude_api_key,
)

#@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6), before_sleep=before_sleep_log(logging.getLogger(__name__), logging.DEBUG))
def get_completion_from_claude(prompt, model="claude-2.0"):
    logging.info(f"Querying Claude with the prompt = " + str(prompt))
    completion = anthropic.completions.create(
        model= model,
        max_tokens_to_sample=10000,
        temperature=0.2, # this is the degree of randomness of the model's output
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
    )
    logging.info("response just after the query:")
    logging.info(completion.completion)
    return completion.completion

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    prompt = "Say hello!"
    response = get_completion_from_claude(prompt)
    print(response)
