# **PyCLI Toolkit Documentation**

## **Version: 2.10.0**

## **Author: Connor**

## **1\. Introduction**

The **PyCLI Toolkit** is a versatile command-line interface (CLI) application built with Python. It provides a wide array of functionalities ranging from basic arithmetic and file operations to advanced text analysis, system diagnostics, and network utilities. Designed for ease of use, it can operate in both standard command-line mode and an interactive shell.

## **2\. Features Overview**

The PyCLI Toolkit is organized into several command categories, each offering specific functionalities:

* **greet**: Simple greeting messages.  
* **farewell**: Simple farewell messages.  
* **info**: Displays information about the application.  
* **calculate**: Performs basic arithmetic operations.  
* **file\_op**: Basic file reading and writing.  
* **text\_util**: Basic text manipulation (reverse, count).  
* **system\_info**: Displays basic system information (current directory, environment variables).  
* **time\_util**: Time and date operations.  
* **network\_util**: Basic network operations (simulated ping, DNS lookup).  
* **data\_util**: Data manipulation (sort lists, find unique elements).  
* **dev\_util**: Developer-focused tools (run Python scripts, create empty files).  
* **json\_util**: JSON parsing and validation.  
* **convert\_util**: Unit conversions (temperature).  
* **config\_util**: Manages application configurations (set, get, list, reset).  
* **data\_process\_util**: Data format conversions (CSV to JSON, JSON to CSV).  
* **text\_filter\_util**: Text filtering and searching within files (grep, filter lines).  
* **text\_transform\_util**: Text transformations (case, URL, Base64 encoding/decoding).  
* **clipboard\_util**: Simulates copying text to the clipboard.  
* **system\_security\_util**: System and security related operations (file hashing, simulated process listing).  
* **network\_adv\_util**: Advanced network operations (simulated port scan, HTTP GET).  
* **file\_system\_util**: Enhanced file system management (list directory contents with filters, compare files).  
* **text\_analysis\_util**: Advanced text analysis (word count, character frequency).  
* **system\_diagnostics\_util**: System information and diagnostics (simulated disk usage, uptime).

## **3\. Installation and Setup**

To use the PyCLI Toolkit, you need Python 3 installed on your system.

1. **Save the script**: Save the provided Python code as cli\_app.py (or any other .py filename you prefer).  
2. **Run from terminal**: Open your terminal or command prompt, navigate to the directory where you saved cli\_app.py, and run commands using python cli\_app.py \<command\> \[arguments\].

## **4\. Usage**

### **General CLI Structure**

The general syntax for using the PyCLI Toolkit is:

python cli\_app.py \[global\_flags\] \<command\> \[subcommand\] \[command\_arguments\]

### **Global Flags**

* \--verbose: Enable verbose output for more detailed logging.  
* \-i or \--interactive: Run the CLI in interactive mode.  
* \--raw: Suppress decorative headers/footers for commands like info and config\_util list, useful for scripting.

### **Interactive Mode**

To start the interactive shell:

python cli\_app.py \--interactive

Once in interactive mode, you'll see a cli\> prompt. You can type commands directly. Global flags like \--verbose and \--raw will persist across commands in the interactive session if enabled at startup. Type exit to quit the interactive shell, or help for a list of commands.

cli\> greet Connor  
cli\> info \--version  
cli\> exit

### **Command Examples**

Here are examples for each command category:

#### **greet**

Greets a user.

python cli\_app.py greet Connor  
python cli\_app.py greet Alice \--loud

#### **farewell**

Bids farewell to a user.

python cli\_app.py farewell Connor  
python cli\_app.py farewell Bob \--loud

#### **info**

Displays application information.

python cli\_app.py info  
python cli\_app.py info \--version  
python cli\_app.py info \--raw

#### **calculate**

Performs basic arithmetic operations.

python cli\_app.py calculate add 5 3  
python cli\_app.py calculate sub 10 4  
python cli\_app.py calculate mul 2.5 4  
python cli\_app.py calculate div 9 3

#### **file\_op**

Basic file reading and writing.

python cli\_app.py file\_op write my\_file.txt "Hello, this is some content."  
python cli\_app.py file\_op read my\_file.txt

#### **text\_util**

Basic text manipulation.

python cli\_app.py text\_util reverse "hello"  
python cli\_app.py text\_util count "Python is great\!"

#### **system\_info**

Displays system-related information.

python cli\_app.py system\_info cwd  
python cli\_app.py system\_info env

#### **time\_util**

Time and date operations.

python cli\_app.py time\_util now  
python cli\_app.py time\_util format "%%Y-%%m-%%d %%H:%%M:%%S"  
python cli\_app.py time\_util format "%%I:%%M:%%S %%p" \# Connor's preferred 12-hour format

#### **network\_util**

Basic network operations (simulated).

python cli\_app.py network\_util ping example.com  
python cli\_app.py network\_util ping localhost \--count 2  
python cli\_app.py network\_util lookup google.com

#### **data\_util**

Data manipulation.

python cli\_app.py data\_util sort "5,2,8,1,9"  
python cli\_app.py data\_util sort "5.5,2.1,8.9" \--reverse  
python cli\_app.py data\_util unique "apple,banana,apple,orange,banana"

