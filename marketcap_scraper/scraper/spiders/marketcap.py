import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os
import requests

class MarketCapSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(MarketCapSpider, self).__init__(*args, **kwargs)
        if 'start_urls' in kwargs:
            self.start_urls = kwargs['start_urls']

    name = 'marketcap'
    allowed_domains = ['companiesmarketcap.com']

    def parse(self, response):
        """Parse each company's detailed page to extract information."""
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract company name
        company_name = self.get_text(soup, "company-name")

        # Create a dictionary to store data
        data = {
            'Name': company_name,
            'Description': self.get_text(soup, "company-description"),
            'Share_Price': self.get_share_price(soup),
            'MarketCap': self.get_market_cap(soup),
            'Country': self.get_country(soup),
            'Revenue': self.get_additional_info(response.url, "revenue"),
            'Price_to_earnings_ratio': self.get_additional_info(response.url, "pe-ratio"),
            'Price_to_sales_ratio': self.get_additional_info(response.url, "ps-ratio"),
            'Total_assets': self.get_additional_info(response.url, "total-assets"),
            'Net_Asset': self.get_additional_info(response.url, "net-assets"),
            'Total_Debt': self.get_additional_info(response.url, "total-debt")
        }

        # Create the directory if it doesn't exist
        save_path = os.path.join(os.getcwd(), 'data', 'market_cap')
        os.makedirs(save_path, exist_ok=True)

        # Save data to a JSON file with the company name
        filename = os.path.join(save_path, f'{company_name}.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.log(f'Saved file {filename}')

    def get_text(self, soup, div_class):
        """Helper method to extract text from a specific div class."""
        try:
            return soup.find("div", class_=div_class).text.strip()
        except AttributeError:
            return "Unable to find the text"

    def get_share_price(self, soup):
        """Helper method to extract the share price."""
        try:
            return soup.find("div", class_="col-lg-6")\
                .find("div", class_="row")\
                .find_next_sibling("div", class_="row")\
                .find("div", class_="info-box")\
                .find("div", class_="line1")\
                .text.strip()
        except AttributeError:
            return "Unable to find the share price"

    def get_market_cap(self, soup):
        """Helper method to extract the market cap."""
        try:
            return soup.find("div", class_="col-lg-6")\
                .find("div", class_="row")\
                .find("div", class_="info-box")\
                .find_next_sibling("div", class_="info-box")\
                .find("div", class_="line1")\
                .text.strip()
        except AttributeError:
            return "Unable to find the market cap"

    def get_country(self, soup):
        """Helper method to extract the country."""
        try:
            return soup.find("div", class_="col-lg-6")\
                .find("div", class_="row")\
                .find("div", class_="info-box")\
                .find_next_sibling("div", class_="info-box")\
                .find_next_sibling("div", class_="info-box")\
                .find("div", class_="line1")\
                .find("span", class_="responsive-hidden")\
                .text.strip()
        except AttributeError:
            return "Unable to find the country"

    def get_additional_info(self, base_url, metric):
        """Helper method to get additional information (revenue, PE ratio, etc.)."""
        metric = metric.strip('/')
        cleaned_base_url = base_url.rsplit('/', 2)[0] + '/'
        additional_url = urljoin(cleaned_base_url, metric + '/')

        try:
            response = requests.get(additional_url)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Error fetching data: {e}"

        soup = BeautifulSoup(response.text, "html.parser")

        try:
            result = soup.find("span", class_="background-ya").text.strip()
            if not result:
                raise AttributeError("No text found")
            return result
        except AttributeError:
            return f"Unable to find the {metric} information"
