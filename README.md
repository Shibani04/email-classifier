<img width="1505" height="828" alt="image" src="https://github.com/user-attachments/assets/9daafcb5-1cbd-44bc-9091-00466a38dfae" /><h1 align="center">AUTOMATED EMAIL CLASSIFICATION USING GENAI-ENHANCED MODELS</h1>
<p align="center">An intelligent AI-powered system that automatically classifies emails into 4 categories — Personal, Spam, Promotions, and Support — using Fine-tuned DistilBERT with <strong>98% accuracy</strong>.</p>

---

## PROJECT OVERVIEW

Email overload is a major challenge in modern communication. Traditional rule-based filters and basic ML models fail to understand the context and meaning behind email content, leading to misclassification.

This project implements an **AI-powered Multi-Class Email Classification System** using state-of-the-art GenAI techniques. It combines classical NLP preprocessing with transformer-based deep learning (DistilBERT) to achieve production-level accuracy. The system connects directly to live email inboxes via IMAP and classifies emails in real time through an interactive Streamlit web interface.

The project demonstrates a complete, modern NLP pipeline — from raw data collection to deployed application — integrated with GenAI capabilities.

---

## OBJECTIVES

- Preprocess email text using tokenization, stopword removal, and lemmatization.
- Combine real-world datasets for a robust and diverse training corpus.
- Fine-tune DistilBERT on the combined email dataset for contextual classification.
- Evaluate the model using confusion matrices and F1-scores.
- Integrate live email inbox access via IMAP for real-time email classification.
- Deploy the system as a professional Streamlit web application.

---

## DATASETS

Two real-world datasets were combined to build a diverse and modern training corpus:

### Dataset 1: Enron Email Corpus
- **Source:** Real corporate emails from the Enron energy company
- **Size after cleaning:** 15,027 emails
- **Columns:** file, message, clean_message, label, processed_text
- **Labels:** Generated using heuristic keyword-based classification rules
- **Why used:** Large volume of real-world unstructured email text covering corporate communication patterns

### Dataset 2: HuggingFace Email Classification Dataset (2024)
- **Source:** jason23322/high-accuracy-email-classifier on HuggingFace
- **Size:** 10,780 modern labeled emails
- **Columns:** id, subject, body, text, category, category_id
- **Why used:** Modern email patterns including newsletters, promotions, and verification emails

### Combined Dataset

| Source | Size | Type |
|---|---|---|
| Enron Corpus | 15,027 emails | Real corporate emails |
| HuggingFace 2024 | 10,780 emails | Modern labeled emails |
| **Total Combined** | **25,807 emails** | **Production-ready** |

### Final Label Distribution

```
• Personal      →  11,366 emails   (44%)
• Spam          →   6,780 emails   (26%)
• Support       →   4,979 emails   (19%)
• Promotions    →   2,682 emails   (10%)
```

> The dataset was saved in pickle format (email_combined.pkl) to ensure consistent, reproducible loading across sessions — solving real-world CSV parsing issues common with raw email text.

---

## BUILT WITH

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Seaborn-4C8CBF?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/NLTK-154F3C?style=for-the-badge&logo=python&logoColor=white"/>
</p>

---

## TEXT PREPROCESSING

The following preprocessing steps were applied to all email text — converting to lowercase, removing HTML tags, URLs, digits, punctuation, stopwords, and applying lemmatization.

**Before preprocessing:**
```
"Anniversary Special: Buy one get one free As our loyal customer..."
```

**After preprocessing:**
```
"anniversary special buy one get one free loyal customer..."
```

---

## MODEL IMPLEMENTED

### Fine-tuned DistilBERT
- **Base Model:** distilbert-base-uncased from HuggingFace
- **Task:** Sequence Classification (4 classes)
- **Training Epochs:** 3
- **Batch Size:** 32 (train and eval)
- **Max Token Length:** 128
- **Optimizer:** Default AdamW (HuggingFace Trainer)
- **Hardware:** Google Colab T4 GPU
- **Training Time:** ~685 seconds (11.4 minutes)
- **Training Samples/Second:** 90.375

#### Label Encoding
```
0 → Personal
1 → Promotions
2 → Spam
3 → Support
```

---

## COMPLETE PIPELINE

```
┌─────────────────────────────────────────────────────────────┐
│                    1. Data Loading                          │
│   Load HuggingFace 2024 dataset (10,780 emails)             │
│   Load Enron dataset from Google Drive (15,027 emails)      │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│               2. Dataset Combination                        │
│   Map HuggingFace categories to 4 labels                    │
│   Concatenate both datasets → 25,807 emails                 │
│   Save as pickle for reproducibility                        │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                 3. Text Preprocessing                       │
│   Lowercase, remove HTML, URLs, digits, punctuation         │
│   Remove stopwords (NLTK)                                   │
│   Lemmatization (WordNetLemmatizer)                         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                4. Train-Test Split                          │
│   Training: 20,645 emails (80%)                             │
│   Testing:   5,162 emails (20%)                             │
│   Strategy: Stratified (maintains class distribution)       │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│               5. DistilBERT Fine-Tuning                     │
│   Tokenize with distilbert-base-uncased tokenizer           │
│   Custom EmailDataset (PyTorch Dataset class)               │
│   HuggingFace Trainer API                                   │
│   3 epochs, batch=32, T4 GPU                                │
│   Training loss: 0.1664                                     │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   6. Evaluation                             │
│   Per-class Precision, Recall, F1-Score                     │
│   Overall Accuracy: 98%  |  Macro F1: 0.97                  │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              7. Real-Time Classification                    │
│   Live inbox via IMAP (Gmail, Outlook, Yahoo)               │
│   Subject + Body combined for best context                  │
│   Streamlit web app with confidence scores                  │
└─────────────────────────────────────────────────────────────┘
```

