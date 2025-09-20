import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_articles(selenium_driver, url: str = "https://medium.com/@jordirojo/list/best-34d13e8e2c33") -> list:

    # Go to your Medium reading list
    selenium_driver.get(url)

    # Wait for article links to appear
    WebDriverWait(selenium_driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
    )

    # Collect unique article URLs
    links = selenium_driver.find_elements(By.CSS_SELECTOR, "a")
    article_urls = set(
        link.get_attribute("href") for link in links
        if link.get_attribute("href") # and "/p/" in link.get_attribute("href")
    )

    # Regex: article URLs always end with -<hexid> or contain /p/<id>
    article_pattern = re.compile(r"(medium\.com/.+?-([0-9a-f]{8,}))|(medium\.com/p/[0-9a-f]+)")

    final_url_arts =  []
    for a in article_urls:
        href = a.split("?")[0]  # strip tracking params
        if article_pattern.search(href):
            final_url_arts.append(href)

    # print("Found articles:")
    # for url in article_urls:
    #     print(url)

    return final_url_arts