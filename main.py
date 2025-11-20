from PubPeer_Scraper.function import process_pmid_list
import pandas as pd

df = pd.read_excel("./PubPeer_Scraper/test_set.xlsx") #the fonctionnality of this pipeline has been assessed for this short dataset

result = process_pmid_list(df['PMID'],
                           get_comment=True, #Extracts the content of the comments
                           ### IMPORTANT: please request access to https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct before turning sentiment analysis on. Then pass your HF token to your working environment.
                           sentiment_analysis=True, #use LLM to analyse the nature of the comments (Commenting the study, Discussing the methods, Reporting incoherences...)
                           ### IMPORTANT: parallelism will be automatically disabled when performing sentiment analysis.
                           parallelise=False, #speed up the process (true for total number of requests >50) #Parallelism is silent.
                           num_workers=4) #number of cores that will be used for multiparallelism (depends on your machine). Stay in the range 2-8 for PubPeer.

df['Number of comments'] = [r[0] for r in result]
df['Comments'] = [r[1] for r in result]
df['Type of comments'] = [r[2] for r in result]

df.to_excel("./PubPeer_Scraper/test_set.xlsx", index=False)
