from datetime import datetime
import json
import os
from crawlbase import CrawlingAPI
from bs4 import BeautifulSoup


def crawl(page_url, api_token):
    # Initialize the CrawlingAPI object with your token
    api = CrawlingAPI({'token': api_token})

    # Get the page content
    response = api.get(page_url)

    # Check if the request was successful
    if response['status_code'] == 200:
        # Extract data
        return response['body']
    else:
        print(f"Error: {response}")


def scrape_data(page_content):
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page_content, 'html.parser')
    # Find the h1 tag with class name "profile-name"
    title_tag = soup.find('h1', class_='profile-name')
    # Extract the title text
    title = title_tag.text.strip()
    # Find the span tag with class name "description"
    description_tag = soup.find('span', class_='description')
    # Extract the description text
    description = description_tag.text.strip()
    # Extract the location
    location = soup.select_one(
        '.section-content-wrapper li.ng-star-inserted').text.strip()
    # Extract the employees
    employees = soup.select_one(
        '.section-content-wrapper li.ng-star-inserted:nth-of-type(2)').text.strip()
    # Extract the company URL
    company_url = soup.select_one(
        '.section-content-wrapper li.ng-star-inserted:nth-of-type(5) a[role="link"]')['href']
    # Extract the company rank
    rank = soup.select_one(
        '.section-content-wrapper li.ng-star-inserted:nth-of-type(6) span').text.strip()
    # Extract the company founder
    founders = soup.select_one(
        '.mat-mdc-card.mdc-card .text_and_value li:nth-of-type(5) field-formatter').text.strip()
    founded = soup.select_one(
        '.mat-mdc-card.mdc-card .text_and_value li:nth-of-type(4) field-formatter').text.strip()

    # return the title and description
    return {
        'title': title,
        'description': description,
        'location': location,
        'employees': employees,
        'company_url': company_url,
        'rank': rank,
        'founded': founded,
        'founders': founders,
    }


if __name__ == "__main__":
    # Specify the Crunchbase page URL to scrape
    page_url = 'https://www.crunchbase.com/organization/anthropic'

    # Specify your Crawlbase token. Use the JavaScript token for Crunchbase
    api_token = 'j6K3RD4jrpM_gpRRVThJHg'

    # Call the crawl function
    page_content = crawl(page_url, api_token)
    data = scrape_data(page_content)

    # 1. Create the "data" folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # 2. Generate a filename with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")  # Use datetime.now()
    filename = f"data/crunchbase_data_{timestamp}.json"

    # 3. Save the data to the JSON file
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {filename}")
