import pickle
import os

def unpickle_to_text(pickle_file_path, output_text_file):
    try:
        # Load the pickled data
        with open(pickle_file_path, 'rb') as f:
            data = pickle.load(f)
        
        # Check the type of data
        if isinstance(data, dict):
            # Write the dictionary contents to the text file
            with open(output_text_file, 'w') as out_file:
                for key, value in data.items():
                    out_file.write(f"{key}: {value}\n")
        elif isinstance(data, list):
            # Write the list contents to the text file
            with open(output_text_file, 'w') as out_file:
                for item in data:
                    out_file.write(f"{item}\n")
        else:
            # Write other types of data to the text file
            with open(output_text_file, 'w') as out_file:
                out_file.write(str(data))
        
        print(f"Data has been successfully unpickled and saved to {output_text_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Configuration
pickle_file_path = '/Users/muhammadibrahim/Downloads/train_data.pkl'  # Set your pickle file path here
output_text_file = 'output_text_file.txt'  # Set the desired output text file name here

unpickle_to_text(pickle_file_path, output_text_file)
