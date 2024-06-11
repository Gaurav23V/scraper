import requests
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from  scraper.items import MarketCapItem  # Import the MarketCapItem class

class MarketCapSpider(scrapy.Spider):
    name = 'marketcap'
    allowed_domains = ['companiesmarketcap.com']
    start_urls = ['https://companiesmarketcap.com/']
    page_number = 1  # Initialize page number

    def parse(self, response):
        """Parse the main page to get company URLs and follow pagination."""
        soup = BeautifulSoup(response.text, "html.parser")

        # Extracting all company URLs on the page
        div_tags = soup.find_all("div", class_="name-div")
        for div_tag in div_tags:
            anchor_tag = div_tag.find("a")
            href_value = anchor_tag["href"]
            full_url = urljoin(response.url, href_value)
            yield scrapy.Request(full_url, callback=self.parse_company_page)

        # Following pagination links up to page 50
        if self.page_number < 50:
            self.page_number += 1
            next_page_url = f'https://companiesmarketcap.com/page/{self.page_number}/'
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_company_page(self, response):
        """Parse each company's detailed page to extract information."""
        soup = BeautifulSoup(response.text, "html.parser")

        # Create a MarketCapItem instance
        item = MarketCapItem()

        # Extracting specific company information and assigning to item fields
        item['Name'] = self.get_text(soup, "company-name")
        item['Description'] = self.get_text(soup, "company-description")
        item['Share_Price'] = self.get_share_price(soup)
        item['MarketCap'] = self.get_market_cap(soup)
        item['Country'] = self.get_country(soup)

        # Collecting additional company metrics from other URLs
        item['Revenue'] = self.get_additional_info(response.url, "revenue")
        item['Price_to_earnings_ratio'] = self.get_additional_info(response.url, "pe-ratio")
        item['Price_to_sales_ratio'] = self.get_additional_info(response.url, "ps-ratio")
        item['Total_assets'] = self.get_additional_info(response.url, "total-assets")
        item['Net_Asset'] = self.get_additional_info(response.url, "net-assets")
        item['Total_Debt'] = self.get_additional_info(response.url, "total-debt")

        # Yielding the scraped data as a MarketCapItem
        yield item

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
        print(f"Fetching URL: {additional_url}")

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