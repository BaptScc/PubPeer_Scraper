import re

def clean_comment_text(text):
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"[^\w\s.,;:!?()%'\"/\-]", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()