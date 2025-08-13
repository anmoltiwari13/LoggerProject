import requests
from bs4 import BeautifulSoup
import time
import json
import re
def fetch_data_with_retry(url, retries=3, delay=2):
    """Fetch data from a URL with retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay* (attempt + 1))  # Exponential backoff
            else:
                raise

def extract_data_from_html(html_content):
    """Extract data from HTML content using BeautifulSoup."""
    if not html_content:
        raise ValueError("No HTML content provided for extraction.")
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []
    for item in soup.find_all('a', href=True):
        if re.search(r'python', item['href'], re.IGNORECASE):   
            data.append(item['href'])
    return data    

def save_data_to_json(data, filename="scrapped_data.json"):
    """Save extracted data to a JSON file."""
    try:
        with open(filename, 'w') as file:
            json.dump(data,file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")

url= "https://www.python.org/"
html_content = fetch_data_with_retry(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data)