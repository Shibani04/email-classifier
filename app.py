from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pickle
import re

# Load model
model_path = "models/distilbert_finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
le = pickle.load(open("models/label_encoder.pkl", "rb"))

def clean_text(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:256]

def classify_email(email_text, sender="", subject=""):
    combined = f"{subject} {email_text}"
    cleaned = clean_text(combined)

    inputs = tokenizer(
        cleaned,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    with torch.no_grad():
        outputs = model(**inputs)

    pred = torch.argmax(outputs.logits, dim=1).item()
    confidence = torch.softmax(outputs.logits, dim=1).max().item() * 100
    category = le.inverse_transform([pred])[0]

    return category, confidence