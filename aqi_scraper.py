#!/usr/bin/env python3
"""
AQI Data Scraper for CPCB (Central Pollution Control Board)
Scrapes AQI data for multiple cities from the CPCB website
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def setup_driver():
    """Setup Chrome WebDriver with anti-detection options"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def create_city_folder(city_name):
    """Create folder for city data"""
    folder_path = f"data/{city_name}"
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def scrape_aqi_data(state, city):
    """Scrape AQI data for a specific state and city"""
    URL = "https://airquality.cpcb.gov.in/ccr/#/caaqm-dashboard-all/caaqm-landing/aqi-repository"
    
    driver = setup_driver()
    
    try:
        print(f"🌐 Navigating to CPCB website...")
        driver.get(URL)
        time.sleep(15)  # Wait longer for Angular app to load
        
        print(f"🔍 Looking for dropdown elements...")
        
        # Find all ng-select dropdowns
        ng_selects = driver.find_elements(By.CSS_SELECTOR, "ng-select.select-box")
        print(f"✅ Found {len(ng_selects)} dropdown elements")
        
        if len(ng_selects) < 4:
            print("❌ Expected at least 4 dropdowns (Frequency, Type, State, City)")
            return {"status": "error", "message": "Not enough dropdowns found"}
        
        # Step 1: Select Frequency = "Daily"
        print(f"📅 Setting Frequency to 'Daily'...")
        try:
            frequency_dropdown = ng_selects[0]
            driver.execute_script("arguments[0].click();", frequency_dropdown)
            time.sleep(3)
            
            # Try multiple approaches to find and interact with the search input
            search_input = None
            
            # Try different selectors for the search input
            selectors = [
                ".ng-select-search",
                "input[type='text']",
                "input[placeholder*='search']",
                "input[placeholder*='Search']",
                ".ng-select-container input",
                "ng-select input"
            ]
            
            for selector in selectors:
                try:
                    search_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input.is_displayed() and search_input.is_enabled():
                        break
                except:
                    continue
            
            if search_input:
                search_input.clear()
                search_input.send_keys("Daily")
                time.sleep(2)
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)
                print("✅ Frequency set to 'Daily'")
            else:
                # Fallback: try typing directly into the dropdown
                actions = ActionChains(driver)
                actions.click(frequency_dropdown)
                actions.send_keys("Daily")
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(3)
                print("✅ Frequency set to 'Daily' (fallback method)")
                
        except Exception as e:
            print(f"❌ Error setting Frequency: {e}")
            return {"status": "error", "message": f"Failed to set Frequency: {e}"}
        
        # Step 2: Select Type = "City Level"
        print(f"🏙️ Setting Type to 'City Level'...")
        try:
            type_dropdown = ng_selects[1]
            driver.execute_script("arguments[0].click();", type_dropdown)
            time.sleep(3)
            
            # Try to find search input again
            search_input = None
            for selector in selectors:
                try:
                    search_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input.is_displayed() and search_input.is_enabled():
                        break
                except:
                    continue
            
            if search_input:
                search_input.clear()
                search_input.send_keys("City Level")
                time.sleep(2)
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)
                print("✅ Type set to 'City Level'")
            else:
                # Fallback method
                actions = ActionChains(driver)
                actions.click(type_dropdown)
                actions.send_keys("City Level")
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(3)
                print("✅ Type set to 'City Level' (fallback method)")
                
        except Exception as e:
            print(f"❌ Error setting Type: {e}")
            return {"status": "error", "message": f"Failed to set Type: {e}"}
        
        # Step 3: Select State
        print(f"🏛️ Setting State to '{state}'...")
        try:
            state_dropdown = ng_selects[2]
            driver.execute_script("arguments[0].click();", state_dropdown)
            time.sleep(3)
            
            # Try to find search input again
            search_input = None
            for selector in selectors:
                try:
                    search_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input.is_displayed() and search_input.is_enabled():
                        break
                except:
                    continue
            
            if search_input:
                search_input.clear()
                search_input.send_keys(state)
                time.sleep(2)
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)
                print(f"✅ State set to '{state}'")
            else:
                # Fallback method
                actions = ActionChains(driver)
                actions.click(state_dropdown)
                actions.send_keys(state)
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(3)
                print(f"✅ State set to '{state}' (fallback method)")
                
        except Exception as e:
            print(f"❌ Error setting State: {e}")
            return {"status": "error", "message": f"Failed to set State: {e}"}
        
        # Step 4: Select City
        print(f"🏙️ Setting City to '{city}'...")
        try:
            city_dropdown = ng_selects[3]
            driver.execute_script("arguments[0].click();", city_dropdown)
            time.sleep(3)
            
            # Try to find search input again
            search_input = None
            for selector in selectors:
                try:
                    search_input = driver.find_element(By.CSS_SELECTOR, selector)
                    if search_input.is_displayed() and search_input.is_enabled():
                        break
                except:
                    continue
            
            if search_input:
                search_input.clear()
                search_input.send_keys(city)
                time.sleep(2)
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)
                print(f"✅ City set to '{city}'")
            else:
                # Fallback method
                actions = ActionChains(driver)
                actions.click(city_dropdown)
                actions.send_keys(city)
                actions.send_keys(Keys.ENTER)
                actions.perform()
                time.sleep(3)
                print(f"✅ City set to '{city}' (fallback method)")
                
        except Exception as e:
            print(f"❌ Error setting City: {e}")
            return {"status": "error", "message": f"Failed to set City: {e}"}
        
        # Step 5: Click Submit button
        print(f"🚀 Clicking Submit button...")
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
            driver.execute_script("arguments[0].click();", submit_button)
            time.sleep(8)  # Wait longer for table to load
            print("✅ Submit button clicked")
        except Exception as e:
            print(f"❌ Error clicking Submit: {e}")
            return {"status": "error", "message": f"Failed to click Submit: {e}"}
        
        # Step 6: Find and click download links for each year
        print(f"📥 Looking for download links...")
        try:
            # Look for table with years and download icons
            table = driver.find_element(By.CSS_SELECTOR, "table")
            rows = table.find_elements(By.CSS_SELECTOR, "tr")
            
            download_links = []
            for row in rows[1:]:  # Skip header row
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                if len(cells) >= 2:
                    year_cell = cells[0].text.strip()
                    download_cell = cells[1]
                    
                    # Look for download icon/link in the second column
                    download_elements = download_cell.find_elements(By.CSS_SELECTOR, "a, button, [class*='download'], [class*='icon'], i, span")
                    
                    if download_elements:
                        download_links.append({
                            'year': year_cell,
                            'element': download_elements[0]
                        })
            
            print(f"✅ Found {len(download_links)} download links")
            
        except Exception as e:
            print(f"❌ Error finding download links: {e}")
            return {"status": "error", "message": f"Failed to find download links: {e}"}
        
        # Create city folder
        city_folder = create_city_folder(city)
        
        # Download files
        if download_links:
            print(f"✅ Found {len(download_links)} download links for years: {[link['year'] for link in download_links]}")
            downloaded_files = []
            for link_info in download_links:
                year = link_info['year']
                element = link_info['element']
                try:
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(3)
                    print(f"✅ Clicked download for year {year}")
                    downloaded_files.append({
                        'year': year,
                        'city': city,
                        'state': state,
                        'file_path': f"{city_folder}/{city}_{year}_AQI_Data.xlsx"
                    })
                except Exception as e:
                    print(f"❌ Error clicking download for year {year}: {e}")
            return {
                "status": "success",
                "message": f"Successfully completed full workflow for {state} -> {city}",
                "download_links_found": len(download_links),
                "years_downloaded": [link['year'] for link in download_links],
                "downloaded_files": downloaded_files,
                "city_folder": city_folder,
                "workflow_completed": True
            }
        else:
            print("❌ No download links found")
            return {
                "status": "warning",
                "message": f"Workflow completed but no download links found for {state} -> {city}",
                "workflow_completed": True
            }
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {"status": "error", "message": f"Unexpected error: {e}"}
    finally:
        driver.quit()

