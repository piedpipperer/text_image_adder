from selenium import webdriver
import base64
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.chrome.service import Service
import re
from pathlib import Path
from medium_pdf_store.selenium.find_articles import get_articles

import platform

if platform.system() == "Windows":
    BASE_FOLDER = Path("C:/Users/Usuario/Dropbox/useful_mediums/")
else:
    BASE_FOLDER = Path("/home/jrojo/Dropbox/useful_mediums/")

# new root ->
# C:\Users\Usuario\Dropbox\useful_mediums


# # ⚡ Connect to the running Chrome with remote debugging
debugger_address = "127.0.0.1:9222"
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = debugger_address

# if platform.system() == "Windows":
# Specify the path to chromedriver.exe if it's not in your PATH
# chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
driver = webdriver.Chrome(
    options=chrome_options, service=Service("C:\\Users\\Usuario\\Documents\\chromedriver-win64\\chromedriver.exe")
)

# best list:
# original_article_urls = [url for url in get_articles(driver) if url.startswith("https://medium.com/")]

# in case is the pending list:
original_article_urls = [
    url
    for url in get_articles(driver, url="https://medium.com/@jordirojo/list/pending-2edc05a5e029")
    if url.startswith("https://medium.com/")
]


# remove the author if applies:
article_names = [
    re.sub(r"^@[^/]+/", "", url.replace("https://medium.com/", "")) for url in original_article_urls
]  # Remove author prefix

# remove the hexadecimal coding at the end.
article_names = [re.sub(r"-[0-9a-f]{12}$", "", url) for url in article_names]  # Remove hexadecimal word at the end

# in addition to this regex. we need also to remove any character that might not be accepted as for a file name:
article_names = [
    re.sub(r'[<>:"/\\|?*]+', "_", name) for name in article_names
]  # Replace invalid characters with underscore


for art_index, url in enumerate(original_article_urls):
    file_name = f"{article_names[art_index]}.pdf"
    output = BASE_FOLDER / f"{datetime.now().year}/{file_name}"

    # Check if the output already exists in the base folder and its subfolders, and skip this iteration if it does
    if bool(next(BASE_FOLDER.rglob(file_name), None)):
        print(
            f"""⚠️ PDF already exists in : {BASE_FOLDER}, 
              with this particular name: {file_name}
              Skipping..."""
        )
        continue

    try:
        driver.get(url)

        # Wait for the main content to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "article")))

        time.sleep(2)  # extra render buffer

        # Print page to PDF via DevTools
        print_options = {
            "printBackground": True,
            "landscape": False,
            "paperWidth": 8.27,  # A4
            "paperHeight": 11.69,
        }
        result = driver.execute_cdp_cmd("Page.printToPDF", print_options)

        # Save file
        pdf_data = base64.b64decode(result["data"])
        with open(output, "wb") as f:
            f.write(pdf_data)

        print(f"✅ PDF saved: {output}")
    except:
        print(f"❌ Error processing {url}. Skipping...")
        continue

driver.quit()
