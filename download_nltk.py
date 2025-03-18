import nltk
import os

# Create a custom directory for NLTK data
nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)

# Download required NLTK resources to the custom directory
print(f"Downloading NLTK resources to {nltk_data_dir}...")
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)
print("Download complete!")
