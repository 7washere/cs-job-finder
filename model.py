from transformers import T5ForSequenceClassification, T5Tokenizer
import torch 
from datasets import Dataset
from transformers import Trainer, TrainingArguments
import pdfplumber
import os 

# PLEASE USE A RESUME THAT IS IN .PDF FORMAT.

# Initialize T5 model and tokenizer
model_name = 't5-small'
model = T5ForSequenceClassification.from_pretrained(model_name, num_labels=2)
tokenizer = T5Tokenizer.from_pretrained(model_name)

def encode_text(text):
    # T5 specific encoding
    return tokenizer(
        text,
        truncation=True,
        padding='max_length',
        max_length=512,
        return_tensors='pt',
        add_special_tokens=True
    )

def analyze_resume(pdf_path):
    try:
        # Extract and preprocess text
        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text:
            raise ValueError("No text extracted from PDF")
        
        processed_text = preprocess_text(raw_text)
        # T5 expects a task prefix
        processed_text = "classify resume: " + processed_text
        inputs = encode_text(processed_text)
        
        # Get model predictions
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][prediction].item()
        
        # Enhanced feedback based on T5 analysis
        feedback = {
            0: {
                "rating": "Needs Improvement",
                "suggestions": [
                    "Add more quantifiable achievements",
                    "Include specific technical skills",
                    "Enhance project descriptions"
                ]
            },
            1: {
                "rating": "Strong Resume",
                "suggestions": [
                    "Consider adding recent certifications",
                    "Keep updating with new projects",
                    "Maintain clear formatting"
                ]
            }
        }
        
        print("\n=== T5 Resume Analysis Results ===")
        print(f"Overall Rating: {feedback[prediction]['rating']}")
        print(f"Confidence: {confidence*100:.2f}%")
        print("\nSuggestions:")
        for suggestion in feedback[prediction]['suggestions']:
            print(f"- {suggestion}")
        
        return prediction, confidence, feedback[prediction]
        
    except Exception as e:
        print(f"Error analyzing resume: {e}")
        return None

