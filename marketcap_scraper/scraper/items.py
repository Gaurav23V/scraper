import scrapy

class MarketCapItem(scrapy.Item):
    Name = scrapy.Field()  # The name of the company
    Description = scrapy.Field()  # A brief description of the company
    Share_Price = scrapy.Field()  # The current share price of the company
    MarketCap = scrapy.Field()  # The market capitalization of the company
    Country = scrapy.Field()  # The country where the company is based
    Revenue = scrapy.Field()  # The company's revenue
    Price_to_earnings_ratio = scrapy.Field()  # The company's P/E ratio
    Price_to_sales_ratio = scrapy.Field()  # The company's P/S ratio
    Total_assets = scrapy.Field()  # The company's total assets
    Total_Debt = scrapy.Field()  # The company's total debt
    Net_Asset = scrapy.Field()  # The company's net assets

