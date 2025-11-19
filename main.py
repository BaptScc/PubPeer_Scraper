from PubPeer_Scraper.function import process_pmid_list
from PubPeer_Scraper.driver import get_driver

driver=get_driver()

import pandas as pd

# pmid_list = ["37781291", "26808342", "25412939"] 

df = pd.read_excel("./integrity_experts.xlsx")

df = df[-100:]

result = process_pmid_list(df['PMID'], parallelise=True, num_workers=4)

df['has_pub_peer_comment'] = result
df[df['has_pub_peer_comment'] > 0]

driver.quit()

