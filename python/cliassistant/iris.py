import datetime
import json
import os
import re
import readline
import atexit
import platform
import psutil
import urllib.parse
import random
import webbrowser # Ensure this is imported for handle_open_url
import pyperclip
import requests
import qrcode
import time # Import time for uptime calculation

# --- Assistant Name ---
ASSISTANT_NAME = "Iris"

# --- Configuration for Persistent Memory ---
MEMORY_FILE = "assistant_memory.json"
HISTORY_FILE = os.path.expanduser('~/.iris_history')

def load_memory():
    """Loads assistant memory from a JSON file."""
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                try:
                    memory = json.load(f)
                    # Ensure all expected keys exist with default values if missing
                    if "assistant_name" not in memory:
                        memory["assistant_name"] = "Iris"
                    if "page_visits" not in memory:
                        memory["page_visits"] = 0
                    if "user_name" not in memory:
                        memory["user_name"] = None
                    if "total_commands_executed" not in memory: # New field
                        memory["total_commands_executed"] = 0
                    return memory
                except json.JSONDecodeError:
                    # File is corrupted or empty, reset memory
                    print(f"Warning: '{MEMORY_FILE}' is corrupted or empty. Resetting memory.")
                    return {"page_visits": 0, "user_name": None, "assistant_name": "Iris", "total_commands_executed": 0}
                except IOError as e:
                    print(f"Error reading memory file '{MEMORY_FILE}': {e}. Starting with default memory.")
                    return {"page_visits": 0, "user_name": None, "assistant_name": "Iris", "total_commands_executed": 0}
        return {"page_visits": 0, "user_name": None, "assistant_name": "Iris", "total_commands_executed": 0}
    except Exception as e:
        print(f"An unexpected error occurred during memory loading: {e}. Starting with default memory.")
        return {"page_visits": 0, "user_name": None, "assistant_name": "Iris", "total_commands_executed": 0}

def save_memory(memory_data):
    """Saves assistant memory to a JSON file."""
    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory_data, f, indent=4)
    except IOError as e:
        print(f"Error saving memory file '{MEMORY_FILE}': {e}. Data might not be persisted.")
    except Exception as e:
        print(f"An unexpected error occurred during memory saving: {e}. Data might not be persisted.")

# --- Global Variables for Session (for games) ---
assistant_memory = load_memory()
ASSISTANT_NAME = assistant_memory.get("assistant_name", "Iris")

# Guess the Number Game State
guess_the_number_game_active = False
secret_number = 0
guess_attempts = 0

# Store session start time for uptime calculation
SESSION_START_TIME = time.time()

# --- Helper Functions ---
def print_response(message):
    """Prints a response prefixed with the assistant's name."""
    print(f"{ASSISTANT_NAME}: {message}")

def show_loading_message(message="Fetching data"):
    """Prints a simple loading message and clears it."""
    print(f"{ASSISTANT_NAME}: {message}...", end='\r', flush=True)
    # Clear the loading message by printing spaces and then a carriage return
    print(" " * (len(message) + len(ASSISTANT_NAME) + 4), end='\r', flush=True)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def greet_user():
    """Greets the user based on the time of day, now generic."""
    current_hour = datetime.datetime.now().hour
    greeting_prefix = ""
    if 0 <= current_hour < 12:
        greeting_prefix = "Good morning"
    elif 12 <= current_hour < 18:
        greeting_prefix = "Good afternoon"
    else:
        greeting_prefix = "Good evening"
    
    return f"{greeting_prefix}!"

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
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "Joke API rate limit exceeded. Please wait a moment before asking for another joke."
        return f"An HTTP error occurred while fetching a joke: {e}"
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to the joke API. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "The joke API took too long to respond."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching a joke: {e}"
    except json.JSONDecodeError:
        return "Failed to decode joke API response. The API might be returning malformed data."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def get_ip_info_from_api(ip_address=""):
    """Fetches geolocation information for an IP address (or current IP if none specified) from IP-API.com."""
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        ip_data = response.json()
        if ip_data.get('status') == 'success':
            return ip_data
        else:
            return {"status": "fail", "message": ip_data.get('message', 'Unknown error from API')}
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return {"status": "fail", "message": "IP info API rate limit exceeded. Please wait a moment."}
        return {"status": "fail", "message": f"An HTTP error occurred while fetching IP info: {e}"}
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Couldn't connect to the IP info API. Please check your internet connection."}
    except requests.exceptions.Timeout:
        return {"status": "fail", "message": "The IP info API took too long to respond."}
    except requests.exceptions.RequestException as e:
        return {"status": "fail", "message": f"An error occurred while fetching IP info: {e}"}
    except json.JSONDecodeError:
        return {"status": "fail", "message": "Failed to decode IP info API response."}
    except Exception as e:
        return {"status": "fail", "message": f"An unexpected error occurred: {e}"}

def get_device_location_coords():
    """Attempts to get the device's current approximate latitude, longitude, and city name."""
    ip_data = get_ip_info_from_api()
    if ip_data and ip_data.get('status') == 'success':
        lat = ip_data.get('lat')
        lon = ip_data.get('lon')
        city = ip_data.get('city', 'your current location')
        return lat, lon, city
    return None, None, None

def get_location_coords_from_name(location_name):
    """Converts a location name to latitude and longitude using Open-Meteo Geocoding API."""
    show_loading_message(f"Finding coordinates for {location_name}")
    encoded_location_name = urllib.parse.quote_plus(location_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_location_name}&count=1&language=en&format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and data.get('results'):
            first_result = data['results'][0]
            lat = first_result.get('latitude')
            lon = first_result.get('longitude')
            display_name = first_result.get('name')
            country = first_result.get('country')
            admin1 = first_result.get('admin1')
            
            full_display_name_parts = [display_name]
            if admin1 and admin1 != display_name:
                full_display_name_parts.append(admin1)
            if country and country != display_name and country != admin1:
                full_display_name_parts.append(country)
            
            full_display_name = ", ".join(filter(None, full_display_name_parts))
            timezone_str = first_result.get('timezone')

            return lat, lon, full_display_name, timezone_str
        else:
            return None, None, "unknown location", None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return None, None, "Geocoding API rate limit exceeded. Please wait a moment.", None
        return None, None, f"API error: {e}", None
    except requests.exceptions.ConnectionError:
        return None, None, "connection error", None
    except requests.exceptions.Timeout:
        return None, None, "timeout error", None
    except requests.exceptions.RequestException as e:
        return None, None, f"API error: {e}", None
    except json.JSONDecodeError:
        return None, None, "parsing error: malformed JSON response", None
    except Exception as e:
        return None, None, f"parsing error: {e}", None

def get_local_time_and_date_for_location(location_name):
    """Fetches local time and date for a specific location using geocoding and timezone APIs."""
    latitude, longitude, display_name, timezone_str_from_geo = get_location_coords_from_name(location_name)

    if latitude is None or longitude is None:
        return None, None, f"Could not find coordinates for '{location_name}'. Reason: {display_name}"

    show_loading_message(f"Getting time for {display_name}")
    timezone_url = f"https://api.open-meteo.com/v1/timezone?latitude={latitude}&longitude={longitude}"
    try:
        response = requests.get(timezone_url, timeout=10)
        response.raise_for_status()
        timezone_data = response.json()

        if 'utc_offset_seconds' in timezone_data:
            utc_offset_seconds = timezone_data['utc_offset_seconds']
            utc_now = datetime.datetime.utcnow()
            local_time = utc_now + datetime.timedelta(seconds=utc_offset_seconds)

            formatted_time = local_time.strftime("%I:%M %p")
            formatted_date = local_time.strftime("%B %d, %Y")

            return formatted_time, formatted_date, display_name
        else:
            return None, None, f"Could not get timezone offset for {display_name}. Missing 'utc_offset_seconds'."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return None, None, f"Timezone API rate limit exceeded for {display_name}. Please wait a moment.", None
        return None, None, f"An HTTP error occurred while fetching timezone info for {display_name}: {e}", None
    except requests.exceptions.ConnectionError:
        return None, None, f"Couldn't connect to the timezone API for {display_name}. Please check your internet connection.", None
    except requests.exceptions.Timeout:
        return None, None, f"The timezone API took too long to respond for {display_name}.", None
    except requests.exceptions.RequestException as e:
        return None, None, f"An error occurred while fetching timezone info for {display_name}: {e}", None
    except json.JSONDecodeError:
        return None, None, f"Failed to decode timezone API response for {display_name}.", None
    except Exception as e:
        return None, None, f"An unexpected error occurred while parsing timezone data for {display_name}: {e}", None

