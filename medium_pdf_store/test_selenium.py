from selenium import webdriver
import base64
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# ⚡ Connect to the running Chrome with remote debugging
debugger_address = "127.0.0.1:9222"

chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = debugger_address

driver = webdriver.Chrome(options=chrome_options)

url = "https://medium.com/@optimzationking2/cover-letters-are-dead-heres-what-recruiters-want-instead-afc1048e70fe"
output = f"/home/jrojo/Dropbox/useful_mediums/{datetime.now().year}/cover-letters-are-dead-heres-what-recruiters-want-instead.pdf"

try:
    driver.get(url)

    # Wait for the main content to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "article"))
    )

    time.sleep(2)  # extra render buffer

    # Print page to PDF via DevTools
    print_options = {
        "printBackground": True,
        "landscape": False,
        "paperWidth": 8.27,   # A4
        "paperHeight": 11.69,
    }
    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

    # Save file
    pdf_data = base64.b64decode(result["data"])
    with open(output, "wb") as f:
        f.write(pdf_data)

    print(f"✅ PDF saved: {output}")

finally:
    driver.quit()