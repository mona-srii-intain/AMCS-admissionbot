import pandas as pd
from datetime import datetime

# Create sample unanswered questions
unanswered = pd.DataFrame({
    'Question': [
        "What programming languages do I need to know for AMCS?",
        "Is there a scholarship available for international students?",
        "Can I transfer credits from another university?"
    ],
    'Confidence': [0.18, 0.22, 0.15],
    'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S') for _ in range(3)]
})

# Save to Excel
unanswered.to_excel('unanswered_questions.xlsx', index=False)
print("Created sample unanswered_questions.xlsx file")
