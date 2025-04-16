# ScrapeSearch
import requests  # Importing the 'requests' library for sending HTTP requests
from bs4 import BeautifulSoup  # Importing the 'BeautifulSoup' class from the 'bs4' module for parsing HTML
import random  # Importing the 'random' module for generating random numbers

def fetch_search_results(query):
    """
    Fetches search results from Google based on the provided query.

    Args:
    query (str): The search query.

    Returns:
    list: A list of URLs extracted from the search results.
    """
    # Construct the search URL
    search_url = f"https://www.google.com/search?q={query}"
    
    # Set a valid User-Agent header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    
    try:
        # Send GET request to fetch search results with a timeout of 7 seconds
        response = requests.get(search_url, headers=headers, allow_redirects=True, timeout=7)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract URLs from search results
        links = soup.find_all("a")
        if links:
            urls = [link.get("href") for link in links if link.get("href") and link.get("href").startswith("http")]
            return urls
        else:
            print("No links found in the search results.")
            return []
    except requests.exceptions.Timeout:
        print("Timeout occurred while fetching search results.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching search results: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def scrape_page(url):
    """
    Scrapes information from a given URL.

    Args:
    url (str): The URL to scrape.

    Returns:
    tuple: A tuple containing page title, description, and snippet of page contents.
    """
    if "twitter.com" in url:
        print("\nSkipping Twitter page:", url)
        return None
    
    try:
        # Send GET request to the URL with a timeout of 7 seconds
        response = requests.get(url, timeout=7)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract page title
        page_title = soup.title.get_text() if soup.title else "No title found"
        
        # Extract page description
        meta_description = soup.find("meta", attrs={"name": "description"})
        page_description = meta_description["content"] if meta_description else "No description found"
        
        # Extract short bit of page contents (text from <p> tags)
        page_contents = ""
        for paragraph in soup.find_all("p"):
            page_contents += paragraph.get_text() + " "
        
        # Print the page title, description, and snippet of page contents
        print(f"\nPage title: {page_title}")
        print(f"Page description: {page_description}")
        print(f"Page snippet: {page_contents[:200]}...")  # Print first 200 characters of page contents
        
        return page_title, page_description, page_contents
    except requests.exceptions.Timeout:
        print(f"\nTimeout occurred while scraping page {url}.")
        return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred while scraping page {url}: {e}")
        return None, None, None
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return None, None, None

def scrape_urls_based_on_query():
    """
    Prompts the user to enter a search query and scrapes URLs based on the query.
    """
    while True:
        # Get user input for the query
        query = input("Welcome to ScrapeSearch\n\nEnter your search query (or 'quit' to exit): ")
        if query.lower() == "quit":
            break
        
        print(f"\nSearching for '{query}' on Google...")
        
        # Fetch search results
        urls = fetch_search_results(query)
        
        if urls:
            print("\nSearch results fetched successfully.")
            
            # Randomly select num_urls from search results
            num_urls = min(5, len(urls))
            selected_urls = random.sample(urls, num_urls)
            
            for url in selected_urls:
                print(f"\nScraping page: {url}")
                result = scrape_page(url)
                
                if result:
                    print("-------------------------------------------------------")

# Start scraping URLs based on the user's query
scrape_urls_based_on_query()
