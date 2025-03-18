import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'dbname': os.getenv('DB_NAME', 'rsl_questions'),  # Changed to lowercase
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASS', 'Shobs@123'),
    'port': int(os.getenv('DB_PORT', 5432))
}

# Flask configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'