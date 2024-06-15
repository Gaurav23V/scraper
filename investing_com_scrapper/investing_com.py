# investing_com.py

from zenrows import ZenRowsClient
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json
import sys
from datetime import datetime

client = ZenRowsClient("14417c9ec1490878fd3a63511a237e8fc97591c5")

def get_company_info(url):
    response = client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract company title
    title_element = soup.find("h1", class_="mb-2.5 text-left text-xl font-bold leading-7 text-[#232526] md:mb-2 md:text-3xl md:leading-8 rtl:soft-ltr")
    company_title = title_element.text.strip() if title_element else "Company title not found"

    # Extract stock price
    price_element = soup.find("div", class_="text-5xl/9 font-bold text-[#232526] md:text-[42px] md:leading-[60px]")
    stock_price = price_element.text.strip() if price_element else "Stock price not found"

    # Find financial summary link
    financial_summary_link = soup.find("a", href=lambda href: href and "financial-summary" in href)
    financial_summary = "Financial summary link not found"  # Set a default value
    financial_details = {}  # Dictionary to hold the financial details

    if financial_summary_link:
        financial_summary_url = urljoin(url, financial_summary_link["href"])
        financial_summary, financial_details = get_financial_summary(financial_summary_url)

    return company_title, stock_price, financial_summary, financial_details

def get_financial_summary(url):
    response = client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    financial_summary_span = soup.find("span", class_="text common-pre-text")
    financial_summary = financial_summary_span.text.strip() if financial_summary_span else "Financial summary not found"

    financial_details = {
        "total_revenue": None,
        "gross_profit": None,
        "operating_income": None,
        "net_income": None,
        "total_assets": None,
        "total_liability": None,
        "total_equity": None
    }

    css_selectors = {
        "total_revenue": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > span.text',
        "gross_profit": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > span.text',
        "operating_income": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > span.text',
        "net_income": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > span.text',
        "total_assets": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > span.text',
        "total_liability": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > span.text',
        "total_equity": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > span.text'
    }

    for key, selector in css_selectors.items():
        span_tag = soup.select_one(selector)
        financial_details[key] = span_tag.get_text(strip=True) if span_tag else None

    return financial_summary, financial_details

def main():
    # Default URL for the company page
    default_url = "https://in.investing.com/equities/uber-technologies-inc"
    
    # Use the URL passed as a command-line argument if provided
    url = sys.argv[1] if len(sys.argv) > 1 else default_url

    company_title, stock_price, financial_summary, financial_details = get_company_info(url)

    output_data = {
        "Company Title": company_title,
        "Stock Price": stock_price,
        "Financial Summary": financial_summary,
        "Total Revenue": financial_details.get("total_revenue"),
        "Gross Profit": financial_details.get("gross_profit"),
        "Operating Income": financial_details.get("operating_income"),
        "Net Income": financial_details.get("net_income"),
        "Total Assets": financial_details.get("total_assets"),
        "Total Liability": financial_details.get("total_liability"),
        "Total Equity": financial_details.get("total_equity")
    }

    # Create the directory if it doesn't exist
    output_dir = "data/investing_com"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate filename based on company title
    filename = os.path.join(output_dir, f"{company_title}.json")

    with open(filename, "w") as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"Data successfully saved to {filename}")

if __name__ == "__main__":
    main()
