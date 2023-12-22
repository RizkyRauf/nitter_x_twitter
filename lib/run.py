import json
from datetime import datetime
from selenium.common.exceptions import TimeoutException, NoSuchCookieException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from lib.util import get_RandomUserAgent, scroll_down, load_more
from lib.content import TwitterContent

class TwitterXScraper:
    
    def configure_browser_options(options, user_agent):
        options.add_argument("--no-sanbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument(f"user-agent={user_agent}")
        return options
    
    def initalize_driver():
        try:
            options = Options()
            user_agent = get_RandomUserAgent()
            TwitterXScraper.configure_browser_options(options, user_agent)
            chrome_driver_path = ChromeDriverManager().install()
            return webdriver.Chrome(service=ChromeService(chrome_driver_path), options=options)
        except Exception as e:
            print(f"Error instalizing driver : {e}")
            raise

    def run_scraper(key, start, end, lang, retweets=True):
        driver = TwitterXScraper.initalize_driver()
        if " " in key:
            key = key.replace(" ", "+")

        # Construct the search URL based on the presence of the retweets flag
        retweets_param = "&e-nativeretweets=on" if retweets else ""
        search_url = f"https://nitter.net/search?f=tweets&q={key}{retweets_param}&since={start}&until={end}&near={lang}"

        driver.get(search_url)

        tweets_data = []

        try:
            while True:
                try:
                    scroll_down(driver)
                except (TimeoutException, NoSuchCookieException, ElementClickInterceptedException) as e:
                    print(f"Error Scrolling down if not content loaded")
                    break

                try:
                    timeline_item_elements = driver.find_elements(By.CLASS_NAME, "timeline-item")
                    for timeline_item in timeline_item_elements:
                        twitter_content = TwitterContent(timeline_item)
                        json_data = twitter_content.to_json_entry()
                        tweets_data.append(json_data)
                except (TimeoutException, NoSuchCookieException, ElementClickInterceptedException) as e:
                    print(f"Error extracting content {e}")

                try:
                    if not load_more(driver):
                        print("No more content to load.")
                        break
                except (TimeoutException, NoSuchCookieException, ElementClickInterceptedException) as e:
                    print(f"Error loading more content {e}")
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