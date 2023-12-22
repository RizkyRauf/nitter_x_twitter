import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class TwitterContent:
    def __init__(self, tweet_element):
        self.tweet_element = tweet_element

    def find_element(self, xpath):
        try:
            return self.tweet_element.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def get_fullname(self):
        xpath_fullname = './/div[@class="tweet-name-row"]/div[@class="fullname-and-username"]/a[@class="fullname"]'
        fullname_element = self.find_element(xpath_fullname)
        return fullname_element.text if fullname_element else "-"

    def get_username(self):
        xpath_username = './/div[@class="tweet-name-row"]/div[@class="fullname-and-username"]/a[@class="username"]'
        username_element = self.find_element(xpath_username)
        return username_element.text.replace("@", '') if username_element else "-"

    def get_date(self):
        xpath_date = './/span[@class="tweet-date"]/a'
        date_element = self.find_element(xpath_date)
        date_str = date_element.get_attribute("title") if date_element else ""
        return datetime.datetime.strptime(date_str, "%b %d, %Y · %I:%M %p UTC").strftime("%Y-%m-%d %H:%M:%S") if date_str else ""

    def get_reply(self):
        xpath_reply = './/div[@class="replying-to"]'
        reply_element = self.find_element(xpath_reply)
        if reply_element:
            reply_links = reply_element.find_elements(By.TAG_NAME, 'a')
            reply_usernames = [link.text.replace("@", '') for link in reply_links] if reply_links else []
            return reply_usernames[0] if reply_usernames else "-"
        return "-"

    def get_tweet(self):
        xpath_tweet = './/div[@class="tweet-content media-body"]'
        tweet_element = self.find_element(xpath_tweet)
        return tweet_element.text.strip() if tweet_element else "-"

    def get_comment_count(self):
        xpath_comment_container = './/span[@class="icon-comment"]/parent::div[@class="icon-container"]'
        comment_container_element = self.find_element(xpath_comment_container)
        comment_text = comment_container_element.text.strip() if comment_container_element else ""
        
        try:
            comment_count = int(comment_text.replace(',', '')) if comment_text.isdigit() else 0
            return comment_count
        except ValueError:
            print(f"Error converting '{comment_text}' to an integer.")
            return 0

    def get_retweet_count(self):
        xpath_retweet_container = './/span[@class="icon-retweet"]/parent::div[@class="icon-container"]'
        retweet_container_element = self.find_element(xpath_retweet_container)
        retweet_text = retweet_container_element.text.strip() if retweet_container_element else ""

        try:
            retweet_count = int(retweet_text.replace(',', '')) if retweet_text.isdigit() else 0
            return retweet_count
        except ValueError:
            print(f"Error converting '{retweet_text}' to an integer.")
            return 0

    def get_like_count(self):
        xpath_like_container = './/span[@class="icon-heart"]/parent::div[@class="icon-container"]'
        like_container_element = self.find_element(xpath_like_container)
        like_text = like_container_element.text.strip() if like_container_element else ""
        
        try:
            like_count = int(like_text.replace(',', '')) if like_text.isdigit() else 0
            return like_count
        except ValueError:
            print(f"Error converting '{like_text}' to an integer.")
            return 0

    def get_link_post(self):
        xpath_link = './/a[@class="tweet-link"]'
        link_element = self.find_element(xpath_link)

        if link_element is not None:
            try:
                link = link_element.get_attribute("href")
                if link:
                    link = link.replace("https://nitter.net/", "https://twitter.com/").replace("#m", "")
                    return link
            except Exception as e:
                print(f"Error extracting link: {e}")

        return None


    def to_json_entry(self):
        data = {
            "username": self.get_username(),
            "fullname": self.get_fullname(),
            "date": self.get_date(),
            "content": self.get_tweet(),
            "reply": self.get_reply(),
            "like": self.get_like_count(),
            "retweet": self.get_retweet_count(),
            "comment": self.get_comment_count(),
            "link_post": self.get_link_post(),
        }
        return data
