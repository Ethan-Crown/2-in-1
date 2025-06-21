"""
Browser automation plugin for superintelligence: allows agents to browse the web via Selenium.
Register as both 'sense' and 'api' plugin.
"""
from superintelligence.registry import register
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import tempfile
import json

BROWSER_HISTORY_FILE = "browser_history.json"

class BrowserSession:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # Use a unique user data dir to avoid conflicts
        self._user_data_dir = tempfile.mkdtemp(prefix="selenium_profile_")
        chrome_options.add_argument(f'--user-data-dir={self._user_data_dir}')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.history = []

    def visit(self, url):
        self.driver.get(url)
        time.sleep(2)
        title = self.driver.title
        screenshot_path = f"screenshot_{int(time.time())}.png"
        self.driver.save_screenshot(screenshot_path)
        entry = {"url": url, "title": title, "screenshot": screenshot_path}
        self.history.append(entry)
        self.save_history()
        return entry

    def save_history(self):
        with open(BROWSER_HISTORY_FILE, "w") as f:
            json.dump(self.history, f)

    def close(self):
        self.driver.quit()

def browse_web(url="https://www.wikipedia.org"):
    session = BrowserSession()
    try:
        result = session.visit(url)
    finally:
        session.close()
    return result

def get_browser_history():
    # Optionally, could aggregate from all sessions if needed
    try:
        with open(BROWSER_HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

register("sense", browse_web)
register("api", browse_web)
