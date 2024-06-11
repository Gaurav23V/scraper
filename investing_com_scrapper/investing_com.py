from zenrows import ZenRowsClient
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json
from datetime import datetime

# Create a single instance of ZenRowsClient outside the functions
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

    # Extract financial summary text
    financial_summary_span = soup.find("span", class_="text common-pre-text")
    financial_summary = financial_summary_span.text.strip() if financial_summary_span else "Financial summary not found"

    # Initialize dictionary to store the financial details
    financial_details = {
        "total_revenue": None,
        "gross_profit": None,
        "operating_income": None,
        "net_income": None,
        "total_assets": None,
        "total_liability": None,
        "total_equity": None
    }

    # CSS selectors for the financial details
    css_selectors = {
        "total_revenue": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > span.text',
        "gross_profit": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > span.text',
        "operating_income": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > span.text',
        "net_income": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section:nth-of-type(2) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > span.text',
        "total_assets": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section:nth-of-type(3) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > span.text',
        "total_liability": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section:nth-of-type(3) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > span.text',
        "total_equity": '#js-main-container > section:nth-of-type(2) > div > section:nth-of-type(2) > section:nth-of-type(3) > section > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > span.text'
    }

    # Extract and assign the financial details
    for key, selector in css_selectors.items():
        span_tag = soup.select_one(selector)
        financial_details[key] = span_tag.get_text(strip=True) if span_tag else None

    return financial_summary, financial_details

def main():
    # URL of the company page
    url = "https://in.investing.com/equities/uber-technologies-inc"

    # Fetch the company information and financial details
    company_title, stock_price, financial_summary, financial_details = get_company_info(url)

    # Create the output dictionary
    output_data = {
        "Company Title": company_title,
        "Stock Price": stock_price,
        "Financial Summary": financial_summary,
        # Directly include financial details at the top level
        "Total Revenue": financial_details.get("total_revenue"),
        "Gross Profit": financial_details.get("gross_profit"),
        "Operating Income": financial_details.get("operating_income"),
        "Net Income": financial_details.get("net_income"),
        "Total Assets": financial_details.get("total_assets"),
        "Total Liability": financial_details.get("total_liability"),
        "Total Equity": financial_details.get("total_equity")
    }

    # Ensure the data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Generate the filename with the timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/investing_com_{timestamp}.json"

    # Write the output data to a JSON file
    with open(filename, "w") as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"Data successfully saved to {filename}")

if __name__ == "__main__":
    main()
