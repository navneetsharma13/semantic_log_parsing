import subprocess
import os

def query_ollama(model_name, prompt):
    # Add Ollama to PATH
    ollama_path = "/usr/local/bin"  # Use the output from `which ollama`
    os.environ["PATH"] += os.pathsep + ollama_path

    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error calling Ollama model {model_name}: {e}")
        return None

# # Example usage
# prompt = "What is the capital of France?"
# response = query_ollama("llama2", prompt)
# print(response)
