# Attempt at building a matcher for the job reqs and the cvs

import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def retrieve_candidate_data():
    conn = sqlite3.connect('cv_database.db')
    c = conn.cursor()
    c.execute("SELECT id, feature1, feature2, ..., label FROM cv_data")  # Adjust feature names accordingly
    data = c.fetchall()
    conn.close()
    
    candidate_ids = [row[0] for row in data]
    candidate_features = [row[1:-1] for row in data]  # Exclude candidate ID and label
    suitability_scores = [row[-1] for row in data]
    
    return candidate_ids, candidate_features, suitability_scores

# Function to train the ranking model
def train_ranking_model(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a random forest regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
    
    return model

def score_candidates(model, candidate_features):
    candidate_scores = model.predict(candidate_features)
    return candidate_scores

# Function to rank candidates based on their scores
def rank_candidates(candidate_ids, candidate_scores):
    ranked_candidates = sorted(zip(candidate_ids, candidate_scores), key=lambda x: x[1], reverse=True)
    return ranked_candidates

# Retrieve candidate features and labels from the database
candidate_ids, candidate_features, suitability_scores = retrieve_candidate_data()

# Train the ranking model
model = train_ranking_model(candidate_features, suitability_scores)

# Score candidates using the trained model
candidate_scores = score_candidates(model, candidate_features)

# Rank candidates based on their scores
ranked_candidates = rank_candidates(candidate_ids, candidate_scores)

# Print the ranked candidates
for candidate_id, score in ranked_candidates:
    print(f"Candidate ID: {candidate_id}, Score: {score}")