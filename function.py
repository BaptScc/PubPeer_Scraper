from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from multiprocessing import Pool
from tqdm import tqdm
import re
from PubPeer_Scraper.driver import get_driver

def get_pubpeer_comment_number(pmid, driver):

    url = f"https://pubpeer.com/search?q={pmid}"

    driver.get(url)

    try: 

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
    
    except TimeoutException:
        print(f"No result for PMID: {pmid}")
        return 0
    
    except Exception:
        print(f"Error for PMID: {pmid} - code: {Exception}")
        return 0


def worker(pmid):
    driver = get_driver()
    result = get_pubpeer_comment_number(pmid, driver)
    driver.quit()
    return result

def process_pmid_list(pmids, parallelise=False, num_workers=2):

    if parallelise == True:  

        print("Parallel processing")
        with Pool(processes=num_workers) as p:
            result_list = list(tqdm(
                p.imap(worker, pmids),
                total=len(pmids)
            ))

        return result_list
    
    else:
        print("Sequential processing")
        driver = get_driver()
        result_list = []

        for pmid in tqdm(pmids):

            result = get_pubpeer_comment_number(pmid, driver)
            print(f"Article PMID: {pmid} --- Number of comments: {result}")
            result_list.append(result)
            
        return result_list