if __name__ == "__main__":
    # Define cities to scrape
    cities = [
        {"state": "Uttar Pradesh", "city": "Lucknow"},
        {"state": "Karnataka", "city": "Mysuru"},
        {"state": "Delhi", "city": "Delhi"},
        {"state": "Uttarakhand", "city": "Dehradun"},
        {"state": "Chandigarh", "city": "Chandigarh"}
    ]
    
    print("🚀 Starting AQI Data Scraping for Multiple Cities")
    print("=" * 60)
    
    results = []
    
    for city_info in cities:
        state = city_info["state"]
        city = city_info["city"]
        
        print(f"\n🏙️ Processing: {state} -> {city}")
        print("-" * 40)
        
        result = scrape_aqi_data(state, city)
        results.append({
            "state": state,
            "city": city,
            "result": result
        })
        
        print(f"📊 Result: {result['status']} - {result['message']}")
        
        # Wait between cities to avoid overwhelming the server
        if city_info != cities[-1]:  # Don't wait after the last city
            print("⏳ Waiting 5 seconds before next city...")
            time.sleep(5)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 SCRAPING SUMMARY")
    print("=" * 60)
    
    successful = 0
    for result in results:
        status = result["result"]["status"]
        if status == "success":
            successful += 1
        print(f"🏙️ {result['state']} -> {result['city']}: {status}")
    
    print(f"\n✅ Successfully processed: {successful}/{len(cities)} cities")
    print("🎉 Scraping completed! Check the data/ folder for downloaded files.") 