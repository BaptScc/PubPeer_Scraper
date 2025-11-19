# PubPeer Scraper: a simple extraction tool
---
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

<br>

```bash
df = pd.read_excel("./your_dataset.xlsx")
```

<br>

Then make sure that your PMIDs are stored in a "PMID" column and in the following types: "int64" or "float64".

<br>

### What are the different options for?
---
<br>

This tool can return up to 3 different results:
- The number of PubPeer comments associated with a PMID (base)
- The content of the comments associated with a PMID

<br>
  
```bash
get_comment=True #or get_comment=False
```

<br>

- The type of comment associated with a PMID - AI-generated descriptor

<br>

```bash
sentiment_analysis=True #or sentiment_analysis=False
```
<br>

You can switch these options on depending on what you need. Please note that ***sentiment_analysis*** can't be used with ***get_comment*** turned off. Turning the ***sentiment_analysis*** on will trigger the download of Llama-3.1-8B from Hugging Face. Please make sure that you have requested access to https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct and passed your HF token on your machine beforehand.

<br>

### How to parallelise?
---
<br>

Multiprocessing was added to the main function to enable faster retrieval of the PubPeer comments (up to 400 per minute). The number of workers can be adapted (2 to 8). Please note that parallelism will be automatically disabled when performing sentiment analysis.

<br>

```bash
parallelise=True #or parallelise=False (default)
num_workers=4 #recommended
```
<br>

---
<br>

If any question please reach out to baptiste.scancar@agrocampus-ouest.fr
