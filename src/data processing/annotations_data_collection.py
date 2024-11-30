import os
import pandas as pd

# Paths to the folders
folder_1 = 'data/loghub_2k/individual_logs'
folder_2 = 'data/loghub_2k/2k_dataset'
folder_3 = 'data/logs_and_annotations'

# Dataset Names
dataset_names = [
    'Apache', 'HPC', 'Linux', 'Proxifier', 'Zookeeper',
    'BGL', 'Hadoop', 'Mac', 'HealthApp', 'OpenSSH',
    'Spark', 'HDFS', 'OpenStack', 'Thunderbird'
]

# Iterate over each dataset
for dataset_name in dataset_names:
    # File paths
    modified_log_path = os.path.join(folder_1, f'{dataset_name}_modified_logs.csv')
    log_file_path = os.path.join(folder_2, dataset_name, f'{dataset_name}_2k.log')
    log_txt_path = os.path.join(folder_3, dataset_name, 'logs.txt')
    annotations_txt_path = os.path.join(folder_3, dataset_name, 'annotations.txt')

    # Read the modified log CSV into a DataFrame
    if not os.path.exists(modified_log_path):
        print(f"File not found: {modified_log_path}")
        continue

    df = pd.read_csv(modified_log_path)

    # Check if LineID column exists
    if 'LineId' not in df.columns:
        print(f"LineId column not found in {modified_log_path}")
        continue

    # Read log.txt and annotations.txt into lists
    with open(log_txt_path, 'r') as log_file:
        log_lines = [line.strip() for line in log_file.readlines()]

    with open(annotations_txt_path, 'r') as annotations_file:
        annotations_lines = [line.strip() for line in annotations_file.readlines()]

    # Add VariableTemplate column
    variable_templates = []
    
    # Iterate over each LineID in the DataFrame
    for line_id in df['LineId']:
        # Read the corresponding line from the 2k log file
        with open(log_file_path, 'r') as log_file:
            lines = [line.strip() for line in log_file.readlines()]

        # Check if line_id is a valid index
        if 0 <= line_id < len(lines):
            log_line = lines[line_id]
            
            # Find the corresponding annotation by searching in log_lines
            variable_template = ''
            for i, log in enumerate(log_lines):
                if log == log_line and i < len(annotations_lines):
                    variable_template = annotations_lines[i]
                    break
            variable_templates.append(variable_template)
        else:
            variable_templates.append('')

    # Add the VariableTemplate column to the DataFrame
    df['VariableTemplate'] = variable_templates

    # Save the updated DataFrame back to the CSV
    df.to_csv(modified_log_path, index=False)

print("Processing complete.")