def get_weather_forecast(latitude, longitude, unit="fahrenheit"):
    """Fetches a daily weather forecast from Open-Meteo with specified units."""
    temp_unit_param = "fahrenheit" if unit.lower() == "fahrenheit" else "celsius"
    show_loading_message(f"Checking the weather ({unit})")
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={latitude}&longitude={longitude}&"
           f"current_weather=true&temperature_unit={temp_unit_param}&windspeed_unit=mph&"
           f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max")
    try:
        response = requests.get(url, timeout=15)
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

            temp_unit_symbol = "°F" if temp_unit_param == "fahrenheit" else "°C"
            wind_unit = weather_data.get('current_weather_units', {}).get('windspeed', 'mph')
            precip_unit = daily_units.get('precipitation_sum', 'mm')

            return (f"Current weather: {weather_desc}, {temp}{temp_unit_symbol}, Wind: {windspeed}{wind_unit}.\n"
                    f"Today's forecast: High {today_max_temp}{temp_unit_symbol}, Low {today_min_temp}{temp_unit_symbol}.\n"
                    f"Precipitation: {today_precip_sum}{precip_unit} (Probability: {today_precip_prob}%)")
        else:
            return "Could not retrieve detailed weather data for the specified location."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "Weather API rate limit exceeded. Please wait a moment before asking for weather."
        return f"An HTTP error occurred while fetching weather: {e}. The location might be invalid or temporary API issues."
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to the weather API. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "The weather API took too long to respond."
    except requests.exceptions.RequestException as e:
        return f"An unexpected error occurred while fetching weather: {e}"
    except json.JSONDecodeError:
        return "Failed to decode weather API response."
    except Exception as e:
        return f"An unexpected error occurred while parsing weather data: {e}"

def get_instant_answer(query):
    """Fetches an instant answer from DuckDuckGo API."""
    show_loading_message(f"Searching for '{query}'")
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Prioritize AbstractText, then Definition, Fallback to others
        if data.get('AbstractText'):
            return data['AbstractText'] + (f" (Source: {data['AbstractURL']})" if data.get('AbstractURL') else "")
        elif data.get('Definition'):
            return data['Definition'] + (f" (Source: {data['DefinitionURL']})" if data.get('DefinitionURL') else "")
        elif data.get('RelatedTopics') and data['RelatedTopics'] and data['RelatedTopics'][0].get('Text'):
            # Sometimes RelatedTopics contains direct answers or short summaries
            return data['RelatedTopics'][0]['Text'] + (f" (Source: {data['RelatedTopics'][0]['FirstURL']})" if data['RelatedTopics'][0].get('FirstURL') else "")
        elif data.get('Answer'): # Direct answer sometimes provided for calculations etc.
            return data['Answer']
        else:
            return f"Sorry, I couldn't find a direct answer for '{query}'."

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "Search API rate limit exceeded. Please wait a moment before searching again."
        return f"An HTTP error occurred while searching: {e}"
    except requests.exceptions.ConnectionError:
        return "Couldn't connect to the information retrieval API. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "The information retrieval API took too long to respond."
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching information: {e}"
    except json.JSONDecodeError:
        return "Failed to decode API response. The API might be returning malformed data."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Conversion Tools Functions ---
