from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def discover_targets(url):
    # Path to your chromedriver.exe
    service = Service(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in the background
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        forms = soup.find_all('form')
        print(f"Found {len(links)} links and {len(forms)} forms.")
        return links, forms
    finally:
        driver.quit()