---

## MODEL EVALUATION

The model was evaluated using:
- Per-class Precision, Recall, F1-Score
- Overall Accuracy
- Macro and Weighted F1-Score

---

## DETAILED CLASSIFICATION REPORT

```
              precision    recall  f1-score   support

    Personal       0.98      0.99      0.99      2274
  Promotions       0.98      0.93      0.95       536
        Spam       0.97      0.97      0.97      1356
     Support       0.98      0.97      0.97       996

    accuracy                           0.98      5162
   macro avg       0.98      0.97      0.97      5162
weighted avg       0.98      0.98      0.98      5162
```

---

## WHAT THESE METRICS MEAN

| Metric | Explanation | Our Score |
|---|---|---|
| Accuracy | Overall correctness of all predictions | 98% |
| Precision | When model predicts a class, how often it is correct | 98% |
| Recall | Out of all actual emails, how many were correctly caught | 97% |
| Macro F1 | Balanced F1 across all 4 classes equally | 0.97 |
| Weighted F1 | F1 weighted by number of samples per class | 0.98 |

---

## TRAINING SUMMARY

```
• Model: DistilBERT (distilbert-base-uncased)
• Dataset Size: 25,807 Emails
• Epochs: 3
• Batch Size: 32
• Optimizer: AdamW
• Hardware: Google Colab T4 GPU
• Training Loss: 0.1664
• Accuracy: 98%
• Macro F1 Score: 0.97
```

---

## MODEL PERSISTENCE

The fine-tuned DistilBERT model and label encoder were saved for reuse without retraining:

```
models/
├── label_encoder.pkl               ← Saved using pickle
└── distilbert_finetuned/           ← Saved using HuggingFace save_pretrained()
    ├── config.json
    ├── model.safetensors
    ├── tokenizer_config.json
    └── tokenizer.json
```

---

## HOW TO RUN THE PROJECT

**Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/email-classifier.git
cd email-classifier
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Run the Streamlit App**
```bash
streamlit run streamlit_app.py
```

**Test Classifier Directly**
```bash
python app.py
```

> Gmail users: Generate an App Password from Google Account → Security → 2-Step Verification → App Passwords

---

## PROJECT STRUCTURE

```
email_classifier/
│
├── app.py                          ← Core DistilBERT classifier
├── email_reader.py                 ← IMAP live inbox fetcher
├── streamlit_app.py                ← Streamlit web application
├── requirements.txt                ← Project dependencies
├── README.md                       ← Project documentation
│
├── notebooks/
│   └── Automated_Email_Classification_Using_GenAI_Enhanced_Models.ipynb
│
└── models/
    ├── label_encoder.pkl
    └── distilbert_finetuned/
        ├── config.json
        ├── model.safetensors
        ├── tokenizer_config.json
        └── tokenizer.json
```

---

## KEY LEARNINGS

- Real-world email datasets are highly unstructured and require robust custom parsing pipelines.
- Combining multiple datasets (old Enron + modern HuggingFace 2024) significantly improves model generalization.
- Fine-tuning pre-trained transformers on domain-specific data achieves production-level results (98% accuracy).
- Saving datasets as pickle files ensures reproducibility across sessions — critical for long training workflows.
- Proper evaluation using F1-score (not just accuracy) is essential for imbalanced class distributions.
- Live system integration via IMAP demonstrates real-world deployment readiness.

---

## FUTURE IMPROVEMENTS

- Fine-tune on larger and more diverse modern email datasets
- Add multi-language email classification support
- Implement active learning for continuous model improvement
- Deploy on cloud platforms (AWS / GCP / Azure)
- Add automated email reply suggestions based on category
- Integrate Gmail OAuth API for secure authentication
- Build a REST API endpoint for enterprise integration

# APPLICATION SCREENSHOTS

## Live Inbox Classification
<img width="1527" height="826" alt="image" src="https://github.com/user-attachments/assets/1eed46cf-0aac-4244-bc66-9abf758e2a16" />


## Personal Email Classification
<img width="1512" height="816" alt="image" src="https://github.com/user-attachments/assets/78154114-abc7-41ed-87ba-8232ae33ca59" />


## Spam Email Detection
<img width="1508" height="820" alt="image" src="https://github.com/user-attachments/assets/98addc28-bc2e-46a9-ac1f-4529415c870d" />


## Context-Aware Support Classification
<img width="1505" height="828" alt="image" src="https://github.com/user-attachments/assets/a735406b-e1ca-49bc-b187-9bbb4242721e" />


