import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

BASE_URL = "https://quotes.toscrape.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_soup(url):
    """Fetch URL and return BeautifulSoup object."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def scrape_page(page_url):
    """Scrape quotes, authors, tags from one page."""
    soup = get_soup(page_url)
    if soup is None:
        return []

    data = []
    quote_blocks = soup.find_all("div", class_="quote")

    for q in quote_blocks:
        quote_text = q.find("span", class_="text").text.strip()
        author = q.find("small", class_="author").text.strip()

        # Extract tags
        tag_elements = q.find_all("a", class_="tag")
        tags = [t.text for t in tag_elements]

        data.append({
            "quote": quote_text,
            "author": author,
            "tags": ", ".join(tags),
            "source_page": page_url
        })

    return data


def scrape_all_pages():
    """Loop through all pages automatically."""
    all_data = []
    page_number = 1

    while True:
        url = f"{BASE_URL}/page/{page_number}/"
        print(f"Scraping Page: {page_number}")

        page_data = scrape_page(url)
        if not page_data:   # no more pages
            break

        all_data.extend(page_data)

        # Random delay to avoid detection
        time.sleep(random.uniform(1, 3))

        page_number += 1

    return all_data


def save_to_csv(data, filename="scraped_quotes.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\nSaved {len(df)} records to {filename}")


# -----------------------
# RUN SCRAPER
# -----------------------
if __name__ == "__main__":
    result = scrape_all_pages()
    save_to_csv(result)
