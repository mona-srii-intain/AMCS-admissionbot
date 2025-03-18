from flask import Flask, render_template, request, jsonify
import threading
import webbrowser
import os
import platform
import time
from database import fetch_qa_data
from chatbot import AMCSChatbot

# Initialize Flask app
app = Flask(__name__)

# Fetch data and initialize chatbot
print("Initializing chatbot...")
df = fetch_qa_data()

if df is not None and not df.empty:
    try:
        chatbot = AMCSChatbot(df)
        print("Chatbot ready!")
    except Exception as e:
        print(f"Error initializing chatbot: {str(e)}")
        exit(1)
else:
    print("Failed to retrieve data from the database.")
    exit(1)

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    system = platform.system().lower()
    
    # Different commands for different operating systems
    if system == 'windows':
        os.system('start http://127.0.0.1:5000/')
    elif system == 'darwin':  # macOS
        os.system('open http://127.0.0.1:5000/')
    elif system == 'linux':
        os.system('xdg-open http://127.0.0.1:5000/')
    else:
        webbrowser.open('http://127.0.0.1:5000/')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Process chat messages and return responses"""
    user_input = request.form['message']
    response, confidence = chatbot.get_response(user_input)
    
    # Format confidence as percentage
    confidence_percent = round(confidence * 100, 1)
    
    return jsonify({
        'response': response,
        'confidence': confidence_percent
    })

if __name__ == '__main__':
    print("Starting server...")
    # Open browser in a separate thread
    threading.Thread(target=open_browser).start()
    print("Server is running at http://127.0.0.1:5000/")
    app.run(port=5000, debug=False, host='0.0.0.0')  # Allow external connections