def convert_temperature(value, from_unit, to_unit):
    """Converts temperature between Celsius, Fahrenheit, and Kelvin."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Convert to Celsius first
    if from_unit == "celsius" or from_unit == "c":
        celsius = value
    elif from_unit == "fahrenheit" or from_unit == "f":
        celsius = (value - 32) * 5/9
    elif from_unit == "kelvin" or from_unit == "k":
        celsius = value - 273.15
    else:
        return "Unsupported 'from' temperature unit. Please use Celsius, Fahrenheit, or Kelvin."

    # Convert from Celsius to target unit
    if to_unit == "celsius" or to_unit == "c":
        result = celsius
    elif to_unit == "fahrenheit" or to_unit == "f":
        result = (celsius * 9/5) + 32
    elif to_unit == "kelvin" or to_unit == "k":
        result = celsius + 273.15
    else:
        return "Unsupported 'to' temperature unit. Please use Celsius, Fahrenheit, or Kelvin."
    
    return f"{value} {from_unit} is {result:.2f} {to_unit}."


UNIT_CONVERSION_FACTORS = {
    "length": {
        "meter": 1.0, "m": 1.0,
        "kilometer": 1000.0, "km": 1000.0,
        "centimeter": 0.01, "cm": 0.01,
        "millimeter": 0.001, "mm": 0.001,
        "mile": 1609.34, "mi": 1609.34,
        "yard": 0.9144, "yd": 0.9144,
        "foot": 0.3048, "ft": 0.3048,
        "inch": 0.0254, "in": 0.0254
    },
    "mass": {
        "kilogram": 1.0, "kg": 1.0,
        "gram": 0.001, "g": 0.001,
        "pound": 0.453592, "lbs": 0.453592, "lb": 0.453592,
        "ounce": 0.0283495, "oz": 0.0283495
    },
    "volume": {
        "liter": 1.0, "l": 1.0,
        "milliliter": 0.001, "ml": 0.001,
        "gallon": 3.78541, "gal": 3.78541,
        "quart": 0.946353, "qt": 0.946353,
        "pint": 0.473176, "pt": 0.473176
    }
}

def get_unit_type(unit):
    """Determines the type of unit (e.g., length, mass, volume, temperature)."""
    unit_lower = unit.lower()
    for unit_type, units in UNIT_CONVERSION_FACTORS.items():
        if unit_lower in units:
            return unit_type
    
    if unit_lower in ["celsius", "fahrenheit", "kelvin", "c", "f", "k"]:
        return "temperature"
    
    return None

def convert_units_general(value, from_unit, to_unit):
    """Converts a value from one unit to another within the same type (excluding temperature)."""
    from_unit_lower = from_unit.lower()
    to_unit_lower = to_unit.lower()

    from_type = get_unit_type(from_unit_lower)
    to_type = get_unit_type(to_unit_lower)

    if from_type is None:
        return f"Unknown 'from' unit: '{from_unit}'. Please check the spelling or specify a supported unit."
    if to_type is None:
        return f"Unknown 'to' unit: '{to_unit}'. Please check the spelling or specify a supported unit."

    if from_type != to_type:
        return f"Cannot convert between '{from_unit_lower}' ({from_type}) and '{to_unit_lower}' ({to_type}). Units must be of the same type."
    
    if from_type == "temperature":
        return convert_temperature(value, from_unit_lower, to_unit_lower)

    # For other unit types (length, mass, volume)
    if from_unit_lower not in UNIT_CONVERSION_FACTORS[from_type] or \
       to_unit_lower not in UNIT_CONVERSION_FACTORS[to_type]:
        return "Internal error: Unit not found in conversion factors. This should not happen if get_unit_type works correctly."

    factor_from = UNIT_CONVERSION_FACTORS[from_type][from_unit_lower]
    factor_to = UNIT_CONVERSION_FACTORS[to_type][to_unit_lower]

    # Convert from 'from_unit' to base unit, then from base unit to 'to_unit'
    value_in_base_unit = value * factor_from
    converted_value = value_in_base_unit / factor_to

    return f"{value} {from_unit} is {converted_value:.2f} {to_unit}."

def base_converter(number_str, from_base, to_base):
    """Converts a number from one base to another."""
    try:
        n = int(number_str, from_base)

        if not (2 <= from_base <= 36 and 2 <= to_base <= 36): # Common range for int(str, base)
            return "Bases must be between 2 and 36."

        if to_base == 2:
            return bin(n)[2:]
        elif to_base == 8:
            return oct(n)[2:]
        elif to_base == 10:
            return str(n)
        elif to_base == 16:
            return hex(n)[2:]
        else:
            # Custom conversion for bases not directly supported by built-in functions
            # This is a basic implementation and can be expanded for full 2-36 range
            result = []
            if n == 0:
                return "0"
            while n > 0:
                remainder = n % to_base
                if remainder < 10:
                    result.append(str(remainder))
                else:
                    result.append(chr(ord('A') + remainder - 10))
                n //= to_base
            return "".join(reversed(result))
            
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

def convert_timestamp_to_datetime(timestamp):
    """Converts a Unix timestamp to a human-readable datetime string."""
    try:
        # Check if timestamp is in milliseconds and convert to seconds if so
        if len(str(int(timestamp))) == 13: # Common for JS timestamps
            timestamp /= 1000

        dt_object = datetime.datetime.fromtimestamp(timestamp)
        return dt_object.strftime("%Y-%m-%d %I:%M:%S %p %Z") # Added %Z for timezone name, but will show local tz
    except ValueError:
        return "Invalid timestamp format. Please provide a numeric Unix timestamp (e.g., '1678886400')."
    except TypeError:
        return "Invalid timestamp type. Please provide a numeric value."
    except OverflowError:
        return "Timestamp value is too large or too small to convert to a valid date."
    except Exception as e:
        return f"An error occurred during timestamp conversion: {e}"

def convert_datetime_to_timestamp(datetime_str):
    """Converts a human-readable datetime string to a Unix timestamp."""
    try:
        # Attempt to parse common formats. Can expand if needed.
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %I:%M:%S %p",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %I:%M:%S %p",
            "%m/%d/%Y",
            "%Y-%m-%d %H:%M:%S.%f", # For microseconds
            "%b %d %Y %H:%M:%S" # e.g., "Jul 20 2025 12:00:00"
        ]
        
        dt_object = None
        for fmt in formats:
            try:
                dt_object = datetime.datetime.strptime(datetime_str, fmt)
                break
            except ValueError:
                continue
        
        if dt_object is None:
            return "Could not parse the datetime string. Please use a common format like 'YYYY-MM-DD HH:MM:SS' or 'MM/DD/YYYY HH:MM:SS AM/PM'."

        return int(dt_object.timestamp())
    except Exception as e:
        return f"An error occurred during datetime to timestamp conversion: {e}"

# --- Game Logic Functions ---
def coin_flip():
    """Simulates a coin flip."""
    return random.choice(["Heads", "Tails"])

def roll_dice(num_dice, num_sides):
    """Simulates rolling multiple dice."""
    if num_dice <= 0 or num_sides <= 0:
        return "Please specify a positive number of dice and sides."
    if num_sides > 1000: # Arbitrary limit to prevent excessive computation/memory
        return "Number of sides is too large. Please use a smaller number."

    results = [random.randint(1, num_sides) for _ in range(num_dice)]
    if num_dice == 1:
        return f"You rolled a {results[0]}."
    else:
        return f"You rolled {num_dice} D{num_sides} dice. Results: {', '.join(map(str, results))}. Total: {sum(results)}."

def handle_start_guess_the_number_game(user_input):
    """Starts the 'Guess the Number' game."""
    global guess_the_number_game_active, secret_number, guess_attempts
    if guess_the_number_game_active:
        return f"A 'Guess the Number' game is already active! I'm thinking of a number between 1 and 100. What's your guess? (Or say 'quit game' to stop.)"
    
    guess_the_number_game_active = True
    secret_number = random.randint(1, 100)
    guess_attempts = 0
    return "I'm thinking of a number between 1 and 100. Can you guess it? Type your guess."

def handle_guess_the_number_game_play(user_input):
    """Handles user guesses during the 'Guess the Number' game."""
    global guess_the_number_game_active, secret_number, guess_attempts
    if not guess_the_number_game_active:
        return "No 'Guess the Number' game is active. Say 'play guess the number' to start one!"

    if user_input.lower().strip() == "quit game":
        game_was_active = guess_the_number_game_active
        number_was = secret_number
        guess_the_number_game_active = False # End game
        return f"Okay, I've ended the 'Guess the Number' game. The number was {number_was}. Thanks for playing!"

    try:
        user_guess = int(user_input.strip())
        if not 1 <= user_guess <= 100:
            return "Please guess a number between 1 and 100."
        
        guess_attempts += 1 # Update attempts
        
        if user_guess < secret_number:
            return f"Too low! Try again. (Attempt: {guess_attempts})"
        elif user_guess > secret_number:
            return f"Too high! Try again. (Attempt: {guess_attempts})"
        else:
            guess_the_number_game_active = False # Game over
            return f"Congratulations! You guessed the number ({secret_number}) in {guess_attempts} attempts! Well done!"
    except ValueError:
        return "That's not a valid number. Please guess a whole number between 1 and 100. Or say 'quit game'."

def handle_rock_paper_scissors(user_input):
    """Plays a round of Rock-Paper-Scissors."""
    choices = ["rock", "paper", "scissors"]
    
    match = re.search(r"^(rock|paper|scissors)", user_input.lower(), re.IGNORECASE)
    if not match:
        return "To play Rock-Paper-Scissors, please say 'rock', 'paper', or 'scissors'."
    
    user_choice = match.group(1)
    iris_choice = random.choice(choices)

    result = ""
    if user_choice == iris_choice:
        result = "It's a tie!"
    elif (user_choice == "rock" and iris_choice == "scissors") or \
         (user_choice == "paper" and iris_choice == "rock") or \
         (user_choice == "scissors" and iris_choice == "paper"):
        result = "You win!"
    else:
        result = "I win!"
    
    return f"You chose {user_choice.title()}, I chose {iris_choice.title()}. {result}"

# --- Text Tools Functions ---
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

def is_palindrome(text):
    """Checks if a string is a palindrome (case and space insensitive)."""
    clean_text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    return clean_text == clean_text[::-1]

def handle_uppercase(user_input):
    """Converts text to uppercase."""
    match = re.search(r"uppercase\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_convert = match.group(1).strip()
        if not text_to_convert:
            return "Please provide text to convert to uppercase."
        return text_to_convert.upper()
    return "Please provide text to convert to uppercase. Example: 'uppercase hello'."

def handle_lowercase(user_input):
    """Converts text to lowercase."""
    match = re.search(r"lowercase\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_convert = match.group(1).strip()
        if not text_to_convert:
            return "Please provide text to convert to lowercase."
        return text_to_convert.lower()
    return "Please provide text to convert to lowercase. Example: 'lowercase WORLD'."

def handle_titlecase(user_input):
    """Converts text to title case."""
    match = re.search(r"titlecase\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_convert = match.group(1).strip()
        if not text_to_convert:
            return "Please provide text to convert to title case."
        return text_to_convert.title()
    return "Please provide text to convert to title case. Example: 'titlecase hello world'."

def handle_palindrome_check(user_input):
    """Checks if a string is a palindrome."""
    match = re.search(r"is palindrome\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
        if not text:
            return "Please provide text to check for palindrome."
        if is_palindrome(text):
            return f"'{text}' IS a palindrome!"
        else:
            return f"'{text}' is NOT a palindrome."
    return "Please provide text to check for palindrome. Example: 'is palindrome Madam'."

# --- System Info Functions ---
def get_system_info():
    """Gathers and returns basic system information."""
    info = []
    info.append(f"Operating System: {platform.system()} {platform.release()} ({platform.version()})")
    info.append(f"Architecture: {platform.machine()}")
    info.append(f"Processor: {platform.processor()}")

    svmem = psutil.virtual_memory()
    info.append(f"Total RAM: {svmem.total / (1024**3):.2f} GB")
    info.append(f"Available RAM: {svmem.available / (1024**3):.2f} GB")

    partitions = psutil.disk_partitions()
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            info.append(f"Disk ({p.mountpoint}): Total {usage.total / (1024**3):.2f} GB, Used {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
        except PermissionError:
            info.append(f"Permission denied to access directory '{p.mountpoint}'.")
        except Exception as e:
            info.append(f"Disk ({p.mountpoint}): Error reading usage - {e}")

    # Add a try-except for cpu_percent to handle potential psutil.NoSuchProcess or other errors
    try:
        info.append(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
    except Exception as e:
        info.append(f"Error getting CPU usage: {e}")

    return "\n".join(info)

def get_network_info():
    """Gathers and returns basic network interface information."""
    info_lines = ["Network Interfaces:"]
    try:
        addrs = psutil.net_if_addrs()
        if not addrs:
            return "No network interfaces found."

        for interface_name, interface_addresses in addrs.items():
            info_lines.append(f"  Interface: {interface_name}")
            for addr in interface_addresses:
                if addr.family == psutil.AF_LINK: # MAC address
                    info_lines.append(f"    MAC Address: {addr.address}")
                elif addr.family == psutil.AF_INET: # IPv4
                    info_lines.append(f"    IPv4 Address: {addr.address}")
                    if addr.netmask:
                        info_lines.append(f"      Netmask: {addr.netmask}")
                    if addr.broadcast:
                        info_lines.append(f"      Broadcast: {addr.broadcast}")
                elif addr.family == psutil.AF_INET6: # IPv6
                    info_lines.append(f"    IPv6 Address: {addr.address}")
                    if addr.netmask:
                        info_lines.append(f"      Netmask: {addr.netmask}")
            info_lines.append("-" * 20) # Separator for clarity
        return "\n".join(info_lines)
    except Exception as e:
        return f"An error occurred while fetching network information: {e}"

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

# --- QR Code Generator Function ---
def generate_qr_code(text, filename="qr_code.png"):
    """Generates a QR code from text and saves it to a file."""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return f"QR code generated and saved as '{filename}' in the current directory."
    except ImportError:
        return "The 'qrcode' library is not installed. Please install it using 'pip install qrcode' to use this feature."
    except Exception as e:
        return f"An error occurred while generating the QR code: {e}"


# --- Command Handlers (Functions to be called by the dispatcher) ---
# These handlers remain in the main script as they directly interact with user input
# and often combine logic from multiple utility modules.

def handle_greeting(user_input):
    """Handles greeting commands."""
    return greet_user() + " How can I help you today?"

def handle_say_command(user_input):
    """Handles the 'say' command, making Iris repeat text."""
    match = re.search(r"say\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_say = match.group(1).strip()
        if not text_to_say: # Handle empty string after 'say'
            return "What would you like me to say?"
        return text_to_say
    return "What would you like me to say?"

def handle_clear_screen(user_input):
    """Clears the terminal screen."""
    clear_screen()
    return "Screen cleared."

def handle_time(user_input):
    """Handles time-related queries, including specific locations."""
    match_location = re.match(r"(?:time in|what's the time in|current time in|get time for|time for|local time in|what time is it in)\s+(.+)", user_input, re.IGNORECASE)
    if match_location:
        location_query = match_location.group(1).strip()
        time_str, date_str, display_name = get_local_time_and_date_for_location(location_query)
        if time_str is not None:
            return f"The current time in {display_name} is {time_str}."
        else:
            return f"Sorry, I couldn't get the time for '{location_query}'. {display_name}"
    return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."

def handle_date(user_input):
    """Handles date-related queries, including specific locations."""
    match_location = re.match(r"(?:date in|what's the date in|today's date in|get date for|date for|local date in|what day is it in)\s+(.+)", user_input, re.IGNORECASE)
    if match_location:
        location_query = match_location.group(1).strip()
        time_str, date_str, display_name = get_local_time_and_date_for_location(location_query)
        if date_str is not None:
            return f"Today's date in {display_name} is {date_str}."
        else:
            return f"Sorry, I couldn't get the date for '{location_query}'. {display_name}"
    return f"Today's date is {datetime.datetime.today().strftime('%B %d, %Y')}."

def handle_who(user_input):
    """Handles queries about user's name or Iris's identity."""
    user_input_lower = user_input.lower().strip()
    if "who are you" in user_input_lower or "your name" in user_input_lower or "what is your name" in user_input_lower or "tell me about yourself" in user_input_lower:
        return f"My name is {ASSISTANT_NAME}. I'm a simple CLI assistant."
    elif "who am i" in user_input_lower or "what is my name" in user_input_lower or "do you know my name" in user_input_lower:
        if assistant_memory.get("user_name"):
            return f"You told me your name is {assistant_memory['user_name']}."
        return "I don't recall you telling me your name. You can tell me by saying 'set my name [your name]'."
    return "I didn't understand that 'who' question. Try 'who are you' or 'who am I'."

def handle_set(user_input):
    """Handles setting user's name or Iris's name."""
    global ASSISTANT_NAME # Need global to update the main script's ASSISTANT_NAME

    # Regex for 'set my name <name>' or 'my name is <name>'
    match_user_name = re.search(r"(?:set my name is|my name is|you can call me|i am)\s+(.+)", user_input, re.IGNORECASE)
    if match_user_name:
        user_name = match_user_name.group(1).strip().title()
        if user_name:
            assistant_memory["user_name"] = user_name
            save_memory(assistant_memory)
            return f"Nice to meet you, {user_name}! I'll remember that."
        return "Please provide a name. Example: 'set my name John'."

    # Regex for 'set assistant name <name>' or 'change assistant name to <name>'
    match_assistant_name = re.search(r"(?:set assistant name to|change assistant name to|call you|rename yourself to)\s+(.+)", user_input, re.IGNORECASE)
    if match_assistant_name:
        new_name = match_assistant_name.group(1).strip().title()
        if new_name:
            old_name = ASSISTANT_NAME
            ASSISTANT_NAME = new_name # Update global variable
            assistant_memory["assistant_name"] = new_name
            save_memory(assistant_memory)
            return f"Understood! You can now call me {ASSISTANT_NAME}. (My previous name was {old_name})."
        return "Please provide a new name for me. Example: 'set assistant name Jarvis'."
    
    return "Invalid format for setting. Use: 'set my name [name]' or 'set assistant name [new name]'."

def handle_how_are_you(user_input):
    """Responds to queries about Iris's well-being."""
    return "I'm doing great, thank you for asking! Ready to assist."

