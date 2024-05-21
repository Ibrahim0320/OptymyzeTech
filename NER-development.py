import spacy
from spacy.training.example import Example
import random
import string
import pandas as pd
from spacy.tokens import Doc, Span

# Load the dataset
file_path = '/Users/muhammadibrahim/Downloads/train_data.pkl'
data = pd.read_pickle(file_path)

# Function to clean entity spans
def clean_entities(entities, text):
    cleaned_entities = []
    for start, end, label in entities:
        # Trim whitespace
        while start < len(text) and text[start].isspace():
            start += 1
        while end > 0 and text[end - 1].isspace():
            end -= 1
        # Remove leading/trailing punctuation
        while start < len(text) and text[start] in string.punctuation:
            start += 1
        while end > 0 and text[end - 1] in string.punctuation:
            end -= 1
        # Add the cleaned entity if valid
        if start < end:
            cleaned_entities.append((start, end, label))
    return cleaned_entities

# Function to convert entities to spans
def entities_to_spans(doc, entities):
    spans = []
    for start, end, label in entities:
        span = doc.char_span(start, end, label=label)
        if span is not None:
            spans.append(span)
    return spans

# Clean the entities in the dataset
cleaned_data = []
for text, annotations in data:
    entities = [(start, end, label) for start, end, label in annotations['entities']]
    cleaned_entities = clean_entities(entities, text)
    cleaned_data.append((text, {"entities": cleaned_entities}))

# Initialize a blank SpaCy model
nlp = spacy.blank("en")

# Create a new NER component
ner = nlp.add_pipe("ner")

# Add labels to the NER component
for _, annotations in cleaned_data:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Disable other components in the pipeline
pipe_exceptions = ["ner"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# Custom function to create examples with spans
def create_examples_with_spans(nlp, texts, annotations):
    examples = []
    for text, annotation in zip(texts, annotations):
        doc = nlp.make_doc(text)
        spans = entities_to_spans(doc, annotation['entities'])
        doc.spans['entities'] = spans
        example = Example.from_dict(doc, annotation)
        examples.append(example)
    return examples

# Start the training
with nlp.disable_pipes(*unaffected_pipes):
    optimizer = nlp.begin_training()
    for itn in range(20):
        random.shuffle(cleaned_data)
        losses = {}
        batches = spacy.util.minibatch(cleaned_data, size=spacy.util.compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            examples = create_examples_with_spans(nlp, texts, annotations)
            nlp.update(examples, drop=0.5, losses=losses)
        print(f"Losses at iteration {itn}: {losses}")

# Save the trained model
output_dir = "NER_model"
nlp.to_disk(output_dir)
