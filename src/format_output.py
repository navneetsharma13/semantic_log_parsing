import csv
import json
import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Format_output:

    @staticmethod
    def format_response(response):
        reg = re.compile("`([^`]+)`")
        template = reg.findall(response)
        if len(template) > 0:
            print(template[-1])
            return template[-1]
        else:
            if "\n" in response.strip():
                logger.warning(response)
                logger.warning("=" * 20)
            return response.strip() 
        
    @staticmethod
    def save_json_output(file_path, output):
        logger.info("output will be saved into " + str(file_path) + " in json format")
        with open(file_path, 'w') as file:
            json.dump(output, file)
        logger.info("the output has been saved in json format!")

    @staticmethod
    def save_raw_output(file_path, output_list):
        logger.info("raw output will be saved into " + str(file_path))
        with open(file_path, 'w') as file:
            file.write('\n'.join(output_list))
        logger.info("raw output has been saved!")

    @staticmethod
    def save_prompt(file_path, prompt):
        logger.info("the prompt: " + prompt)
        logger.info("will be saved into " + str(file_path))
        with open(file_path, 'w') as file:
            file.write(prompt)
        logger.info("the prompt has been saved!")

    @staticmethod
    def format_string(unformatted):
        logger.info("the unformatted string: " + unformatted)
        formatted = re.sub(r'{[^}]*}*', '<*>', unformatted)
        logger.info("the formatted string: " + formatted)
        return formatted

    @staticmethod
    def format_output_file_into_csv(raw_file_path, formatted_file_path):
        with open(raw_file_path, 'r') as raw_file:
            with open(formatted_file_path, 'w', newline='') as formatted_file:
                writer = csv.writer(formatted_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                header = ['LLM_output']
                writer.writerow(header)
                for line in raw_file:
                    formatted_log_line = Format_output.format_string(line)
                    formatted_file.write(str(formatted_log_line))
        logger.info("the formatted csv file path: " + formatted_file_path)
        logger.info("the output has been formatted!")

    @staticmethod
    def add_index(formatted_output_file_path):
        logger.info("add index as LineIDs to formatted output file...")
        df = pd.read_csv(formatted_output_file_path)
        df['Line_ID'] = df.index + 1
        df.to_csv(formatted_output_file_path, index=False)

    @staticmethod
    def save_int_output(file_path, output_list):
        logger.info("int output will be saved into " + str(file_path))
        with open(file_path, 'w') as file:
            file.write('\n'.join(str(output) for output in output_list))
        logger.info("int output has been saved!")
