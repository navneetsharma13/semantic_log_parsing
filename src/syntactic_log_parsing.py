#%%
import time
import os
import logging
from pathlib import Path
import datetime
from config import config
from gpt_model import get_completion_from_gpt
#from claude import get_completion_from_claude
from format_output import Format_output

# Set the ROOT_DIR to your repository root.
ROOT_DIR = os.path.dirname(os.path.abspath(''))
# Set the DATA_DIR to the directory where your data resides.
DATA_DIR = os.path.join(ROOT_DIR, 'data')

save_dir_path = os.path.join(ROOT_DIR, 'results')

now_time = datetime.datetime.now()
date_string = now_time.strftime('%Y-%m-%d-%H-%M-%S')
save_dir_separator = now_time.strftime('%Y%m%d%H%M%S')

save_dir_now = os.path.join(save_dir_path, save_dir_separator)
raw_save_dir = os.path.join(save_dir_now, "raw_results/")
Path(raw_save_dir).mkdir(parents=True, exist_ok=True)
raw_output_file_name = 'output.txt'
raw_output_file_path = raw_save_dir + raw_output_file_name
prompt_file_name = 'prompt.txt'
prompt_file_path = raw_save_dir + prompt_file_name

formatted_save_dir = os.path.join(save_dir_now, "formatted_results/")
Path(formatted_save_dir).mkdir(parents=True, exist_ok=True)
formatted_output_file_name = 'output.csv'
formatted_output_file_path = formatted_save_dir + formatted_output_file_name

# the application logs
log_save_dir = os.path.join(save_dir_now, "logs/")  # for the outputs of logging module
Path(log_save_dir).mkdir(parents=True, exist_ok=True)
log_file_name = 'output.log'
app_log_file_path = log_save_dir + log_file_name
logging.basicConfig(filename=app_log_file_path, filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO, force = True)

# raw datasets to be analyzed
log_file_path = os.path.join(DATA_DIR, 'log_messages_corrected.txt')

#ground truth for the analyzed dataset
ground_truth = os.path.join(DATA_DIR, 'ground_truth_corrected_by_Khan2022.txt')

# load logs from log file line by line
def load_logs(file_path):
    logging.info("logs will be loaded from " + str(file_path))
    with open(file_path, 'r') as file:
        log_message = file.readlines()
    return log_message

logs = load_logs(log_file_path)

#to keep the outputs of the model
output_data = []
index = 0 

# logs per call
logs_per_call = 1

# to run with few-shot prompt
while index < len(logs):
    log_message = str(logs[index])
    logging.info("current index: " + str(index))
    logging.info("current log message: ")
    logging.info(log_message)
    
    prompt_enh = f"""
    You will be provided with a log message delimited by <MSG> and </MSG>. 
    The log texts describe various system events in a software system. 
    A log message usually contains a header that is automatically produced by the logging framework, including information such as timestamp, class, and logging level (INFO, DEBUG, WARN etc.). 
    The log message typically consists of two parts: 
    1. Template - message body, that contains constant strings (or keywords) describing the system events; 
    2. Parameters/Variables - dynamic variables, which reflect specific runtime status.
    You must identify and abstract all the dynamic variables in the log message with suitable placeholders inside angle brackets to extract the corresponding template.
    You must output the template corresponding to the log message. Print only the input log's template surrounded by <TPL> and </TPL>. 
    Never print an explanation of how the template is constructed.

    Here are a few examples of log messages (labeled with Q:) and corresponding templates (labeled with A:):

    Q: <MSG>[081109 204453 34 INFO dfs.FSNamesystem: BLOCK* NameSystem.addStoredBlock: blockMap updated: 10.250.11.85:50010 is added to blk_2377150260128098806 size 67108864]</MSG>
    A: <TPL>[BLOCK* NameSystem.addStoredBlock: blockMap updated: <*>:<*> is added to <*> size <*>]</TPL>

    Q: <MSG>- 1129734520 2005.10.19 R17-M0-N0-I:J18-U01 2005-10-19-08.08.40.058960 R17-M0-N0-I:J18-U01 RAS KERNEL INFO shutdown complete</MSG>
    A: <TPL>shutdown complete</TPL>

    Q: <MSG>20231114T101914E ERROR 14 while processing line 123: cannot find input '42'</MSG>
    A: <TPL>ERROR <*> while processing line <*>: cannot find input <*></TPL>

    Q: <MSG>2023-01-14 23:05:14 INFO: Reading data from /user/input/file.txt</MSG>
    A: <TPL>Reading data from <*> </TPL>

    Here is the input log message: <MSG>{log_message}</MSG>
    Please print the corresponding template.
    """
    # response = get_completion_from_claude(prompt_enh)
    response = get_completion_from_gpt(prompt_enh)
    logging.info("the response received from the model: ")
    formatted_response = Format_output.format_response(response)
    logging.info(formatted_response)
    output_data.append(formatted_response)
    if index == 0:
        Format_output.save_prompt(prompt_file_path, prompt_enh)

    index += logs_per_call

    # Sleep for 1 second after every log message
    time.sleep(1)
# %%
