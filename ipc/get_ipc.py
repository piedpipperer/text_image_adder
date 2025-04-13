from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_ipc(year: int) -> float:
    base_url = "https://www.estadistica.ad/portal/apps/sites/#/estadistica-ca/pages/estadistiques-i-dades-detall"
    query_params = f"?Idioma=ca&N2=303&N3=16&DV=629&From={year}&To={year}&Var=Cap"
    url = f"{base_url}{query_params}"
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
        ipc = round(float(data_cell.text.strip().replace("%", "").replace(",", ".")), 4) / 100
    except Exception as e:
        raise Exception("❌ Something went wrong:", e)
    finally:
        driver.quit()
    return ipc


def calculate_compound_interest(year1: int, year2: int) -> float:
    compound_interest = round(100 * (1 + get_ipc(year1)) * (1 + get_ipc(year2)) - 100, 4)
    return compound_interest


if __name__ == "__main__":
    year1 = 2023
    year2 = 2024
    print(f"Compound interest from {year1} to {year2}: {calculate_compound_interest(year1, year2)}%")
