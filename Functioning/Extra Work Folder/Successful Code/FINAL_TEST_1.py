from Working_code import *



'''
def clear_database()
    try:
        conn = sqlite3.connect('cv_database.db')
        c = conn.cursor()
        c.execute("DELETE FROM cv_data")  # Delete all rows from the table
        conn.commit()
        conn.close()
        print("Data cleared successfully.")  # Print success message
    except sqlite3.Error as e:
        print("Error clearing data:", e)  # Print error message if an exception occurs

# Call the function to clear the database
clear_database()
'''

# Specify the folder containing CVs
cv_folder_path = "Test"

# Verify the path exists
if os.path.isdir(cv_folder_path):
    # Process CVs in the folder
    iterate_over_cv_folder_extract_and_parse_and_store(cv_folder_path)
else:
    print("Error: Invalid CV folder path!")


# Test Run
job_description= '''
Senior Quality Assurance Engineer We are on the hunt for an exceptional Senior QA Engineer to join and elevate our team.
This role is perfect for someone who is not just looking for a job but an opportunity to make a significant impact. 
Key Responsibilities: Develop, enhance, and maintain both front-end and back-end automated testing frameworks using 
cutting-edge tools and technologies, alongside conducting manual testing when necessary.Take charge of our CI/CD 
processes, crafting a comprehensive test strategy, and embedding quality standards within automated pipelines.
Define, track, and optimize quality and performance metrics for our applications to ensure they meet our high standards.
Lead by example, reviewing test procedures and mentoring team members on best practices in automated testing. 
Serve as the linchpin for quality control, ensuring application changes meet our rigorous standards for excellence.
Requirements: Proven track record as a Quality Assurance Engineer, boasting a deep understanding of automated testing
frameworks for both front-end (e.g., Playwright) and back-end (e.g., xUnit) development. 
Experience with AWS DevOps, cloud services, and an ability to seamlessly integrate test cases into comprehensive 
suites for automation.Familiarity with test design, methodologies, and tools, with ISTQB or similar certifications
being a huge plus. A strong team player with outstanding analytical abilities, you pride yourself on being 
independent, solution-focused, and proactive.Excellent communication skills in English, both verbal and written,
are essential. What We Offer: Competitive salaries that stand above market standards.Annual bonuses reflecting
both personal and company performance.A generous learning and development budget to support your professional
growth. 25 days of paid leave annually to ensure work-life balance.
'''



# Preprocess job description
job_description = preprocess_text(job_description)
# Retrieve candidate features from the database
candidate_ids, candidate_features = retrieve_candidate_data()
# Calculate similarity between job description and candidate features
similarity_scores = calculate_similarity(job_description, [f[1] for f in candidate_features])
# Rank candidates based on similarity scores
ranked_candidates = candidate_ranking(candidate_ids, similarity_scores)


# Print the ranked candidates
for candidate_info, score in ranked_candidates:
    # Extract the name from the candidate_info
    candidate_name = candidate_info.split('\n')[0]
    print(f"Candidate Name: {candidate_name}, Similarity Score: {score}")