def handle_calculator(user_input):
    """Performs basic arithmetic calculations."""
    try:
        # Remove common command phrases, keeping the expression
        clean_command = re.sub(r"^(calculate|what is|compute|solve)\s+", "", user_input, flags=re.IGNORECASE).strip()

        # Replace word operators with symbols
        clean_command = clean_command.replace("plus", "+").replace("add", "+")
        clean_command = clean_command.replace("minus", "-").replace("subtract", "-")
        clean_command = clean_command.replace("times", "*").replace("multiplied by", "*")
        clean_command = clean_command.replace("divided by", "/").replace("divide by", "/")

        # Handle "subtract X from Y" specifically
        subtract_from_match = re.search(r"(\d+(\.\d+)?)\s*-\s*(\d+(\.\d+)?)", clean_command)
        if subtract_from_match:
            # This regex matches "X - Y", not "subtract X from Y" which is handled by previous replacements
            pass # No special handling needed here, standard eval will work
        else:
            # For "subtract X from Y", ensure it's correctly parsed
            subtract_from_pattern = re.compile(r"subtract\s+(\d+(\.\d+)?)\s+from\s+(\d+(\.\d+)?)", re.IGNORECASE)
            sub_match = subtract_from_pattern.search(user_input)
            if sub_match:
                num1 = float(sub_match.group(1))
                num2 = float(sub_match.group(3))
                clean_command = f"{num2} - {num1}" # Reorder for eval

        # Basic validation to prevent arbitrary code execution
        # Ensure only allowed characters are present. This is a crucial security measure.
        allowed_chars_pattern = re.compile(r"^[0-9.+\-*/() ]+$")
        if not allowed_chars_pattern.match(clean_command):
            return "Invalid characters or format detected in the calculation. Please use numbers and standard operators (+, -, *, /)."

        # Ensure there's at least one number in the expression
        if not re.search(r"\d", clean_command):
            return "I need a valid mathematical expression to calculate. Example: '5 plus 3', 'calculate 10 / 2', 'subtract 5 from 10'."

        result = eval(clean_command)
        return f"The result is: {result}"
    except (ValueError, SyntaxError, NameError):
        return "Please provide valid numbers and a clear operation for calculation. Example: '5 plus 3', 'calculate 10 / 2', 'subtract 5 from 10'."
    except ZeroDivisionError:
        return "Cannot divide by zero!"
    except Exception as e:
        return f"An unexpected error occurred during calculation: {e}. Please check your input format."

