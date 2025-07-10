from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time
import os
from datetime import date, timedelta

from scrape_table_all import scrape_table, initialize_csv
from return_dates import return_dates

# Update this path to your chromedriver location on Windows
chromedriver_path = r"C:\nepse_scraper\Sharesansar\chromedriver.exe"  # Use raw string or double backslashes

# Set up Chrome options and service
service = Service(executable_path=chromedriver_path)
options = Options()
# options.add_argument('--headless')  # Optional: run in headless mode

# Launch browser
browser = webdriver.Chrome(service=service, options=options)
browser.maximize_window()
browser.get("https://www.sharesansar.com/today-share-price")

# Wait for the page to load and find the sector dropdown
wait = WebDriverWait(browser, 5)
try:
    # Wait for the sector dropdown to be present and visible
    sector_dropdown = wait.until(EC.element_to_be_clickable((By.ID, 'sector')))
    
    # If it's a select dropdown, use Select class
    select = Select(sector_dropdown)
    select.select_by_visible_text('All Sector')
except Exception as e:
    print(f"Error with sector dropdown: {e}")
    # Alternative approach - try sending keys directly
    try:
        sector_dropdown = browser.find_element(By.ID, 'sector')
        sector_dropdown.click()
        time.sleep(1)
        sector_dropdown.clear()
        sector_dropdown.send_keys('All Sector')
    except Exception as e2:
        print(f"Alternative approach also failed: {e2}")

# Define date range - Continue from where you left off
sdate = date(2021, 3, 24)  # Start from the day after your last scraped date
edate = date(2025, 7, 9)   # End date (adjust as needed)
dates = return_dates(sdate, edate)

print(f"Continuing scraping from {sdate} to {edate}")
print(f"Total new dates to scrape: {len(dates)}")

# CSV file setup - DON'T clear existing data
csv_filename = "all_stock_data.csv"
# Comment out initialize_csv to preserve existing data
# initialize_csv(csv_filename)  # This would clear your existing data!

if os.path.exists(csv_filename):
    print(f"Appending new data to existing {csv_filename}")
else:
    print(f"Warning: {csv_filename} not found. Creating new file.")

for day in dates:
    print(f"Processing date: {day}")
    # Enter the date
    try:
        # Wait for date input to be available
        date_input = wait.until(EC.element_to_be_clickable((By.ID, 'fromdate')))
        date_input.clear()
        date_input.send_keys(day)
        
        # Click Search button
        search_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_todayshareprice_submit')))
        search_button.click()
        
        # Wait for the page to load
        time.sleep(3)
        
        # Scrape the table
        html = browser.page_source
        scrape_table(data=html, date=day, csv_filename=csv_filename)
        
    except Exception as e:
        print(f"Error processing date {day}: {e}")
        continue

print(f"\nScraping completed!")
print(f"Data from {sdate} to {edate} has been appended to {csv_filename}")

# Close browser
browser.quit()


