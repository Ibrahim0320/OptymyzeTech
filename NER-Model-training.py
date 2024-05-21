import spacy
import pickle
import random


# Initialize a blank English model
nlp = spacy.blank('en')

# Load training data from a pickle file
train_data = pickle.load(open('/Users/muhammadibrahim/Downloads/train_data.pkl', 'rb'))
print(train_data[0])  # Print the first training data entry to confirm it's loaded correctly


'''
def train_model(train_data):
    # Check if 'ner' exists in the pipeline, if not, add it
    if 'ner' not in nlp.pipe_names:
        # Add the 'ner' component to the pipeline if it's not there
        ner = nlp.add_pipe('ner', last=True)
    else:
        ner = nlp.get_pipe('ner')
    
    # Add new entity labels to 'ner'
    for _, annotations in train_data:
        for ent in annotations['entities']:
            ner.add_label(ent[2])
    
    # Disable other pipeline components during training to train only NER
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(10):
            print(f"Starting iteration {itn}")
            random.shuffle(train_data)
            losses = {}
            for text, annotations in train_data:
                try:
                    doc = nlp.make_doc(text)
                    example = spacy.training.Example.from_dict(doc, annotations)
                    nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
                except Exception as e:
                    print(f"Skipping example due to an error: {e}")
            print(f"Losses at iteration {itn}: {losses}")

# Train the model
train_model(train_data)

# Save the trained model to disk
nlp.to_disk('nlp_model')
'''



nlp_model = spacy.load('nlp_model')



train_data[0][0]

doc = nlp_model(train_data[0][0])
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}- {ent.text}')
