from PubPeer_Scraper.function import get_pubpeer_comment_number
from PubPeer_Scraper.driver import get_driver

driver=get_driver()

pmid_list = ["37781291", "26808342", "25412939"] 

for pmid in pmid_list: 
    get_pubpeer_comment_number(pmid, driver)

driver.quit()