import os
import pandas as pd
import random

# Define the base path where the individual modified logs are located
individual_logs_path = 'data/loghub_2k/individual_logs'  # Directory for individual modified files

# Define the path where the sample combined raw logs should be saved
sample_rawlogs_combined_path = 'data/loghub_2k/sample_combined_raw_logs.txt'
# Ensure the output directory for the sample combined dataset exists
os.makedirs(os.path.dirname(sample_rawlogs_combined_path), exist_ok=True)

# Define the path where the sample ground truth template should be saved
sample_ground_truth_path = 'data/loghub_2k/sample_ground_truth_template.csv'
# Ensure the output directory for the sample ground truth file exists
os.makedirs(os.path.dirname(sample_ground_truth_path), exist_ok=True)

# List of all folder names
folders = [
    'Apache', 'HPC', 'Linux', 'Proxifier', 'Zookeeper',
    'BGL', 'Hadoop', 'Mac', 'HealthApp', 'OpenSSH',
    'Spark', 'HDFS', 'OpenStack', 'Thunderbird'
]

# Initialize an empty list to store log template ground truth data DataFrames
ground_truth_data = []
# Initialize an empty list to store the raw log lines
all_selected_raw_lines = []

# Loop through each folder
for folder in folders:
    # Construct the file path for the individual modified log CSV
    individual_log_file = os.path.join(individual_logs_path, f"{folder}_modified_logs.csv")
    
    # Load the individual modified CSV file into a pandas DataFrame
    df = pd.read_csv(individual_log_file)
    
    # Select 15 random rows from the DataFrame
    if len(df) >= 15:
        sample_df = df.sample(n=15, random_state=42)
    else:
        sample_df = df  # If less than 15 rows, take all rows

    # Extract the LineId column to identify which raw log lines we need
    line_ids = sample_df['LineId']

    # Construct the file path for the raw log file
    file_path_rawlogs = os.path.join('data/loghub_2k/2k_dataset', folder, f"{folder}_2k.log")

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

    # Append the selected raw lines to the combined list
    all_selected_raw_lines.extend(selected_raw_lines)

    # Extract the required columns: System, EventTemplate
    df_ground_truth = sample_df[['System', 'EventTemplate', 'VariableTemplate']].copy()
    # Append the rows to the ground truth data list
    ground_truth_data.append(df_ground_truth)

# Concatenate all the ground truth data into a single DataFrame
combined_ground_truth_df = pd.concat(ground_truth_data, ignore_index=True)

# Save the resulting ground truth DataFrame to a new CSV file
combined_ground_truth_df.to_csv(sample_ground_truth_path, index=False)

# Write all selected raw log lines to the output text file without any additional formatting
with open(sample_rawlogs_combined_path, 'w') as output_file:
    # Add a newline after each raw log line to match original format
    output_file.writelines([line + '\n' for line in all_selected_raw_lines])

# Optional print statements to verify the number of lines written and consistency
print(f"Total number of raw log lines written: {len(all_selected_raw_lines)}")
print(f"Total number of records in sample ground truth: {combined_ground_truth_df.shape[0]}")

# Ensure that the number of raw log lines matches the number of ground truth records
if len(all_selected_raw_lines) == combined_ground_truth_df.shape[0]:
    print("Success: The number of raw log lines matches the number of sample ground truth records.")
else:
    print("Error: The number of raw log lines does not match the number of sample ground truth records.")