# main_scraper.py

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import subprocess
import sys
import os

# Hardcoded URLs for both scrapers
MARKETCAP_URL = 'https://companiesmarketcap.com/microsoft/marketcap/'
INVESTING_COM_URL = 'https://in.investing.com/equities/uber-technologies-inc'  # Example URL
CRUNCHBASE_URL = 'https://www.crunchbase.com/organization/anthropic'  # Example Crunchbase URL

# Function to run the MarketCap spider
def run_marketcap_spider(start_url):
    from marketcap_scraper.scraper.spiders.marketcap import MarketCapSpider  # Import the spider class
    
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    # Use the provided URL
    process.crawl(MarketCapSpider, start_urls=[start_url])
    
    process.start()

# Function to run the investing_com.py script
def run_investing_com_scraper(url):
    script_path = 'investing_com_scrapper/investing_com.py'
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} does not exist.")
        sys.exit(1)
    
    # Pass the URL as an argument to the investing_com.py script
    command = [sys.executable, script_path, url]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("investing_com scraper ran successfully.")
        print(result.stdout)
    else:
        print("Error running investing_com scraper:")
        print(result.stderr)

# Function to run crunchbase.py script
def run_crunchbase_scraper(url):
    script_path = 'crunchbase_scrapper/crunchbase_scraper.py'
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} does not exist.")
        sys.exit(1)
    
    command = [sys.executable, script_path, url]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("crunchbase scraper ran successfully.")
        print(result.stdout)
    else:
        print("Error running crunchbase scraper:")
        print(result.stderr)

# Main function to run all scrapers
def main():
    # Run the MarketCap spider with the hardcoded URL
    print(f"Starting MarketCap scraper with URL: {MARKETCAP_URL}")
    run_marketcap_spider(MARKETCAP_URL)
    
    # Run the investing_com scraper with the hardcoded URL
    print(f"Starting investing_com scraper with URL: {INVESTING_COM_URL}")
    run_investing_com_scraper(INVESTING_COM_URL)
    
    # Run the crunchbase scraper with the hardcoded URL
    print(f"Starting crunchbase scraper with URL: {CRUNCHBASE_URL}")
    run_crunchbase_scraper(CRUNCHBASE_URL)

if __name__ == '__main__':
    main()
