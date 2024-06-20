# Financial Information Scraper

## Project Overview

Welcome to the Financial Information Scraper! This project is designed to scrape financial data for any company available on the internet. With this tool, users can easily obtain detailed financial information such as stock prices, revenue, profit margins, and other relevant metrics. The scraped data is saved in JSON format in the `data` folder for easy access and further analysis.

## Features

- **User-Friendly**: Simply run the script and enter the company name to fetch financial information.
- **Comprehensive Data**: Collects a wide range of financial metrics.
- **JSON Output**: Stores the data in a structured JSON format for easy use.
- **Automated Storage**: All data is saved automatically in the `data` folder.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your local machine.
- Git installed for cloning the repository.
- Necessary Python libraries, which can be installed using the provided requirements file.

### Installation

1. **Clone the Repository**

   Open your terminal and run the following command to clone the repository:

   ```bash
   git clone https://github.com/yourusername/financial-info-scraper.git
   ```

2. **Navigate to the Project Directory**

   Change to the project directory:

   ```bash
   cd financial-info-scraper
   ```

3. **Install Dependencies**

   Use `pip` to install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```
   ---

### Usage

To use the scraper, follow these steps:

1. **Run the Scraper Script**

   Execute the main script by running:

   ```bash
   python main_scraper.py
   ```

2. **Enter the Company Name**

   After running the script, you will be prompted to enter the name of the company whose financial details you want to scrape. Type the name and press Enter.

   ```text
   Please enter the company name: [Company Name]
   ```

3. **View the Output**

   The scraped data will be saved in the `data` folder in JSON format. The file will be named based on the company name and timestamp, making it easy to locate.

   Example file name: `company_name_2024-06-20_12-00.json`


Happy scraping!

---
