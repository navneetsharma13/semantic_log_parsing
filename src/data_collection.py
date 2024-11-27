import os
import pandas as pd

# Define the base path where the folders are located
base_path = 'data/loghug/2k_dataset'  # Replace with the actual path to your folders

# Define the path where individual modified datasets should be saved
output_individual_path = 'data/loghug/individual_logs/'  # Directory for individual modified files
# Ensure the output directory for individual files exists
os.makedirs(output_individual_path, exist_ok=True)

# Define the path where the final combined dataset should be saved
output_rawlogs_combined_path = 'data/loghug/combined_raw_logs.txt'
# Ensure the output directory for the final dataset exists
os.makedirs(os.path.dirname(output_rawlogs_combined_path), exist_ok=True)

# Define the path where the ground truth template should be saved
output_ground_truth_path = 'data/loghug/ground_truth_template.csv'
# Ensure the output directory for the ground truth file exists
os.makedirs(os.path.dirname(output_ground_truth_path), exist_ok=True)

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

    # Append the selected raw lines to the combined list
    all_selected_raw_lines.extend(selected_raw_lines)

    # Extract the required columns: System, EventId, Content, EventTemplate
    df_ground_truth = unique_event_df[['System','EventTemplate']].copy()
    # Append the rows to the ground truth data list
    ground_truth_data.append(df_ground_truth)
    
    # Save the modified DataFrame to an individual CSV file
    individual_output_file = os.path.join(output_individual_path, f"{folder}_modified_logs.csv")
    unique_event_df.to_csv(individual_output_file, index=False)

# Concatenate all the ground truth data into a single DataFrame
combined_ground_truth_df = pd.concat(ground_truth_data, ignore_index=True)

# Save the resulting ground truth DataFrame to a new CSV file
combined_ground_truth_df.to_csv(output_ground_truth_path, index=False)

# Write all selected raw log lines to the output text file without any additional formatting
with open(output_rawlogs_combined_path, 'w') as output_file:
    # Add a newline after each raw log line to match original format
    output_file.writelines([line + '\n' for line in all_selected_raw_lines])

# Optional print statements to verify the number of lines written and consistency
print(f"Total number of raw log lines written: {len(all_selected_raw_lines)}")
print(f"Total number of records in ground truth: {combined_ground_truth_df.shape[0]}")

# Ensure that the number of raw log lines matches the number of ground truth records
if len(all_selected_raw_lines) == combined_ground_truth_df.shape[0]:
    print("Success: The number of raw log lines matches the number of ground truth records.")
else:
    print("Error: The number of raw log lines does not match the number of ground truth records.")
