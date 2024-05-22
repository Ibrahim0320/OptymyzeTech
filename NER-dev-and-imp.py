'''NER Development

import spacy
import pickle
import random
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from spacy.training.example import Example
import sys, fitz


nlp = spacy.blank('en')

train_data = pickle.load(open('/Users/muhammadibrahim/Downloads/train_data.pkl', 'rb'))

def train_model(nlp, train_data):
    # Check if the NER component is already in the pipeline
    if 'ner' not in nlp.pipe_names:
        ner = nlp.add_pipe('ner', last=True)
    else:
        ner = nlp.get_pipe('ner')

    # Add labels to the NER component
    for _, annotations in train_data:
        for ent in annotations['entities']:
            ner.add_label(ent[2])

    # Disable other pipelines
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()

        for epoch in range(10):
            print(f"Iteration {epoch} starting...")
            random.shuffle(train_data)
            losses = {}

            for text, annotations in train_data:
                try:
                    example = Example.from_dict(nlp.make_doc(text), annotations)
                    nlp.update([example], drop=0.5, losses=losses, sgd=optimizer)
                except Exception as e:
                    pass

            print(losses)

# Train the model
train_model(nlp, train_data)

nlp.to_disk('nlp_GIT_model2')
'''


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
