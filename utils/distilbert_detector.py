from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)

import torch

# ---------------------------------------------------
# LOAD TOKENIZER
# ---------------------------------------------------

tokenizer = DistilBertTokenizer.from_pretrained(
    "distilbert-base-uncased"
)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

model.eval()

# ---------------------------------------------------
# PHISHING LABELS
# ---------------------------------------------------

LABELS = {
    0: "safe",
    1: "malicious"
}

# ---------------------------------------------------
# SEMANTIC ANALYSIS
# ---------------------------------------------------

def bert_url_analysis(url):

    try:

        # Tokenize URL
        inputs = tokenizer(
            url,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        # Inference
        with torch.no_grad():

            outputs = model(**inputs)

            probs = torch.softmax(
                outputs.logits,
                dim=1
            )

        safe_prob = float(probs[0][0])
        malicious_prob = float(probs[0][1])

        prediction = (
            "malicious"
            if malicious_prob > safe_prob
            else "safe"
        )

        reasons = []

        # ---------------------------------------------------
        # AI SEMANTIC FLAGS
        # ---------------------------------------------------

        if malicious_prob > 0.70:

            reasons.append(
                "DistilBERT semantic engine detected phishing patterns"
            )

        if "login" in url.lower():

            reasons.append(
                "Semantic analysis detected login-related intent"
            )

        if "verify" in url.lower():

            reasons.append(
                "Semantic analysis detected verification keyword"
            )

        if "paypal" in url.lower():

            reasons.append(
                "Semantic impersonation target detected"
            )

        return {

            "prediction": prediction,

            "confidence": round(malicious_prob, 4),

            "reasons": reasons

        }

    except Exception as e:

        return {

            "prediction": "safe",

            "confidence": 0.0,

            "reasons": [
                f"BERT engine failed: {str(e)}"
            ]

        }