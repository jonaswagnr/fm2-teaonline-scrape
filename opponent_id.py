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
    for value in range(1, 40):
        # Navigate to the URL for each card
        card_url = f'https://www.basededatostea.xyz/extend/result/opponents?opponent={str(value)}'
        driver.get(card_url)

        # Extract data based on the new requirements
        opponent_name = driver.find_element(By.CSS_SELECTOR, "h2.izquierda").text

        card_data.append([str(value), opponent_name])

finally:
    # Close the driver
    driver.quit()

# Write the collected data to a CSV file
with open('opponent_id.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the column headers
    writer.writerow(['copponent_id', 'opponent_name'])
    # Write the rows of data
    writer.writerows(card_data)