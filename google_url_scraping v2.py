from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Get domain from user
domain = input("Enter the domain (e.g., youtube): ")

# Set up the browser (using Chrome in this example)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Running Chrome in headless mode
driver = webdriver.Chrome(options=options)

base_url = f"https://www.google.com/search?q=site:{domain}.com.au"
driver.get(base_url)

all_urls = []

try:
    while True:
        # Wait for the page to load and find the search results
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

        # Extract all URLs using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for a in soup.find_all('a', href=True):
            if domain in a['href']:  # Ensuring we're getting relevant links
                all_urls.append(a['href'])

        # Click the Next button
        next_button = driver.find_element_by_id('pnnext')
        if next_button:
            next_button.click()
        else:
            # If no next button is found, break the loop
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

# Save the URLs to an Excel file
df = pd.DataFrame(all_urls, columns=['URL'])
df.to_excel("scraped_urls.xlsx", index=False)

print("URLs have been saved to 'scraped_urls.xlsx'.")
