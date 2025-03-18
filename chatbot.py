import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
from datetime import datetime

class AMCSChatbot:
    def __init__(self, df, unanswered_file='unanswered_questions.xlsx'):
        # Load data from the provided DataFrame
        self.df = df
        self.unanswered_file = unanswered_file
        
        # Preprocess questions
        self.df['Processed_Question'] = self.df['Questions'].apply(self.preprocess_text)
        
        # Initialize TF-IDF Vectorizer
        self.tfidf_vectorizer = TfidfVectorizer()
        
        # Fit and transform the processed questions
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['Processed_Question'])
        
        # Fallback response when confidence is too low
        self.fallback_response = ("Please contact AMCS department for further information.\n"
                                "Official website: https://www.psgtech.edu/department_page.php\n"
                                "Contact number: 0422 - 2572177, 2572477, 4344777")
    
    def preprocess_text(self, text):
        """Preprocess text by lowercasing and removing non-alphanumeric characters"""
        text = str(text).lower()  # Convert to lowercase
        # Replace non-alphanumeric with spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text).strip()
        # Split by spaces to get words
        words = text.split()
        return ' '.join(words)
    
    def store_unanswered_question(self, question, confidence):
        """Store questions that couldn't be answered with high confidence"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create a new DataFrame for this question
        new_row = pd.DataFrame({
            'Question': [question],
            'Confidence': [confidence],
            'Timestamp': [timestamp]
        })
        
        # If file exists, append to it
        if os.path.exists(self.unanswered_file):
            try:
                existing_df = pd.read_excel(self.unanswered_file)
                updated_df = pd.concat([existing_df, new_row], ignore_index=True)
                updated_df.to_excel(self.unanswered_file, index=False)
            except Exception as e:
                print(f"Error updating unanswered questions file: {str(e)}")
        else:
            # Create new file
            try:
                new_row.to_excel(self.unanswered_file, index=False)
            except Exception as e:
                print(f"Error creating unanswered questions file: {str(e)}")
    
    def get_response(self, query, confidence_threshold=0.3):
        """Get response for a user query with confidence check"""
        processed_query = self.preprocess_text(query)
        query_vector = self.tfidf_vectorizer.transform([processed_query])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        max_sim_idx = similarity_scores.argmax()
        max_similarity = similarity_scores[max_sim_idx]
        
        # Check confidence threshold
        if max_similarity >= confidence_threshold:
            return self.df.iloc[max_sim_idx]['Answers'], max_similarity
        else:
            # Store the unanswered question
            self.store_unanswered_question(query, max_similarity)
            return self.fallback_response, max_similarity