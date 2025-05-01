from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch 
from datasets import Dataset
from transformers import Trainer, TrainingArguments
import pdfplumber

# PLEASE USE A RESUME THAT IS IN .PDF FORMAT.


model_name = 'distilbert-base-uncased'
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=2)  # For binary classification (good/bad)
tokenizer = DistilBertTokenizer.from_pretrained(model_name) 

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text