from .modules import *

def fetch_msn_data(stock):
    url = f"https://www.msn.com/en-gb/money/stockdetails/{stock}-us-stock/fi-a1plh7?id=a1plh7"
    
    soup = seleniumScraper.scrape(url=url,sleep=0)

    try:
        data_dict = {}

        # Find all the factsRow elements
        facts_rows = soup.find_all('div', class_='factsRow-DS-EntryPoint1-1')

        for row in facts_rows:
            key = row.find('span', class_='factsRowKeyText-DS-EntryPoint1-1').get('title', '').strip()
            value = row.find('div', class_='factsRowValue-DS-EntryPoint1-1').get('title', '').strip()
            data_dict[key] = value

        return data_dict
    except Exception as e:
        print(f"Exception occurred: {e}")  
        return {}  

def fetch_zack_data(stock):
    url = f"https://www.zacks.com/stock/quote/{stock}"

    soup = requestsHtmlScraper.scrape(url=url,wait=0)

    try:
        fetched_dev = soup.find('div', class_='zr_rankbox composite_group')
        head_data = fetched_dev.find("p",class_="rank_view")
        main_data = head_data.find_all("span",class_="composite_val")

        keys = ["value","growth","momentum","vgm"]
        # Dictionary to store the key-value pairs
        result_dict = {}
        result_dict['insdustry'] = soup.find("a",class_="sector").text.replace("Industry:","").strip()

        for i, container in enumerate(main_data):
            # Extract review details and remove any unwanted characters
            value = container.text.strip()
            
            # Map each cleaned value to a corresponding key
            if i < len(keys):
                result_dict[keys[i]] = value
            else:
                print("Warning: More values than keys provided!")

        return result_dict
    except Exception as e:
        print(f"Exception occurred: {e}")   
        return {} 

def fetch_zack_data2(stock):
    url = f"https://www.zacks.com/stock/research/{stock}/price-target-stock-forecast"

    soup = requestsHtmlScraper.scrape(url=url,wait=0)
    
    try:
        avg_price_target = soup.find_all('th', class_='align_center')[-1]
        lst_data = soup.find_all('td', class_='align_center')
        lst_data.append(avg_price_target)

        keys = ["highest_price_target","lowest_price_target","upside_to_avg_price_target","avg_price_target"]
        # Dictionary to store the key-value pairs
        result_dict = {}

        for i, container in enumerate(lst_data):
            # Extract review details and remove any unwanted characters
            value = container.text.replace("\n11.25%","").strip()
            
            # Map each cleaned value to a corresponding key
            if i < len(keys):
                result_dict[keys[i]] = value
            else:
                print("Warning: More values than keys provided!")

        return result_dict
    except Exception as e:
        print(f"Exception occurred: {e}")  
        return {}  

# Usage
def scrape_stock(stock_name):
    try:
        if stock_name:
            result  = fetch_msn_data(stock_name)

            result2 = fetch_zack_data(stock_name)
            if result2:  result.update(result2)

            result3 = fetch_zack_data2(stock_name)
            if result3: result.update(result3)
            
            requestsHtmlScraper.close_session()
            seleniumScraper.quit_driver()
            return result
        return {} 
    
    except Exception as e:
        print(f"scrape_stock method exception : {e}")
        requestsHtmlScraper.close_session()
        seleniumScraper.quit_driver()
        return {}