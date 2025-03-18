import pandas as pd
import os
from add_new_qa import add_qa_pair

def process_unanswered_questions(unanswered_file='unanswered_questions.xlsx', 
                                processed_file='processed_questions.xlsx'):
    """Process unanswered questions and add them to the database"""
    if not os.path.exists(unanswered_file):
        print(f"No unanswered questions file found at {unanswered_file}")
        return False
        
    try:
        # Read unanswered questions
        df = pd.read_excel(unanswered_file)
        if len(df) == 0:
            print("No unanswered questions to process.")
            return False
            
        print(f"Found {len(df)} unanswered questions to process.")
        
        # Create a new DataFrame for processed questions
        processed_df = pd.DataFrame(columns=['Question', 'Answer', 'Confidence', 'Timestamp', 'Processed'])
        
        # Process each question
        for index, row in df.iterrows():
            print(f"\nQuestion {index+1}: {row['Question']}")
            print(f"Confidence: {row['Confidence']}")
            print(f"Timestamp: {row['Timestamp']}")
            
            answer = input("Enter an answer (or press Enter to skip): ")
            
            if answer.strip():
                # Add to database
                success = add_qa_pair(row['Question'], answer)
                
                # Add to processed DataFrame
                new_row = {
                    'Question': row['Question'],
                    'Answer': answer,
                    'Confidence': row['Confidence'],
                    'Timestamp': row['Timestamp'],
                    'Processed': 'Yes' if success else 'Failed'
                }
                processed_df = pd.concat([processed_df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                # Skip this question
                new_row = {
                    'Question': row['Question'],
                    'Answer': '',
                    'Confidence': row['Confidence'],
                    'Timestamp': row['Timestamp'],
                    'Processed': 'Skipped'
                }
                processed_df = pd.concat([processed_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Save processed questions
        if not processed_df.empty:
            # If processed file exists, append to it
            if os.path.exists(processed_file):
                existing_df = pd.read_excel(processed_file)
                updated_df = pd.concat([existing_df, processed_df], ignore_index=True)
                updated_df.to_excel(processed_file, index=False)
            else:
                processed_df.to_excel(processed_file, index=False)
        
        # Clear or archive the unanswered questions file
        response = input("\nDo you want to clear the unanswered questions file? (y/n): ")
        if response.lower() == 'y':
            # Create empty DataFrame with same columns
            empty_df = pd.DataFrame(columns=df.columns)
            empty_df.to_excel(unanswered_file, index=False)
            print(f"Cleared unanswered questions file.")
        
        return True
    except Exception as e:
        print(f"Error processing unanswered questions: {str(e)}")
        return False

if __name__ == "__main__":
    process_unanswered_questions()
