# AMCS Department Admission Chatbot

This chatbot application facilitates admission inquiries for the Applied Mathematics and Computational Sciences (AMCS) Department at PSG College of Technology.

## Features

- Interactive web interface for student inquiries
- Database-backed question-answer system using PostgreSQL
- TF-IDF and cosine similarity for intelligent question matching
- Automatic logging of unanswered questions for continuous improvement
- Admin tools for adding new Q&A pairs

## Demo

[Watch the demo video](https://github.com/mona-srii-intain/AMCS-admissionbot/blob/main/AMCS_demo.screenrec?raw=true)

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure PostgreSQL database
4. Run the application: `python app.py`

## Project Structure

- `app.py`: Main application server
- `chatbot.py`: Core chatbot functionality
- `database.py`: Database connector
- `import_excel_to_db.py`: Tool to import Q&A pairs from Excel
- `process_unanswered.py`: Tool to process unanswered questions
- `add_new_qa.py`: Tool to add new Q&A pairs
- `static/`: Static assets (CSS, JS, images)
- `templates/`: HTML templates

## License

[MIT License](LICENSE)
