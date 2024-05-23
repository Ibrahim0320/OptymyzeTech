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
import random

def text_to_training_data(text_file_path):
    training_data = []
    with open(text_file_path, 'r') as file:
        content = file.read().strip().split('\n\n')
        for example in content:
            if example.strip():
                parts = example.split('\n')
                text = parts[0].replace('Text: ', '')
                entities = eval(parts[1].replace('Entities: ', ''))
                training_data.append((text, {'entities': entities}))
    return training_data

# Configuration
text_file_path = 'output_text_file.txt'  # The text file you manually edited

training_data = text_to_training_data(text_file_path)

# Load pretrained transformer model
nlp = spacy.blank("en")
transformer = nlp.add_pipe("transformer")
ner = nlp.add_pipe("ner")

# Add labels to the NER component
labels = ["PERSON", "ORG", "GPE", "DATE", "PRODUCT", "LANGUAGE", "NORP", "CARDINAL", "ORDINAL"]
for label in labels:
    ner.add_label(label)

# Convert to spaCy's format
examples = []
for text, annotations in training_data:
    try:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)
    except Exception as e:
        print(f"Error with example:\nText: {text}\nAnnotations: {annotations}\nError: {e}")

# Train the model
optimizer = nlp.begin_training()
for itn in range(20):
    random.shuffle(examples)
    losses = {}
    for example in examples:
        nlp.update([example], drop=0.5, losses=losses)
    print(f"Iteration {itn + 1}, Losses: {losses}")

# Save the trained model
nlp.to_disk("Improved_ner_model")


# Test the model
#nlp = spacy.load("trained_ner_model")
#doc = nlp("Your test text here")
#for ent in doc.ents:
#    print(ent.text, ent.label_)
