from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from multiprocessing import Pool
from tqdm import tqdm
import re
from PubPeer_Scraper.driver import get_driver
from PubPeer_Scraper.text_cleaner import clean_comment_text
from PubPeer_Scraper.sentiment_analysis import classify_comment, load_package

def get_pubpeer_comment_number(pmid, driver, get_comment=True, sentiment_analysis=False, labels = None, pipe=None):

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

        if get_comment == True and count !=0:
            link = soup.select_one("a[href^='/publications/']")
            pubpeer_link = link["href"] if link else None

            if pubpeer_link is None: #safer
                return count, ""

            comment_url = f"https://pubpeer.com{pubpeer_link}"

            comments = get_pubpeer_comment(comment_url, driver)

            if sentiment_analysis == True:

                comment_type = classify_comment(comments, labels, pipe)

            else:

                comment_type = ""

            return count, comments, comment_type
        
        elif get_comment == True and count ==0:
            comments = ""
            comment_type = ""
            return count, comments, comment_type  

        return count, "", ""
    
    except TimeoutException:
        print(f"No result for PMID: {pmid}")
        if get_comment == True:
            return 0, "", ""
        else:
            return 0, "", ""
    
    except Exception as e:
        print(f"Error for PMID: {pmid} - code: {e}")
        if get_comment == True:
            return 0, "", ""
        else:
            return 0, "", ""


def get_pubpeer_comment(comment_url, driver):
    driver.get(comment_url)

    try:

        WebDriverWait(driver, 20).until(
            lambda d: "vertical-timeline-block" in d.page_source
                      or "There are currently no comments" in d.page_source
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        all_comments = []


        blocks = soup.select("div.vertical-timeline-block")

        if not blocks:
            return ""

        for block in blocks:

            id_tag = block.select_one("strong.inner-id")
            if not id_tag:
                continue

            comment_id = id_tag.get_text(strip=True)

            content_div = block.select_one("div.ibox-content")
            if not content_div:
                continue

            for trash in content_div.select("div.comment-footer, a[href], img"):
                trash.decompose()

            comment_text = content_div.get_text(separator=" ", strip=True)
            if not comment_text:
                continue

            cleaned = clean_comment_text(comment_text)

            entry = f"{comment_id} {cleaned}"
            all_comments.append(entry)

        return "\n\n".join(all_comments)

    except TimeoutException:
        print(f"Timeout loading comment page: {comment_url}")
        return ""

    except Exception as e:
        print(f"Error extracting comments from {comment_url}: {e}")
        return ""


def worker(args):
    pmid, get_comment, sentiment_analysis, labels, pipe = args
    driver = get_driver()
    result = get_pubpeer_comment_number(pmid, driver, get_comment, sentiment_analysis, labels, pipe)
    driver.quit()
    return result



def process_pmid_list(pmids, parallelise=False, num_workers=2, get_comment=True, sentiment_analysis=False):

    if sentiment_analysis == True:
        labels, pipe = load_package()
    else:
        labels, pipe = None, None

    if parallelise and sentiment_analysis == True:
        print("Warning: switched back to sequential processing")

    if parallelise and sentiment_analysis == False:
        print("Parallel processing")

        with Pool(processes=num_workers) as p:
            args = [(pmid, get_comment, sentiment_analysis, labels, pipe) for pmid in pmids]
            result_list = list(tqdm(p.imap(worker, args), total=len(pmids)))

        return result_list

    else:
        print("Sequential processing")

        driver = get_driver()
        result_list = []

        for pmid in tqdm(pmids):
            count, comments, comment_type = get_pubpeer_comment_number(
                pmid, driver, get_comment, sentiment_analysis, labels, pipe
            )

            print(f"Article PMID: {pmid} --- Number of comments: {count}")

            if get_comment:
                print(f"Comments:\n{comments}")

            if sentiment_analysis:
                print(f"Comment type: {comment_type}")

            result_list.append((count, comments, comment_type))

        driver.quit()
        return result_list