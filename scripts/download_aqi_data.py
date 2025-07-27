import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# ------------------- CONFIGURATION -------------------
FREQUENCY = "Daily"  # Options: Daily, Monthly, etc.
TYPE = "City Level"  # Options: City Level, Station Level
STATE = "Uttar Pradesh"
CITY = "Lucknow"
# Set to None to download all years, or set to a specific year (e.g., "2025") to update only that year
YEAR_TO_UPDATE = None
DATA_DIR = "data"
# Path to your chromedriver (update if needed)
CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), "..", "chromedriver")
CHROMEDRIVER_PATH = os.path.abspath(CHROMEDRIVER_PATH)
# -----------------------------------------------------

URL = "https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing/aqi-repository"

# Prepare output directory
city_dir = os.path.join(DATA_DIR, CITY.replace(" ", "_"))
os.makedirs(city_dir, exist_ok=True)

def main():
    # Set up Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)
    try:
        driver.get(URL)
        time.sleep(10)  # Let page load longer for dynamic content

        # Select Frequency
        freq_select = wait.until(EC.presence_of_element_located((By.ID, "frequency")))
        Select(freq_select).select_by_visible_text(FREQUENCY)

        # Select Type
        type_select = wait.until(EC.presence_of_element_located((By.ID, "type")))
        Select(type_select).select_by_visible_text(TYPE)

        # Select State
        state_select = wait.until(EC.presence_of_element_located((By.ID, "state")))
        Select(state_select).select_by_visible_text(STATE)

        # Select City
        city_select = wait.until(EC.presence_of_element_located((By.ID, "city")))
        Select(city_select).select_by_visible_text(CITY)

        # Click Submit/Show Data button
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Show Data")]')))
        submit_btn.click()
        time.sleep(2)

        # Wait for table to load
        table = wait.until(EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "table")]')))
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 2:
                continue
            year = cols[0].text.strip()
            if YEAR_TO_UPDATE and year != str(YEAR_TO_UPDATE):
                continue
            xls_link = cols[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            if not xls_link:
                print(f"No XLS link for year {year}")
                continue
            out_path = os.path.join(city_dir, f"AQI_{CITY.replace(' ', '_')}_{year}.xls")
            print(f"Downloading {year} to {out_path} ...")
            download_xls(xls_link, out_path)
            print(f"Saved: {out_path}")
            if YEAR_TO_UPDATE:
                break  # Only one year needed
    finally:
        driver.quit()

def download_xls(url, out_path):
    import requests
    resp = requests.get(url)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(resp.content)

if __name__ == "__main__":
    main() 