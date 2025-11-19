from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

def get_pubpeer_comment_number(pmid, driver):

    url = f"https://pubpeer.com/search?q={pmid}"

    driver.get(url)

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/publications']")))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    footer = soup.find("div", class_="panel-footer")
    span = footer.find("span", class_="pull-right") if footer else None

    if not span:
        count = 0
    else:
        text = span.get_text(strip=True).lower()
        m = re.search(r"(\d+)\s*comment", text)
        count = int(m.group(1)) if m else 0

    return count

