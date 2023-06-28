from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def click_text_in_browser(url, text_to_click):
    chrome_options = Options()
    # Configure Selenium webdriver (You may need to download the appropriate driver for your browser)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Navigate to the provided URL
    driver.get(url)

    # Get the page source
    page_source = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the element containing the desired text
    element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text_to_click}')]")
    element.click()

    # Close the browser
    driver.quit()
