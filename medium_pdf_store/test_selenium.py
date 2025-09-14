from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime 
import base64

# Path to your Chrome profile (Google login persists)
chrome_profile = "/home/jrojo/.config/google-chrome/Default"  # Linux example

# chrome_profile = "/home/jrojo/.config/google-chrome"  # parent folder of profiles


options = Options()
options.add_argument(f"--user-data-dir={chrome_profile}")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# options.add_argument("--headless")  # comment out first to see browser

driver = webdriver.Chrome(options=options)
# for cookie in cookies:
#     driver.add_cookie(cookie)

url = "https://medium.com/@optimzationking2/cover-letters-are-dead-heres-what-recruiters-want-instead-afc1048e70fe"
output = f"/home/jrojo/Dropbox/useful_mediums/{datetime.now().year}/cover-letters-are-dead-heres-what-recruiters-want-instead.pdf"


try:
    # url = "https://medium.com/some-paid-article"
    driver.get(url)

    # Wait for the main content to load (adjust selector if needed)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "article"))
    )

    time.sleep(2)  # give it a moment to fully render

    # Save as PDF using Chrome DevTools command
    print_options = {
        'printBackground': True,
        'landscape': False,
        'paperWidth': 8.27,   # A4 size
        'paperHeight': 11.69
    }
    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

    # Save the PDF
    pdf_data = base64.b64decode(result['data'])
    with open(output, "wb") as f:
        f.write(pdf_data)
    
    print("✅ PDF saved!")

finally:
    driver.quit()