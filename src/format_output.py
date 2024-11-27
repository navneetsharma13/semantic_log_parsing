import csv
import json
import re
import pandas as pd
import logging
import os

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
    def remove_TPL_from_output(raw_file_path, formatted_file_path):
        # Define the file path
        raw_output_file_path = raw_file_path  # Update to the correct path if needed
        processed_output_file_path = formatted_file_path

        # Ensure the directory for processed output exists
        os.makedirs(os.path.dirname(processed_output_file_path), exist_ok=True)

        # Read the raw output and remove the <TPL> tags
        with open(raw_output_file_path, 'r') as raw_file:
            raw_lines = raw_file.readlines()

        processed_lines = [re.sub(r'</?TPL>', '', line).strip() for line in raw_lines]

        # Write the processed output to a new file
        with open(processed_output_file_path, 'w') as processed_file:
            processed_file.writelines([line + '\n' for line in processed_lines])
        print(f"Processed output saved to: {processed_output_file_path}")    


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

    # @staticmethod
    # def add_index(formatted_output_file_path):
    #     logger.info("add index as LineIDs to formatted output file...")
    #     df = pd.read_csv(formatted_output_file_path)
    #     df['Line_ID'] = df.index + 1
    #     df.to_csv(formatted_output_file_path, index=False)

    @staticmethod
    def add_index(formatted_output_file_path):
        logger.info("Adding index as LineIDs to formatted output file...")

        try:
            # Reading the CSV with some error handling
            df = pd.read_csv(
                formatted_output_file_path,
                sep=",",  # Adjust as needed based on your CSV format
                quoting=csv.QUOTE_MINIMAL,
                on_bad_lines='warn',  # Skip or warn about bad lines
                error_bad_lines=False  # Ignore lines with too many/few columns
            )
            
            # Adding an index column
            df['Line_ID'] = df.index + 1

            # Saving the updated CSV
            df.to_csv(formatted_output_file_path, index=False)
            logger.info("Successfully added index to the formatted output file.")
            
        except pd.errors.ParserError as e:
            logger.error(f"Error parsing CSV file: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")


    @staticmethod
    def save_int_output(file_path, output_list):
        logger.info("int output will be saved into " + str(file_path))
        with open(file_path, 'w') as file:
            file.write('\n'.join(str(output) for output in output_list))
        logger.info("int output has been saved!")
