from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import re  # Import regular expressions to extract numbers

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
    
# Adding a short delay to ensure the page loads correctly
time.sleep(1)
    
# 3. Click the div tag with id="mod-5"
mod_5_div = driver.find_element(By.ID, "mod-5")
mod_5_div.click()
    






try:
    # Initialize the list to store card data
    card_data = []

    # Loop through the card values '001' to '006'
    for value in range(1, 723):
        # Navigate to the URL for each card
        card_url = f'https://www.basededatostea.xyz/extend/result/cards?card={str(value).zfill(3)}'
        driver.get(card_url)

        # Extract data based on the new requirements
        card_name = driver.find_element(By.CSS_SELECTOR, "h1.main-card-name").text

        stats_text_element = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(2)")
        stats_text = stats_text_element.text

        # Initialize atk and dfd to 0 by default
        atk, dfd = 0, 0

        # Check if stats_text is not empty
        if stats_text:
            extracted_numbers = re.findall(r'\d+', stats_text)
            if len(extracted_numbers) >= 2:
                # If at least two numbers are found, extract the first two as ATK and DFD
                atk, dfd = map(int, extracted_numbers[:2])
            # No need for an else here since atk, dfd are already initialized to 0
        else:
            # If stats_text is empty, atk and dfd remain 0
            pass
        
        guardian_stars = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(3)").text.split(' | ')
        guardian_star1, guardian_star2 = guardian_stars if len(guardian_stars) == 2 else ("N/A", "N/A")
        
        type_ = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(4)").text
        starchips = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(5)").text
        password = driver.find_element(By.CSS_SELECTOR, "div.col.s12.l6.izquierda.result-data-card.centrado > div > p:nth-child(6)").text

        card_data.append([str(value).zfill(3), card_name, atk, dfd, guardian_star1, guardian_star2, type_, starchips, password])

finally:
    # Close the driver
    driver.quit()

# Write the collected data to a CSV file
with open('card_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the column headers
    writer.writerow(['card_id', 'card_name', 'atk', 'dfd', 'guardian_star1', 'guardian_star2', 'type', 'starchips', 'password'])
    # Write the rows of data
    writer.writerows(card_data)