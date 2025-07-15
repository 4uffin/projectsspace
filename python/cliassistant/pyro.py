import datetime
import json
import os
import requests
import time
import re
import platform
import psutil
import urllib.parse
import random
import readline # Import the readline module
import atexit # Import atexit for persistent history

# --- Assistant Name ---
ASSISTANT_NAME = "Pyro" 

# --- Configuration for Persistent Memory ---
MEMORY_FILE = "assistant_memory.json"
HISTORY_FILE = os.path.expanduser('~/.pyro_history') # Hidden file in user's home directory for history

def load_memory():
    """Loads assistant memory from a JSON file."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            try:
                memory = json.load(f)
                # Ensure all expected keys exist with default values if missing
                if "assistant_name" not in memory:
                    memory["assistant_name"] = "Pyro"
                if "page_visits" not in memory:
                    memory["page_visits"] = 0
                if "user_name" not in memory:
                    memory["user_name"] = None
                return memory
            except json.JSONDecodeError:
                print(f"Warning: '{MEMORY_FILE}' is corrupted or empty. Resetting memory.")
                return {"page_visits": 0, "user_name": None, "assistant_name": "Pyro"}
    return {"page_visits": 0, "user_name": None, "assistant_name": "Pyro"}

def save_memory(memory_data):
    """Saves assistant memory to a JSON file."""
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory_data, f, indent=4)

# --- Global Variables for Session ---
command_history = [] # This will be managed by readline for persistent history
assistant_memory = load_memory()
ASSISTANT_NAME = assistant_memory.get("assistant_name", "Pyro")

# --- Helper Functions ---
def get_time():
    """Returns the current time in 12-hour format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def get_date():
    """Returns the current date."""
    today = datetime.datetime.today()
    return today.strftime("%B %d, %Y")

def greet_user():
    """Greets the user based on the time of day, using remembered name if available."""
    current_hour = datetime.datetime.now().hour
    greeting_prefix = ""
    # CHANGED: Good morning now from 00:00 (midnight) to 11:59 AM
    if 0 <= current_hour < 12: 
        greeting_prefix = "Good morning"
    elif 12 <= current_hour < 18:
        greeting_prefix = "Good afternoon"
    else: # 18 (6 PM) to 23 (11:59 PM)
        greeting_prefix = "Good evening"

    if assistant_memory["user_name"]:
        return f"{greeting_prefix}, {assistant_memory['user_name']}!"
    else:
        return f"{greeting_prefix}!"

def show_loading_message(message="Fetching data"):
    """Prints a simple loading message and clears it."""
    print(f"{ASSISTANT_NAME}: {message}...", end='\r', flush=True)
    # Clear the loading message by printing spaces and then a carriage return
    print(" " * (len(message) + len(ASSISTANT_NAME) + 4), end='\r', flush=True)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- API Integration Functions ---
def get_random_joke():
    """Fetches a random joke from JokeAPI."""
    show_loading_message("Fetching a joke")
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single&blacklistFlags=racist,sexist,explicit", timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        joke_data = response.json()
        if joke_data.get('error') == False and joke_data.get('type') == 'single':
            return joke_data['joke']
        else:
            return "Sorry, couldn't find a suitable joke right now."
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to the joke API. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "The joke API took too long to respond."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching a joke: {e}"

def get_ip_info(ip_address=""):
    """Fetches geolocation information for an IP address (or current IP if none specified) from IP-API.com."""
    show_loading_message("Looking up IP info")
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        ip_data = response.json()
        if ip_data.get('status') == 'success':
            return ip_data # Return the full dict
        else:
            return {"status": "fail", "message": ip_data.get('message', 'Unknown error from API')}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Couldn't connect to the IP info API. Please check your internet connection."}
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "The IP info API took too long to respond."}
    except requests.exceptions.RequestException as e:
        return {"status": "fail", "message": f"An error occurred while fetching IP info: {e}"}

def get_device_location_coords():
    """Attempts to get the device's current approximate latitude, longitude, and city name."""
    ip_data = get_ip_info() # Call without argument to get current public IP
    if ip_data and ip_data.get('status') == 'success':
        lat = ip_data.get('lat')
        lon = ip_data.get('lon')
        city = ip_data.get('city', 'your current location')
        return lat, lon, city
    return None, None, None # Return None for all if failed

