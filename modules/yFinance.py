import yfinance as yf

def get_stock_info(stock_name):
    """
    Fetches the current stock price, company name, and currency for a given stock ticker.

    Args:
        stock_name (str): The stock ticker symbol (e.g., "AAPL" for Apple, "GOOGL" for Alphabet).

    Returns:
        dict: A dictionary containing the current stock price, company name, and currency.
    """
    try:
        # Fetch stock data using yfinance
        stock = yf.Ticker(stock_name)
        stock_info = stock.info

        # Extract required fields
        current_stock_price = stock_info.get("currentPrice", "N/A")
        stock_company_name = stock_info.get("longName", "N/A")
        currency = stock_info.get("currency", "N/A")

        # Return the data in the desired format
        return {
            "currentStockPrice": current_stock_price,
            "stockCompanyName": stock_company_name,
            "currency": currency,
        }
    except Exception as e:
        # Handle errors (e.g., invalid stock ticker)
        return {"error": str(e)}
