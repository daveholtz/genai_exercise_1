# Course Q&A Platform

A Streamlit-based platform for managing course questions and student answers.

## Features

- Email-based authentication
- Sequential navigation through questions
- Answer submission and storage
- Progress tracking
- View all submitted answers
- SQLite database for persistent storage

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your email address to begin
2. Navigate through questions using Previous/Next buttons
3. Submit your answers in the text area
4. Track your progress with the progress bar
5. View all your submitted answers using the checkbox at the bottom

## Data Storage

All answers are stored in a SQLite database located in the `data` directory. 