def get_location_coords_from_name(location_name):
    """Converts a location name to latitude and longitude using Open-Meteo Geocoding API."""
    show_loading_message(f"Finding coordinates for {location_name}")
    encoded_location_name = urllib.parse.quote_plus(location_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_location_name}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and data.get('results'):
            # Take the first result, often the most relevant
            first_result = data['results'][0]
            lat = first_result.get('latitude')
            lon = first_result.get('longitude')
            display_name = first_result.get('name')
            country = first_result.get('country')
            
            # Add state/region if available for better display
            admin1 = first_result.get('admin1')
            if admin1:
                display_name = f"{display_name}, {admin1}"
            
            # The Geocoding API response also includes timezone, which is useful
            timezone_str = first_result.get('timezone')
            
            return lat, lon, f"{display_name}, {country}", timezone_str
        else:
            return None, None, "unknown location", None # Indicate timezone not found
    except requests.exceptions.ConnectionError:
        return None, None, "connection error", None
    except requests.exceptions.Timeout:
        return None, None, "timeout error", None
    except requests.exceptions.RequestException as e:
        return None, None, f"API error: {e}", None
    except Exception as e:
        return None, None, f"parsing error: {e}", None

def get_local_time_and_date_for_location(location_name):
    """Fetches local time and date for a specific location using geocoding and timezone APIs."""
    latitude, longitude, display_name, timezone_str_from_geo = get_location_coords_from_name(location_name)

    if latitude is None or longitude is None:
        # display_name here already contains the specific error from get_location_coords_from_name
        return None, None, f"Could not find coordinates for '{location_name}'. Reason: {display_name}"

    # Now use the dedicated timezone API for offset, if we have coordinates
    show_loading_message(f"Getting time for {display_name}")
    timezone_url = f"https://api.open-meteo.com/v1/timezone?latitude={latitude}&longitude={longitude}"
    try:
        response = requests.get(timezone_url, timeout=10)
        response.raise_for_status()
        timezone_data = response.json()

        if 'utc_offset_seconds' in timezone_data:
            utc_offset_seconds = timezone_data['utc_offset_seconds']
            # Convert current UTC time to target timezone
            utc_now = datetime.datetime.utcnow()
            local_time = utc_now + datetime.timedelta(seconds=utc_offset_seconds)
            
            # Format time (12-hour format)
            formatted_time = local_time.strftime("%I:%M %p")
            # Format date
            formatted_date = local_time.strftime("%B %d, %Y")

            return formatted_time, formatted_date, display_name
        else:
            return None, None, f"Could not get timezone offset for {display_name}. Missing 'utc_offset_seconds'."
    except requests.exceptions.ConnectionError:
        return None, None, f"Couldn't connect to the timezone API for {display_name}. Please check your internet connection."
    except requests.exceptions.Timeout:
        return None, None, f"The timezone API took too long to respond for {display_name}."
    except requests.exceptions.RequestException as e:
        # This will catch 404s, 500s, etc. and print the specific error
        return None, None, f"An error occurred while fetching timezone info for {display_name}: {e}"
    except Exception as e:
        return None, None, f"An unexpected error occurred while parsing timezone data for {display_name}: {e}"


