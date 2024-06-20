const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
const fs = require("fs");
const path = require("path");

// Use the stealth plugin
puppeteer.use(StealthPlugin());

// Function to initialize Puppeteer and perform necessary setup
async function setupBrowser() {
  try {
    // Launch a new browser instance using puppeteer-extra
    const browser = await puppeteer.launch({
      headless: true, // Change to true if you want headless mode
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--disable-gpu",
      ],
    });

    // Return the browser instance
    return browser;
  } catch (error) {
    console.error("Error in setupBrowser:", error);
    throw error;
  }
}

// Function to navigate to a URL and extract company title, stock price, and financial data
async function scrapeData(company_name) {
  let browser;
  try {
    // Setup Puppeteer and get browser instance
    browser = await setupBrowser();

    // Create a new page
    const page = await browser.newPage();

    // Set a user agent to mimic a real browser
    await page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    );

    const url = "https://www.investing.com/"

    // Navigate to the specified URL
    await page.goto(url, {
      waitUntil: "networkidle2", // Wait until the network is idle
    });

    // Click on the search button to reveal the search input
    await page.click(".mainSearch_search-button__zHjdB");

    // Focus on the search input and type "uber"
    const searchInputSelector = 'input[type="search"]';
    await page.click(searchInputSelector);
    await page.type(searchInputSelector, company_name);
    await page.keyboard.press("Enter");

    // Wait for the new page to load
    await page.waitForNavigation({
      waitUntil: "networkidle2",
    });

    // Click on the anchor tag with class name "js-inner-all-results-quote-item row"
    await page.click("a.js-inner-all-results-quote-item.row");

    // Wait for the new page to load
    await page.waitForNavigation({
      waitUntil: "networkidle2",
    });

    // Wait for the first h1 tag to be loaded
    await page.waitForSelector("h1");

    // Extract the text from the first h1 tag (Company Title)
    const company_title = await page.evaluate(() => {
      const h1Element = document.querySelector("h1");
      return h1Element ? h1Element.innerText : "No H1 Tag Found";
    });

    const title = company_title;

    // Extract the stock price using the specified CSS selector
    const stock_price = await page.evaluate(() => {
      const priceElement = document.querySelector(".text-5xl\\/9"); // Adjust the selector as per your needs
      return priceElement
        ? priceElement.textContent.trim()
        : "Stock Price Not Found";
    });

    const stockPrice = stock_price;

    // Open a new page with the modified URL
    const newUrl = page.url() + "-financial-summary";
    await page.goto(newUrl, {
      waitUntil: "networkidle2", // Wait until the network is idle
    });

    // Extract the text inside a p tag with id "profile-story"
    const financialSummary = await page.evaluate(() => {
      const profileStory = document.querySelector("p#profile-story");
      return profileStory ? profileStory.textContent : "";
    });

    // Extract the text from all td tags
    const tdElements = await page.$$("td");
    const textArray = await Promise.all(
      tdElements.map((td) => td.evaluate((node) => node.textContent.trim()))
    );

    const total_revenue = textArray[textArray.indexOf("Total Revenue") + 1];
    const gross_profit = textArray[textArray.indexOf("Gross Profit") + 1];
    const operating_income =
      textArray[textArray.indexOf("Operating Income") + 1];
    const net_income = textArray[textArray.indexOf("Net Income") + 1];
    const total_assets = textArray[textArray.indexOf("Total Assets") + 1];
    const total_liabilities =
      textArray[textArray.indexOf("Total Liabilities") + 1];
    const total_equity = textArray[textArray.indexOf("Total Equity") + 1];
    const period_length = textArray[textArray.indexOf("Period Length:") + 1];
    const cashFromOperatingActivities =
      textArray[textArray.indexOf("Cash From Operating Activities") + 1];
    const cashFromInvestingActivities =
      textArray[textArray.indexOf("Cash From Investing Activities") + 1];
    const cashFromFinancingActivities =
      textArray[textArray.indexOf("Cash From Financing Activities") + 1];
    const netChangeInCash =
      textArray[textArray.indexOf("Net Change in Cash") + 1];

    const spanTexts = await page.$$eval("span.float_lang_base_2", (spans) =>
      spans.map((span) => span.textContent)
    );

    const [
      gross_margin,
      operating_margin,
      net_profit_margin,
      return_on_investment,
      quick_ratio,
      current_ratio,
      lt_debt_to_equity,
      total_debt_to_equity,
      cash_flow,
      revenue,
      operating_cash_flow,
    ] = spanTexts.slice(0, 11);

    // Create the scrapedData object here
    const scrapedData = {
      title,
      stockPrice,
      financial_summary: {
        financialSummary,
        total_revenue,
        gross_profit,
        operating_income,
        net_income,
        total_assets,
        total_liabilities,
        total_equity,
        period_length,
        cashFromOperatingActivities,
        cashFromInvestingActivities,
        cashFromFinancingActivities,
        netChangeInCash,
        ratios: {
          gross_margin,
          operating_margin,
          net_profit_margin,
          return_on_investment,
          quick_ratio,
          current_ratio,
          lt_debt_to_equity,
          total_debt_to_equity,
        },
        cash_flows: {
          cash_flow,
          revenue,
          operating_cash_flow,
        },
      },
    };

    // Modify the path to go back one directory and then into 'data/investing_com'
    const dataDir = path.join(__dirname, "..", "data", "investing_com");

    // Ensure the 'investing_com' directory exists within 'data'
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true }); // Create the directory recursively
    }

    // Determine the file name and path
    const sanitizedTitle = scrapedData.title.replace(/[^a-zA-Z0-9]/g, "_"); // Replace non-alphanumeric characters with underscores
    const filePath = path.join(dataDir, `${sanitizedTitle}.json`);

    // Save the scraped data to a JSON file
    fs.writeFileSync(filePath, JSON.stringify(scrapedData, null, 2));

    console.log(`Data saved to ${filePath}`);
  } catch (error) {
    console.error("Error in scrapeData:", error);
  } finally {
    // Close the browser after scraping is done (if browser is defined)
    if (browser) {
      await browser.close();
    }
  }
}

// Get the URL from the command line arguments
const company_name = process.argv[2];
if (company_name) {
  scrapeData(company_name);
} else {
  console.error(
    "No company_name provided. Please pass the company_name as a command-line argument."
  );
}
