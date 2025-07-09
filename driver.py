from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time
from datetime import date

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
wait = WebDriverWait(browser, 10)
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

# Define date range
sdate = date(2021, 6, 3)
edate = date(2021, 6, 6)
dates = return_dates(sdate, edate)

# Initialize the CSV file (removes existing file if present)
csv_filename = "all_stock_data.csv"
initialize_csv(csv_filename)

for day in dates:
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
        time.sleep(5)
        
        # Scrape the table
        html = browser.page_source
        scrape_table(data=html, date=day, csv_filename=csv_filename)
        
    except Exception as e:
        print(f"Error processing date {day}: {e}")
        continue

# Close browser
browser.quit()


