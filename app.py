from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from modules.scraper import scrape_stock
from modules.yFinance import get_stock_info  # Import the get_stock_info function

app = Flask(__name__)
api = Api(app)

class UrlScraper(Resource):
    def get(self, stock_name=None):
        # Ignore favicon.ico requests
        if request.path == "/favicon.ico":
            return '', 204  # No Content

        stock_name = stock_name or request.args.get("stock")
        
        if not stock_name:
            return {"error": "Stock name is required."}, 400
        
        scraped_results = scrape_stock(stock_name=stock_name)
        return jsonify(scraped_results)

class StockInfo(Resource):
    def get(self):
        # Get the stock name from the query parameter
        stock_name = request.args.get("stock")
        
        if not stock_name:
            return {"error": "Stock name is required."}, 400
        
        # Use the get_stock_info function to fetch stock data
        stock_data = get_stock_info(stock_name)
        return jsonify(stock_data)

# Define a dedicated route for favicon.ico
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content

# Define routes for both URL parameter and query parameter
api.add_resource(UrlScraper, "/", "/<string:stock_name>")
api.add_resource(StockInfo, "/stock-info")  # New route for stock info

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True, use_reloader=True)
