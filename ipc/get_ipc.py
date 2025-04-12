from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_ipc(year):
    url = f"https://www.estadistica.ad/portal/apps/sites/#/estadistica-ca/pages/estadistiques-i-dades-detall?Idioma=ca&N2=303&N3=16&DV=629&From={year}&To={year}&Var=Cap"
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        # Wait for JavaScript to build the page (important!)
        time.sleep(10)
        # Try to find the iframe now
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "iframeContent")))
        # Switch to the iframe
        driver.switch_to.frame("iframeContent")
        # Find the information table
        data_cell = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'td.tdDatos[data-field="A_{year}"]'))
        )
        ipc = float(data_cell.text.strip().replace("%", "").replace(",", ".")) / 100
    except Exception as e:
        print("❌ Something went wrong:", e)
        ipc = None
    finally:
        driver.quit()
    return ipc


get_ipc(2023)


def calculate_compound_interest(year1, year2):
    compound_interest = 100 * (1 + get_ipc(year1)) * (1 + get_ipc(year2)) - 100
    return compound_interest


calculate_compound_interest(2023, 2024)
