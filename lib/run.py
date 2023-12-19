import json
from datetime import datetime
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from lib.util import getRandomUserAgent, scroll_down, load_more
from lib.content import TwitterContent

class NitterTwitterScraper:
    @staticmethod
    def configure_browser_options(options, user_agent):
        options.add_argument("--no-sandbox")
        # options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument(f"user-agent={user_agent}")
        return options

    @staticmethod
    def initialize_driver():
        try:
            options = Options()
            user_agent = getRandomUserAgent()
            NitterTwitterScraper.configure_browser_options(options, user_agent)
            chrome_driver_path = ChromeDriverManager().install()
            return webdriver.Chrome(service=ChromeService(chrome_driver_path), options=options)
        except Exception as e:
            print(f"Error initializing driver: {e}")
            raise

    @staticmethod
    def run_scraper(key, start, end, lang):
        driver = NitterTwitterScraper.initialize_driver()
        if " " in key:
            key = key.replace(" ", "+")
        driver.get(f"https://nitter.net/search?f=tweets&q={key}&since={start}&until={end}&near={lang}")

        tweets_data = []  # List to store tweet data

        try:
            while True:
                try:
                    scroll_down(driver)
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                    print(f"Error scrolling down if not content loaded")
                    break

                try:
                    timeline_item_elements = driver.find_elements(By.CLASS_NAME, "timeline-item")
                    for timeline_item in timeline_item_elements:
                        twitter_content = TwitterContent(timeline_item)
                        json_data = twitter_content.to_json_entry()
                        tweets_data.append(json_data)
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                    print(f"Error extracting content: {e}")

                try:
                    if not load_more(driver):
                        print("No more content to load.")
                        break
                except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                    print(f"Error loading more content: {e}")
                    break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Generate filename based on key and current datetime
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{key}_{current_datetime}.json"

        # Close the file after the loop
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(tweets_data, json_file, indent=2)

        # Close the driver
        driver.quit()