#### **dev\_util**

Developer-focused tools.

python cli\_app.py dev\_util create\_file empty.txt  
\# To run a script (assuming test\_script.py exists):  
\# python cli\_app.py dev\_util run\_script test\_script.py

#### **json\_util**

JSON parsing and validation.

python cli\_app.py json\_util parse '{"name": "Alice", "age": 30}'  
python cli\_app.py json\_util validate '{"key": "value"}'  
\# Assuming data.json exists:  
\# python cli\_app.py json\_util parse data.json \--file

#### **convert\_util**

Unit conversions.

python cli\_app.py convert\_util temp 25 C  
python cli\_app.py convert\_util temp 77 F

#### **config\_util**

Manages application configurations.

python cli\_app.py config\_util set username Connor  
python cli\_app.py config\_util get username  
python cli\_app.py config\_util list  
python cli\_app.py config\_util reset

#### **data\_process\_util**

Data format conversions.

\# Assuming example.csv exists with headers: Name,Age  
\# Name,Age  
\# Alice,30  
\# Bob,24  
python cli\_app.py data\_process\_util csv\_to\_json example.csv  
python cli\_app.py data\_process\_util csv\_to\_json example.csv \--key-column Name  
python cli\_app.py data\_process\_util csv\_to\_json example.csv \--output-filepath output.json

\# Assuming example.json exists as a list of objects: \[{"Name": "Alice", "Age": 30}\]  
python cli\_app.py data\_process\_util json\_to\_csv example.json  
python cli\_app.py data\_process\_util json\_to\_csv example.json \--output-filepath output.csv

#### **text\_filter\_util**

Text filtering and searching within files.

\# Assuming log.txt contains various log entries  
python cli\_app.py text\_filter\_util grep log.txt "ERROR"  
python cli\_app.py text\_filter\_util grep log.txt "warning" \--ignore-case  
python cli\_app.py text\_filter\_util filter\_lines log.txt "success"  
python cli\_app.py text\_filter\_util filter\_lines log.txt "debug" \--exclude

#### **text\_transform\_util**

Text transformations.

python cli\_app.py text\_transform\_util upper "hello world"  
python cli\_app.py text\_transform\_util lower "HELLO WORLD"  
python cli\_app.py text\_transform\_util title "hello world"  
python cli\_app.py text\_transform\_util url\_encode "hello world\!"  
python cli\_app.py text\_transform\_util url\_decode "hello%20world%21"  
python cli\_app.py text\_transform\_util base64\_encode "secret text"  
python cli\_app.py text\_transform\_util base64\_decode "c2VjcmV0IHRleHQ="

#### **clipboard\_util**

Simulates copying text to the clipboard.

python cli\_app.py clipboard\_util copy "This text is copied\!"

#### **system\_security\_util**

System and security related operations.

\# Assuming my\_document.txt exists  
python cli\_app.py system\_security\_util hash\_file my\_document.txt  
python cli\_app.py system\_security\_util list\_processes

#### **network\_adv\_util**

Advanced network operations (simulated).

python cli\_app.py network\_adv\_util port\_scan example.com "22,80,443,8080"  
python cli\_app.py network\_adv\_util http\_get http://www.example.com

#### **file\_system\_util**

Enhanced file system management.

python cli\_app.py file\_system\_util list\_dir .  
python cli\_app.py file\_system\_util list\_dir /path/to/my/dir \--recursive \--type file  
python cli\_app.py file\_system\_util list\_dir . \--min-size 1024 \--max-size 102400  
python cli\_app.py file\_system\_util list\_dir . \--modified-after "2024-01-01 12:00:00"

\# Create two files for comparison  
\# echo "Line 1" \> file\_a.txt  
\# echo "Line 1\\nLine 2" \> file\_b.txt  
python cli\_app.py file\_system\_util compare\_files file\_a.txt file\_b.txt

#### **text\_analysis\_util**

Advanced text analysis.

python cli\_app.py text\_analysis\_util word\_count "This is a test sentence."  
python cli\_app.py text\_analysis\_util word\_count my\_document.txt \--file  
python cli\_app.py text\_analysis\_util char\_frequency "Hello World\!"  
python cli\_app.py text\_analysis\_util char\_frequency my\_document.txt \--file

#### **system\_diagnostics\_util**

System information and diagnostics (simulated).

python cli\_app.py system\_diagnostics\_util disk\_usage  
python cli\_app.py system\_diagnostics\_util uptime

## **5\. Configuration**

The PyCLI Toolkit uses a cli\_config.json file to store configurations.

* config\_util set \<key\> \<value\>: Sets a configuration value.  
* config\_util get \<key\>: Retrieves a configuration value.  
* config\_util list: Lists all stored configurations.  
* config\_util reset: Deletes the configuration file, resetting all settings.

## **6\. Troubleshooting and Notes**

* **Simulated Features**: Many network and system diagnostic commands are simulated for demonstration purposes. They do not interact with actual external systems or hardware.  
* **File Paths**: Ensure correct file paths are provided, especially for commands that interact with the file system.  
* **Dependencies**: The core script uses only standard Python libraries. No external pip installations are required.  
* **Error Messages**: The CLI provides informative error messages for invalid inputs or operations.