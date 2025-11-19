# PubPeer Scraper: a simple extraction tool

<br>

This Git Hub repository was made to quickly retrieve and analyse PubPeer comments linked to a list of PMIDs.

Start by cloning this repository in your working environment. Please note that high performance computing is preferable to use parallelism.

<br>

```bash
git clone https://github.com/BaptScc/PubPeer_Scraper.git
cd PubPeer_Scraper
```

<br>

### How to run the main function?
---
<br>

Open the ***main.py*** script and replace the example dataset by your dataset

```bash
df = pd.read_excel("./your_dataset.xlsx")
```

Then make sure that your PMIDs are stored in a "PMID" column and in the following types: "int64" or "float64".

<br>

### What are the different options for?

<br>

This tool can return up to 3 different results:
- The number of PubPeer comments associated with a PMID (base)
- The content of the comments associated with a PMID
```bash
get_comment=True
```
- The type of comment associated with a PMID - AI-generated descriptor
```bash
sentiment_analysis=True
```
<br>

In order 
  
