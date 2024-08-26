from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import concurrent.futures
import time
import csv
import re




def fetch_card_data(value):
    # Initialize the WebDriver for the current thread
   # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 1. Navigate to the page

    driver.get('https://www.basededatostea.xyz/')
    
    # 2. Click the a tag with class "btn" and href="/extend"
    extend_button = driver.find_element(By.CSS_SELECTOR, 'a.btn[href="/extend"]')
    extend_button.click()

    cookie_consent_selector = 'button[aria-label="Consent"]' # Example selector, adjust as needed
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_consent_selector))
    ).click()

    cookie_consent_selector = 'a.btn-flat.waves-effect.waves-green.amber-text'
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_consent_selector))
    ).click()   
    try:
        card_url = f'https://www.basededatostea.xyz/extend/result/cards?card={str(value).zfill(3)}'
        driver.get(card_url)
        
        # Extract data based on the new requirements
        card_name = driver.find_element(By.CSS_SELECTOR, "h1.main-card-name").text
        stats_text = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(2)").text
        atk, dfd = re.findall(r'\d+', stats_text)[:2]
        
        guardian_stars = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(3)").text.split(' | ')
        guardian_star1, guardian_star2 = guardian_stars if len(guardian_stars) == 2 else ("N/A", "N/A")
        
        type_ = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(4)").text
        starchips = re.search(r'\d+', driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(5)").text).group()
        password = re.search(r'\d+', driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(6)").text).group()

        return [str(value).zfill(3), card_name, atk, dfd, guardian_star1, guardian_star2, type_, starchips, password]
    finally:
        driver.quit()

# The main block
if __name__ == "__main__":
    card_data = []
    # Use ThreadPoolExecutor to create a pool of threads for concurrent execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Schedule the fetch_card_data function to be executed for each card value
        future_to_value = {executor.submit(fetch_card_data, value): value for value in range(1, 723)}
        
        for future in concurrent.futures.as_completed(future_to_value):
            try:
                data = future.result()
                card_data.append(data)
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    
    # After collecting all data, write it to a CSV file
    with open('card_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['card_id', 'card_name', 'atk', 'dfd', 'guardian_star1', 'guardian_star2', 'type', 'starchips', 'password'])
        writer.writerows(card_data)
