const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
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
async function scrapeData(url) {
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

    // Navigate to the specified URL
    await page.goto(url, {
      waitUntil: "networkidle2", // Wait until the network is idle
    });
    await page.waitForTimeout(2000); // Wait for 2 seconds
    await page.click('input[data-test="search-section"]');
    await page.click('input[data-test="search-section"]');
    await page.keyboard.type(searchQuery);

    // Wait for the search results page to load
    await page.waitForNavigation();
  } catch (error) {
    console.error("Error in scrapeData:", error);
  } finally {
    // Close the browser after scraping is done (if browser is defined)
    if (browser) {
      await browser.close();
    }
  }
}

const url = "https://www.investing.com/";
scrapeData(url);