def handle_history(user_input):
    """Provides info on command history."""
    return "You can use your Up/Down arrow keys to browse command history."

def handle_clear_history(user_input):
    """Clears the assistant's command history."""
    print_response(f"Are you sure you want to clear {ASSISTANT_NAME}'s command history? (yes/no)")
    confirmation = input("You: ").strip().lower()
    if confirmation == "yes":
        try:
            readline.clear_history()
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            return "Command history cleared."
        except Exception as e:
            return f"Error clearing history: {e}. You might not have permission or the file is in use."
    else:
        return "Command history not cleared."

def handle_show_history(user_input):
    """Displays the command history."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history_lines = f.readlines()
            if history_lines:
                formatted_history = [f"{i+1}. {line.strip()}" for i, line in enumerate(history_lines)]
                return "\nCommand History:\n" + "\n".join(formatted_history)
            else:
                return "Command history is empty."
        else:
            return "No command history file found."
    except IOError as e:
        return f"Error reading history file: {e}. You might not have permission."
    except Exception as e:
        return f"An unexpected error occurred while showing history: {e}"

def handle_page_visits(user_input):
    """Displays the number of times the assistant has been started."""
    return f"{ASSISTANT_NAME} has been started {assistant_memory['page_visits']} times."

def handle_iris_stats(user_input):
    """Displays technical statistics about Iris."""
    stats = []
    stats.append(f"Total times started: {assistant_memory['page_visits']}")
    stats.append(f"Total commands executed: {assistant_memory['total_commands_executed']}")

    # Calculate session uptime
    uptime_seconds = time.time() - SESSION_START_TIME
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    stats.append(f"Current session uptime: {int(hours)}h {int(minutes)}m {int(seconds)}s")

    # Get memory file size
    try:
        if os.path.exists(MEMORY_FILE):
            file_size_bytes = os.path.getsize(MEMORY_FILE)
            file_size_mb = file_size_bytes / (1024 * 1024)
            stats.append(f"Persistent memory file size: {file_size_mb:.2f} MB")
        else:
            stats.append("Persistent memory file not found.")
    except Exception as e:
        stats.append(f"Error getting memory file size: {e}")

    return "\nIris Technical Stats:\n" + "\n".join(stats)

def handle_forget_me(user_input):
    """Resets user-specific data in Iris's memory."""
    print_response("Are you sure you want me to forget your name and reset user-specific data? (yes/no)")
    confirmation = input("You: ").strip().lower()
    if confirmation == "yes":
        assistant_memory["user_name"] = None
        # Optionally, you could reset other user-specific data here if any
        save_memory(assistant_memory)
        return "Okay, I've forgotten your name and cleared user-specific data."
    else:
        return "No changes made. I will continue to remember you."

def handle_joke(user_input):
    """Fetches and tells a random joke."""
    return get_random_joke()

def handle_ip_info(user_input):
    """Displays public IP information for self or a specified IP/domain."""
    match_specific_ip = re.search(r"(?:ip info for|lookup ip|check ip|get ip for|what is the ip of)\s+(.+)", user_input, re.IGNORECASE)
    
    ip_to_check = ""
    if match_specific_ip:
        ip_to_check = match_specific_ip.group(1).strip()
        show_loading_message(f"Looking up IP info for {ip_to_check}")
    else:
        show_loading_message("Looking up your current IP info")

    ip_data = get_ip_info_from_api(ip_to_check)
    if ip_data.get('status') == 'success':
        org = ip_data.get('org', 'N/A')
        return (f"IP: {ip_data.get('query', 'N/A')}\n"
                f"Location: {ip_data.get('city', 'N/A')}, {ip_data.get('regionName', 'N/A')}, {ip_data.get('country', 'N/A')}\n"
                f"ISP/Org: {ip_data.get('isp', 'N/A')} / {org}")
    else:
        target_ip_message = f" for {ip_to_check}" if ip_to_check else ""
        return f"Could not get IP info{target_ip_message}: {ip_data.get('message', 'Unknown error')}. Please check the IP/domain."

def handle_weather(user_input):
    """Fetches and displays weather information for a location."""
    unit = "fahrenheit"
    if "in celsius" in user_input.lower():
        unit = "celsius"
    elif "in fahrenheit" in user_input.lower():
        unit = "fahrenheit"
    
    match = re.search(r"(?:weather in|forecast for|how's the weather in|get weather for|what's the weather like in|show weather for)\s*(.+)?", user_input, re.IGNORECASE)
    
    location_query = None
    if match and match.group(1):
        location_query = match.group(1).strip()

    if location_query:
        latitude, longitude, display_name, _ = get_location_coords_from_name(location_query)
        if latitude is not None and longitude is not None:
            return f"Fetching weather for {display_name}...\n" + get_weather_forecast(latitude, longitude, unit=unit)
        else:
            # Corrected multi-line f-string using triple quotes
            return (f"""Could not find weather for '{location_query}'. Reason: {display_name.replace('unknown location', 'The location could not be found or there was an API error')
                    .replace('connection error', 'A connection error occurred').replace('timeout error', 'The request timed out')}. Please try a more specific or valid location name.""")
    else:
        # Fallback to device location
        latitude, longitude, location_name = get_device_location_coords()
        if latitude is not None and longitude is not None:
            return f"Fetching weather for {location_name.title()}...\n" + get_weather_forecast(latitude, longitude, unit=unit)
        else:
            return "Could not determine your current location. Please try specifying a location, e.g., 'weather in London'."

def handle_system_info(user_input):
    """Displays system hardware and OS information."""
    return get_system_info()

def handle_network_info(user_input):
    """Displays network interface information."""
    return get_network_info()

