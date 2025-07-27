import argparse
import sys # Import sys to exit the program
import os # Import os for file path operations
from datetime import datetime # Import datetime for time utilities
import time # Import time for simulated delays
import subprocess # Import subprocess to run external commands
import json # Import json for JSON operations
import logging # Import logging module
import csv # Import csv for CSV operations
import re # Import re for regular expressions
import urllib.parse # Import for URL encoding/decoding
import base64 # Import for Base64 encoding/decoding
import hashlib # Import hashlib for file hashing
import difflib # Import difflib for file comparison
from collections import Counter # Import Counter for character frequency

# Configure logging
# Set up basic logging configuration
# This will output logs to the console
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Define application version
APP_VERSION = "2.10.0" # Updated version for System Information & Diagnostics

# Define configuration file path
# For simplicity, using current working directory. In a real app,
# you'd use os.path.expanduser('~/.cli_config.json') or app-specific data dirs.
CONFIG_FILE = "cli_config.json"

# Global flag to indicate if the CLI is running in interactive mode
IS_INTERACTIVE_SESSION = False

# Custom argparse error handler for interactive mode
class InteractiveArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        logger.error(f"Error: {message}")
        # Only exit if not in an interactive session
        if not IS_INTERACTIVE_SESSION:
            sys.exit(2)

def _load_config():
    """Loads configuration from the CONFIG_FILE."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error reading configuration file '{CONFIG_FILE}': Invalid JSON format. {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading configuration from '{CONFIG_FILE}': {e}")
        return {}

def _save_config(config):
    """Saves configuration to the CONFIG_FILE."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving configuration to '{CONFIG_FILE}': {e}")

def greet(name, loud=False, verbose=False):
    """
    Greets the given name.
    Args:
        name (str): The name of the person to greet.
        loud (bool): If True, the greeting will be in uppercase.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Preparing to greet '{name}'...")
    message = f"Hello, {name}! Welcome to your Python CLI."
    if loud:
        message = message.upper()
    print(message)
    if verbose:
        logger.debug("Greeting completed.")

def farewell(name, loud=False, verbose=False):
    """
    Bids farewell to the given name.
    Args:
        name (str): The name of the person to bid farewell to.
        loud (bool): If True, the farewell will be in uppercase.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Preparing to bid farewell to '{name}'...")
    message = f"Goodbye, {name}! See you next time."
    if loud:
        message = message.upper()
    print(message)
    if verbose:
        logger.debug("Farewell completed.")

def show_info(version_only=False, verbose=False, raw_output=False):
    """
    Displays information about the CLI application.
    Args:
        version_only (bool): If True, only prints the version number.
        verbose (bool): If True, prints additional details.
        raw_output (bool): If True, suppresses decorative headers/footers.
    """
    if verbose:
        logger.debug("Displaying application information.")

    if version_only:
        print(f"Version: {APP_VERSION}")
    else:
        if not raw_output:
            print(f"--- Python CLI Application Info ---")
        print(f"Version: {APP_VERSION}")
        print(f"Description: A versatile command-line tool for various tasks.")
        print(f"Author: Connor") # Personalized for you, Connor!
        if not raw_output:
            print(f"-----------------------------------")
    if verbose:
        logger.debug("Info display completed.")

def calculate(operation, num1, num2, verbose=False):
    """
    Performs a basic arithmetic calculation.
    Args:
        operation (str): The arithmetic operation ('add', 'sub', 'mul', 'div').
        num1 (float): The first number.
        num2 (float): The second number.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Performing calculation: {num1} {operation} {num2}")

    result = None
    if operation == 'add':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'mul':
        result = num1 * num2
    elif operation == 'div':
        if num2 == 0:
            logger.error("Division by zero is not allowed.")
            return # Return instead of sys.exit(1) in interactive mode
        result = num1 / num2
    else:
        logger.error(f"Invalid operation '{operation}'. Supported operations are 'add', 'sub', 'mul', 'div'.")
        return # Return instead of sys.exit(1) in interactive mode

    print(f"Result: {result}")
    if verbose:
        logger.debug("Calculation completed.")

def read_file_content(filepath, verbose=False):
    """
    Reads and prints the content of a specified file.
    Args:
        filepath (str): The path to the file to read.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Attempting to read file: {filepath}")
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            print(f"--- Content of {filepath} ---")
            print(content)
            print(f"-----------------------------")
    except FileNotFoundError:
        logger.error(f"File not found at '{filepath}'.")
        return
    except Exception as e:
        logger.error(f"Error reading file '{filepath}': {e}")
        return
    if verbose:
        logger.debug("File read operation completed.")

def write_file_content(filepath, content, verbose=False):
    """
    Writes content to a specified file.
    Args:
        filepath (str): The path to the file to write to.
        content (str): The content to write.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Attempting to write to file: {filepath}")
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Content successfully written to '{filepath}'.")
    except Exception as e:
        logger.error(f"Error writing to file '{filepath}': {e}")
        return
    if verbose:
        logger.debug("File write operation completed.")

def reverse_string(text, verbose=False):
    """
    Reverses a given string.
    Args:
        text (str): The string to reverse.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Reversing string: '{text}'")
    reversed_text = text[::-1]
    print(f"Reversed string: {reversed_text}")
    if verbose:
        logger.debug("String reversal completed.")

def count_characters(text, verbose=False):
    """
    Counts the number of characters in a given string.
    Args:
        text (str): The string to count characters from.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Counting characters in string: '{text}'")
    count = len(text)
    print(f"Character count: {count}")
    if verbose:
        logger.debug("Character count completed.")

def show_cwd(verbose=False):
    """
    Displays the current working directory.
    Args:
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug("Getting current working directory.")
    current_directory = os.getcwd()
    print(f"Current Working Directory: {current_directory}")
    if verbose:
        logger.debug("Current working directory displayed.")

def show_env_vars(verbose=False):
    """
    Displays environment variables.
    Args:
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug("Displaying environment variables.")
    print("--- Environment Variables ---")
    for key, value in os.environ.items():
        print(f"{key}={value}")
    print("-----------------------------")
    if verbose:
        logger.debug("Environment variables displayed.")

def show_current_time(verbose=False):
    """
    Displays the current date and time.
    Args:
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug("Getting current date and time.")
    now = datetime.now()
    # Connor prefers 12-hour format
    print(f"Current Date and Time: {now.strftime('%Y-%m-%d %I:%M:%S %p')}")
    if verbose:
        logger.debug("Current date and time displayed.")

def format_time(format_string, verbose=False):
    """
    Displays the current date and time in a specified format.
    Args:
        format_string (str): The format string for datetime.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Formatting current date and time with format: '{format_string}'")
    try:
        now = datetime.now()
        formatted_time = now.strftime(format_string)
        print(f"Formatted Time: {formatted_time}")
    except ValueError as e:
        logger.error(f"Invalid format string '{format_string}'. {e}")
        logger.info("Refer to Python's datetime.strftime documentation for valid format codes.")
        return
    if verbose:
        logger.debug("Time formatting completed.")

def ping_host(host, count=4, verbose=False):
    """
    Simulates pinging a host.
    Args:
        host (str): The hostname or IP address to ping.
        count (int): The number of simulated pings.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Simulating ping to {host} for {count} times.")
    print(f"Pinging {host} with simulated data:")
    for i in range(count):
        # Simulate network delay
        time.sleep(0.1)
        print(f"Reply from {host}: bytes=32 time={i*10 + 2}ms TTL=64 (simulated)")
    print(f"\n--- Ping statistics for {host} ---")
    print(f"Packets: Sent = {count}, Received = {count}, Lost = 0 (0% loss)")
    print("Approximate round trip times in milli-seconds:")
    print("Minimum = 2ms, Maximum = 32ms, Average = 17ms (simulated)")
    if verbose:
        logger.debug("Simulated ping completed.")

def lookup_host(hostname, verbose=False):
    """
    Simulates DNS lookup for a hostname.
    Args:
        hostname (str): The hostname to look up.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Simulating DNS lookup for {hostname}.")
    # Simple simulated mapping
    simulated_ips = {
        "example.com": "93.184.216.34",
        "google.com": "142.250.190.46",
        "github.com": "140.82.113.3",
        "localhost": "127.0.0.1"
    }
    ip_address = simulated_ips.get(hostname.lower(), "N/A (Simulated: Host not found)")

    print(f"--- DNS Lookup for {hostname} ---")
    print(f"Address: {ip_address}")
    print(f"Aliases: None (simulated)")
    print("---------------------------------")
    if verbose:
        logger.debug("Simulated DNS lookup completed.")

def sort_list(numbers_str, reverse_sort=False, verbose=False):
    """
    Sorts a comma-separated list of numbers.
    Args:
        numbers_str (str): A comma-separated string of numbers.
        reverse_sort (bool): If True, sorts in descending order.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Sorting numbers: '{numbers_str}' (reverse={reverse_sort})")
    try:
        numbers = [float(x.strip()) for x in numbers_str.split(',')]
        numbers.sort(reverse=reverse_sort)
        print(f"Sorted list: {numbers}")
    except ValueError:
        logger.error("Invalid number in list. Please provide comma-separated numbers.")
        return
    if verbose:
        logger.debug("List sorting completed.")

