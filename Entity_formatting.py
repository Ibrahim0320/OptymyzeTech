# Correctly formatting extracted entities for SQL database

def format_extracted_entities(entities):
    formatted_output = []
    current_entity = None
    
    for entity in entities:
        if " - " in entity:
            label, value = entity.split(" - ", 1)
            value = value.strip()
            
            if label == "PERSON" and current_entity != "NAME":
                current_entity = "NAME"
                formatted_output.append(f"NAME                          - {value}")
            elif label == "GPE":
                current_entity = "LOCATION"
                formatted_output.append(f"LOCATION                      - {value}")
            elif label == "ORG":
                current_entity = "COMPANIES WORKED AT"
                formatted_output.append(f"COMPANIES WORKED AT           - {value}")
            elif label == "DATE":
                current_entity = "DATE"
                formatted_output.append(f"DATE                          - {value}")
            elif "Engineer" in value or "Consultant" in value or "Developer" in value or "Mentor" in value or "Assistant" in value:
                current_entity = "DESIGNATION"
                formatted_output.append(f"DESIGNATION                   - {value}")
            elif "Bachelors" in value or "Masters" in value or "M.Sc." in value or "Degree" in value:
                current_entity = "DEGREE"
                formatted_output.append(f"DEGREE                        - {value}")
            elif label == "LANGUAGE":
                current_entity = "LANGUAGE"
                formatted_output.append(f"LANGUAGE                      - {value}")
        else:
            print(f"Skipping invalid entry: {entity}")
    
    return "\n".join(formatted_output)


# Provided example input
extracted_entities = [
    "IBRAHIM GPE",
    "M.Sc. GPE",
    "Applied Data Science ORG",
    "Github PERSON",
    "Masters ORG",
    "Navy ORG",
    "Optymyze Technologies Tech Consulting ORG",
    "April, 2024 - May, 2024 DATE",
    "Atwo month DATE",
    "Berlin GPE",
    "the United States GPE",
    "The Finnish Defence Forces - Puolustusvoimat ORG",
    "Coastal Combat Engineer PRODUCT",
    "July DATE",
    "2023 - December DATE",
    "2023 DATE",
    "¢ Serving PERSON",
    "50 CARDINAL",
    "Only one CARDINAL",
    "First ORDINAL",
    "10 CARDINAL",
    "The University of Gothenburg - Géteborgs Universitet",
    "Student Mentor ORG",
    "September DATE",
    "2022 - May DATE",
    "2023 DATE",
    "Year 1 and Year 2 DATE",
    "Chalmers University of Technology - Chalmers ORG",
    "Research Assistent ORG",
    "November DATE",
    "2021 - December DATE",
    "2021 DATE",
    "Atwo month DATE",
    "the BuildSense Research ORG",
    "the Department of Architecture and Civil Engineering ORG",
    "Applied Data Science",
    "Univerity of Gothenburg ORG",
    "September, 2024 - Now DATE",
    "Joint ORG",
    "the University of Gothenburg ORG",
    "Chalmers University of Technology",
    "Bachelors ORG",
    "Gothenburg GPE",
    "September DATE",
    "2020- June, 2023 DATE",
    "the University of Gothenburg ORG",
    "Chalmers University ORG",
    "Microsoft ORG",
    "Excel PRODUCT",
    "Research ORG",
    "Multicultural ORG",
    "English LANGUAGE",
    "Swedish NORP",
    "Urdu - Native ORG",
    "French LANGUAGE",
    "Finnish - Professional NORP",
    "Dutch - Limited ORG",
    "German NORP",
    "Company NORP",
    "April, 2024 DATE",
    "2024 DATE",
    "Udemy GPE",
    "March, 2024 DATE",
    "2024 DATE",
    "Udemy GPE",
    "2024 DATE",
    "Accenture Data Analytics and Visualisation",
    "Accenture North America WORK_OF_ART",
    "March, 2024 DATE",
    "7 CARDINAL",
    "Prepared PRODUCT",
    "PowerPoint ORG",
    "Boston Consulting Group| ORG",
    "March, 2024 DATE",
    "BCG ORG",
    "GenAl Consulting ORG",
    "Conducted ORG",
    "Integrated NORP",
    "10 CARDINAL",
    "10 CARDINAL"
]

# Format the output
formatted_output = format_extracted_entities(extracted_entities)
print(formatted_output)