def handle_word_count(user_input):
    """Counts words in a given text."""
    match = re.search(r"(?:word count for|words in|count words in|how many words in|get word count for)\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_count = match.group(1).strip()
        if not text_to_count:
            return "Please provide text to count words."
        return f"The text contains {get_word_count(text_to_count)} words."
    return "Please provide text to count words. Example: 'word count for hello world'."

def handle_char_count(user_input):
    """Counts characters in a given text."""
    match = re.search(r"(?:character count for|chars in|count chars in|how many characters in|get char count for)\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_count = match.group(1).strip()
        if not text_to_count:
            return "Please provide text to count characters."
        return f"The text contains {get_character_count(text_to_count)} characters (including spaces)."
    return "Please provide text to count characters. Example: 'char count for hello world'."

def handle_reverse_string(user_input):
    """Reverses a given string."""
    match = re.search(r"reverse(?: text| string)?\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_reverse = match.group(1).strip()
        if not text_to_reverse:
            return "Please provide text to reverse."
        return f"Reversed text: '{reverse_string(text_to_reverse)}'"
    return "Please provide text to reverse. Example: 'reverse hello world'."

def handle_convert(user_input):
    """Dispatches to specific conversion types (units, bases, timestamps)."""
    user_input_lower = user_input.lower()

    # Unit conversion (length, mass, volume, temperature)
    match_unit = re.search(r"convert\s+([\d.]+)\s+([a-zA-Z]+)\s+to\s+([a-zA-Z]+)", user_input_lower)
    if match_unit:
        try:
            value = float(match_unit.group(1))
            from_unit = match_unit.group(2)
            to_unit = match_unit.group(3)
            return convert_units_general(value, from_unit, to_unit)
        except ValueError:
            return "Invalid value provided for unit conversion. Please use a number (e.g., 'convert 10 miles to km')."
        except Exception as e:
            return f"An error occurred during unit conversion: {e}"

    # Base conversion
    match_base = re.search(r"convert base\s+([a-zA-Z0-9]+)\s+from\s+(\d+)\s+to\s+(\d+)", user_input_lower)
    if match_base:
        try:
            number_str = match_base.group(1)
            from_base = int(match_base.group(2))
            to_base = int(match_base.group(3))
            return base_converter(number_str, from_base, to_base)
        except ValueError as e:
            return f"Invalid base values or number for conversion: {e}. Please use integers for bases (e.g., 'convert base 10 from 10 to 2')."
        except Exception as e:
            return f"An error occurred during base conversion: {e}"
    
    # Timestamp conversion
    match_timestamp_to_datetime = re.search(r"convert timestamp\s+([\d.]+)", user_input_lower)
    if match_timestamp_to_datetime:
        try:
            timestamp = float(match_timestamp_to_datetime.group(1))
            return convert_timestamp_to_datetime(timestamp)
        except ValueError:
            return "Invalid timestamp. Please provide a numeric Unix timestamp (e.g., 'convert timestamp 1678886400')."
        except Exception as e:
            return f"An error occurred during timestamp conversion: {e}"

    match_datetime_to_timestamp = re.search(r"convert to timestamp\s+(.+)", user_input_lower)
    if match_datetime_to_timestamp:
        datetime_str = match_datetime_to_timestamp.group(1).strip()
        timestamp = convert_datetime_to_timestamp(datetime_str)
        if isinstance(timestamp, int):
            return f"The Unix timestamp for '{datetime_str}' is: {timestamp}"
        else:
            return timestamp # This will be an error message from the function
            
    return ("Invalid format for conversion. Use one of these:\n"
            "  - Unit: 'convert [value] [from_unit] to [to_unit]'\n"
            "  - Base: 'convert base [number] from [base] to [base]'\n"
            "  - Timestamp to Date/Time: 'convert timestamp [unix timestamp]'\n"
            "  - Date/Time to Timestamp: 'convert to timestamp [date and time]'")

def handle_url_encoding(user_input):
    """Encodes or decodes URLs."""
    user_input_lower = user_input.lower()
    match_encode = re.search(r"(?:url encode|encode url|encode link)\s+(.+)", user_input_lower)
    if match_encode:
        text_to_encode = match.group(1).strip()
        if not text_to_encode:
            return "Please provide text to URL encode."
        return f"URL encoded: '{url_encode(text_to_encode)}'"
    
    match_decode = re.search(r"(?:url decode|decode url|decode link)\s+(.+)", user_input_lower)
    if match_decode:
        text_to_decode = match.group(1).strip()
        if not text_to_decode:
            return "Please provide text to URL decode."
        return f"URL decoded: '{url_decode(text_to_decode)}'"
    
    return "Invalid format for URL encoding/decoding. Use: 'url encode [text]' or 'url decode [text]'."

def handle_copy_to_clipboard(user_input):
    """Copies text to the clipboard."""
    match = re.search(r"^copy\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_copy = match.group(1).strip()
        if not text_to_copy:
            return "Please provide text to copy."
        try:
            pyperclip.copy(text_to_copy)
            return f"Copied '{text_to_copy}' to your clipboard."
        except pyperclip.PyperclipException as e:
            return f"Could not access clipboard: {e}. Please ensure you have a copy/paste mechanism (e.g., xclip/xsel on Linux) or a GUI environment configured."
        except Exception as e:
            return f"An unexpected error occurred while copying to clipboard: {e}"
    return "Please provide text to copy. Example: 'copy hello world'."

def handle_paste_from_clipboard(user_input):
    """Retrieves text from the clipboard."""
    try:
        pasted_text = pyperclip.paste()
        if pasted_text:
            return f"Content from clipboard: '{pasted_text}'"
        else:
            return "Your clipboard is empty or contains no readable text."
    except pyperclip.PyperclipException as e:
        return f"Could not access clipboard: {e}. Please ensure you have a copy/paste mechanism (e.g., xclip/xsel on Linux) or a GUI environment configured."
    except Exception as e:
        return f"An unexpected error occurred while pasting from clipboard: {e}"

def handle_generate_qr_code(user_input):
    """Generates a QR code from text."""
    match = re.search(r"^(?:generate qr|create qr|make qr code for|qr code for)\s+(.+)", user_input, re.IGNORECASE)
    if match:
        text_to_encode = match.group(1).strip()
        if not text_to_encode:
            return "Please provide text to generate a QR code. Example: 'generate qr hello world'."
        return generate_qr_code(text_to_encode)
    return "Invalid format for QR code generation. Use: 'generate qr [text to encode]'."

def handle_search(user_input):
    """Fetches instant answers from DuckDuckGo."""
    # Updated regex to correctly capture "search [topic]"
    match = re.search(r"^(?:what is|who is|tell me about|search(?: for)?)\s+(.+)", user_input, re.IGNORECASE)
    if match:
        query = match.group(1).strip()
        if not query:
            return "Please provide a topic for information retrieval. Example: 'search what is photosynthesis?'"
        return get_instant_answer(query)
    return "Invalid format. Use: 'search [topic]', 'what is [topic]', 'who is [person]', or 'tell me about [topic]'."

def handle_dictionary_lookup(user_input):
    """Looks up word definitions."""
    match = re.search(r"^(?:define|what is the definition of|meaning of)\s+(.+)", user_input, re.IGNORECASE)
    if match:
        word_to_define = match.group(1).strip()
        if not word_to_define:
            return "Please provide a word to define. Example: 'define ephemeral'."
        return get_definition(word_to_define)
    return "Invalid format. Use: 'define [word]', 'what is the definition of [word]', or 'meaning of [word]'."

def handle_open_url(user_input):
    """Opens a specified URL in the default web browser."""
    # This regex tries to find a URL-like string starting with http(s):// or www.
    # or just a common domain suffix (e.g., .com, .org, .net).
    url_match = re.search(r"(https?://\S+|www\.\S+|(\S+\.(com|org|net|gov|edu|io|co|ai)(/\S*)?))", user_input, re.IGNORECASE)

    if url_match:
        url = url_match.group(0)
        # Prepend 'http://' if the URL doesn't have a scheme and starts with 'www.' or a bare domain
        if not url.startswith("http://") and not url.startswith("https://"):
            if url.startswith("www.") or "." in url: # Basic check for a valid-looking domain
                url = "http://" + url
            else:
                return f"Sorry, '{url}' doesn't look like a valid URL to open. Please include http:// or www. for clarity."
        
        try:
            print_response(f"Opening {url} in your web browser...")
            webbrowser.open(url)
            return "Done!"
        except Exception as e:
            return f"An error occurred while trying to open the URL: {e}"
    else:
        return "Please specify a URL to open. Example: 'open google.com' or 'go to https://example.com'."

def handle_coin_flip_command(user_input):
    """Handles the coin flip command."""
    return coin_flip()

def handle_dice_roll_command(user_input):
    """Handles dice roll commands."""
    match = re.search(r"roll\s+(?:(\d+)d(\d+)|a die|dice)", user_input, re.IGNORECASE)
    if match:
        if match.group(1) and match.group(2):
            num_dice = int(match.group(1))
            num_sides = int(match.group(2))
            return roll_dice(num_dice, num_sides)
        else: # "roll a die" or "roll dice"
            return roll_dice(1, 6) # Default to 1 six-sided die
    return "Please specify how many dice and sides (e.g., 'roll 2d6') or just 'roll dice'."

def handle_list_files_in_directory_command(user_input):
    """Handles listing files in a directory."""
    match = re.search(r"list files(?:\s+(.+))?", user_input, re.IGNORECASE)
    path = "." # Default to current directory
    if match and match.group(1):
        path = match.group(1).strip()
    return list_files_in_directory(path)

def handle_help(user_input):
    """Displays a categorized list of available commands."""
    help_message = ["Available Commands:"]
    
    # Group commands by category
    categories = {}
    for cmd_key, details in COMMAND_DETAILS.items():
        category = details["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(cmd_key)
    
    # Sort categories and commands within categories for consistent display
    for category in sorted(categories.keys()):
        help_message.append(f"\n\n--- {category} ---") # Added extra newline here
        for cmd_key in sorted(categories[category]):
            details = COMMAND_DETAILS[cmd_key]
            description = details["description"]
            examples = ", ".join([f"'{ex}'" for ex in details["examples"]])
            help_message.append(f"  - {cmd_key.title()}: {description}")
            if examples:
                help_message.append(f"    Examples: {examples}")
            help_message.append("") # Added a blank line after each command for separation
    
    help_message.append("\nType 'exit' or 'quit' to end the session.")
    return "\n".join(help_message)

def handle_exit(user_input):
    """Handles the exit command."""
    return f"Exiting. Goodbye, {assistant_memory['user_name'] if assistant_memory['user_name'] else 'Connor'}!"


# --- Command Details and Aliases ---
# This dictionary will contain command details for the help message
# Key: The primary command keyword (first word or full multi-word command if unique)
# Value: A dictionary with 'handler' (function), 'category', 'description', and 'examples'
COMMAND_DETAILS = {
    "hello": {
        "handler": handle_greeting,
        "category": "General",
        "description": "Greets you.",
        "examples": ["hello", "hi", "good morning"]
    },
    "say": {
        "handler": handle_say_command,
        "category": "General",
        "description": "Makes Iris say something.",
        "examples": ["say Hello there!"]
    },
    "clear": {
        "handler": handle_clear_screen,
        "category": "Utilities",
        "description": "Clears the terminal screen.",
        "examples": ["clear", "cls"]
    },
    "time": {
        "handler": handle_time,
        "category": "Time & Date",
        "description": "Displays the current time or time in a specified location.",
        "examples": ["time", "time in Paris"]
    },
    "date": {
        "handler": handle_date,
        "category": "Time & Date",
        "description": "Displays the current date or date in a specified location.",
        "examples": ["date", "date in Tokyo"]
    },
    "who": {
        "handler": handle_who,
        "category": "Personalization",
        "description": "Asks about your name or Iris's name.",
        "examples": ["who am i", "who are you"]
    },
    "set": {
        "handler": handle_set,
        "category": "Personalization",
        "description": "Sets your name or Iris's name.",
        "examples": ["set my name Connor", "set assistant name Jarvis"]
    },
    "how": {
        "handler": handle_how_are_you,
        "category": "General",
        "description": "Asks Iris how she is doing.",
        "examples": ["how are you"]
    },
    "calculate": {
        "handler": handle_calculator,
        "category": "Utilities",
        "description": "Performs basic arithmetic operations.",
        "examples": ["calculate 5 + 3", "10 minus 5", "subtract 5 from 10"]
    },
    "history": {
        "handler": handle_history,
        "category": "Utilities",
        "description": "Provides info on command history.",
        "examples": ["history"]
    },
    "show history": { # New command
        "handler": handle_show_history,
        "category": "Utilities",
        "description": "Displays the command history from this session and previous sessions.",
        "examples": ["show history"]
    },
    "clear history": { # Full phrase for direct match
        "handler": handle_clear_history,
        "category": "Utilities",
        "description": "Clears the command history (requires confirmation).",
        "examples": ["clear history"]
    },
    "page visits": { # Full phrase for direct match
        "handler": handle_page_visits,
        "category": "General",
        "description": "Shows how many times Iris has been started.",
        "examples": ["page visits"]
    },
    "iris stats": { # New command
        "handler": handle_iris_stats,
        "category": "General",
        "description": "Displays technical statistics about Iris's usage and performance.",
        "examples": ["iris stats", "stats"]
    },
    "forget me": { # New command
        "handler": handle_forget_me,
        "category": "Personalization",
        "description": "Resets your name and other user-specific data Iris remembers.",
        "examples": ["forget me"]
    },
    "joke": {
        "handler": handle_joke,
        "category": "Web Tools",
        "description": "Tells a random joke.",
        "examples": ["joke", "tell me a joke"]
    },
    "ip": {
        "handler": handle_ip_info,
        "category": "Network Info",
        "description": "Displays your public IP address or info for a specific IP/domain.",
        "examples": ["ip info", "ip info for 8.8.8.8"]
    },
    "weather": {
        "handler": handle_weather,
        "category": "Web Tools",
        "description": "Gets current weather or forecast for a location.",
        "examples": ["weather", "weather London in celsius"]
    },
    "system": {
        "handler": handle_system_info,
        "category": "System Info",
        "description": "Displays system hardware and OS information.",
        "examples": ["system info", "my computer specs"]
    },
    "network": {
        "handler": handle_network_info,
        "category": "System Info",
        "description": "Displays network interface information.",
        "examples": ["network info"]
    },
    "word": {
        "handler": handle_word_count,
        "category": "Text Analysis",
        "description": "Counts words in a given text.",
        "examples": ["word count This is a sentence."]
    },
    "char": {
        "handler": handle_char_count,
        "category": "Text Analysis",
        "description": "Counts characters in a given text.",
        "examples": ["char count Hello world!"]
    },
    "reverse": {
        "handler": handle_reverse_string,
        "category": "Text Analysis",
        "description": "Reverses a given string.",
        "examples": ["reverse hello", "reverse string world"]
    },
    "uppercase": {
        "handler": handle_uppercase,
        "category": "Text Analysis",
        "description": "Converts text to uppercase.",
        "examples": ["uppercase hello"]
    },
    "lowercase": {
        "handler": handle_lowercase,
        "category": "Text Analysis",
        "description": "Converts text to lowercase.",
        "examples": ["lowercase WORLD"]
    },
    "titlecase": {
        "handler": handle_titlecase,
        "category": "Text Analysis",
        "description": "Converts text to title case.",
        "examples": ["titlecase hello world"]
    },
    "palindrome": {
        "handler": handle_palindrome_check, # This is now correctly mapped
        "category": "Text Analysis",
        "description": "Checks if a string is a palindrome.",
        "examples": ["palindrome is Madam"]
    },
    "convert": {
        "handler": handle_convert,
        "category": "Utilities",
        "description": "Converts units, bases, or timestamps.",
        "examples": [
            "convert 10 miles to km",
            "convert base 10 from 10 to 2",
            "convert timestamp 1678886400",
            "convert to timestamp 2023-03-15 12:00:00"
        ]
    },
    "url": {
        "handler": handle_url_encoding,
        "category": "Web Tools",
        "description": "Encodes or decodes URLs.",
        "examples": ["url encode hello world", "url decode hello%20world"]
    },
    "copy": {
        "handler": handle_copy_to_clipboard,
        "category": "Utilities",
        "description": "Copies text to your clipboard.",
        "examples": ["copy This text"]
    },
    "paste": {
        "handler": handle_paste_from_clipboard,
        "category": "Utilities",
        "description": "Retrieves text from your clipboard.",
        "examples": ["paste"]
    },
    "open": {
        "handler": handle_open_url,
        "category": "Web Tools",
        "description": "Opens a URL in your default web browser.",
        "examples": ["open google.com", "open https://example.com"]
    },
    "generate": {
        "handler": handle_generate_qr_code,
        "category": "Utilities",
        "description": "Generates a QR code from text.",
        "examples": ["generate qr code Hello Iris"]
    },
    "search": {
        "handler": handle_search,
        "category": "Web Tools",
        "description": "Gets instant answers from DuckDuckGo.",
        "examples": ["search what is AI", "search who is Albert Einstein"]
    },
    "dictionary": {
        "handler": handle_dictionary_lookup,
        "category": "Web Tools",
        "description": "Looks up word definitions.",
        "examples": ["dictionary egregious", "define ephemeral"]
    },
    "coin": {
        "handler": handle_coin_flip_command, # Corrected handler
        "category": "Games & Randomness",
        "description": "Flips a coin.",
        "examples": ["coin flip", "flip a coin"]
    },
    "dice": {
        "handler": handle_dice_roll_command, # Corrected handler
        "category": "Games & Randomness",
        "description": "Rolls dice.",
        "examples": ["dice roll", "roll 2d6"]
    },
    "guess": {
        "handler": handle_start_guess_the_number_game, # This starts the game
        "category": "Games & Randomness",
        "description": "Play 'Guess the Number'.",
        "examples": ["guess the number", "play guess the number"]
    },
    "rock": {
        "handler": handle_rock_paper_scissors,
        "category": "Games & Randomness",
        "description": "Play 'Rock-Paper-Scissors'.",
        "examples": ["rock", "paper", "scissors"]
    },
    "list": {
        "handler": handle_list_files_in_directory_command, # Corrected handler
        "category": "File System",
        "description": "Lists files and directories in a given path.",
        "examples": ["list files", "list files .", "list files /home"]
    },
    "help": {
        "handler": handle_help,
        "category": "General",
        "description": "Displays this help message.",
        "examples": ["help", "?"]
    },
    "exit": {
        "handler": handle_exit,
        "category": "General",
        "description": "Exits the assistant.",
        "examples": ["exit", "quit", "goodbye"]
    }
}

# --- Command Aliases ---
# Map common user phrases/shorthands to the primary command key
COMMAND_ALIASES = {
    "hi": "hello", "hey": "hello", "good morning": "hello", "good afternoon": "hello", "good evening": "hello", "what's up": "hello", "howdy": "hello",
    "cls": "clear", "clear screen": "clear",
    "what's the time": "time", "current time": "time", "tell me the time": "time", "what time is it": "time",
    "today's date": "date", "tell me the date": "date", "what day is it": "date", "what's today's date": "date",
    "your name": "who", "what is your name": "who", "tell me about yourself": "who",
    "my name is": "set", "you can call me": "set", "i am": "set",
    "change assistant name to": "set", "call you": "set", "set your name to": "set", "rename yourself to": "set",
    "how are you doing": "how", "how's it going": "how", "how are things": "how", "are you well": "how",
    "what is": "calculate", "compute": "calculate", "solve": "calculate",
    "show my commands": "history", "my past commands": "history", "command history": "history",
    "show past commands": "show history", # New alias
    "show command history": "show history", # New alias
    "visits count": "page visits", "how many times have you been started": "page visits", "how many visits": "page visits", "show visits": "page visits",
    "stats": "iris stats", "technical stats": "iris stats", "show stats": "iris stats", # New aliases
    "forget my name": "forget me", "reset my data": "forget me", # New aliases
    "tell me a joke": "joke", "random joke": "joke", "got any jokes": "joke", "cheer me up": "joke", "make me laugh": "joke",
    "my ip info": "ip", "what's my ip": "ip", "show my ip": "ip", "what is my current ip": "ip", "find my ip": "ip",
    "lookup ip": "ip", "check ip": "ip", "get ip for": "ip", "what is the ip of": "ip",
    "weather forecast": "weather", "current weather": "weather", "how's the weather": "weather", "what's the weather like in": "weather", "show weather for": "weather",
    "my computer specs": "system", "show system info": "system", "what are your specs": "system", "computer info": "system",
    "show network info": "network", "what is my network config": "network", "display network details": "network",
    "words in": "word", "count words in": "word", "how many words in": "word", "get word count for": "word",
    "chars in": "char", "count chars in": "char", "how many characters in": "char", "get char count for": "char",
    "reverse text": "reverse", "reverse string": "reverse",
    "upper case": "uppercase", "lower case": "lowercase", "title case": "titlecase",
    "encode url": "url", "decode url": "url", "encode link": "url", "decode link": "url",
    "flip a coin": "coin", "toss a coin": "coin",
    "roll a die": "dice", "throw dice": "dice", "simulate dice roll": "dice",
    "visit": "open", "navigate to": "open", "browse to": "open", "take me to": "open", "go to": "open",
    "create qr": "generate", "make qr code for": "generate", "qr code for": "generate",
    "tell me about": "search",
    "define": "dictionary", "what is the definition of": "dictionary", "meaning of": "dictionary",
    "play guess the number": "guess", "start guess game": "guess",
    "paper": "rock", "scissors": "rock", # These map to rock for the RPS handler
    "show files in": "list", "ls": "list", "dir": "list", "show directory contents": "list", "what's in": "list",
    "?": "help", "commands": "help", "cmds": "help", "what can you do": "help", "list commands": "help", "show commands": "help",
    "quit": "exit", "bye": "exit", "goodbye": "exit", "see ya": "exit"
}

# --- Command Dispatch Table ---
# This map is used by assistant_response to find the correct handler function
COMMAND_MAP = {cmd_key: details["handler"] for cmd_key, details in COMMAND_DETAILS.items()}


def assistant_response(user_input):
    """Processes user commands and returns a response using a command dispatch table."""
    global guess_the_number_game_active # Access global variable for game state

    user_input_lower = user_input.lower().strip()

    # Special handling for guess the number game when active
    if guess_the_number_game_active:
        # If the game is active, all numeric inputs or "quit game" go to the game handler
        if re.match(r"^\s*(\d+)\s*$", user_input_lower) or user_input_lower == "quit game":
            return handle_guess_the_number_game_play(user_input)

    # Check for direct exit commands first, as they don't need alias processing
    if user_input_lower in ["exit", "quit", "goodbye", "bye", "close", "see ya"]:
        return handle_exit(user_input)

    # Try to find a direct alias match
    primary_command_key = COMMAND_ALIASES.get(user_input_lower)

    # If no direct alias, try to match multi-word command prefixes or single words
    if primary_command_key is None:
        # Sort keys by length descending to match longer phrases first (e.g., "clear history" before "clear")
        sorted_command_keys = sorted(COMMAND_DETAILS.keys(), key=len, reverse=True)
        for cmd_key in sorted_command_keys:
            if user_input_lower.startswith(cmd_key):
                primary_command_key = cmd_key
                break
    
    # If still no primary command key, check if the first word is a command
    if primary_command_key is None:
        first_word = user_input_lower.split(' ', 1)[0]
        if first_word in COMMAND_DETAILS:
            primary_command_key = first_word

    # Dispatch to the appropriate handler
    if primary_command_key and primary_command_key in COMMAND_MAP:
        # Increment total commands executed only for recognized commands
        assistant_memory["total_commands_executed"] += 1
        save_memory(assistant_memory) # Save after each command for persistence
        handler_func = COMMAND_MAP[primary_command_key]
        return handler_func(user_input) # Pass original user_input for full context parsing in handlers
    else:
        return f"Sorry, I don't recognize '{user_input}'. Type 'help' to see what I can do."


def main():
    global assistant_memory, ASSISTANT_NAME # Ensure ASSISTANT_NAME is accessible globally in main

    # Setup readline for command history (consistent across platforms if possible)
    if 'libedit' in readline.__doc__ or platform.system() != 'Windows':
        readline.set_history_length(1000)
        if os.path.exists(HISTORY_FILE):
            try:
                readline.read_history_file(HISTORY_FILE)
            except Exception as e:
                print(f"Warning: Could not read history file: {e}. History might be incomplete.")
        atexit.register(lambda: readline.write_history_file(HISTORY_FILE)) # Ensure history is saved on exit

    assistant_memory["page_visits"] += 1
    save_memory(assistant_memory)

    current_time_str = datetime.datetime.now().strftime('%I:%M %p')
    user_name_part = f", {assistant_memory['user_name']}" if assistant_memory['user_name'] else ""
    
    print_response(f"{greet_user().replace('!', '')}{user_name_part}! Welcome to {ASSISTANT_NAME}! It's {current_time_str} MDT in Layton, Utah. Type 'help' for commands.")
    
    while True:
        try:
            user_input = input("\nYou: ")
            response = assistant_response(user_input)
            
            if response:
                print_response(response)
            
            # The exit check should be after printing the response from handle_exit
            # This is now handled inside assistant_response for direct exit commands
            if user_input.lower().strip() in ["exit", "quit", "goodbye", "bye", "close", "see ya"]:
                save_memory(assistant_memory) # Ensure memory is saved on explicit exit
                break
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print_response(f"Exiting. Goodbye, Connor!")
            save_memory(assistant_memory) # Ensure memory is saved on Ctrl+C
            break
        except Exception as e:
            print_response(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
