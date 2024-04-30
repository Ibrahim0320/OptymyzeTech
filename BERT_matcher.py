# Attempting to use a BERT matcher for the CV matching

import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

def load_model_and_tokenizer(model_name='bert-base-uncased'):
    """
    Load BERT tokenizer and model.
    """
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    return tokenizer, model


def encode_text(tokenizer, model, text):
    """
    Encode the text into a BERT embedding.
    """
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    outputs = model(**inputs)
    # Get the mean of the last hidden state to represent the document
    # Ensure output is a 1D array
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()



def BERT():
    # Load model and tokenizer
    tokenizer, model = load_model_and_tokenizer()

    # Example texts
    job_description = "Experienced software engineer with expertise in Python and machine learning."
    cv_text = "Software developer with extensive experience in developing machine learning applications using Python."

    # Encode texts
    job_embed = encode_text(tokenizer, model, job_description)
    cv_embed = encode_text(tokenizer, model, cv_text)

    # Calculate similarity
    similarity = cosine_similarity([job_embed], [cv_embed])
    print(f"Cosine Similarity: {similarity[0][0]}")

BERT()