def find_unique_elements(elements_str, verbose=False):
    """
    Finds unique elements in a comma-separated list.
    Args:
        elements_str (str): A comma-separated string of elements.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Finding unique elements in: '{elements_str}'")
    elements = [x.strip() for x in elements_str.split(',')]
    unique_elements = sorted(list(set(elements))) # Sort for consistent output
    print(f"Unique elements: {unique_elements}")
    if verbose:
        logger.debug("Unique elements found.")

def run_python_script(script_path, verbose=False):
    """
    Executes an external Python script.
    Args:
        script_path (str): The path to the Python script to execute.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Attempting to run Python script: {script_path}")
    if not os.path.exists(script_path):
        logger.error(f"Script not found at '{script_path}'.")
        return
    if not script_path.lower().endswith(".py"):
        logger.error(f"'{script_path}' is not a Python script (must end with .py).")
        return

    try:
        # Use subprocess.run to execute the script
        result = subprocess.run(
            [sys.executable, script_path], # Use sys.executable for current Python interpreter
            capture_output=True,
            text=True,
            check=True # Raise an exception for non-zero exit codes
        )
        print(f"--- Output of {script_path} ---")
        print(result.stdout)
        if result.stderr:
            logger.warning(f"Errors from {script_path}:\n{result.stderr}")
        print(f"---------------------------------")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running script '{script_path}': Process exited with code {e.returncode}")
        logger.error(f"Stdout:\n{e.stdout}")
        logger.error(f"Stderr:\n{e.stderr}")
        return
    except Exception as e:
        logger.error(f"An unexpected error occurred while running script '{script_path}': {e}")
        return
    if verbose:
        logger.debug("Script execution completed.")