def get_weather_forecast(latitude, longitude):
    """Fetches a daily weather forecast from Open-Meteo."""
    show_loading_message("Checking the weather")
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={latitude}&longitude={longitude}&"
           f"current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&"
           f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&timezone=America%2FDenver")
    try:
        response = requests.get(url, timeout=15) # Increased timeout for weather API
        response.raise_for_status()
        weather_data = response.json()

        current = weather_data.get('current_weather', {})
        daily = weather_data.get('daily', {})
        daily_units = weather_data.get('daily_units', {})

        if current and daily and daily.get('time') and len(daily['time']) > 0:
            temp = current.get('temperature', 'N/A')
            windspeed = current.get('windspeed', 'N/A')
            weathercode = current.get('weathercode', 'N/A')
            
            weather_desc = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing rime fog",
                51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
                56: "Light freezing drizzle", 57: "Dense freezing drizzle",
                61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                66: "Light freezing rain", 67: "Heavy freezing rain",
                71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
                77: "Snow grains",
                80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
                85: "Slight snow showers", 86: "Heavy snow showers",
                95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
            }.get(weathercode, "Unknown weather condition")

            today_max_temp = daily['temperature_2m_max'][0]
            today_min_temp = daily['temperature_2m_min'][0]
            today_precip_sum = daily['precipitation_sum'][0]
            today_precip_prob = daily['precipitation_probability_max'][0]

            temp_unit = daily_units.get('temperature_2m_max', '°F')
            wind_unit = weather_data.get('current_weather_units', {}).get('windspeed', 'mph')
            precip_unit = daily_units.get('precipitation_sum', 'mm')

            return (f"Current weather: {weather_desc}, {temp}{temp_unit}, Wind: {windspeed}{wind_unit}.\n"
                    f"Today's forecast: High {today_max_temp}{temp_unit}, Low {today_min_temp}{temp_unit}.\n"
                    f"Precipitation: {today_precip_sum}{precip_unit} (Probability: {today_precip_prob}%)")
        else:
            return "Could not retrieve detailed weather data for the specified location."
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to the weather API. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "The weather API took too long to respond."
    except requests.exceptions.HTTPError as e:
        return f"An HTTP error occurred while fetching weather: {e}. The location might be invalid or temporary API issues."
    except requests.exceptions.RequestException as e:
        return f"An unexpected error occurred while fetching weather: {e}"
    except Exception as e:
        return f"An unexpected error occurred while parsing weather data: {e}"

