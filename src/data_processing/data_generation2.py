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

# Annotation Categories
categories = {
    'OID': 'Object ID',
    'LOI': 'Location Indicator',
    'OBN': 'Object Name',
    'TID': 'Type Indicator',
    'SID': 'Switch Indicator',
    'TDA': 'Time or Duration of an Action',
    'CRS': 'Computing Resources',
    'OBA': 'Object Amount',
    'STC': 'Status Code',
    'OTP': 'Other Parameters'
}


total_found = 0
# Iterate over each dataset
for dataset_name in dataset_names:
    # File paths
    file_path_structured_corrected = os.path.join(folder_2, dataset_name, f"{dataset_name}_2k.log_structured_corrected.csv")
    log_txt_path = os.path.join(folder_3, dataset_name, 'logs.txt')
    annotations_txt_path = os.path.join(folder_3, dataset_name, 'annotations.txt')
    modified_log_path = os.path.join(folder_1, f"{dataset_name}_modified_logs.csv")

    # Load the structured CSV file into a pandas DataFrame
    df = pd.read_csv(file_path_structured_corrected)
    
    # Modify 'EventId' to include the system name as '{folder}_{EventId}'
    df['EventId'] = df['EventId'].apply(lambda x: f"{dataset_name}_{x}")
    
    # Add a new column indicating the system (folder name)
    df['System'] = dataset_name

    # Drop duplicates based on the 'EventId' column, keeping the first occurrence
    unique_event_df = df.drop_duplicates(subset='EventId', keep='first')

    # Ensure no missing 'LineId' values before proceeding
    unique_event_df = unique_event_df.dropna(subset=['LineId']).copy()
    unique_event_df['LineId'] = unique_event_df['LineId'].astype(int)

    # Read log.txt and annotations.txt into lists
    with open(log_txt_path, 'r') as log_file:
        log_lines = [line.strip() for line in log_file.readlines()]

    with open(annotations_txt_path, 'r') as annotations_file:
        annotations_lines = [line.strip() for line in annotations_file.readlines()]

    # Create a list to store variable templates
    variable_templates = []
    found = 0

    # Iterate over each LineID in the DataFrame
    for line_id in unique_event_df['LineId']:
        # Check if line_id is a valid index in log_lines
        if 0 <= line_id - 1 < len(log_lines):
            log_line = log_lines[line_id - 1]  # Subtract 1 because LineId is 1-based
            
            # Find the corresponding annotation by searching in log_lines
            variable_template = ''
            if log_line in log_lines:
                index = log_lines.index(log_line)
                if index < len(annotations_lines):
                    variable_template = annotations_lines[index]
                    found += 1
            variable_templates.append(variable_template)
        else:
            variable_templates.append('')

    # Add the VariableTemplate column to the DataFrame
    unique_event_df['VariableTemplate'] = variable_templates

    # Add columns for each category to count occurrences in VariableTemplate
    for category in categories.keys():
        unique_event_df[category] = unique_event_df['VariableTemplate'].apply(lambda x: x.split().count(category) if pd.notna(x) else 0)

    # Save the updated DataFrame to an individual CSV file
    unique_event_df.to_csv(modified_log_path, index=False)
    total_found = total_found+found
    print(f'Found: {found}')

print("Processing complete.")
print(f'Total Found: {total_found}')
