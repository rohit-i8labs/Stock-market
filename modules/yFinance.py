import yfinance as yf

def get_stock_info(stock_name):
    """
    Fetches detailed stock information, including current stock price, company name,
    currency, country, sector, industry, market cap, dividend yield, and 52-week high/low.

    Args:
        stock_name (str): The stock ticker symbol (e.g., "AAPL" for Apple, "GOOGL" for Alphabet).

    Returns:
        dict: A dictionary containing detailed stock information.
    """
    try:
        # Fetch stock data using yfinance
        stock = yf.Ticker(stock_name)
        stock_info = stock.info

        # Extract required fields
        current_stock_price = stock_info.get("currentPrice", "N/A")
        stock_company_name = stock_info.get("longName", "N/A")
        currency = stock_info.get("currency", "N/A")
        country = stock_info.get("country", "N/A")
        sector = stock_info.get("sector", "N/A")
        industry = stock_info.get("industry", "N/A")
        market_cap = stock_info.get("marketCap", "N/A")
        dividend_yield = stock_info.get("dividendYield", "N/A")
        fifty_two_week_high = stock_info.get("fiftyTwoWeekHigh", "N/A")
        fifty_two_week_low = stock_info.get("fiftyTwoWeekLow", "N/A")

        # Return the data in the desired format
        return {
            "currentStockPrice": current_stock_price,
            "stockCompanyName": stock_company_name,
            "currency": currency,
            "country": country,
            "sector": sector,
            "industry": industry,
            "marketCap": market_cap,
            "dividendYield": dividend_yield,
            "52WeekHigh": fifty_two_week_high,
            "52WeekLow": fifty_two_week_low,
        }
    except Exception as e:
        # Handle errors (e.g., invalid stock ticker)
        return {"error": str(e)}