def get_system_info():
    """Gathers and returns basic system information."""
    info = []
    info.append(f"Operating System: {platform.system()} {platform.release()} ({platform.version()})")
    info.append(f"Architecture: {platform.machine()}")
    info.append(f"Processor: {platform.processor()}")

    # RAM
    svmem = psutil.virtual_memory()
    info.append(f"Total RAM: {svmem.total / (1024**3):.2f} GB")
    info.append(f"Available RAM: {svmem.available / (1024**3):.2f} GB")

    # Disk Usage
    partitions = psutil.disk_partitions()
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            info.append(f"Disk ({p.mountpoint}): Total {usage.total / (1024**3):.2f} GB, Used {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
        except PermissionError:
            info.append(f"Disk ({p.mountpoint}): Permission denied to access usage.")
        except Exception as e:
            info.append(f"Disk ({p.mountpoint}): Error reading usage - {e}")

    # CPU Usage (current)
    info.append(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")

    return "\n".join(info)

def get_word_count(text):
    """Counts words in a given text."""
    words = text.split()
    return len(words)

def get_character_count(text):
    """Counts characters in a given text."""
    return len(text)

def reverse_string(text):
    """Reverses a given string."""
    return text[::-1]

def base_converter(number_str, from_base, to_base):
    """Converts a number from one base to another."""
    try:
        n = int(number_str, from_base)
        
        if to_base == 2:
            return bin(n)[2:]
        elif to_base == 8:
            return oct(n)[2:]
        elif to_base == 10:
            return str(n)
        elif to_base == 16:
            return hex(n)[2:]
        else:
            return "Unsupported target base. Please use 2, 8, 10, or 16."
    except ValueError:
        return f"Invalid number '{number_str}' for base {from_base}. Please ensure the number is valid for the given base (e.g., '101' for base 2, 'A' for base 16)."
    except Exception as e:
        return f"An error occurred during base conversion: {e}"

def url_encode(text):
    """URL-encodes a given string."""
    return urllib.parse.quote_plus(text)

def url_decode(text):
    """URL-decodes a given string."""
    return urllib.parse.unquote_plus(text)

def coin_flip():
    """Simulates a coin flip."""
    return random.choice(["Heads", "Tails"])

def roll_dice(num_dice, num_sides):
    """Simulates rolling multiple dice."""
    if num_dice <= 0 or num_sides <= 0:
        return "Please specify a positive number of dice and sides."
    
    results = [random.randint(1, num_sides) for _ in range(num_dice)]
    if num_dice == 1:
        return f"You rolled a {results[0]}."
    else:
        return f"You rolled {num_dice} D{num_sides} dice. Results: {', '.join(map(str, results))}. Total: {sum(results)}."

def list_files_in_directory(path="."):
    """Lists files and directories in a given path."""
    try:
        if not os.path.exists(path):
            return f"Error: Directory '{path}' not found."
        if not os.path.isdir(path):
            return f"Error: '{path}' is a file, not a directory."

        contents = os.listdir(path)
        if not contents:
            return f"The directory '{path}' is empty."
        
        output = [f"Contents of '{path}':"]
        for item in sorted(contents, key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                output.append(f"- [DIR] {item}")
            else:
                output.append(f"- [FILE] {item}")
        return "\n".join(output)
    except PermissionError:
        return f"Permission denied to access directory '{path}'. You might not have the necessary rights."
    except Exception as e:
        return f"An unexpected error occurred while listing files: {e}"

def assistant_response(command):
    """Processes user commands and returns a response."""
    global assistant_memory, ASSISTANT_NAME
    
    command = command.strip() 
    if not command:
        return ""

    # readline handles history, no need to append here directly
    # command_history.append(command) 

    command_lower = command.lower()

    # --- Personalization & Utilities Commands (Moved higher for 'say' command priority) ---
    if command_lower.startswith("say "):
        text_to_say = command_lower.split("say ", 1)[1].strip()
        if text_to_say:
            return text_to_say
        else:
            return "What would you like me to say?"
    elif command_lower == "clear screen" or command_lower == "cls":
        clear_screen()
        return "Screen cleared."

    # --- General Commands (rest of the conditions remain in current order) ---
    if any(phrase in command_lower for phrase in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        if ASSISTANT_NAME.lower() in command_lower or "your name" not in command_lower:
            return greet_user() + " How can I help you today?"
    # Time in specific location (placed before general time to ensure specificity)
    elif command_lower.startswith("time in "): 
        location_query = command_lower.split("time in ", 1)[1].strip()
        if location_query:
            time_str, date_str, display_name = get_local_time_and_date_for_location(location_query)
            if time_str is not None:
                return f"The current time in {display_name} is {time_str}."
            else:
                return f"Sorry, I couldn't get the time for '{location_query}'. {display_name}"
        else:
            return "Please specify a location after 'time in'. Example: 'time in London'."
    elif "time" in command_lower or "what's the time" in command_lower or "current time" in command_lower or "tell me the time" in command_lower:
        return f"The current time is {get_time()}."
    # Date in specific location (placed before general date to ensure specificity)
    elif command_lower.startswith("date in "): 
        location_query = command_lower.split("date in ", 1)[1].strip()
        if location_query:
            time_str, date_str, display_name = get_local_time_and_date_for_location(location_query)
            if date_str is not None:
                return f"Today's date in {display_name} is {date_str}."
            else:
                return f"Sorry, I couldn't get the date for '{location_query}'. {display_name}"
        else:
            return "Please specify a location after 'date in'. Example: 'date in Tokyo'."
    elif "date" in command_lower or "what day is it" in command_lower or "today's date" in command_lower or "tell me the date" in command_lower:
        return f"Today's date is {get_date()}."
    elif "your name" in command_lower or "who are you" in command_lower or "what is your name" in command_lower:
        return f"My name is {ASSISTANT_NAME}. I'm a simple CLI assistant."
    elif "my name is" in command_lower or "you can call me" in command_lower or "i am" in command_lower:
        name = ""
        if "my name is" in command_lower:
            parts = command_lower.split("my name is", 1)
            if len(parts) > 1:
                name = parts[1].strip().title()
        elif "you can call me" in command_lower:
            parts = command_lower.split("you can call me", 1)
            if len(parts) > 1:
                name = parts[1].strip().title()
        elif "i am" in command_lower:
            parts = command_lower.split("i am", 1)
            if len(parts) > 1:
                potential_name = parts[1].strip().title()
                if potential_name and len(potential_name.split()) == 1 and potential_name.lower() not in ["bored", "fine", "good", "happy", "sad", "sick"]:
                    name = potential_name
                elif len(potential_name.split()) > 1:
                     name = potential_name

        if name:
            assistant_memory["user_name"] = name
            save_memory(assistant_memory)
            return f"Nice to meet you, {name}! I'll remember that."
        else:
            return "Please tell me your name clearly, for example: 'my name is [your name]', 'you can call me [your name]', or 'I am [your name]'."
    elif "what is my name" in command_lower or "do you know my name" in command_lower:
        if assistant_memory["user_name"]:
            return f"Your name is {assistant_memory['user_name']}."
        else:
            return "I don't recall your name. You can tell me by saying 'my name is [your name]'."
    elif any(phrase in command_lower for phrase in ["how are you", "how are you doing", "how's it going", "how are things"]):
        return "I'm doing great, thank you for asking! Ready to assist."
    
    # Calculator with more flexible parsing
    elif any(op_word in command_lower for op_word in ["plus", "minus", "times", "divided by", "add", "subtract", "multiply", "divide", "+", "-", "*", "/"]) or \
         any(keyword in command_lower for keyword in ["calculate", "what is", "compute", "solve"]):
        try:
            clean_command = command_lower.replace("what is", "").replace("calculate", "").replace("compute", "").replace("solve", "").strip()
            
            clean_command = clean_command.replace("plus", "+")
            clean_command = clean_command.replace("minus", "-")
            clean_command = clean_command.replace("times", "*")
            clean_command = clean_command.replace("multiplied by", "*")
            clean_command = clean_command.replace("divided by", "/")
            clean_command = clean_command.replace("add to", "+")
            
            if "subtract from" in clean_command:
                parts = clean_command.split("subtract from", 1)
                val1_str = parts[0].strip()
                val2_str = parts[1].strip()

                num1_match = re.search(r'(\d+(\.\d+)?)\s*$', val1_str)
                num2_match = re.search(r'^\s*(\d+(\.\d+)?)', val2_str)

                if num1_match and num2_match:
                    num1 = float(num1_match.group(1))
                    num2 = float(num2_match.group(1))
                    expression = f"{num2} - {num1}"
                else:
                    return "Please provide two clear numbers for subtraction, eg., 'subtract 5 from 10'."
            else:
                expression = clean_command
            
            allowed_chars = "0123456789.+-*/ "
            expression_filtered = "".join(c for c in expression if c in allowed_chars)
            
            if not expression_filtered.strip():
                return "I need a valid mathematical expression to calculate."

            result = eval(expression_filtered)
            return f"The result is: {result}"
        except (ValueError, SyntaxError, NameError):
            return "Please provide valid numbers and a clear operation for calculation. Example: '5 plus 3', 'calculate 10 / 2', 'subtract 5 from 10'."
        except ZeroDivisionError:
            return "Cannot divide by zero!"
        except Exception as e:
            return f"An error occurred during calculation: {e}. Please check your input format."

    elif "history" in command_lower or "show my commands" in command_lower or "my past commands" in command_lower or "command history" in command_lower:
        # readline history is internal; for display, we'd need to read it, but that's complex with readline.
        # For simplicity, if we were tracking it in a list, we'd use that.
        # Since we use readline, the user can just use up/down arrows.
        return "You can use your Up/Down arrow keys to browse command history."
        # If we wanted to dump *all* history:
        # try:
        #     readline.write_history_file(HISTORY_FILE + ".tmp") # write current buffer
        #     with open(HISTORY_FILE + ".tmp", 'r') as f:
        #         history_lines = [line.strip() for line in f if line.strip()]
        #     os.remove(HISTORY_FILE + ".tmp")
        #     if history_lines:
        #         return "Your command history:\n" + "\n".join([f"- '{cmd}'" for cmd in history_lines])
        #     else:
        #         return "No commands in history yet."
        # except Exception as e:
        #     return f"Error reading history: {e}"

    elif "clear history" in command_lower or "delete history" in command_lower or "erase history" in command_lower:
        print(f"{ASSISTANT_NAME}: Are you sure you want to clear {ASSISTANT_NAME}'s command history? (yes/no)")
        confirmation = input("You: ").strip().lower()
        if confirmation == "yes":
            readline.clear_history() # Clear readline's internal history
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE) # Delete the persistent file
            return "Command history cleared."
        else:
            return "Command history not cleared."
    elif "page visits" in command_lower or "visits count" in command_lower or "how many times have you been started" in command_lower or "how many visits" in command_lower:
        return f"{ASSISTANT_NAME} has been started {assistant_memory['page_visits']} times."
    
    # --- API Commands ---
    elif "tell me a joke" in command_lower or "joke" in command_lower or "random joke" in command_lower or "got any jokes" in command_lower:
        return get_random_joke()
    elif "my ip info" in command_lower or "what's my ip" in command_lower or "show my ip" in command_lower or "what is my current ip" in command_lower:
        ip_data = get_ip_info()
        if ip_data.get('status') == 'success':
            return (f"IP: {ip_data.get('query', 'N/A')}\n"
                    f"Location: {ip_data.get('city', 'N/A')}, {ip_data.get('regionName', 'N/A')}, {ip_data.get('country', 'N/A')}\n"
                    f"ISP: {ip_data.get('isp', 'N/A')}")
        else:
            return f"Could not get your IP info: {ip_data.get('message', 'Unknown error')}"
    elif command_lower.startswith("ip info for") or command_lower.startswith("lookup ip") or command_lower.startswith("check ip"):
        ip_to_check = ""
        if command_lower.startswith("ip info for"):
            parts = command_lower.split("ip info for", 1)
            if len(parts) > 1:
                ip_to_check = parts[1].strip()
        elif command_lower.startswith("lookup ip"):
            parts = command_lower.split("lookup ip", 1)
            if len(parts) > 1:
                ip_to_check = parts[1].strip()
        elif command_lower.startswith("check ip"):
            parts = command_lower.split("check ip", 1)
            if len(parts) > 1:
                ip_to_check = parts[1].strip()

        if ip_to_check:
            ip_data = get_ip_info(ip_to_check)
            if ip_data.get('status') == 'success':
                 return (f"IP: {ip_data.get('query', 'N/A')}\n"
                         f"Location: {ip_data.get('city', 'N/A')}, {ip_data.get('regionName', 'N/A')}, {ip_data.get('country', 'N/A')}\n"
                         f"ISP: {ip_data.get('isp', 'N/A')}")
            else:
                 return f"Could not get IP info for {ip_to_check}: {ip_data.get('message', 'Unknown error')}. Please check the IP/domain."
        else:
            return "Please specify an IP address or domain. Example: 'ip info for 8.8.8.8' or 'lookup ip google.com'."
    elif "what's the weather" in command_lower or "weather forecast" in command_lower or command_lower == "weather" or command_lower == "current weather" or command_lower == "how's the weather":
        # General weather request - try to get device location
        latitude, longitude, location_name = get_device_location_coords()
        if latitude is not None and longitude is not None:
            return f"Fetching weather for {location_name.title()}...\n" + get_weather_forecast(latitude, longitude)
        else:
            # Fallback to Layton, UT if auto-detection fails
            return "Could not determine your current location. Fetching weather for Layton, UT instead...\n" + get_weather_forecast(latitude=41.0664, longitude=-111.9703)
    elif "weather in utah" in command_lower: # Specific request for Utah
        return get_weather_forecast(latitude=41.0664, longitude=-111.9703) # Still hardcoded for "Utah"
    elif command_lower.startswith("weather in "): # Specific location by name
        location_query = command_lower.split("weather in ", 1)[1].strip()
        if location_query:
            latitude, longitude, display_name, _ = get_location_coords_from_name(location_query) # _ for timezone_str we don't need here
            if latitude is not None and longitude is not None:
                return f"Fetching weather for {display_name}...\n" + get_weather_forecast(latitude, longitude)
            else:
                return f"Could not find weather for '{location_query}'. Reason: {display_name.replace('unknown location', 'The location could not be found or there was an API error').replace('connection error', 'A connection error occurred').replace('timeout error', 'The request timed out')}. Please try a more specific or valid location name."
        else:
            return "Please specify a location after 'weather in'. Example: 'weather in London'."
    elif "system info" in command_lower or "my computer specs" in command_lower or "show system info" in command_lower:
        return get_system_info()
    
    # --- Text Manipulation Commands ---
    elif command_lower.startswith("word count for") or command_lower.startswith("words in"):
        text_to_count = ""
        if command_lower.startswith("word count for"):
            text_to_count = command_lower.split("word count for", 1)[1].strip()
        elif command_lower.startswith("words in"):
            text_to_count = command_lower.split("words in", 1)[1].strip()
        if text_to_count:
            return f"The text contains {get_word_count(text_to_count)} words."
        else:
            return "Please provide text to count words. Example: 'word count for hello world'."
    elif command_lower.startswith("character count for") or command_lower.startswith("chars in"):
        text_to_count = ""
        if command_lower.startswith("character count for"):
            text_to_count = command_lower.split("character count for", 1)[1].strip()
        elif command_lower.startswith("chars in"):
            text_to_count = command_lower.split("chars in", 1)[1].strip()
        if text_to_count:
            return f"The text contains {get_character_count(text_to_count)} characters (including spaces)."
        else:
            return "Please provide text to count characters. Example: 'character count for hello world'."
    elif command_lower.startswith("reverse"):
        text_to_reverse = command_lower.split("reverse", 1)[1].strip()
        if text_to_reverse:
            return f"Reversed text: '{reverse_string(text_to_reverse)}'"
        else:
            return "Please provide text to reverse. Example: 'reverse hello world'."
    
    # --- Programming/Developer Tools Commands ---
    elif command_lower.startswith("base convert"):
        match = re.search(r"base convert\s+([a-zA-Z0-9]+)\s+from\s+(\d+)\s+to\s+(\d+)", command_lower)
        if match:
            number_str = match.group(1)
            try:
                from_base = int(match.group(2))
                to_base = int(match.group(3))
                return base_converter(number_str, from_base, to_base)
            except ValueError:
                return "Invalid base values. Please use integers for bases (e.g., 'base convert 10 from 10 to 2')."
        else:
            return "Invalid format for base conversion. Use: 'base convert [number] from [base] to [base]' (e.g., 'base convert 10 from 10 to 2'). Supported bases: 2, 8, 10, 16."
    elif command_lower.startswith("encode url"):
        text_to_encode = command_lower.split("encode url", 1)[1].strip()
        if text_to_encode:
            return f"URL encoded: '{url_encode(text_to_encode)}'"
        else:
            return "Please provide text to URL encode. Example: 'encode url hello world'."
    elif command_lower.startswith("decode url"):
        text_to_decode = command_lower.split("decode url", 1)[1].strip()
        if text_to_decode:
            return f"URL decoded: '{url_decode(text_to_decode)}'"
        else:
            return "Please provide text to URL decode. Example: 'decode url hello%20world'."

    # --- Fun/Engagement Commands ---
    elif "coin flip" in command_lower or "flip a coin" in command_lower:
        return coin_flip()
    elif command_lower.startswith("roll dice"):
        match = re.search(r"roll dice\s*(\d+)[dD](\d+)", command_lower)
        if match:
            try:
                num_dice = int(match.group(1))
                num_sides = int(match.group(2))
                return roll_dice(num_dice, num_sides)
            except ValueError:
                return "Invalid number of dice or sides. Please use integers (e.g., 'roll dice 2d6')."
        else:
            return "Invalid format for rolling dice. Use: 'roll dice [number]d[sides]' (e.g., 'roll dice 1d6', 'roll dice 3d10')."
    
    # --- File System (Read-Only) Commands ---
    elif command_lower.startswith("list files"):
        path_to_list = command_lower.split("list files", 1)[1].strip()
        if path_to_list:
            return list_files_in_directory(path_to_list)
        else:
            return list_files_in_directory(".")
    elif command_lower.startswith("show files in"):
        path_to_list = command_lower.split("show files in", 1)[1].strip()
        if path_to_list:
            return list_files_in_directory(path_to_list)
        else:
            return "Please specify a directory. Example: 'show files in /path/to/directory' or 'list files'."

    # --- Personalization & Utilities Commands (rest of these are below general) ---
    elif command_lower.startswith("change assistant name to"):
        new_name = command_lower.split("change assistant name to", 1)[1].strip().title()
        if new_name:
            old_name = ASSISTANT_NAME
            ASSISTANT_NAME = new_name
            assistant_memory["assistant_name"] = new_name
            save_memory(assistant_memory)
            return f"Understood! You can now call me {ASSISTANT_NAME}. (My previous name was {old_name})."
        else:
            return "Please provide a new name. Example: 'change assistant name to Jarvis'."
    
    elif "help" in command_lower or "commands" in command_lower or "cmds" in command_lower or "?" in command_lower or "what can you do" in command_lower or "list commands" in command_lower:
        return f"""
        I am {ASSISTANT_NAME}, your CLI assistant. Here are my commands:

        General Commands:
        - Greetings: 'hello', 'hi', 'hey', 'good morning/afternoon/evening'.
        - Time: 'time', 'what's the time'.
        - Time in Location: 'time in [city/place name]' (e.g., 'time in London', 'time in Tokyo').
        - Date: 'date', 'today's date'.
        - Date in Location: 'date in [city/place name]' (e.g., 'date in London', 'date in Tokyo').
        - About Me: 'who are you', 'your name'.
        - Your Name: 'my name is [name]', 'you can call me [name]'.
        - Recall Name: 'what is my name'.
        - How I'm Doing: 'how are you'.
        - Calculator: Basic math operations like '5 + 3', '10 minus 5', '5 times 3', '10 divided by 2', 'subtract 5 from 10'.
        - Command History: Use Up/Down arrow keys.
        - Clear History: 'clear history' (requires confirmation).
        - Usage Stats: 'page visits', 'how many visits'.
        - Help: 'help', 'commands', 'cmds', '?', 'what can you do'.
        - Exit: 'exit', 'quit', 'goodbye'.

        API Integrations:
        - Random Joke: 'tell me a joke', 'joke'.
        - IP Information:
            - Your IP: 'my ip info', 'what's my ip'.
            - Specific IP/Domain: 'ip info for [IP/Domain]'.
        - Weather Forecast:
            - Device Location: 'weather', 'what's the weather', 'current weather', 'how's the weather' (attempts to auto-detect location).
            - Specific (Hardcoded): 'weather in Utah' (fetches for Layton, UT).
            - Specific Location by Name: 'weather in [city/place name]' (e.g., 'weather in London', 'weather in Paris').
        - System Information: 'system info', 'my computer specs'.

        Text Tools:
        - Word Count: 'word count for [text]'.
        - Character Count: 'character count for [text]'.
        - Reverse Text: 'reverse [text]'.

        Developer Tools:
        - Base Conversion: 'base convert [number] from [base] to [base]' (bases: 2, 8, 10, 16).
        - URL Encode: 'encode url [text]'.
        - URL Decode: 'decode url [text]'.

        Fun Commands:
        - Coin Flip: 'coin flip'.
        - Roll Dice: 'roll dice [number]d[sides]' (e.g., 'roll dice 2d6').

        File System (Read-Only):
        - List Files: 'list files [path]' (lists current directory if no path).

        Personalization & Utilities:
        - Change Name: 'change assistant name to [new name]'.
        - Echo Text: 'say [text]'.
        - Clear Screen: 'clear screen' or 'cls'.
        """
    elif "exit" in command_lower or "quit" in command_lower or "goodbye" in command_lower or "bye" in command_lower or "close" in command_lower:
        return f"Goodbye! Have a great day, Connor."
    else:
        return "I'm sorry, I don't understand that command yet. Type 'help' for a list of commands."

def main():
    global assistant_memory, ASSISTANT_NAME
    ASSISTANT_NAME = assistant_memory.get("assistant_name", "Pyro")

    # Enable readline for command history on Unix-like systems (Linux Mint)
    # This also helps on Windows if pyreadline is installed
    if 'libedit' in readline.__doc__ or platform.system() != 'Windows':
        readline.set_history_length(1000) # Keep history up to 1000 commands
        # For persistent history: read history on startup, write on exit
        if os.path.exists(HISTORY_FILE):
            readline.read_history_file(HISTORY_FILE)
        atexit.register(readline.write_history_file, HISTORY_FILE)

    assistant_memory["page_visits"] += 1
    save_memory(assistant_memory)

    current_time_str = datetime.datetime.now().strftime('%I:%M %p')
    print(f"{ASSISTANT_NAME}: {greet_user()} Welcome to {ASSISTANT_NAME}! It's {current_time_str} MDT in Layton, Utah. Type 'help' for commands.")
    
    while True:
        try:
            user_input = input("\nYou: ") 
            response = assistant_response(user_input)
            
            if response: 
                print(f"{ASSISTANT_NAME}: {response}")
            
            if "exit" in user_input.lower().strip() or "quit" in user_input.lower().strip() or "goodbye" in user_input.lower().strip() or "bye" in user_input.lower().strip() or "close" in user_input.lower().strip():
                break
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(f"\n{ASSISTANT_NAME}: Exiting. Goodbye, Connor!")
            break
        except Exception as e:
            print(f"{ASSISTANT_NAME}: An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
