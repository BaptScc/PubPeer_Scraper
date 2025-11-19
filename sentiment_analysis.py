import torch
from transformers import pipeline
from transformers.utils import logging

logging.set_verbosity_error() #fix topk and temp warnings

def load_package():
    labels = [
        "Questions about the study",
        "Commenting the study",
        "Discussing the methods",
        "Incoherence or discrepancies",
        "Image duplication or manipulation",
        "Ethical issues",
        "Data availability",
    ]

    pipe = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-3B-Instruct", #convenient
        dtype=torch.bfloat16,
        device_map="auto",
        pad_token_id=128001 #fix warning
    )
    return labels, pipe


# adapted from Ortega et al., 2022
def classify_comment(comment, labels, pipe):
    prompt = f"""
Classify PubPeer comments into exactly one category.

Categories:
- Questions about the study
- Commenting the study
- Discussing the methods
- Incoherence or discrepancies
- Image duplication or manipulation
- Ethical issues
- Data availability

Rules:
- Output ONLY one category.
- Use EXACT wording from the list.
- No explanation. No extra text.
- Do NOT repeat the comment.

Answer with only one label.

Comment:
{comment}

Answer:
"""
    out = pipe(prompt, max_new_tokens=10, do_sample=False)[0]["generated_text"]
    text = out.split("Answer:")[-1].strip()

    for cat in labels:
        if cat.lower() in text.lower():
            return cat

    return "error"

# comment = "The text states 65 animals but the figure shows 54."
# comment = '#1 Figure 1E and 1F, as well as supplemental table 1, show that the K-Ds of SKP1-FBXO22 binding to BACH1-BTB without and with hemin, are 124nM and 84nM, while the K-Ds of BACH1-FL without and with hemin are 44 and 29nM. However, in the text of the paper, the authors state: "Using biolayer interferometry (BLI), we determined similar affinities between FBXO22 and BACH1BTB or BACH1FL (KD 124 nM and KD 84 nM, Figures 1E and 1F; Table S1), further substantiating that the BTB domain is the sole binding site for FBXO22." Comparing just the non-hemin treated conditions, one observes that the K-Ds are 124nM for BTB only versus 44nM for the FL. This suggests that the FL form has nearly a three-fold higher affinity for FBXO22 than the BTB only. Thus, the affinities are NOT similar and perhaps the FL form of the protein harbors more binding sites to FBXO22 than just the BTB domain. Either, the figures/table are correct and the interpretation of the data is incorrect, or vice versa. Can the authors please address this discrepancy?'
# comment = "This is a very interesting study, I'm glad this has become an important topic in meta-research"
# comment = "I'd like to report some image manipulation in this study"
# print(classify_comment(comment))






