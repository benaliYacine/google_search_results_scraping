from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def extract_google_urls(domain):
    # Start a new instance of Chrome in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    # Note: You'll need to have the chromedriver executable in your PATH or specify its location.
    driver = webdriver.Chrome(options=options)
    
    base_url = f"https://www.google.com/search?q=site:{domain}.com.au"
    driver.get(base_url)
    
    urls = []
    
    while True:
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Find all anchor tags
        for a in soup.find_all("a"):
            href = a.get('href')
            if href and (href.startswith("http://") or href.startswith("https://")):
                urls.append(href)
        
        # Try to click on the "Next" button
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "pnnext"))
            )
            next_button.click()
        except:
            break
    
    driver.quit()
    
    # Save URLs to Excel
    df = pd.DataFrame(urls, columns=['URL'])
    df.to_excel("urls.xlsx", index=False)

if __name__ == "__main__":
    domain = input("Enter the domain (without .com.au): ")
    extract_google_urls(domain)
    print("URLs saved to urls.xlsx")
