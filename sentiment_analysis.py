import torch
from transformers import pipeline
from transformers.utils import logging

logging.set_verbosity_error() #fix topk and temp warnings

def load_package():
    labels = [
        "Commenting or discussing the study",
        "Logical problem",
        "Image problem",
        "Ethical issues",
        "Data availability",
    ]

    pipe = pipeline(
        "text-generation",
        #model="meta-llama/Llama-3.2-3B-Instruct", #convenient
        model="meta-llama/Llama-3.1-8B-Instruct", #more performant
        dtype=torch.bfloat16,
        device_map="auto",
        pad_token_id=128001 #fix warning
    )
    return labels, pipe


# adapted from Ortega et al., 2022
def classify_comment(comment: str, labels, pipe):
    prompt = f"""
You are a classifier of PubPeer comments. Your task is to assign EXACTLY ONE label to the comment.

Valid labels (use EXACT wording):
1. Commenting or discussing the study
2. Logical problem
3. Image problem
4. Ethical issues
5. Data availability

DEFINITIONS (READ CAREFULLY):

- Commenting or discussing the study:
  General discussion, interpretation, questions or opinions about the study, its results, methods or implications.
  No specific claim of an error, no clear image issue, no ethical concern, and no request for underlying data.

- Logical problem:
  Problems in methods, numbers, statistics, experimental design, or interpretation.
  Examples: inconsistencies between figures and text, wrong sample sizes, impossible values, incorrect conclusions.
  NOT primarily about duplicated images, suspicious western blots or re-used panels. If the main issue is about images, DO NOT choose this label.

- Image problem:
  Concerns about duplicated panels, overlapping figures, duplicated western blots, re-used xenograft photos, suspicious similarities between images, or reuse of images in different papers.
  This includes retraction notices when the reason is duplicated images or image manipulation.
  If both "Logical problem" and "Image problem" could apply, ALWAYS choose "Image problem".

- Ethical issues:
  Concerns about ethics approval, consent, animal welfare, patient safety, or scientific misconduct that is not specifically about images or data availability.

- Data availability:
  Concerns about missing datasets, raw data not provided, inability to reproduce the work because data are unavailable, or explicit requests to share underlying data, raw gels, blots or images.
  Example triggers: "upload scans of the original gels", "provide raw data", "can you share the original blots?".

PRIORITY RULES:
- If the main concern involves duplicated or suspicious figures, blots, panels, rulers or images, choose "Image problem" even if the text also mentions errors, retraction or logical issues.
- If the main concern is a request for raw data, raw gels/blots, or underlying datasets, choose "Data availability".
- Otherwise, if the main concern is about numbers, methods, or logic, choose "Logical problem".

EXAMPLES:

Example 1
Comment:
"Is it possible for the authors to upload or link to scans of the original gels for these Western Blots?"
Correct label: Data availability

Example 2
Comment:
"Fig 4A. Two panels overlap despite different descriptions. Could the authors check?"
Correct label: Image problem

Example 3
Comment:
"Figure 1E shows 54 animals but the text states 65 animals. The statistics are reported as if n=65."
Correct label: Logical problem

RULES FOR OUTPUT:
- Your answer MUST be exactly one of the five labels above.
- The FIRST line of your answer must be exactly the chosen label, with no quotes and no extra text.
- Do NOT repeat or summarize the comment.
- Do NOT add explanations or additional lines.

Comment:
{comment}

Answer:
"""

    out = pipe(prompt, max_new_tokens=8, do_sample=False)[0]["generated_text"]
    text = out.split("Answer:")[-1].strip()

    first_line = text.splitlines()[0].strip()

    for cat in labels:
        if first_line == cat:
            return cat

    for cat in labels:
        if first_line.lower() == cat.lower():
            return cat

    for cat in labels:
        if cat.lower() in first_line.lower():
            return cat

    return "error"

# comment = "The text states 65 animals but the figure shows 54."
# comment = '#1 Figure 1E and 1F, as well as supplemental table 1, show that the K-Ds of SKP1-FBXO22 binding to BACH1-BTB without and with hemin, are 124nM and 84nM, while the K-Ds of BACH1-FL without and with hemin are 44 and 29nM. However, in the text of the paper, the authors state: "Using biolayer interferometry (BLI), we determined similar affinities between FBXO22 and BACH1BTB or BACH1FL (KD 124 nM and KD 84 nM, Figures 1E and 1F; Table S1), further substantiating that the BTB domain is the sole binding site for FBXO22." Comparing just the non-hemin treated conditions, one observes that the K-Ds are 124nM for BTB only versus 44nM for the FL. This suggests that the FL form has nearly a three-fold higher affinity for FBXO22 than the BTB only. Thus, the affinities are NOT similar and perhaps the FL form of the protein harbors more binding sites to FBXO22 than just the BTB domain. Either, the figures/table are correct and the interpretation of the data is incorrect, or vice versa. Can the authors please address this discrepancy?'
# comment = "This is a very interesting study, I'm glad this has become an important topic in meta-research"
# comment = "I'd like to report some image manipulation in this study"
# print(classify_comment(comment))






