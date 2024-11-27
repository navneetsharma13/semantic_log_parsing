import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# File paths
ground_truth_file_path = 'data/loghub_2k/ground_truth_template.csv'  # Update the path if necessary
processed_output_file_path = 'results/20241127211340/formatted_results/output_processed.txt'


# Load ground truth data
ground_truth_df = pd.read_csv(ground_truth_file_path)
ground_truth_templates = ground_truth_df['EventTemplate'].tolist()
ground_truth_systems = ground_truth_df['System'].tolist()

# Load processed output data
with open(processed_output_file_path, 'r') as processed_file:
    processed_templates = [line.strip() for line in processed_file.readlines()]

# Ensure the lists are of the same length for comparison
min_length = min(len(ground_truth_templates), len(processed_templates))
ground_truth_templates = ground_truth_templates[:min_length]
processed_templates = processed_templates[:min_length]
ground_truth_systems = ground_truth_systems[:min_length]

# Calculate evaluation metrics
accuracy = accuracy_score(ground_truth_templates, processed_templates)
precision = precision_score(ground_truth_templates, processed_templates, average='weighted', zero_division=0)
recall = recall_score(ground_truth_templates, processed_templates, average='weighted', zero_division=0)
f1 = f1_score(ground_truth_templates, processed_templates, average='weighted', zero_division=0)

# Print evaluation metrics
print(f"Parsing Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1 Score: {f1 * 100:.2f}%")

# Calculate correctly parsed templates for each system
correct_parsed_counts = {}
for system, gt_template, processed_template in zip(ground_truth_systems, ground_truth_templates, processed_templates):
    if gt_template == processed_template:
        if system not in correct_parsed_counts:
            correct_parsed_counts[system] = 0
        correct_parsed_counts[system] += 1

# Print correctly parsed templates for each system
print("\nCorrectly Parsed Templates per System:")
for system, count in correct_parsed_counts.items():
    print(f"{system}: {count}")

# Visualization of correctly parsed templates per system
systems = list(correct_parsed_counts.keys())
counts = list(correct_parsed_counts.values())

plt.figure(figsize=(10, 6))
plt.bar(systems, counts, color='skyblue')
plt.xlabel('System')
plt.ylabel('Number of Correctly Parsed Templates')
plt.title('Correctly Parsed Templates per System')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Visualization of evaluation metrics
metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
values = [accuracy, precision, recall, f1]

# Static visualization using Matplotlib
plt.figure(figsize=(8, 5))
plt.bar(metrics, values, color='lightgreen')
plt.xlabel('Metrics')
plt.ylabel('Score')
plt.title('Evaluation Metrics for Parsing')
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig('results/evaluation_metrics.png')
plt.savefig('results/evaluation_metrics.pdf')
plt.show()