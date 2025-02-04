from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional, Union
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import random
import time
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
]

HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def is_scrapable(url):
    """
    Checks if the given URL is scrapable by analyzing the response for CAPTCHA, IP block, or human verification.
    """
    session = HTMLSession()
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.html.render(timeout=20)  # Render JavaScript if necessary
        
        # Check for CAPTCHA indicators
        if "captcha" in response.text.lower() or "human verification" in response.text.lower():
            print(f"{url} is not scrapable due to CAPTCHA or human verification.")
            return False

        # Check for Cloudflare security
        if "Cloudflare" in response.text:
            print(f"{url} has Cloudflare security.")
            return False

        # Check for IP blocking
        if response.status_code == 403 or "access denied" in response.text.lower():
            print(f"{url} is not scrapable due to IP blocking.")
            print(f"Response code: {response.status_code}")
            return False
        print(f"{url} is scrapable.")
        return True

    except Exception as e:
        print(f"Error checking scrapability for {url}: {e}")
        return False

class SeleniumScraper:
    def __init__(self):
        """
        Initializes the Selenium WebDriver with Alpine-specific configurations.
        """
        self.chrome_options = Options()
        
        # Alpine-specific Chrome arguments
        self.chrome_options.add_argument('--headless=new')  # New headless mode
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-software-rasterizer')
        self.chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        self.chrome_options.add_argument("--window-size=1920x1080")
        
        # Additional Alpine-specific settings
        # self.chrome_options.binary_location = "/usr/bin/chromium-browser"
        
        # Set ChromeDriver path
        service = Service(
            executable_path="/usr/bin/chromedriver",
            # executable_path="./modules/chromedriver",
            log_path="/dev/null"  # Suppress logging
        )
        
        try:
            self.driver = webdriver.Chrome(
                service=service,
                options=self.chrome_options
            )
            print("Chrome WebDriver initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Chrome WebDriver: {e}")
            raise
    
    def scrape(self, url, sleep=0):
        """
        Scrapes the given URL using the initialized WebDriver.
        """
        try:
            print(f"Navigating to {url}...")
            self.driver.get(url)

            # Wait for the page to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            if sleep > 0:
                time.sleep(sleep)

            print(f"Redirected URL: {self.driver.current_url}")
            page_source = self.driver.page_source
            print("Page successfully loaded.")

            soup = BeautifulSoup(page_source, "html.parser")
            print("Soup object created.")
            return soup

        except Exception as e:
            print(f"Scraping error: {e}")
            return None

    def quit_driver(self):
        """
        Quits the WebDriver instance.
        """
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                print("WebDriver quit successfully")
            except Exception as e:
                print(f"Error quitting WebDriver: {e}")

# Your RequestsHTMLScraper class remains unchanged
class RequestsHTMLScraper:
    def __init__(self, user_agent: str = random.choice(USER_AGENTS), timeout: int = 30):
        self.session = HTMLSession()
        self.session.headers.update(HEADERS)
        self.timeout = timeout
        
    def scrape(self, url: str, method: str = 'get', params: dict = None, 
               data: dict = None, headers: dict = HEADERS, render: bool = False, 
               wait: int = 0) -> Optional[BeautifulSoup]:
        try:
            request_headers = self.session.headers.copy()
            if headers:
                request_headers.update(headers)
            
            if method.lower() == 'get':
                response = self.session.get(
                    url, 
                    params=params, 
                    headers=request_headers,
                    timeout=self.timeout
                )
            elif method.lower() == 'post':
                response = self.session.post(
                    url, 
                    params=params, 
                    data=data, 
                    headers=request_headers,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if render:
                response.html.render(timeout=wait)
            
            response.raise_for_status()
            soup = BeautifulSoup(response.html.html, 'html.parser')
            print(f"Successfully scraped: {url}")
            return soup
            
        except requests.RequestException as e:
            print(f"Error scraping {e}")
            return None
        except Exception as e:
            print(f"Unexpected error scraping {url}: {e}")
            return None

    def close_session(self):
        if hasattr(self, 'session'):
            self.session.close()

# Initialize scrapers
seleniumScraper = SeleniumScraper()
requestsHtmlScraper = RequestsHTMLScraper()