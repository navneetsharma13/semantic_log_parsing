import re
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: Load Ground Truth and Predicted Output Files
def load_files(ground_truth_file, output_file):
    with open(ground_truth_file, 'r') as gt_file:
        ground_truth_lines = [line.strip() for line in gt_file.readlines()]

    output_df = pd.read_csv(output_file, delimiter=',', on_bad_lines='skip')
    predicted_lines = output_df.iloc[:, 0].dropna().apply(lambda x: x.replace('<TPL>', '').replace('</TPL>', '').strip()).tolist()
    
    return ground_truth_lines, predicted_lines

# Step 2: Refined Normalization to Maintain Constant Structure
def normalize_line(line):
    # Replace numbers, hexadecimal values, and other dynamic parts with <*>
    line = re.sub(r'\b\d+\b', '<*>', line)  # Replace any number
    line = re.sub(r'\b0x[0-9a-fA-F]+\b', '<*>', line)  # Replace hexadecimal values
    line = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '<*>', line)  # Replace email addresses
    line = re.sub(r'\b[a-fA-F0-9]{4,}\b', '<*>', line)  # Replace alphanumeric IDs (e.g., UUIDs)
    return line

# Step 3: Normalize Ground Truth and Predicted Output
def normalize_lines(lines):
    return [normalize_line(line) for line in lines]

# Step 4: Convert Predicted Output to Ground Truth Format and Save to New CSV
def convert_output_to_ground_truth_format(output_file, new_output_file):
    output_df = pd.read_csv(output_file)
    output_df['TPL'] = output_df.iloc[:, 0].apply(lambda x: normalize_line(x.replace('<TPL>', '').replace('</TPL>', '').strip()))
    output_df[['TPL']].to_csv(new_output_file, index=False)

# Step 5: Evaluate Metrics
def evaluate_metrics(ground_truth, predictions):
    # Ensure the lists are of the same length
    min_length = min(len(ground_truth), len(predictions))
    ground_truth = ground_truth[:min_length]
    predictions = predictions[:min_length]
    
    # Calculate evaluation metrics
    accuracy = accuracy_score(ground_truth, predictions)
    precision = precision_score(ground_truth, predictions, average='micro')
    recall = recall_score(ground_truth, predictions, average='micro')
    f1 = f1_score(ground_truth, predictions, average='micro')
    
    return accuracy, precision, recall, f1

# Step 6: Main Workflow
def main():
    # File paths
    ground_truth_file = 'data/ground_truth_corrected_by_Khan2022.txt'
    output_file = 'results/20241123140418/formatted_results/output.csv'
    new_output_file = 'new_formatted_output.csv'
    
    # Convert predicted output to ground truth format
    convert_output_to_ground_truth_format(output_file, new_output_file)
    
    # Load files
    ground_truth_lines, predicted_lines = load_files(ground_truth_file, new_output_file)
    
    # Normalize lines
    normalized_ground_truth = normalize_lines(ground_truth_lines)
    normalized_predictions = normalize_lines(predicted_lines)
    
    # Evaluate metrics
    accuracy, precision, recall, f1 = evaluate_metrics(normalized_ground_truth, normalized_predictions)
    
    # Print the results
    print(f'Accuracy: {accuracy:.2f}')
    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1 Score: {f1:.2f}')

if __name__ == '__main__':
    main()