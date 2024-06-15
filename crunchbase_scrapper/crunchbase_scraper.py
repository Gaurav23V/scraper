# crunchbase.py

from datetime import datetime
import json
import os
import sys
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
    title = title_tag.text.strip() if title_tag else "Company title not found"
    # Find the span tag with class name "description"
    description_tag = soup.find('span', class_='description')
    # Extract the description text
    description = description_tag.text.strip() if description_tag else "Description not found"
    # Extract the location
    location_tag = soup.select_one('.section-content-wrapper li.ng-star-inserted')
    location = location_tag.text.strip() if location_tag else "Location not found"
    # Extract the employees
    employees_tag = soup.select_one('.section-content-wrapper li.ng-star-inserted:nth-of-type(2)')
    employees = employees_tag.text.strip() if employees_tag else "Employees count not found"
    # Extract the company URL
    company_url_tag = soup.select_one('.section-content-wrapper li.ng-star-inserted:nth-of-type(5) a[role="link"]')
    company_url = company_url_tag['href'] if company_url_tag else "Company URL not found"
    # Extract the company rank
    rank_tag = soup.select_one('.section-content-wrapper li.ng-star-inserted:nth-of-type(6) span')
    rank = rank_tag.text.strip() if rank_tag else "Rank not found"
    # Extract the company founder
    founders_tag = soup.select_one('.mat-mdc-card.mdc-card .text_and_value li:nth-of-type(5) field-formatter')
    founders = founders_tag.text.strip() if founders_tag else "Founders not found"
    # Extract founded date
    founded_tag = soup.select_one('.mat-mdc-card.mdc-card .text_and_value li:nth-of-type(4) field-formatter')
    founded = founded_tag.text.strip() if founded_tag else "Founded date not found"

    # return the title and description
    return {
        'title': title,
        'description': description,
        'location': location,
        'employees': employees,
        'company_url': company_url,
        'rank': rank,
        'founders': founders,
        'founded': founded
    }


def main():
    # Check if a URL is provided as an argument
    if len(sys.argv) > 1:
        page_url = sys.argv[1]
    else:
        page_url = 'https://www.crunchbase.com/organization/anthropic'  # Default URL if not provided

    # Specify your Crawlbase token. Use the JavaScript token for Crunchbase
    api_token = 'j6K3RD4jrpM_gpRRVThJHg'

    # Call the crawl function
    page_content = crawl(page_url, api_token)
    data = scrape_data(page_content)

    # 1. Create the "data/crunchbase" folder if it doesn't exist
    if not os.path.exists("data/crunchbase"):
        os.makedirs("data/crunchbase")

    # 2. Generate a filename based on the company title
    filename = f"data/crunchbase/{data['title']}.json"

    # 3. Save the data to the JSON file
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
