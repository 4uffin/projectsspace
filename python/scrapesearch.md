# ScrapeSearch Script

The **ScrapeSearch** script is a Python program designed to scrape search results from Google based on a user-provided query and extract information from the retrieved URLs. It utilizes the `requests` library for sending HTTP requests and the `BeautifulSoup` library for parsing HTML content.

## Required Installations

Before running the script, make sure you have the following packages installed:

- pip install requests
- pip install beautifulsoup4

## Functions Overview

### `fetch_search_results(query)`
- Constructs a Google search URL based on the provided query.
- Sends a GET request to fetch search results from Google.
- Parses the HTML content of the search results page using BeautifulSoup.
- Extracts URLs from the search results and returns them as a list.

### `scrape_page(url)`
- Checks if the URL is from Twitter. If it is, the function skips scraping and returns None.
- Sends a GET request to the URL to scrape.
- Parses the HTML content of the page using BeautifulSoup.
- Extracts the page title, description, and a snippet of page contents.
- Prints the extracted information.

### `scrape_urls_based_on_query()`
- Prompts the user to enter a search query.
- Fetches search results based on the query using `fetch_search_results`.
- Randomly selects a maximum of 5 URLs from the search results.
- Scrapes each selected URL using the `scrape_page` function.
- Prints the page title, description, and snippet of page contents for each URL.

## Usage
1. Run the script.
2. Enter a search query when prompted.
3. The script will fetch search results and scrape information from the retrieved URLs.
4. Repeat steps 2-3 as desired.
5. To exit the program, enter "quit" when prompted for a search query.

## Notes
- Error handling is implemented to handle timeouts, HTTP errors, and other exceptions.
- The script avoids scraping Twitter pages.
- The maximum number of URLs to scrape per query is set to 5.
