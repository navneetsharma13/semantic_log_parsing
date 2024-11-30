import os
import pandas as pd

# Define the base path where the folders are located
base_path = 'data/loghub_2k/2k_dataset'  # Replace with the actual path to your folders

# Define the path where individual modified datasets should be saved
output_individual_path = 'data/loghub_2k/individual_logs/'  # Directory for individual modified files
# Ensure the output directory for individual files exists
os.makedirs(output_individual_path, exist_ok=True)

# List of all folder names
folders = [
    'Apache', 'HPC', 'Linux', 'Proxifier', 'Zookeeper',
    'BGL', 'Hadoop', 'Mac', 'HealthApp', 'OpenSSH',
    'Spark', 'HDFS', 'OpenStack', 'Thunderbird'
]

# Loop through each folder
for folder in folders:
    # Construct the file paths
    file_path_structured_corrected = os.path.join(base_path, folder, f"{folder}_2k.log_structured_corrected.csv")
    file_path_rawlogs = os.path.join(base_path, folder, f"{folder}_2k.log")
    
    # Load the structured CSV file into a pandas DataFrame
    df = pd.read_csv(file_path_structured_corrected)
    
    # Modify 'EventId' to include the system name as '{folder}_{EventId}'
    df['EventId'] = df['EventId'].apply(lambda x: f"{folder}_{x}")
    
    # Add a new column indicating the system (folder name)
    df['System'] = folder

    # Drop duplicates based on the 'EventId' column, keeping the first occurrence
    unique_event_df = df.drop_duplicates(subset='EventId', keep='first')

    # Ensure no missing 'LineId' values before proceeding
    unique_event_df = unique_event_df.dropna(subset=['LineId']).copy()
    unique_event_df['LineId'] = unique_event_df['LineId'].astype(int)

    # Extract the LineId column to identify which raw log lines we need
    line_ids = unique_event_df['LineId']

    # Read the raw log file into a list of lines, ignoring any trailing empty lines
    with open(file_path_rawlogs, 'r') as raw_log_file:
        raw_log_lines = [line.rstrip() for line in raw_log_file if line.strip()]

    # Select the raw log lines using the LineId values
    selected_raw_lines = []
    for line_id in line_ids:
        try:
            selected_raw_lines.append(raw_log_lines[line_id - 1])  # Subtract 1 because LineId is 1-based
        except IndexError:
            print(f"Warning: LineId {line_id} is out of range for file {file_path_rawlogs}")

    # Save the modified DataFrame to an individual CSV file
    individual_output_file = os.path.join(output_individual_path, f"{folder}_modified_logs.csv")
    unique_event_df.to_csv(individual_output_file, index=False)

print("Individual log files processing complete.")
