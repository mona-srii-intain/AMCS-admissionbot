import pandas as pd
import psycopg2
from config import DB_CONFIG

def add_qa_pair(question, answer):
    """Add a new question-answer pair to the database"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        
        cursor = conn.cursor()
        
        # Insert the new QA pair
        cursor.execute(
            'INSERT INTO "botQuestionsFinal" ("Questions", "Answers") VALUES (%s, %s)',
            (question, answer)
        )
        
        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully added new QA pair to database!")
        return True
    except Exception as e:
        print(f"Error adding QA pair: {str(e)}")
        return False

def add_qa_from_excel(excel_file):
    """Add new QA pairs from an Excel file"""
    try:
        # Read Excel file
        df = pd.read_excel(excel_file)
        print(f"Found {len(df)} question-answer pairs in {excel_file}.")
        
        # Connect to database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        
        cursor = conn.cursor()
        
        # Insert each row
        success_count = 0
        for index, row in df.iterrows():
            try:
                cursor.execute(
                    'INSERT INTO "botQuestionsFinal" ("Questions", "Answers") VALUES (%s, %s)',
                    (row['Questions'], row['Answers'])
                )
                success_count += 1
            except Exception as e:
                print(f"Error adding row {index}: {str(e)}")
        
        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully added {success_count} out of {len(df)} QA pairs to database!")
        return True
    except Exception as e:
        print(f"Error adding QA pairs from Excel: {str(e)}")
        return False

if __name__ == "__main__":
    
    # Interactive mode
    print("Add a new question-answer pair to the database")
    print("----------------------------------------------")
    question = input("Enter the question: ")
    answer = input("Enter the answer: ")
    add_qa_pair(question, answer)
