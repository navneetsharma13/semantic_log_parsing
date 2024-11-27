import openai
import re
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your API key

# Step 1: Load Ground Truth and Parsed Log
def load_files(ground_truth_file, parsed_log_file):
    with open(ground_truth_file, 'r') as gt_file:
        ground_truth_lines = [line.strip() for line in gt_file.readlines()]

    parsed_log_df = pd.read_csv(parsed_log_file)
    parsed_lines = parsed_log_df['TPL'].dropna().tolist()
    
    return ground_truth_lines, parsed_lines

# Step 2: Get Semantic Knowledge from LLM
def get_semantic_prompt(parsed_log):
    prompt = f"Given the following log entry: '{parsed_log}', provide the semantic understanding
      or context behind this log message. Include information that would help 
    categorize and understand the reason and significance of the log."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use your preferred model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    semantic_knowledge = response.choices[0].message['content']
    return semantic_knowledge

# Step 3: Generate Enhanced Prompt
def generate_enhanced_prompt(parsed_log):
    semantic_knowledge = get_semantic_prompt(parsed_log)
    enhanced_prompt = f"Log Entry: '{parsed_log}'. Semantic Context: {semantic_knowledge}. Based on this, generate the log template."
    return enhanced_prompt

# Step 4: Use Enhanced Prompt for Final Parsing
def final_parse_log(raw_log):
    enhanced_prompt = generate_enhanced_prompt(raw_log)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": enhanced_prompt}],
        temperature=0.5
    )
    final_template = response.choices[0].message['content']
    return final_template

# Step 5: Main Workflow for Evaluation
def main():
    # File paths
    ground_truth_file = 'ground_truth_file.txt'
    parsed_log_file = 'normalized_output_file.csv'
    
    # Load files
    ground_truth_lines, parsed_lines = load_files(ground_truth_file, parsed_log_file)
    
    # Parse logs with enhanced prompts and evaluate metrics
    final_templates = [final_parse_log(parsed_log) for parsed_log in parsed_lines]
    
    # Evaluate metrics
    accuracy, precision, recall, f1 = evaluate_metrics(ground_truth_lines, final_templates)
    
    # Print the results
    print(f'Accuracy: {accuracy:.2f}')
    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1 Score: {f1:.2f}')

# Step 6: Evaluation Metrics Function
def evaluate_metrics(ground_truth, predictions):
    # Ensure lists are of the same length
    min_length = min(len(ground_truth), len(predictions))
    ground_truth = ground_truth[:min_length]
    predictions = predictions[:min_length]

    # Calculate metrics
    accuracy = accuracy_score(ground_truth, predictions)
    precision = precision_score(ground_truth, predictions, average='micro')
    recall = recall_score(ground_truth, predictions, average='micro')
    f1 = f1_score(ground_truth, predictions, average='micro')

    return accuracy, precision, recall, f1

if __name__ == '__main__':
    main()
