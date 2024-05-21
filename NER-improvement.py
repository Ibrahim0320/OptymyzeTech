# Correcting the mistakes the NER makes and retraining

import spacy
from spacy.training.example import Example
import random

# Corrected Data Annotations
corrected_data = [
    ("MUHAMMAD IBRAHIM M.Sc. in Applied Data Science Email: ibrahim.muhammad02@outlook.com LinkedIn: linkedin.com/in/muhibrahim7 Github: github.com/ibrahim0320", 
     {"entities": [(0, 15, "PERSON"), (17, 42, "DEGREE"), (50, 81, "EMAIL"), (91, 122, "URL"), (131, 154, "URL")]}),
    ("CAREER SUMMARY: I am an incoming Masters student within the field of data science with a profound passion for machine learning, artificial intelligence, and data analytics. Combined with a background in engineering physics, I am committed to enhancing my skills and knowledge in this field with the aim of making a meaningful impact in the industry.", 
     {"entities": [(22, 29, "DEGREE")]}),
    ("Optymyze Technologies Tech Consulting Coastal Combat Engineer | July, 2023 - December, 2023", 
     {"entities": [(0, 30, "ORG"), (31, 50, "TITLE"), (53, 58, "DATE"), (60, 64, "DATE"), (67, 76, "DATE")]}),
    # Add more corrected examples
]

# Initialize a blank SpaCy model
nlp = spacy.blank("en")

# Create the NER component and add it to the pipeline
ner = nlp.add_pipe("ner")

# Add labels to the NER component
for _, annotations in corrected_data:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Disable other pipeline components
pipe_exceptions = ["ner"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# Custom function to create examples with spans
def create_examples_with_spans(nlp, texts, annotations):
    examples = []
    for text, annotation in zip(texts, annotations):
        doc = nlp.make_doc(text)
        spans = []
        for start, end, label in annotation['entities']:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                spans.append(span)
        doc.spans['entities'] = spans
        example = Example.from_dict(doc, annotation)
        examples.append(example)
    return examples

# Start the training
with nlp.disable_pipes(*unaffected_pipes):
    optimizer = nlp.begin_training()
    for itn in range(20):
        random.shuffle(corrected_data)
        losses = {}
        batches = spacy.util.minibatch(corrected_data, size=spacy.util.compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            examples = create_examples_with_spans(nlp, texts, annotations)
            nlp.update(examples, drop=0.5, losses=losses)
        print(f"Losses at iteration {itn}: {losses}")

# Save the trained model
output_dir = "NER_model_v2"
nlp.to_disk(output_dir)
