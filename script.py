from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Step 1: Navigate to the page
driver.get('https://www.basededatostea.xyz/home')

# Wait and click the cookie consent button
# Adjust the selector below to match the cookie consent button on the website
cookie_consent_selector = 'button[aria-label="Consent"]' # Example selector, adjust as needed
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_consent_selector))
).click()

cookie_consent_selector = 'a.btn-flat.waves-effect.waves-green.amber-text'
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_consent_selector))
).click()


mod_15_btn = 'div.hide-on-med-and-down:nth-child(6)'
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, mod_15_btn))
).click()


# Step 2: Insert value into the input tag
# Insert '713' into the input tag with the class "input-def"
input_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'input-def'))
)
input_element.send_keys('713' + Keys.ENTER)

# Step 3: Click the button
click_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn.btn-flat.waves-effect.waves-yellow.transparent.izquierda'))
)
click_element.click()

# Step 4: Wait for the redirect to the new page
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

# Step 5: Extract all table tags with its contents
tables = driver.find_elements(By.TAG_NAME, 'table')

for table in tables:
    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, 'tr')
    
    for row in rows:
        # Find all cells within the row
        cells = row.find_elements(By.TAG_NAME, 'td')  # Use 'th' if you also want to include headers
        
        # Extract the text from each cell and combine it, separated by a space or other preferred delimiter
        row_text = ' '.join([cell.text for cell in cells])
        
        # Now you have the text content of the row, you can print it or store it as needed
        print(row_text)

# Don't forget to close the driver after your script is done
driver.quit()

