from Cv_to_req_matcher import *
from gensim.models import Word2Vec, KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity


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



# Load pre-trained Word2Vec model (here we assume it's Google's pre-trained model)
model = KeyedVectors.load_word2vec_format('path_to_model/GoogleNews-vectors-negative300.bin', binary=True)

def document_vector(doc):
    """Create document vectors by averaging word vectors. Remove out-of-vocabulary words."""
    words = doc.split()
    word_vectors = [model[word] for word in words if word in model]
    if not word_vectors:
        return np.zeros(model.vector_size)
    return np.mean(word_vectors, axis=0)

# Example usage
doc_vector1 = document_vector(preprocess_text(job_description))
doc_vectors_cv = [document_vector(preprocess_text(cv)) for cv in candidate_features]
similarities = cosine_similarity([doc_vector1], doc_vectors_cv)



print(similarities)