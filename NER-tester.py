
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