def create_empty_file(filepath, verbose=False):
    """
    Creates an empty file at the specified path.
    Args:
        filepath (str): The path where the empty file will be created.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Attempting to create empty file: {filepath}")
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            pass # Create an empty file
        print(f"Empty file '{filepath}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating file '{filepath}': {e}")
        return
    if verbose:
        logger.debug("Empty file creation completed.")

def parse_json(json_input, is_filepath=False, verbose=False):
    """
    Parses and pretty-prints JSON from a string or file.
    Args:
        json_input (str): The JSON string or file path.
        is_filepath (bool): If True, json_input is treated as a file path.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Parsing JSON (from file: {is_filepath}): '{json_input}'")
    content = ""
    if is_filepath:
        try:
            with open(json_input, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            logger.error(f"JSON file not found at '{json_input}'.")
            return
        except Exception as e:
            logger.error(f"Error reading JSON file '{json_input}': {e}")
            return
    else:
        content = json_input

    try:
        parsed_json = json.loads(content)
        print("--- Pretty-printed JSON ---")
        print(json.dumps(parsed_json, indent=4))
        print("---------------------------")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format. {e}")
        return
    except Exception as e:
        logger.error(f"An unexpected error occurred during JSON parsing: {e}")
        return
    if verbose:
        logger.debug("JSON parsing completed.")

def validate_json(json_string, verbose=False):
    """
    Validates if a string is a valid JSON.
    Args:
        json_string (str): The string to validate.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Validating JSON string: '{json_string}'")
    try:
        json.loads(json_string)
        print("JSON is valid.")
    except json.JSONDecodeError as e:
        logger.error(f"JSON is invalid. Error: {e}")
        return
    except Exception as e:
        logger.error(f"An unexpected error occurred during JSON validation: {e}")
        return
    if verbose:
        logger.debug("JSON validation completed.")

def celsius_to_fahrenheit(celsius, verbose=False):
    """
    Converts Celsius to Fahrenheit.
    Args:
        celsius (float): Temperature in Celsius.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Converting {celsius}°C to Fahrenheit.")
    fahrenheit = (celsius * 9/5) + 32
    print(f"{celsius}°C is {fahrenheit}°F")
    if verbose:
        logger.debug("Celsius to Fahrenheit conversion completed.")

def fahrenheit_to_celsius(fahrenheit, verbose=False):
    """
    Converts Fahrenheit to Celsius.
    Args:
        fahrenheit (float): Temperature in Fahrenheit.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Converting {fahrenheit}°F to Celsius.")
    celsius = (fahrenheit - 32) * 5/9
    print(f"{fahrenheit}°F is {celsius}°C")
    if verbose:
        logger.debug("Fahrenheit to Celsius conversion completed.")

def set_config_value(key, value, verbose=False):
    """Sets a configuration value."""
    if verbose:
        logger.debug(f"Setting config: '{key}' = '{value}'")
    config = _load_config()
    config[key] = value
    _save_config(config)
    print(f"Configuration '{key}' set to '{value}'.")
    if verbose:
        logger.debug("Config set operation completed.")

def get_config_value(key, verbose=False):
    """Gets a configuration value."""
    if verbose:
        logger.debug(f"Getting config for key: '{key}'")
    config = _load_config()
    value = config.get(key)
    if value is not None:
        print(f"Configuration '{key}': {value}")
    else:
        logger.warning(f"Configuration key '{key}' not found.")
    if verbose:
        logger.debug("Config get operation completed.")

def list_all_configs(verbose=False, raw_output=False):
    """
    Lists all configuration values.
    Args:
        verbose (bool): If True, prints additional details.
        raw_output (bool): If True, suppresses decorative headers/footers.
    """
    if verbose:
        logger.debug("Listing all configurations.")
    config = _load_config()
    if not config:
        print("No configurations found.")
        return
    if not raw_output:
        print("--- Current Configurations ---")
    for key, value in config.items():
        print(f"{key}: {value}")
    if not raw_output:
        print("------------------------------")
    if verbose:
        logger.debug("Config list operation completed.")

def reset_configs(verbose=False):
    """Resets all configurations."""
    if verbose:
        logger.debug("Resetting all configurations.")
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            print("All configurations reset.")
        else:
            print("No configuration file found to reset.")
    except Exception as e:
        logger.error(f"Error resetting configurations: {e}")
        return
    if verbose:
        logger.debug("Config reset operation completed.")

def csv_to_json_converter(input_filepath, output_filepath=None, key_column=None, verbose=False):
    """
    Converts a CSV file to JSON.
    Args:
        input_filepath (str): Path to the input CSV file.
        output_filepath (str, optional): Path to save the JSON output. If None, prints to stdout.
        key_column (str, optional): Name of the column to use as the key in JSON objects.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Converting CSV '{input_filepath}' to JSON (key_column: {key_column}).")
    data = []
    try:
        with open(input_filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        logger.error(f"CSV file not found at '{input_filepath}'.")
        return
    except Exception as e:
        logger.error(f"Error reading CSV file '{input_filepath}': {e}")
        return

    json_output = {}
    if key_column:
        if not data:
            logger.error("CSV file is empty, cannot use a key column.")
            return
        if key_column not in data[0]: # Check if key_column exists in the first row (headers)
            logger.error(f"Error: Key column '{key_column}' not found in CSV headers.")
            return
        for item in data:
            key = item.pop(key_column) # Remove key_column from item and use its value as key
            json_output[key] = item
    else:
        json_output = data # Default to a list of dictionaries

    try:
        if output_filepath:
            with open(output_filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_output, jsonfile, indent=4)
            print(f"JSON data successfully written to '{output_filepath}'.")
        else:
            print("--- Converted JSON ---")
            print(json.dumps(json_output, indent=4))
            print("----------------------")
    except Exception as e:
        logger.error(f"Error writing JSON output: {e}")
        return
    if verbose:
        logger.debug("CSV to JSON conversion completed.")

def json_to_csv_converter(input_filepath, output_filepath=None, verbose=False):
    """
    Converts a JSON file (or string) to CSV.
    Assumes JSON is a list of objects or a dictionary of objects.
    Args:
        input_filepath (str): Path to the input JSON file.
        output_filepath (str, optional): Path to save the CSV output. If None, prints to stdout.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Converting JSON '{input_filepath}' to CSV.")
    json_data = None
    try:
        with open(input_filepath, 'r', encoding='utf-8') as jsonfile:
            json_data = json.load(jsonfile)
    except FileNotFoundError:
        logger.error(f"JSON file not found at '{input_filepath}'.")
        return
    except json.JSONDecodeError as e:
        logger.error(f"Error reading JSON file '{input_filepath}': Invalid JSON format. {e}")
        return
    except Exception as e:
        logger.error(f"Error reading JSON file '{input_filepath}': {e}")
        return

    if isinstance(json_data, dict):
        # If it's a dictionary of objects (e.g., from csv_to_json with key_column)
        # Convert it to a list of objects, adding the key back as a column
        processed_data = []
        for key, value in json_data.items():
            if isinstance(value, dict):
                row = {**{'_key': key}, **value} # Add a default key column, can be renamed later
                processed_data.append(row)
            else:
                logger.warning(f"Skipping non-object value for key '{key}' in JSON to CSV conversion.")
        json_data = processed_data
    elif not isinstance(json_data, list):
        logger.error("JSON input must be a list of objects or a dictionary of objects for CSV conversion.")
        return

    if not json_data:
        print("No data found in JSON for CSV conversion.")
        return

    # Collect all unique fieldnames (headers)
    fieldnames = set()
    for row in json_data:
        if isinstance(row, dict):
            fieldnames.update(row.keys())
        else:
            logger.warning(f"Skipping non-object row in JSON to CSV conversion: {row}")
    fieldnames = sorted(list(fieldnames)) # Sort for consistent header order

    try:
        if output_filepath:
            with open(output_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(json_data)
            print(f"CSV data successfully written to '{output_filepath}'.")
        else:
            # Write to a string buffer to print to stdout
            import io
            output_buffer = io.StringIO()
            writer = csv.DictWriter(output_buffer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(json_data)
            print("--- Converted CSV ---")
            print(output_buffer.getvalue())
            print("---------------------")
    except Exception as e:
        logger.error(f"Error writing CSV output: {e}")
        return
    if verbose:
        logger.debug("JSON to CSV conversion completed.")

def grep_file_content(filepath, pattern, ignore_case=False, verbose=False):
    """
    Searches for lines matching a regex pattern in a file.
    Args:
        filepath (str): The path to the file to search.
        pattern (str): The regex pattern to search for.
        ignore_case (bool): If True, performs a case-insensitive search.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Searching for pattern '{pattern}' in '{filepath}' (ignore_case={ignore_case}).")
    try:
        flags = re.IGNORECASE if ignore_case else 0
        compiled_pattern = re.compile(pattern, flags)
        found_lines = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if compiled_pattern.search(line):
                    found_lines.append(f"{line_num}: {line.strip()}")
        if found_lines:
            print(f"--- Matches in {filepath} for '{pattern}' ---")
            for line in found_lines:
                print(line)
            print("---------------------------------------------")
        else:
            print(f"No matches found for '{pattern}' in '{filepath}'.")
    except FileNotFoundError:
        logger.error(f"File not found at '{filepath}'.")
        return
    except re.error as e:
        logger.error(f"Invalid regex pattern '{pattern}': {e}")
        return
    except Exception as e:
        logger.error(f"Error searching file '{filepath}': {e}")
        return
    if verbose:
        logger.debug("Grep operation completed.")

def filter_file_lines(filepath, keyword, exclude=False, verbose=False):
    """
    Filters lines in a file that contain (or exclude) a specific keyword.
    Args:
        filepath (str): The path to the file to filter.
        keyword (str): The keyword to search for.
        exclude (bool): If True, excludes lines containing the keyword.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Filtering lines in '{filepath}' for keyword '{keyword}' (exclude={exclude}).")
    try:
        filtered_lines = []
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if (keyword in line and not exclude) or (keyword not in line and exclude):
                    filtered_lines.append(f"{line_num}: {line.strip()}")
        if filtered_lines:
            print(f"--- Filtered Lines in {filepath} ---")
            for line in filtered_lines:
                print(line)
            print("------------------------------------")
        else:
            print(f"No lines found matching filter criteria for '{keyword}' in '{filepath}'.")
    except FileNotFoundError:
        logger.error(f"File not found at '{filepath}'.")
        return
    except Exception as e:
        logger.error(f"Error filtering file '{filepath}': {e}")
        return
    if verbose:
        logger.debug("Filter lines operation completed.")

def to_upper(text, verbose=False):
    """Converts text to uppercase."""
    if verbose:
        logger.debug(f"Converting to uppercase: '{text}'")
    print(f"Uppercase: {text.upper()}")
    if verbose:
        logger.debug("Uppercase conversion completed.")

def to_lower(text, verbose=False):
    """Converts text to lowercase."""
    if verbose:
        logger.debug(f"Converting to lowercase: '{text}'")
    print(f"Lowercase: {text.lower()}")
    if verbose:
        logger.debug("Lowercase conversion completed.")

def to_title(text, verbose=False):
    """Converts text to title case."""
    if verbose:
        logger.debug(f"Converting to title case: '{text}'")
    print(f"Title Case: {text.title()}")
    if verbose:
        logger.debug("Title case conversion completed.")

def url_encode_text(text, verbose=False):
    """URL-encodes a string."""
    if verbose:
        logger.debug(f"URL encoding: '{text}'")
    encoded_text = urllib.parse.quote_plus(text)
    print(f"URL Encoded: {encoded_text}")
    if verbose:
        logger.debug("URL encoding completed.")

def url_decode_text(text, verbose=False):
    """URL-decodes a string."""
    if verbose:
        logger.debug(f"URL decoding: '{text}'")
    try:
        decoded_text = urllib.parse.unquote_plus(text)
        print(f"URL Decoded: {decoded_text}")
    except Exception as e:
        logger.error(f"Error decoding URL string '{text}': {e}")
        return
    if verbose:
        logger.debug("URL decoding completed.")

def base64_encode_text(text, verbose=False):
    """Base64-encodes a string."""
    if verbose:
        logger.debug(f"Base64 encoding: '{text}'")
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    print(f"Base64 Encoded: {encoded_bytes.decode('utf-8')}")
    if verbose:
        logger.debug("Base64 encoding completed.")

def base64_decode_text(text, verbose=False):
    """Base64-decodes a Base64 string."""
    if verbose:
        logger.debug(f"Base64 decoding: '{text}'")
    try:
        decoded_bytes = base64.b64decode(text.encode('utf-8'))
        print(f"Base64 Decoded: {decoded_bytes.decode('utf-8')}")
    except base64.binascii.Error as e:
        logger.error(f"Invalid Base64 string '{text}': {e}")
        return
    except Exception as e:
        logger.error(f"Error decoding Base64 string '{text}': {e}")
        return
    if verbose:
        logger.debug("Base64 decoding completed.")

def copy_to_clipboard(text, verbose=False):
    """
    Simulates copying text to the system clipboard.
    Note: Real clipboard integration often requires external libraries like pyperclip
    and may have limitations in sandboxed environments.
    Args:
        text (str): The text to simulate copying.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Attempting to copy to clipboard: '{text}'")
    # In a real application, you would use a library like pyperclip here:
    # try:
    #     import pyperclip
    #     pyperclip.copy(text)
    #     print(f"Text copied to clipboard: '{text}'")
    # except ImportError:
    #     logger.warning("pyperclip not installed. Cannot copy to clipboard. Please install it with 'pip install pyperclip'.")
    #     print(f"Simulated clipboard copy: '{text}'")
    # except Exception as e:
    #     logger.error(f"Error copying to clipboard: {e}")
    print(f"Simulated clipboard copy: '{text}'")
    if verbose:
        logger.debug("Simulated clipboard copy operation completed.")

def hash_file(filepath, verbose=False):
    """
    Calculates MD5 and SHA256 hashes of a file.
    Args:
        filepath (str): The path to the file.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Calculating hashes for file: '{filepath}'")
    if not os.path.exists(filepath):
        logger.error(f"File not found at '{filepath}'.")
        return
    if not os.path.isfile(filepath):
        logger.error(f"Path '{filepath}' is not a file.")
        return

    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
                sha256_hash.update(byte_block)
        print(f"--- Hashes for {filepath} ---")
        print(f"MD5:    {md5_hash.hexdigest()}")
        print(f"SHA256: {sha256_hash.hexdigest()}")
        print("-----------------------------")
    except Exception as e:
        logger.error(f"Error calculating hash for '{filepath}': {e}")
        return
    if verbose:
        logger.debug("File hashing completed.")

def list_processes(verbose=False):
    """
    Simulates listing basic information about running processes.
    Note: A true cross-platform implementation would use psutil.
    Args:
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug("Simulating listing of processes.")
    print("--- Simulated Process List ---")
    print("PID   Name             Status")
    print("------------------------------")
    print("1     systemd          Running")
    print("123   python_cli.py    Running")
    print("456   bash             Running")
    print("789   chrome           Running")
    print("1011  code             Sleeping")
    print("------------------------------")
    logger.info("Note: This is a simulated process list for demonstration purposes.")
    if verbose:
        logger.debug("Simulated process listing completed.")

def simulated_port_scan(host, ports_str, verbose=False):
    """
    Simulates scanning a host for common open ports.
    Args:
        host (str): The hostname or IP address to scan.
        ports_str (str): Comma-separated list of ports to simulate scanning.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Simulating port scan for {host} on ports: {ports_str}")
    
    try:
        ports = [int(p.strip()) for p in ports_str.split(',')]
    except ValueError:
        logger.error("Invalid port list. Please provide comma-separated numbers.")
        return

    common_open_ports = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        3389: "RDP",
        8080: "HTTP Proxy"
    }

    print(f"--- Simulated Port Scan for {host} ---")
    for port in ports:
        if port in common_open_ports:
            print(f"Port {port} ({common_open_ports[port]}): OPEN (simulated)")
        else:
            print(f"Port {port}: CLOSED (simulated)")
    print("-------------------------------------")
    logger.info("Note: This is a simulated port scan for demonstration purposes.")
    if verbose:
        logger.debug("Simulated port scan completed.")

def simulated_http_get(url, verbose=False):
    """
    Simulates making a GET request to a URL and displays mock headers/content.
    Args:
        url (str): The URL to make a GET request to.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Simulating HTTP GET request to: {url}")
    
    print(f"--- Simulated HTTP GET Request to {url} ---")
    print("Status: 200 OK (simulated)")
    print("Headers:")
    print("  Content-Type: text/html; charset=UTF-8")
    print("  Date: " + datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    print("  Server: SimulatedWebServer/1.0")
    print("Content (first 100 chars):")
    mock_content = f"<html><body><h1>Welcome to {url}!</h1><p>This is a simulated response for your GET request. The content is dynamically generated to show how a real response might look. You can extend this functionality to fetch actual web content if network access is enabled in your environment.</p></body></html>"
    print(mock_content[:100] + "...")
    print("------------------------------------------")
    logger.info("Note: This is a simulated HTTP GET request for demonstration purposes.")
    if verbose:
        logger.debug("Simulated HTTP GET request completed.")

def list_directory_content(path, recursive=False, filter_type='all', min_size=None, max_size=None, modified_after=None, verbose=False):
    """
    Lists files and directories with various filters.
    Args:
        path (str): The directory path to list.
        recursive (bool): If True, lists contents recursively.
        filter_type (str): 'all', 'file', or 'dir'.
        min_size (float, optional): Minimum file size in bytes.
        max_size (float, optional): Maximum file size in bytes.
        modified_after (str, optional): Date/time string (e.g., '2023-01-01 10:00:00') for filtering.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Listing directory '{path}' (recursive: {recursive}, type: {filter_type}, min_size: {min_size}, max_size: {max_size}, modified_after: {modified_after})")

    if not os.path.isdir(path):
        logger.error(f"Error: Directory not found at '{path}'.")
        return

    modified_after_ts = None
    if modified_after:
        try:
            # Attempt to parse common datetime formats
            modified_after_dt = datetime.strptime(modified_after, '%Y-%m-%d %H:%M:%S')
            modified_after_ts = modified_after_dt.timestamp()
        except ValueError:
            try:
                modified_after_dt = datetime.strptime(modified_after, '%Y-%m-%d')
                modified_after_ts = modified_after_dt.timestamp()
            except ValueError:
                logger.error(f"Invalid date/time format for --modified-after: '{modified_after}'. Use 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD'.")
                return

    print(f"--- Listing Contents of '{path}' ---")
    
    for root, dirs, files in os.walk(path):
        current_level_path = os.path.relpath(root, path)
        if current_level_path == ".":
            current_level_path = "" # For the root directory itself

        # Process directories
        if filter_type in ['all', 'dir']:
            for dname in dirs:
                full_path = os.path.join(root, dname)
                # No size/modified checks for directories in this implementation, but could be added
                print(f"DIR: {os.path.join(current_level_path, dname)}")

        # Process files
        if filter_type in ['all', 'file']:
            for fname in files:
                full_path = os.path.join(root, fname)
                try:
                    file_size = os.path.getsize(full_path)
                    file_mtime = os.path.getmtime(full_path)

                    size_ok = True
                    if min_size is not None and file_size < min_size:
                        size_ok = False
                    if max_size is not None and file_size > max_size:
                        size_ok = False
                    
                    time_ok = True
                    if modified_after_ts is not None and file_mtime < modified_after_ts:
                        time_ok = False

                    if size_ok and time_ok:
                        print(f"FILE: {os.path.join(current_level_path, fname)} ({file_size} bytes, Modified: {datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')})")
                except OSError as e:
                    logger.warning(f"Could not get info for '{full_path}': {e}")
                except Exception as e:
                    logger.error(f"An unexpected error occurred processing file '{full_path}': {e}")

        if not recursive:
            break # Only list top-level if not recursive

    print("------------------------------------")
    if verbose:
        logger.debug("Directory listing completed.")

def compare_two_files(filepath1, filepath2, verbose=False):
    """
    Compares the content of two files and displays differences.
    Args:
        filepath1 (str): Path to the first file.
        filepath2 (str): Path to the second file.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Comparing files: '{filepath1}' and '{filepath2}'")

    if not os.path.exists(filepath1):
        logger.error(f"Error: File not found at '{filepath1}'.")
        return
    if not os.path.exists(filepath2):
        logger.error(f"Error: File not found at '{filepath2}'.")
        return
    if not os.path.isfile(filepath1):
        logger.error(f"Error: Path '{filepath1}' is not a file.")
        return
    if not os.path.isfile(filepath2):
        logger.error(f"Error: Path '{filepath2}' is not a file.")
        return

    try:
        with open(filepath1, 'r', encoding='utf-8', errors='ignore') as f1:
            lines1 = f1.readlines()
        with open(filepath2, 'r', encoding='utf-8', errors='ignore') as f2:
            lines2 = f2.readlines()

        differ = difflib.UnifiedDiff()
        diff = list(differ.compare(lines1, lines2))

        if not diff:
            print(f"Files '{filepath1}' and '{filepath2}' are identical.")
        else:
            print(f"--- Differences between '{filepath1}' and '{filepath2}' ---")
            for line in diff:
                sys.stdout.write(line) # difflib output already contains newlines
            print("--------------------------------------------------")
    except Exception as e:
        logger.error(f"Error comparing files: {e}")
        return
    if verbose:
        logger.debug("File comparison completed.")

def _get_text_from_source(text_input, is_filepath):
    """Helper to get text content from either a string or a file."""
    if is_filepath:
        if not os.path.exists(text_input):
            logger.error(f"File not found at '{text_input}'.")
            return None
        if not os.path.isfile(text_input):
            logger.error(f"Path '{text_input}' is not a file.")
            return None
        try:
            with open(text_input, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file '{text_input}': {e}")
            return None
    else:
        return text_input

def word_count_analysis(text_input, is_filepath, verbose=False):
    """
    Counts words and lines in a given text or file.
    Args:
        text_input (str): The text string or file path.
        is_filepath (bool): If True, text_input is treated as a file path.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Performing word count (from file: {is_filepath}) on: '{text_input}'")

    content = _get_text_from_source(text_input, is_filepath)
    if content is None:
        return

    lines = content.splitlines()
    num_lines = len(lines)
    
    # Use regex to split words, handling various delimiters and multiple spaces
    words = re.findall(r'\b\w+\b', content.lower())
    num_words = len(words)

    print(f"--- Word Count Analysis ---")
    print(f"Lines: {num_lines}")
    print(f"Words: {num_words}")
    print("---------------------------")
    if verbose:
        logger.debug("Word count analysis completed.")

def char_frequency_analysis(text_input, is_filepath, verbose=False):
    """
    Analyzes character frequency in a given text or file.
    Args:
        text_input (str): The text string or file path.
        is_filepath (bool): If True, text_input is treated as a file path.
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug(f"Performing character frequency analysis (from file: {is_filepath}) on: '{text_input}'")

    content = _get_text_from_source(text_input, is_filepath)
    if content is None:
        return

    # Count all characters, including spaces and punctuation
    char_counts = Counter(content)

    print(f"--- Character Frequency Analysis ---")
    # Sort by character for consistent output, then by count descending
    sorted_chars = sorted(char_counts.items(), key=lambda item: (item[0].lower(), item[0]))
    
    for char, count in sorted_chars:
        if char == ' ':
            print(f"' ' (Space): {count}")
        elif char == '\n':
            print(f"'\\n' (Newline): {count}")
        elif char == '\t':
            print(f"'\\t' (Tab): {count}")
        else:
            print(f"'{char}': {count}")
    print("------------------------------------")
    if verbose:
        logger.debug("Character frequency analysis completed.")

def simulated_disk_usage(verbose=False):
    """
    Simulates displaying disk space usage for various partitions.
    Args:
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug("Simulating disk usage display.")

    print("--- Simulated Disk Usage ---")
    print("Filesystem      Size  Used Avail Use% Mounted on")
    print("------------------------------------------------")
    # Personalized for Connor's 256 GB SSD
    total_gb = 256
    used_gb = 120
    avail_gb = total_gb - used_gb
    use_percent = (used_gb / total_gb) * 100

    print(f"/dev/sda1       {total_gb}G {used_gb}G  {avail_gb}G {use_percent:.0f}% /")
    print(f"tmpfs           4.0G  0B  4.0G   0% /dev/shm")
    print(f"/dev/sdb1       1.0T  500G  500G  50% /mnt/data")
    print("------------------------------------------------")
    logger.info("Note: This is a simulated disk usage report for demonstration purposes.")
    if verbose:
        logger.debug("Simulated disk usage display completed.")

def simulated_system_uptime(verbose=False):
    """
    Simulates displaying system uptime.
    Args:
        verbose (bool): If True, prints additional details.
    """
    if verbose:
        logger.debug("Simulating system uptime display.")

    # Simulate uptime in seconds (e.g., 5 days, 10 hours, 30 minutes, 15 seconds)
    total_seconds = (5 * 24 * 3600) + (10 * 3600) + (30 * 60) + 15
    
    days = total_seconds // (24 * 3600)
    total_seconds %= (24 * 3600)
    hours = total_seconds // 3600
    total_seconds %= 3600
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    uptime_str = []
    if days > 0:
        uptime_str.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        uptime_str.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        uptime_str.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0:
        uptime_str.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    if not uptime_str:
        display_uptime = "0 seconds"
    else:
        display_uptime = ", ".join(uptime_str)

    print("--- Simulated System Uptime ---")
    print(f"System has been up for: {display_uptime}")
    print("-------------------------------")
    logger.info("Note: This is a simulated system uptime for demonstration purposes.")
    if verbose:
        logger.debug("Simulated system uptime display completed.")


def setup_parser():
    """
    Sets up the argparse parser with all commands and subcommands.
    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    # Use custom parser for interactive mode error handling
    parser = InteractiveArgumentParser(
        description="A versatile Python CLI application for various tasks including greetings, calculations, file operations, text utilities, system information, time utilities, network utilities, data utilities, developer utilities, JSON utilities, unit conversions, configuration management, advanced data/text processing, text transformations, clipboard utilities, system/security utilities, advanced network utilities, enhanced file system management, advanced text analysis, and system information & diagnostics.",
        epilog="Use 'python your_script_name.py <command> --help' for command-specific help."
    )

    # Add a global verbose argument
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for more details."
    )
    # Add interactive mode flag
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run the CLI in interactive mode."
    )
    # Add a global raw output argument
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Suppress decorative headers/footers for commands like 'info' and 'config_util list'."
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Greet command ---
    greet_parser = subparsers.add_parser(
        "greet",
        help="Greet a user."
    )
    greet_parser.add_argument(
        "name",
        type=str,
        help="The name of the person to greet."
    )
    greet_parser.add_argument(
        "--loud",
        action="store_true",
        help="Make the greeting loud (uppercase)."
    )

    # --- Farewell command ---
    farewell_parser = subparsers.add_parser(
        "farewell",
        help="Bid farewell to a user."
    )
    farewell_parser.add_argument(
        "name",
        type=str,
        help="The name of the person to bid farewell to."
    )
    farewell_parser.add_argument(
        "--loud",
        action="store_true",
        help="Make the farewell loud (uppercase)."
    )

    # --- Info command ---
    info_parser = subparsers.add_parser(
        "info",
        help="Display information about the application."
    )
    info_parser.add_argument(
        "--version",
        action="store_true",
        help="Only display the application version."
    )

    # --- Calculate command ---
    calculate_parser = subparsers.add_parser(
        "calculate",
        help="Perform basic arithmetic operations."
    )
    calculate_parser.add_argument(
        "operation",
        type=str,
        choices=['add', 'sub', 'mul', 'div'], # Restrict choices for operation
        help="The arithmetic operation to perform (add, sub, mul, div)."
    )
    calculate_parser.add_argument(
        "num1",
        type=float, # Allow floating-point numbers
        help="The first number."
    )
    calculate_parser.add_argument(
        "num2",
        type=float, # Allow floating-point numbers
        help="The second number."
    )

    # --- File Operations command ---
    file_op_parser = subparsers.add_parser(
        "file_op",
        help="Perform basic file reading and writing operations."
    )
    file_op_subparsers = file_op_parser.add_subparsers(dest="file_op_command", help="File operation commands")

    # Read file sub-command
    read_parser = file_op_subparsers.add_parser(
        "read",
        help="Read content from a file."
    )
    read_parser.add_argument(
        "filepath",
        type=str,
        help="The path to the file to read."
    )

    # Write file sub-command
    write_parser = file_op_subparsers.add_parser(
        "write",
        help="Write content to a file."
    )
    write_parser.add_argument(
        "filepath",
        type=str,
        help="The path to the file to write to."
    )
    write_parser.add_argument(
        "content",
        type=str,
        help="The content to write to the file."
    )

    # --- Text Utility command (basic operations) ---
    text_util_parser = subparsers.add_parser(
        "text_util",
        help="Perform basic text manipulation operations (e.g., reverse, count)."
    )
    text_util_subparsers = text_util_parser.add_subparsers(dest="text_util_command", help="Text utility commands")

    # Reverse string sub-command
    reverse_parser = text_util_subparsers.add_parser(
        "reverse",
        help="Reverse a given string."
    )
    reverse_parser.add_argument(
        "text",
        type=str,
        help="The string to reverse."
    )

    # Count characters sub-command
    count_parser = text_util_subparsers.add_parser(
        "count",
        help="Count characters in a given string."
    )
    count_parser.add_argument(
        "text",
        type=str,
        help="The string to count characters from."
    )

    # --- System Info command ---
    system_info_parser = subparsers.add_parser(
        "system_info",
        help="Display system-related information."
    )
    system_info_subparsers = system_info_parser.add_subparsers(dest="system_info_command", help="System information commands")

    # Current Working Directory sub-command
    cwd_parser = system_info_subparsers.add_parser(
        "cwd",
        help="Display the current working directory."
    )

    # Environment Variables sub-command
    env_parser = system_info_subparsers.add_parser(
        "env",
        help="Display environment variables."
    )

    # --- Time Utility command ---
    time_util_parser = subparsers.add_parser(
        "time_util",
        help="Perform time-related operations."
    )
    time_util_subparsers = time_util_parser.add_subparsers(dest="time_util_command", help="Time utility commands")

    # Show current time sub-command
    now_parser = time_util_subparsers.add_parser(
        "now",
        help="Display the current date and time."
    )

    # Format time sub-command
    format_parser = time_util_subparsers.add_parser(
        "format",
        help="Display the current date and time in a specified format."
    )
    format_parser.add_argument(
        "format_string",
        type=str,
        help="The format string (e.g., '%%Y-%%m-%%d %%I:%%M:%%S %%p')."
    )

    # --- Network Utility command ---
    network_util_parser = subparsers.add_parser(
        "network_util",
        help="Perform basic network-related operations (e.g., ping, lookup)."
    )
    network_util_subparsers = network_util_parser.add_subparsers(dest="network_util_command", help="Network utility commands")

    # Ping sub-command
    ping_parser = network_util_subparsers.add_parser(
        "ping",
        help="Simulate pinging a host."
    )
    ping_parser.add_argument(
        "host",
        type=str,
        help="The hostname or IP address to ping."
    )
    ping_parser.add_argument(
        "--count",
        type=int,
        default=4,
        help="Number of simulated pings to send (default: 4)."
    )

    # Lookup sub-command
    lookup_parser = network_util_subparsers.add_parser(
        "lookup",
        help="Simulate DNS lookup for a hostname."
    )
    lookup_parser.add_argument(
        "hostname",
        type=str,
        help="The hostname to look up."
    )

    # --- Data Utility command ---
    data_util_parser = subparsers.add_parser(
        "data_util",
        help="Perform data manipulation operations (e.g., sort, unique)."
    )
    data_util_subparsers = data_util_parser.add_subparsers(dest="data_util_command", help="Data utility commands")

    # Sort list sub-command
    sort_parser = data_util_subparsers.add_parser(
        "sort",
        help="Sort a comma-separated list of numbers."
    )
    sort_parser.add_argument(
        "numbers",
        type=str,
        help="Comma-separated numbers to sort (e.g., '5,2,8,1')."
    )
    sort_parser.add_argument(
        "--reverse",
        action="store_true",
        help="Sort in descending order."
    )

    # Find unique elements sub-command
    unique_parser = data_util_subparsers.add_parser(
        "unique",
        help="Find unique elements in a comma-separated list."
    )
    unique_parser.add_argument(
        "elements",
        type=str,
        help="Comma-separated elements (e.g., 'apple,banana,apple,orange')."
    )

    # --- Developer Utility command ---
    dev_util_parser = subparsers.add_parser(
        "dev_util",
        help="Perform developer-focused operations."
    )
    dev_util_subparsers = dev_util_parser.add_subparsers(dest="dev_util_command", help="Developer utility commands")

    # Run script sub-command
    run_script_parser = dev_util_subparsers.add_parser(
        "run_script",
        help="Execute an external Python script."
    )
    run_script_parser.add_argument(
        "script_path",
        type=str,
        help="The path to the Python script to execute."
    )

    # Create file sub-command
    create_file_parser = dev_util_subparsers.add_parser(
        "create_file",
        help="Create an empty file."
    )
    create_file_parser.add_argument(
        "filepath",
        type=str,
        help="The path where the empty file will be created."
    )

    # --- JSON Utility command ---
    json_util_parser = subparsers.add_parser(
        "json_util",
        help="Perform JSON parsing and validation operations."
    )
    json_util_subparsers = json_util_parser.add_subparsers(dest="json_util_command", help="JSON utility commands")

    # Parse JSON sub-command
    parse_json_parser = json_util_subparsers.add_parser(
        "parse",
        help="Parse and pretty-print JSON from a string or file."
    )
    parse_json_parser.add_argument(
        "json_input",
        type=str,
        help="The JSON string or path to a JSON file."
    )
    parse_json_parser.add_argument(
        "--file",
        action="store_true",
        help="Treat json_input as a file path instead of a string."
    )

    # Validate JSON sub-command
    validate_json_parser = json_util_subparsers.add_parser(
        "validate",
        help="Validate if a string is a valid JSON."
    )
    validate_json_parser.add_argument(
        "json_string",
        type=str,
        help="The JSON string to validate."
    )

    # --- Convert Utility command ---
    convert_util_parser = subparsers.add_parser(
        "convert_util",
        help="Perform unit conversion operations."
    )
    convert_util_subparsers = convert_util_parser.add_subparsers(dest="convert_util_command", help="Conversion utility commands")

    # Temperature conversion sub-command
    temp_parser = convert_util_subparsers.add_parser(
        "temp",
        help="Convert temperatures between Celsius and Fahrenheit."
    )
    temp_parser.add_argument(
        "value",
        type=float,
        help="The temperature value to convert."
    )
    temp_parser.add_argument(
        "unit",
        type=str,
        choices=['C', 'F'],
        help="The unit of the input temperature (C for Celsius, F for Fahrenheit)."
    )

    # --- Config Utility command ---
    config_util_parser = subparsers.add_parser(
        "config_util",
        help="Manage application configurations."
    )
    config_util_subparsers = config_util_parser.add_subparsers(dest="config_util_command", help="Configuration commands")

    # Set config sub-command
    set_config_parser = config_util_subparsers.add_parser(
        "set",
        help="Set a configuration key-value pair."
    )
    set_config_parser.add_argument(
        "key",
        type=str,
        help="The configuration key."
    )
    set_config_parser.add_argument(
        "value",
        type=str,
        help="The value to set for the configuration key."
    )

    # Get config sub-command
    get_config_parser = config_util_subparsers.add_parser(
        "get",
        help="Get the value of a configuration key."
    )
    get_config_parser.add_argument(
        "key",
        type=str,
        help="The configuration key to retrieve."
    )

    # List configs sub-command
    list_config_parser = config_util_subparsers.add_parser(
        "list",
        help="List all current configurations."
    )

    # Reset configs sub-command
    reset_config_parser = config_util_subparsers.add_parser(
        "reset",
        help="Reset all configurations to default (clears the config file)."
    )

    # --- Data Process Utility command ---
    data_process_util_parser = subparsers.add_parser(
        "data_process_util",
        help="Perform data format conversions (e.g., CSV to JSON)."
    )
    data_process_util_subparsers = data_process_util_parser.add_subparsers(dest="data_process_util_command", help="Data processing commands")

    # CSV to JSON sub-command
    csv_to_json_parser = data_process_util_subparsers.add_parser(
        "csv_to_json",
        help="Convert a CSV file to JSON."
    )
    csv_to_json_parser.add_argument(
        "input_filepath",
        type=str,
        help="Path to the input CSV file."
    )
    csv_to_json_parser.add_argument(
        "--output-filepath",
        type=str,
        help="Optional: Path to save the JSON output. If not provided, output is printed to stdout."
    )
    csv_to_json_parser.add_argument(
        "--key-column",
        type=str,
        help="Optional: Name of the CSV column to use as the key in JSON objects."
    )

    # JSON to CSV sub-command
    json_to_csv_parser = data_process_util_subparsers.add_parser(
        "json_to_csv",
        help="Convert a JSON file (or string) to CSV."
    )
    json_to_csv_parser.add_argument(
        "input_filepath",
        type=str,
        help="Path to the input JSON file."
    )
    json_to_csv_parser.add_argument(
        "--output-filepath",
        type=str,
        help="Optional: Path to save the CSV output. If not provided, output is printed to stdout."
    )

    # --- Text Filter Utility command ---
    text_filter_util_parser = subparsers.add_parser(
        "text_filter_util",
        help="Perform text filtering and searching operations on files."
    )
    text_filter_util_subparsers = text_filter_util_parser.add_subparsers(dest="text_filter_util_command", help="Text filtering commands")

    # Grep sub-command
    grep_parser = text_filter_util_subparsers.add_parser(
        "grep",
        help="Search for lines matching a regex pattern in a file."
    )
    grep_parser.add_argument(
        "filepath",
        type=str,
        help="The path to the file to search."
    )
    grep_parser.add_argument(
        "pattern",
        type=str,
        help="The regex pattern to search for."
    )
    grep_parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Perform a case-insensitive search."
    )

    # Filter lines sub-command
    filter_lines_parser = text_filter_util_subparsers.add_parser(
        "filter_lines",
        help="Filter lines in a file that contain (or exclude) a specific keyword."
    )
    filter_lines_parser.add_argument(
        "filepath",
        type=str,
        help="The path to the file to filter."
    )
    filter_lines_parser.add_argument(
        "keyword",
        type=str,
        help="The keyword to search for."
    )
    filter_lines_parser.add_argument(
        "--exclude",
        action="store_true",
        help="Exclude lines containing the keyword instead of including them."
    )

    # --- Text Transform Utility command (case conversion, encoding/decoding) ---
    text_transform_util_parser = subparsers.add_parser(
        "text_transform_util",
        help="Perform text transformation operations (e.g., case conversion, encoding/decoding)."
    )
    text_transform_util_subparsers = text_transform_util_parser.add_subparsers(dest="text_transform_util_command", help="Text transformation commands")

    # Uppercase sub-command
    upper_parser = text_transform_util_subparsers.add_parser(
        "upper",
        help="Convert text to uppercase."
    )
    upper_parser.add_argument(
        "text",
        type=str,
        help="The text to convert to uppercase."
    )

    # Lowercase sub-command
    lower_parser = text_transform_util_subparsers.add_parser(
        "lower",
        help="Convert text to lowercase."
    )
    lower_parser.add_argument(
        "text",
        type=str,
        help="The text to convert to lowercase."
    )

    # Title case sub-command
    title_parser = text_transform_util_subparsers.add_parser(
        "title",
        help="Convert text to title case."
    )
    title_parser.add_argument(
        "text",
        type=str,
        help="The text to convert to title case."
    )

    # URL Encode sub-command
    url_encode_parser = text_transform_util_subparsers.add_parser(
        "url_encode",
        help="URL-encode a string."
    )
    url_encode_parser.add_argument(
        "text",
        type=str,
        help="The string to URL-encode."
    )

    # URL Decode sub-command
    url_decode_parser = text_transform_util_subparsers.add_parser(
        "url_decode",
        help="URL-decode a string."
    )
    url_decode_parser.add_argument(
        "text",
        type=str,
        help="The string to URL-decode."
    )

    # Base64 Encode sub-command
    base64_encode_parser = text_transform_util_subparsers.add_parser(
        "base64_encode",
        help="Base64-encode a string."
    )
    base64_encode_parser.add_argument(
        "text",
        type=str,
        help="The string to Base64-encode."
    )

    # Base64 Decode sub-command
    base64_decode_parser = text_transform_util_subparsers.add_parser(
        "base64_decode",
        help="Base64-decode a string."
    )
    base64_decode_parser.add_argument(
        "text",
        type=str,
        help="The Base64 string to decode."
    )

    # --- Clipboard Utility command ---
    clipboard_util_parser = subparsers.add_parser(
        "clipboard_util",
        help="Interact with the system clipboard."
    )
    clipboard_util_subparsers = clipboard_util_parser.add_subparsers(dest="clipboard_util_command", help="Clipboard commands")

    # Copy sub-command
    copy_parser = clipboard_util_subparsers.add_parser(
        "copy",
        help="Copy text to the clipboard."
    )
    copy_parser.add_argument(
        "text",
        type=str,
        help="The text to copy to the clipboard."
    )

    # --- System & Security Utility command ---
    system_security_util_parser = subparsers.add_parser(
        "system_security_util",
        help="Perform system and security related operations."
    )
    system_security_util_subparsers = system_security_util_parser.add_subparsers(dest="system_security_util_command", help="System/Security commands")

    # Hash file sub-command
    hash_file_parser = system_security_util_subparsers.add_parser(
        "hash_file",
        help="Calculate MD5 and SHA256 hashes of a file."
    )
    hash_file_parser.add_argument(
        "filepath",
        type=str,
        help="The path to the file to hash."
    )

    # List processes sub-command
    list_processes_parser = system_security_util_subparsers.add_parser(
        "list_processes",
        help="List basic information about running processes (simulated)."
    )

    # --- Advanced Network Utility command ---
    network_adv_util_parser = subparsers.add_parser(
        "network_adv_util",
        help="Perform advanced network operations (simulated)."
    )
    network_adv_util_subparsers = network_adv_util_parser.add_subparsers(dest="network_adv_util_command", help="Advanced Network commands")

    # Port scan sub-command
    port_scan_parser = network_adv_util_subparsers.add_parser(
        "port_scan",
        help="Simulate scanning a host for common open ports."
    )
    port_scan_parser.add_argument(
        "host",
        type=str,
        help="The hostname or IP address to scan."
    )
    port_scan_parser.add_argument(
        "ports",
        type=str,
        help="Comma-separated list of ports to scan (e.g., '22,80,443')."
    )

    # HTTP GET sub-command
    http_get_parser = network_adv_util_subparsers.add_parser(
        "http_get",
        help="Simulate making a GET request to a URL."
    )
    http_get_parser.add_argument(
        "url",
        type=str,
        help="The URL to make a GET request to (e.g., 'http://example.com')."
    )

    # --- File System Utility command ---
    file_system_util_parser = subparsers.add_parser(
        "file_system_util",
        help="Perform enhanced file system management operations."
    )
    file_system_util_subparsers = file_system_util_parser.add_subparsers(dest="file_system_util_command", help="File System commands")

    # List directory sub-command
    list_dir_parser = file_system_util_subparsers.add_parser(
        "list_dir",
        help="List files and directories with filters."
    )
    list_dir_parser.add_argument(
        "path",
        type=str,
        default=".",
        nargs="?", # Make path optional, default to current directory
        help="The directory path to list (default: current directory)."
    )
    list_dir_parser.add_argument(
        "--recursive",
        action="store_true",
        help="List contents recursively in subdirectories."
    )
    list_dir_parser.add_argument(
        "--type",
        type=str,
        choices=['all', 'file', 'dir'],
        default='all',
        help="Filter by type: 'all' (default), 'file', or 'dir'."
    )
    list_dir_parser.add_argument(
        "--min-size",
        type=float,
        help="Minimum file size in bytes (only applies to files)."
    )
    list_dir_parser.add_argument(
        "--max-size",
        type=float,
        help="Maximum file size in bytes (only applies to files)."
    )
    list_dir_parser.add_argument(
        "--modified-after",
        type=str,
        help="Filter files modified after this date/time (e.g., 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD')."
    )

    # Compare files sub-command
    compare_files_parser = file_system_util_subparsers.add_parser(
        "compare_files",
        help="Compare the content of two files and show differences."
    )
    compare_files_parser.add_argument(
        "filepath1",
        type=str,
        help="Path to the first file."
    )
    compare_files_parser.add_argument(
        "filepath2",
        type=str,
        help="Path to the second file."
    )

    # --- Advanced Text Analysis Utility command ---
    text_analysis_util_parser = subparsers.add_parser(
        "text_analysis_util",
        help="Perform advanced text analysis operations."
    )
    text_analysis_util_subparsers = text_analysis_util_parser.add_subparsers(dest="text_analysis_util_command", help="Text Analysis commands")

    # Word Count sub-command
    word_count_parser = text_analysis_util_subparsers.add_parser(
        "word_count",
        help="Count words and lines in text or a file."
    )
    word_count_parser.add_argument(
        "text_input",
        type=str,
        help="The text string or path to a file."
    )
    word_count_parser.add_argument(
        "--file",
        action="store_true",
        help="Treat text_input as a file path instead of a string."
    )

    # Character Frequency sub-command
    char_frequency_parser = text_analysis_util_subparsers.add_parser(
        "char_frequency",
        help="Analyze character frequency in text or a file."
    )
    char_frequency_parser.add_argument(
        "text_input",
        type=str,
        help="The text string or path to a file."
    )
    char_frequency_parser.add_argument(
        "--file",
        action="store_true",
        help="Treat text_input as a file path instead of a string."
    )

    # --- System Information & Diagnostics Utility command ---
    system_diagnostics_util_parser = subparsers.add_parser(
        "system_diagnostics_util",
        help="Perform system information and diagnostics operations (simulated)."
    )
    system_diagnostics_util_subparsers = system_diagnostics_util_parser.add_subparsers(dest="system_diagnostics_util_command", help="System Diagnostics commands")

    # Disk Usage sub-command
    disk_usage_parser = system_diagnostics_util_subparsers.add_parser(
        "disk_usage",
        help="Display simulated disk space usage."
    )

    # Uptime sub-command
    uptime_parser = system_diagnostics_util_subparsers.add_parser(
        "uptime",
        help="Display simulated system uptime."
    )

    return parser

def execute_command(args):
    """
    Executes the appropriate command based on parsed arguments.
    Args:
        args (argparse.Namespace): The parsed arguments.
    """
    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Check for global --raw flag if applicable
    raw_output = getattr(args, 'raw', False)

    if args.command == "greet":
        greet(args.name, args.loud, args.verbose)
    elif args.command == "farewell":
        farewell(args.name, args.loud, args.verbose)
    elif args.command == "info":
        show_info(args.version, args.verbose, raw_output)
    elif args.command == "calculate":
        calculate(args.operation, args.num1, args.num2, args.verbose)
    elif args.command == "file_op":
        if args.file_op_command == "read":
            read_file_content(args.filepath, args.verbose)
        elif args.file_op_command == "write":
            write_file_content(args.filepath, args.content, args.verbose)
        else:
            logger.error("Invalid 'file_op' command. Use 'read' or 'write'.")
    elif args.command == "text_util":
        if args.text_util_command == "reverse":
            reverse_string(args.text, args.verbose)
        elif args.text_util_command == "count":
            count_characters(args.text, args.verbose)
        else:
            logger.error("Invalid 'text_util' command. Use 'reverse' or 'count'.")
    elif args.command == "system_info":
        if args.system_info_command == "cwd":
            show_cwd(args.verbose)
        elif args.system_info_command == "env":
            show_env_vars(args.verbose)
        else:
            logger.error("Invalid 'system_info' command. Use 'cwd' or 'env'.")
    elif args.command == "time_util":
        if args.time_util_command == "now":
            show_current_time(args.verbose)
        elif args.time_util_command == "format":
            format_time(args.format_string, args.verbose)
        else:
            logger.error("Invalid 'time_util' command. Use 'now' or 'format'.")
    elif args.command == "network_util":
        if args.network_util_command == "ping":
            ping_host(args.host, args.count, args.verbose)
        elif args.network_util_command == "lookup":
            lookup_host(args.hostname, args.verbose)
        else:
            logger.error("Invalid 'network_util' command. Use 'ping' or 'lookup'.")
    elif args.command == "data_util":
        if args.data_util_command == "sort":
            sort_list(args.numbers, args.reverse, args.verbose)
        elif args.data_util_command == "unique":
            find_unique_elements(args.elements, args.verbose)
        else:
            logger.error("Invalid 'data_util' command. Use 'sort' or 'unique'.")
    elif args.command == "dev_util":
        if args.dev_util_command == "run_script":
            run_python_script(args.script_path, args.verbose)
        elif args.dev_util_command == "create_file":
            create_empty_file(args.filepath, args.verbose)
        else:
            logger.error("Invalid 'dev_util' command. Use 'run_script' or 'create_file'.")
    elif args.command == "json_util":
        if args.json_util_command == "parse":
            parse_json(args.json_input, args.file, args.verbose)
        elif args.json_util_command == "validate":
            validate_json(args.json_string, args.verbose)
        else:
            logger.error("Invalid 'json_util' command. Use 'parse' or 'validate'.")
    elif args.command == "convert_util":
        if args.convert_util_command == "temp":
            if args.unit.upper() == 'C':
                celsius_to_fahrenheit(args.value, args.verbose)
            elif args.unit.upper() == 'F':
                fahrenheit_to_celsius(args.value, args.verbose)
            else:
                logger.error("Invalid temperature unit. Use 'C' or 'F'.")
        else:
            logger.error("Invalid 'convert_util' command. Use 'temp'.")
    elif args.command == "config_util":
        if args.config_util_command == "set":
            set_config_value(args.key, args.value, args.verbose)
        elif args.config_util_command == "get":
            get_config_value(args.key, args.verbose)
        elif args.config_util_command == "list":
            list_all_configs(args.verbose, raw_output) # Pass raw_output here
        elif args.config_util_command == "reset":
            reset_configs(args.verbose)
        else:
            logger.error("Invalid 'config_util' command. Use 'set', 'get', 'list', or 'reset'.")
    elif args.command == "data_process_util":
        if args.data_process_util_command == "csv_to_json":
            csv_to_json_converter(args.input_filepath, args.output_filepath, args.key_column, args.verbose)
        elif args.data_process_util_command == "json_to_csv":
            json_to_csv_converter(args.input_filepath, args.output_filepath, args.verbose)
        else:
            logger.error("Invalid 'data_process_util' command. Use 'csv_to_json' or 'json_to_csv'.")
    elif args.command == "text_filter_util":
        if args.text_filter_util_command == "grep":
            grep_file_content(args.filepath, args.pattern, args.ignore_case, args.verbose)
        elif args.text_filter_util_command == "filter_lines":
            filter_file_lines(args.filepath, args.keyword, args.exclude, args.verbose)
        else:
            logger.error("Invalid 'text_filter_util' command. Use 'grep' or 'filter_lines'.")
    elif args.command == "text_transform_util":
        if args.text_transform_util_command == "upper":
            to_upper(args.text, args.verbose)
        elif args.text_transform_util_command == "lower":
            to_lower(args.text, args.verbose)
        elif args.text_transform_util_command == "title":
            to_title(args.text, args.verbose)
        elif args.text_transform_util_command == "url_encode":
            url_encode_text(args.text, args.verbose)
        elif args.text_transform_util_command == "url_decode":
            url_decode_text(args.text, args.verbose)
        elif args.text_transform_util_command == "base64_encode":
            base64_encode_text(args.text, args.verbose)
        elif args.text_transform_util_command == "base64_decode":
            base64_decode_text(args.text, args.verbose)
        else:
            logger.error("Invalid 'text_transform_util' command. Use 'upper', 'lower', 'title', 'url_encode', 'url_decode', 'base64_encode', or 'base64_decode'.")
    elif args.command == "clipboard_util":
        if args.clipboard_util_command == "copy":
            copy_to_clipboard(args.text, args.verbose)
        else:
            logger.error("Invalid 'clipboard_util' command. Use 'copy'.")
    elif args.command == "system_security_util":
        if args.system_security_util_command == "hash_file":
            hash_file(args.filepath, args.verbose)
        elif args.system_security_util_command == "list_processes":
            list_processes(args.verbose)
        else:
            logger.error("Invalid 'system_security_util' command. Use 'hash_file' or 'list_processes'.")
    elif args.command == "network_adv_util":
        if args.network_adv_util_command == "port_scan":
            simulated_port_scan(args.host, args.ports, args.verbose)
        elif args.network_adv_util_command == "http_get":
            simulated_http_get(args.url, args.verbose)
        else:
            logger.error("Invalid 'network_adv_util' command. Use 'port_scan' or 'http_get'.")
    elif args.command == "file_system_util":
        if args.file_system_util_command == "list_dir":
            list_directory_content(args.path, args.recursive, args.type, args.min_size, args.max_size, args.modified_after, args.verbose)
        elif args.file_system_util_command == "compare_files":
            compare_two_files(args.filepath1, args.filepath2, args.verbose)
        else:
            logger.error("Invalid 'file_system_util' command. Use 'list_dir' or 'compare_files'.")
    elif args.command == "text_analysis_util":
        if args.text_analysis_util_command == "word_count":
            word_count_analysis(args.text_input, args.file, args.verbose)
        elif args.text_analysis_util_command == "char_frequency":
            char_frequency_analysis(args.text_input, args.file, args.verbose)
        else:
            logger.error("Invalid 'text_analysis_util' command. Use 'word_count' or 'char_frequency'.")
    elif args.command == "system_diagnostics_util":
        if args.system_diagnostics_util_command == "disk_usage":
            simulated_disk_usage(args.verbose)
        elif args.system_diagnostics_util_command == "uptime":
            simulated_system_uptime(args.verbose)
        else:
            logger.error("Invalid 'system_diagnostics_util' command. Use 'disk_usage' or 'uptime'.")
    else:
        logger.error("No command provided. Use --help for available commands.")


def main():
    """
    Main function to parse arguments and run the CLI.
    """
    parser = setup_parser()

    # Step 1: Parse only the global arguments first to determine interactive mode
    # and capture global flags like --verbose, --raw.
    # We use parse_known_args to allow unknown arguments for subcommands later.
    global_args, remaining_argv = parser.parse_known_args()

    global IS_INTERACTIVE_SESSION
    if global_args.interactive:
        IS_INTERACTIVE_SESSION = True
        logger.info(f"Welcome to the interactive CLI (Version {APP_VERSION}). Type 'exit' to quit.")
        logger.info("Type 'help' for a list of commands, or 'command --help' for specific command help.")
        logger.info("Use --verbose for debug output, and --raw for script-friendly output.")

        # Store initial global flags to re-apply them to interactive commands
        initial_global_flags = []
        if global_args.verbose:
            initial_global_flags.append('--verbose')
        if global_args.raw:
            initial_global_flags.append('--raw')

        while True:
            try:
                command_line = input("cli> ").strip()
                if command_line.lower() == 'exit':
                    logger.info("Exiting interactive mode. Goodbye!")
                    break
                if command_line.lower() == 'help':
                    parser.print_help()
                    continue
                if not command_line:
                    continue

                # Combine initial global flags with the current command line input
                # This ensures global flags are respected for each interactive command
                full_command_args = initial_global_flags + command_line.split()

                try:
                    # Parse arguments for the current interactive command
                    # We need to explicitly pass the arguments list to parse_args
                    interactive_args = parser.parse_args(full_command_args)
                    
                    # If no command is selected, it means the input was empty or only global flags
                    # or an invalid command was given, which argparse.error will handle.
                    if interactive_args.command is None:
                        # This case is usually handled by InteractiveArgumentParser.error,
                        # but keeping this check for clarity/safety.
                        logger.error("No command specified. Type 'help' for usage.")
                    else:
                        execute_command(interactive_args)
                except SystemExit as e:
                    # argparse.parse_args() calls sys.exit() on error or --help.
                    # We catch it here to keep the interactive loop going.
                    if e.code != 0: # Only log if it's an actual error exit
                        logger.error(f"Command execution failed.")
                except Exception as e: # Catch any other unexpected errors during command execution
                    logger.critical(f"An unhandled error occurred during command execution: {e}")
                    logger.info("Please report this issue.")

            except KeyboardInterrupt:
                logger.info("\nExiting interactive mode. Goodbye!")
                break
            except Exception as e:
                logger.critical(f"An unhandled error occurred in interactive mode: {e}")
                logger.info("Please report this issue.")
    else:
        # Non-interactive mode
        # Use the already parsed global_args and the remaining_argv for the command
        # Reconstruct sys.argv for the parser to work as expected for non-interactive mode.
        # This is the standard way argparse expects arguments for non-interactive.
        # The remaining_argv already contains the command and its specific arguments.
        # The global_args (verbose, raw) are already captured in 'args' here.
        args = parser.parse_args(remaining_argv, namespace=global_args) # Pass remaining_argv and merge into global_args namespace

        if args.command is None:
            parser.print_help()
            sys.exit(1)
        execute_command(args)

if __name__ == "__main__":
    main()
