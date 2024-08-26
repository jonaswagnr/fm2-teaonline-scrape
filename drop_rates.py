from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

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
    for value in range(369, 393):
        # Navigate to the URL for each card
        card_url = f'https://www.basededatostea.xyz/extend/result/cards?card={str(value).zfill(3)}'
        driver.get(card_url)
        
    

        # Target the tbody within the first div with class "drop-rate"
        try:
            # Use CSS selector to find the tbody inside the first "drop-rate" div
            tbody = driver.find_element(By.CSS_SELECTOR, "div.drop-rate:nth-of-type(1) tbody")
            # Extract all rows from the tbody
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            # Process each row to extract and store data
            for row in rows:
                # Splitting row text into columns
                columns = row.find_elements(By.TAG_NAME, "td")
                text_content = [col.text for col in columns]
                if len(text_content) >= 4:
                    # Assuming the pattern matches the columns: opponent, sa-pow, bcd-pt, sa-tec
                    card_data.append([str(value).zfill(3)] + text_content[:4])
        except Exception as e:
            print(f"Error processing card {str(value).zfill(3)}: {str(e)}")

finally:
    # Close the driver
    driver.quit()

# Write the collected data to a CSV file
with open('drop_rates.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the column headers
    writer.writerow(['card_id', 'opponent', 'sa-pow', 'bcd-pt', 'sa-tec'])
    # Write the rows of data
    writer.writerows(card_data)