# main_scraper.py

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import subprocess
import sys
import os

INVESTING_COM_URL = 'https://investing.com'

# Function to run the MarketCap spider


def run_marketcap_spider(company_name):
    # Import the spider class
    from marketcap_scraper.scraper.spiders.marketcap import MarketCapSpider

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # Define the base URL template
    base_url = 'https://companiesmarketcap.com/{}/marketcap/'

    # Construct the full URL using the company name
    start_url = base_url.format(company_name)

    # Use the provided URL
    process.crawl(MarketCapSpider, start_urls=[start_url])

    process.start()


def run_investing_scraper(company_name):
    try:
        # Specify the relative or absolute path to index.js
        # Adjust this path as needed
        index_js_path = os.path.join('investing_com_puppeteer', 'index.js')

        # Run the Node.js script with the URL
        result = subprocess.run(
            ['node', index_js_path, company_name], capture_output=True, text=True)

        # Print the output from the Node.js script
        print(result.stdout)
        if result.stderr:
         print("Errors:")
         print(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to run crunchbase.py script


def run_crunchbase_scraper(company_name):
    script_path = 'crunchbase_scrapper/crunchbase_scraper.py'
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} does not exist.")
        sys.exit(1)

    # Define the base URL template
    base_url = 'https://www.crunchbase.com/organization/{}'

    # Construct the full URL using the company name
    start_url = base_url.format(company_name)

    command = [sys.executable, script_path, start_url]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("crunchbase scraper ran successfully.")
        print(result.stdout)
    else:
        print("Error running crunchbase scraper:")
        print(result.stderr)

# Main function to run all scrapers


def main():
    # Get the company name from user input
    company_name = input("Enter the company name: ")

    # Run the MarketCap spider with the provided company name
    print(f"Starting MarketCap scraper")
    run_marketcap_spider(company_name)

    # Run the investing_com scraper with the provided company name
    print(f"Starting investing_com scraper")
    run_investing_scraper(company_name)

    # Run the crunchbase scraper with the provided company name
    print(f"Starting crunchbase scraper")
    run_crunchbase_scraper(company_name)


if __name__ == '__main__':
    main()
