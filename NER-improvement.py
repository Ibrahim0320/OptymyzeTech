# Correcting the mistakes the NER makes and retraining

import spacy
from spacy.training.example import Example
from spacy.tokens import DocBin
import random

# Corrected Data Annotations
train_data = [
    ("MUHAMMAD IBRAHIM M.Sc. in Applied Data Science Email: ibrahim.muhammad02@outlook.com LinkedIn: linkedin.com/in/muhibrahim7 Github: github.com/ibrahim0320", 
     {"entities": [(0, 15, "PERSON"), (17, 42, "DEGREE"), (50, 81, "EMAIL"), (91, 122, "URL"), (131, 154, "URL")]}),
    ("CAREER SUMMARY: I am an incoming Masters student within the field of data science with a profound passion for machine learning, artificial intelligence, and data analytics. Combined with a background in engineering physics, I am committed to enhancing my skills and knowledge in this field with the aim of making a meaningful impact in the industry.", 
     {"entities": [(22, 29, "DEGREE")]}),
    ("Optymyze Technologies Tech Consulting Coastal Combat Engineer | July, 2023 - December, 2023", 
     {"entities": [(0, 30, "ORG"), (31, 50, "TITLE"), (53, 58, "DATE"), (60, 64, "DATE"), (67, 76, "DATE")]}),
    # Add more corrected examples
]



# Load pretrained transformer model
nlp = spacy.blank("en")
transformer = nlp.add_pipe("transformer")
ner = nlp.add_pipe("ner")

# Add labels to the NER component
for label in ["PERSON", "ORG", "GPE", "DATE", "PRODUCT", "LANGUAGE", "NORP", "CARDINAL", "ORDINAL"]:
    ner.add_label(label)



# Convert to spaCy's format
examples = []
for text, annotations in train_data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
    examples.append(example)

# Train the model
nlp.begin_training()
for itn in range(20):
    random.shuffle(examples)
    for example in examples:
        nlp.update([example])

# Save the trained model
nlp.to_disk("Improved_ner_model")

# Test the model
nlp = spacy.load("trained_ner_model")
doc = nlp("Your test text here")
for ent in doc.ents:
    print(ent.text, ent.label_)
