from fastapi import FastAPI, Query
from typing import Optional
from modules.scraper import scrape_stock

app = FastAPI()

@app.get("/")
async def url_scraper(stock: Optional[str] = Query(None, description="Stock name to scrape")):
    if not stock:
        return {"error": "Stock name is required."}
    
    scraped_results = scrape_stock(stock_name=stock)
    return scraped_results

@app.get("/{stock_name}")
async def url_scraper_with_param(stock_name: str):
    scraped_results = scrape_stock(stock_name=stock_name)
    return scraped_results

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return "", 204
