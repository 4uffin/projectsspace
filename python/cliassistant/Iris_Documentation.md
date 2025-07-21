# **Iris CLI Assistant Documentation**

## **Project Overview**

Iris is a simple Command-Line Interface (CLI) assistant written in Python. It provides a variety of functionalities, from basic utilities like time and date checks to more complex features like unit conversions, system information retrieval, and interactive games. The assistant is designed to be extensible and user-friendly, offering quick access to information and tools directly from the terminal.

## **Features**

Iris offers a range of features categorized for easy understanding:

### **Core Functionality**

* **Persistent Memory**: Remembers user's name and total commands executed across sessions by saving data to assistant\_memory.json.  
* **Dynamic Greeting**: Greets the user based on the time of day (morning, afternoon, evening).  
* **Clear Screen**: Clears the terminal output for a clean interface.

### **Information Retrieval**

* **Time and Date**: Provides current time and date, with the ability to query for specific locations worldwide.  
* **Location Information**: Fetches geolocation details for IP addresses.  
* **Weather Forecast**: Provides current weather and daily forecasts for any given location, with options for Fahrenheit or Celsius units.  
* **Instant Answers**: Retrieves direct answers to a wide range of questions using the DuckDuckGo API.

### **Utility Tools**

* **Unit Conversion**: Converts values between various units of length, mass, volume, and temperature (Celsius, Fahrenheit, Kelvin).  
* **Base Conversion**: Converts numbers between different bases (e.g., binary, decimal, hexadecimal).  
* **URL Encoding/Decoding**: Encodes and decodes URL strings.  
* **Timestamp Conversion**: Converts Unix timestamps to human-readable dates/times and vice-versa.  
* **QR Code Generation**: Creates QR codes from text and saves them as PNG image files.

### **Text Manipulation**

* **Word and Character Count**: Counts words and characters in a given text.  
* **String Reversal**: Reverses any given string.  
* **Palindrome Check**: Determines if a string is a palindrome.  
* **Text Case Conversion**: Converts text to uppercase, lowercase, or title case.

### **Games**

* **Coin Flip**: Simulates a coin flip (Heads or Tails).  
* **Dice Roll**: Simulates rolling one or multiple dice with a specified number of sides.  
* **Guess the Number**: An interactive game where the user guesses a secret number between 1 and 100\.  
* **Rock-Paper-Scissors**: Play a round of Rock-Paper-Scissors against Iris.

### **System Information**

* **System Details**: Displays information about the operating system, architecture, processor, RAM, disk usage, and CPU usage.  
* **Network Info**: Lists details about network interfaces, including MAC and IP addresses.  
* **File Listing**: Lists files and directories in a specified path.

## **Setup and Installation**

To run Iris, ensure you have Python installed (Python 3.x recommended).

### **Prerequisites**

The iris.py project utilizes several external Python libraries. You can install them using pip:

Bash

pip install requests psutil qrcode pyperclip readline

* requests: For making HTTP requests to various APIs (JokeAPI, IP-API.com, Open-Meteo, DuckDuckGo).  
* psutil: For retrieving system and network information.  
* qrcode: For generating QR codes.  
* pyperclip: For clipboard operations.  
* readline: For history in interactive mode (Linux/macOS).

### **Running the Assistant**

1. Save the provided code as iris.py.  
2. Open your terminal or command prompt.  
3. Navigate to the directory where you saved iris.py.  
4. Run the assistant using the command:  
   Bash  
   python iris.py

## **Usage**

Upon launching, Iris will greet you and display the current time. You can then type commands at the prompt.

### **Basic Interaction**

* help: Displays a list of available commands.  
* say \[text\]: Iris will repeat the provided text.  
* clear: Clears the terminal screen.  
* exit, quit, goodbye, bye, close, see ya: Exits the assistant.

### **Examples of Commands**

* **Time and Date**:  
  * what time is it?  
  * what's the date in London?  
* **Jokes**:  
  * tell me a joke  
* **Weather**:  
  * weather in New York  
  * weather in Paris in celsius  
* **Calculations**:  
  * calculate 10 \+ 5  
  * solve 2 \* (3 \+ 4\)  
* **Unit Conversion**:  
  * convert 10 miles to km  
  * convert 25 celsius to fahrenheit  
* **Base Conversion**:  
  * convert 1010 from base 2 to base 10  
* **Games**:  
  * play guess the number  
  * rock (for Rock-Paper-Scissors)  
* **System Info**:  
  * system info  
  * network info  
  * list files  
* **QR Code**:  
  * generate qr code for hello world as my\_qr.png

## **File Structure and Memory Management**

* iris.py: The main script containing all the logic for the Iris CLI assistant.  
* assistant\_memory.json: A JSON file used for persistent storage of assistant memory, including user\_name, assistant\_name, page\_visits, and total\_commands\_executed. This file is automatically loaded on startup and saved on exit.  
* \~/.iris\_history: A history file managed by the readline module (on Unix-like systems) to remember previous commands typed by the user.

## **API Integrations**

Iris leverages several external APIs to provide its functionalities:

* **JokeAPI**: For fetching random jokes.  
* **IP-API.com**: For retrieving geolocation information based on IP addresses.  
* **Open-Meteo Geocoding API**: For converting location names to geographical coordinates.  
* **Open-Meteo Timezone API**: For getting local time and date based on coordinates.  
* **Open-Meteo Forecast API**: For fetching current weather and forecasts.  
* **DuckDuckGo Instant Answer API**: For providing quick answers to factual queries.