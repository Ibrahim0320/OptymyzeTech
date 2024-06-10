import sqlite3

def fetch_and_format_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('InfoDatabase.db')
    cursor = conn.cursor()

    # Fetch all candidates' information
    cursor.execute('''
        SELECT id, name, email FROM Candidates
    ''')
    candidates = cursor.fetchall()

    for candidate in candidates:
        candidate_id, name, email = candidate
        print(f"Candidate Name: {name}\nEmail: {email}\n")

        # Fetch education details
        cursor.execute('''
            SELECT details FROM Education WHERE candidate_id = ?
        ''', (candidate_id,))
        education = cursor.fetchall()
        print("Education:")
        for edu in education:
            print(f"- {edu[0]}")

        # Fetch work experience details
        cursor.execute('''
            SELECT details FROM WorkExperience WHERE candidate_id = ?
        ''', (candidate_id,))
        experiences = cursor.fetchall()
        print("Work Experience:")
        for exp in experiences:
            print(f"- {exp[0]}")

        # Fetch skills
        cursor.execute('''
            SELECT details FROM Skills WHERE candidate_id = ?
        ''', (candidate_id,))
        skills = cursor.fetchall()
        print("Skills:")
        for skill in skills:
            print(f"- {skill[0]}")

        # Fetch extracurricular activities
        cursor.execute('''
            SELECT details FROM Extracurriculars WHERE candidate_id = ?
        ''', (candidate_id,))
        activities = cursor.fetchall()
        print("Extracurricular Activities:")
        for act in activities:
            print(f"- {act[0]}")
        
        #print("\n---------------------------------\n")

    # Close the connection to the database
    conn.close()

# Call the function to fetch and display the data
data= fetch_and_format_data()


