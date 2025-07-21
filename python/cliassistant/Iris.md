# **Iris CLI Assistant Documentation**

Iris is a versatile command-line interface (CLI) assistant written in Python. It provides a wide range of functionalities, including general utilities, web tools, system information, text analysis, games, and more. Iris is designed to be interactive and helpful for various daily tasks.

## **Table of Contents**

1. [Features](https://www.google.com/search?q=%23features)  
2. [Setup and Installation](https://www.google.com/search?q=%23setup-and-installation)  
3. [Usage](https://www.google.com/search?q=%23usage)  
4. [Commands](https://www.google.com/search?q=%23commands)  
   * [General Commands](https://www.google.com/search?q=%23general-commands)  
   * [Personalization Commands](https://www.google.com/search?q=%23personalization-commands)  
   * [Utilities](https://www.google.com/search?q=%23utilities)  
   * [Time & Date Commands](https://www.google.com/search?q=%23time--date-commands)  
   * [Web Tools](https://www.google.com/search?q=%23web-tools)  
   * [System & Network Information](https://www.google.com/search?q=%23system--network-information)  
   * [Text Analysis Tools](https://www.google.com/search?q=%23text-analysis-tools)  
   * [Games & Randomness](https://www.google.com/search?q=%23games--randomness)  
   * [File System Commands](https://www.google.com/search?q=%23file-system-commands)  
5. [Persistent Memory](https://www.google.com/search?q=%23persistent-memory)  
6. [Error Handling](https://www.google.com/search?q=%23error-handling)  
7. [Dependencies](https://www.google.com/search?q=%23dependencies)

## **Features**

* **Interactive CLI:** Engages with the user through a command-line interface.  
* **Persistent Memory:** Remembers user's name, assistant's name, and usage statistics across sessions.  
* **Time & Date:** Provides current time and date, including for specific locations worldwide.  
* **Web Tools:** Fetches jokes, IP information, weather forecasts, and instant answers from DuckDuckGo.  
* **Utilities:** Includes a calculator, unit converter, base converter, URL encoder/decoder, QR code generator, and clipboard integration.  
* **System Information:** Displays details about the operating system, hardware, and network.  
* **Text Analysis:** Offers word count, character count, string reversal, case conversion, and palindrome checks.  
* **Games:** Features simple interactive games like "Guess the Number," "Coin Flip," and "Rock-Paper-Scissors."  
* **Command History:** Supports browsing and clearing command history.  
* **Customizable:** Allows changing the assistant's name and remembering the user's name.

## **Setup and Installation**

### **Prerequisites**

* Python 3.x installed on your system.  
* Internet connection for web-based functionalities.

### **Installation Steps**

1. **Save the script:** Save the provided iris.py code to a file named iris.py on your computer.  
2. **Install dependencies:** Iris uses several external Python libraries. You can install them using pip:  
   pip install requests pyperclip qrcode psutil

   * requests: For making HTTP requests to external APIs (jokes, weather, IP info, search).  
   * pyperclip: For cross-platform clipboard operations.  
   * qrcode: For generating QR codes.  
   * psutil: For accessing system and process utilities (system info, network info).

## **Usage**

To run Iris, open your terminal or command prompt, navigate to the directory where you saved iris.py, and execute the script:

python iris.py

Iris will greet you and prompt you for commands.

## **Commands**

Here's a detailed list of commands you can use with Iris, categorized for easy reference. Many commands have aliases for convenience.

### **General Commands**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| hello, hi, hey | Greets you. | hello, hi, good morning |
| say \[text\] | Makes Iris repeat the provided text. | say Hello there\! |
| help, ?, commands | Displays a list of all available commands. | help, ?, commands |
| page visits | Shows how many times Iris has been started. | page visits, how many times have you been started |
| iris stats | Displays technical statistics about Iris's usage. | iris stats, stats |
| how are you | Asks Iris how she is doing. | how are you doing, how's it going |
| exit, quit, bye | Exits the assistant. | exit, quit, goodbye |

### **Personalization Commands**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| who am i, who are you | Asks about your name or Iris's identity. | who am i, who are you |
| set my name \[name\] | Sets the user's name for Iris to remember. | set my name Connor, my name is John |
| set assistant name \[name\] | Changes Iris's name. | set assistant name Jarvis, call you Athena |
| forget me | Resets your name and other user-specific data. | forget me |

### **Utilities**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| clear, cls | Clears the terminal screen. | clear, cls |
| calculate \[expression\] | Performs basic arithmetic operations. | calculate 5 \+ 3, 10 minus 5, subtract 5 from 10 |
| history | Provides information on command history. | history |
| show history | Displays the command history from current and previous sessions. | show history |
| clear history | Clears the command history (requires confirmation). | clear history |
| convert \[value\] \[from\] to \[to\] | Converts units (length, mass, volume, temperature). | convert 10 miles to km, convert 25 celsius to fahrenheit |
| convert base \[num\] from \[base\] to \[base\] | Converts a number between different bases. | convert base 10 from 10 to 2, convert base FF from 16 to 10 |
| convert timestamp \[timestamp\] | Converts a Unix timestamp to a human-readable date/time. | convert timestamp 1678886400 |
| convert to timestamp \[datetime\] | Converts a date/time string to a Unix timestamp. | convert to timestamp 2023-03-15 12:00:00 |
| copy \[text\] | Copies the specified text to your clipboard. | copy This text will be copied. |
| paste | Retrieves text from your clipboard. | paste |
| generate qr \[text\] | Generates a QR code from the given text and saves it as qr\_code.png. | generate qr Hello World\! |

### **Time & Date Commands**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| time, what's the time | Displays the current local time. | time |
| time in \[location\] | Displays the current time in a specified city/location. | time in Paris, time in Tokyo |
| date, today's date | Displays the current local date. | date |
| date in \[location\] | Displays the current date in a specified city/location. | date in London, date in Sydney |

### **Web Tools**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| joke, tell me a joke | Fetches and tells a random joke. | joke, tell me a joke |
| ip info, what's my ip | Displays your public IP address and basic geolocation. | ip info, what's my ip |
| ip info for \[ip/domain\] | Displays IP information for a specific IP address or domain. | ip info for 8.8.8.8, ip info for google.com |
| weather, weather in \[location\] | Gets current weather or forecast for your location or a specified city. Unit can be celsius or fahrenheit. | weather, weather London in celsius |
| search \[query\] | Gets instant answers for a query using DuckDuckGo. | search what is AI, who is Albert Einstein |
| define \[word\] | Looks up the definition of a word. | define ephemeral, meaning of egregious |
| url encode \[text\] | URL-encodes a given string. | url encode hello world, encode url my website.com |
| url decode \[text\] | URL-decodes a given string. | url decode hello%20world, decode url example.com%2Fpath |
| open \[url\] | Opens a specified URL in your default web browser. | open google.com, go to https://example.com |

### **System & Network Information**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| system info | Displays system hardware and OS information. | system info, my computer specs |
| network info | Displays network interface information. | network info, show network details |

### **Text Analysis Tools**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| word count \[text\] | Counts words in a given text. | word count This is a sentence., words in my document |
| char count \[text\] | Counts characters (including spaces) in a given text. | char count Hello world\!, chars in some text |
| reverse \[text\] | Reverses a given string. | reverse hello, reverse string world |
| uppercase \[text\] | Converts text to uppercase. | uppercase hello |
| lowercase \[text\] | Converts text to lowercase. | lowercase WORLD |
| titlecase \[text\] | Converts text to title case. | titlecase hello world |
| is palindrome \[text\] | Checks if a string is a palindrome. | is palindrome Madam, palindrome racecar |

### **Games & Randomness**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| coin flip | Simulates a coin flip (Heads or Tails). | coin flip, flip a coin |
| roll dice, roll \[NdS\] | Simulates rolling dice (e.g., 2 dice with 6 sides). | roll dice, roll 2d6 |
| play guess the number | Starts the "Guess the Number" game (1-100). | play guess the number, guess the number |
| \[number\] (during game) | Your guess in the "Guess the Number" game. | 50, 75 |
| quit game (during game) | Quits the "Guess the Number" game. | quit game |
| rock, paper, scissors | Plays a round of Rock-Paper-Scissors against Iris. | rock, paper, scissors |

### **File System Commands**

| Command/Alias | Description | Examples |
| :---- | :---- | :---- |
| list files \[path\] | Lists files and directories in the specified path (defaults to current directory). | list files, list files ., list files /home/user |

## **Persistent Memory**

Iris uses a JSON file named assistant\_memory.json to store certain data persistently across sessions. This includes:

* The number of times Iris has been started (page\_visits).  
* Your preferred name (user\_name).  
* The assistant's name (assistant\_name).  
* Total commands executed (total\_commands\_executed).

This file is automatically created and updated in the same directory as iris.py.

## **Error Handling**

Iris includes basic error handling for API requests, file operations, and user input. If an error occurs, Iris will attempt to provide a descriptive message. For network-related commands, ensure you have an active internet connection.

## **Dependencies**

The iris.py script relies on the following standard Python libraries and external libraries:

* **Standard Libraries:**  
  * datetime: For handling dates and times.  
  * json: For reading and writing JSON data (persistent memory).  
  * os: For interacting with the operating system (clearing screen, file paths).  
  * re: For regular expressions (command parsing).  
  * readline: For command history (on non-Windows systems).  
  * atexit: For registering cleanup functions (saving history on exit).  
  * platform: For getting system information.  
  * urllib.parse: For URL encoding/decoding.  
  * random: For games and random choices.  
  * webbrowser: For opening URLs in a web browser.  
  * time: For time-related calculations (e.g., uptime).  
* **External Libraries (install via pip):**  
  * requests: Used for making HTTP requests to various APIs (JokeAPI, IP-API.com, Open-Meteo, DuckDuckGo).  
  * pyperclip: Used for copying text to and pasting from the system clipboard.  
  * qrcode: Used for generating QR codes.  
  * psutil: Used for retrieving system and process information (CPU usage, RAM, disk usage, network interfaces).