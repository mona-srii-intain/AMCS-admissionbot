import pandas as pd
import psycopg2
from config import DB_CONFIG

def import_excel_to_db(excel_file='conversation_data.xlsx'):
    try:
        # Read Excel file
        print(f"Reading data from {excel_file}...")
        df = pd.read_excel(excel_file)
        print(f"Found {len(df)} question-answer pairs in Excel file.")
        
        # Connect to database
        print("Connecting to database...")
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        
        cursor = conn.cursor()
        
        # Clear existing data (optional - remove this if you want to keep existing data)
        cursor.execute('TRUNCATE TABLE "botQuestionsFinal"')
        print("Cleared existing data from database.")
        
        # Insert each row
        for index, row in df.iterrows():
            cursor.execute(
                'INSERT INTO "botQuestionsFinal" ("Questions", "Answers") VALUES (%s, %s)',
                (row['Questions'], row['Answers'])
            )
        
        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully imported {len(df)} question-answer pairs to database!")
        return True
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return False

if __name__ == "__main__":
    import_excel_to_db()
