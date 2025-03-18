import psycopg2
import pandas as pd
from config import DB_CONFIG

def fetch_qa_data():
    """Fetch question-answer pairs from the database"""
    try:
        # Connect to the database
        print("Connecting to database...")
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        
        # Execute query
        cur = conn.cursor()
        print('Executing query: SELECT "Questions", "Answers" FROM "botQuestionsFinal"')
        cur.execute('SELECT "Questions", "Answers" FROM "botQuestionsFinal"')
        table = cur.fetchall()
        
        # Convert to DataFrame 
        conversation_data = pd.DataFrame(table, columns=['Questions', 'Answers'])
        
        if len(conversation_data) == 0:
            print("Warning: No data found in the database!")
            return None
        
        # Close connections
        cur.close()
        conn.close()
        
        print(f"Successfully retrieved {len(conversation_data)} QA pairs from database.")
        return conversation_data
        
    except Exception as e:
        print(f"Database error: {str(e)}")
        
        # Try to use the Excel file as fallback
        try:
            print("Trying to use conversation_data.xlsx as fallback...")
            conversation_data = pd.read_excel('conversation_data.xlsx')
            print(f"Successfully loaded {len(conversation_data)} QA pairs from Excel file.")
            return conversation_data
        except Exception as excel_error:
            print(f"Excel fallback error: {str(excel_error)}")
            return None