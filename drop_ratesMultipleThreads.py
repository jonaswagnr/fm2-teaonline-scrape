from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import csv
import time

def setup_initial_page(driver):
    # Navigate to the base page
    driver.get('https://www.basededatostea.xyz/')
    
    # Click the a tag with class "btn" and href="/extend"
    extend_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn[href="/extend"]'))
    )
    extend_button.click()

    # Handle cookie consent
    cookie_consent_selector = 'button[aria-label="Consent"]'  # Adjust this selector if needed
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_consent_selector))
    ).click()

    # Another consent button if present
    cookie_consent_selector_2 = 'a.btn-flat.waves-effect.waves-green.amber-text'  # Adjust this selector if needed
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_consent_selector_2))
    ).click()   
    
    time.sleep(1)  # Ensure page has loaded
    
    # Click the div tag with id="mod-5"
    mod_5_div = driver.find_element(By.ID, "mod-5")
    mod_5_div.click()
    time.sleep(1)  # Wait for any dynamic content to load

def scrape_card_data(value):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        setup_initial_page(driver)  # Execute the initial page setup for each thread
        
        card_url = f'https://www.basededatostea.xyz/extend/result/cards?card={str(value).zfill(3)}'
        driver.get(card_url)
        time.sleep(1)  # Ensure page has loaded
        
        data = []
        try:
            tbody = driver.find_element(By.CSS_SELECTOR, "div.drop-rate:nth-of-type(1) tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                text_content = [col.text for col in columns]
                if len(text_content) >= 4:
                    data.append([str(value).zfill(3)] + text_content[:4])
        except Exception as e:
            print(f"Error processing card {str(value).zfill(3)}: {str(e)}")
        return data
    finally:
        driver.quit()

def main():
    card_range = range(1, 723)  # Define the range of cards to scrape
    all_card_data = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        futures = [executor.submit(scrape_card_data, value) for value in card_range]
        for future in futures:
            all_card_data.extend(future.result())
    
    # Write collected data to a CSV file
    with open('drop_rates.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['card_id', 'opponent', 'sa-pow', 'bcd-pt', 'sa-tec'])
        writer.writerows(all_card_data)

if __name__ == "__main__":
    main()
