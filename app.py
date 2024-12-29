import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('data/course_answers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (email TEXT PRIMARY KEY, created_at TIMESTAMP)
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS answers
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         email TEXT,
         question_number INTEGER,
         answer TEXT,
         submitted_at TIMESTAMP,
         FOREIGN KEY (email) REFERENCES users(email))
    ''')
    conn.commit()
    conn.close()

# Course tasks
QUESTIONS = [
    """Search for each of the following six major generative text-based language models—GPT-4, PaLM 2, LLaMA 2, Claude 2, DeepSeek 3—please provide:
1. The organization responsible for its development
2. The year it was first publicly introduced
3. Whether it is open-source or closed access
4. Its approximate number of parameters (if publicly disclosed)
5. The context window size (i.e., maximum size of inputs)""",

    """Logical puzzle - Cal Alumni:
Chris Pine, Ashley Judd, Aaron Rodgers, Ashley Judd
Cal Landmarks: Sather Tower, Doe Library, Memorial Glade, Sproul Plaza
Times of Day: Morning, Noon, Afternoon, Evening

Each alumnus visited exactly one of the landmarks at a distinct time of day.
Clues:
1. Aaron Rodgers did not visit in the morning, and he did not visit Memorial Glade.
2. The person who visited Sather Tower did so in the morning.
3. Ashley Judd visited sometime after the person who went to Doe Library but before the person who went to Sproul Plaza.
4. Ashley Judd visited earlier in the day than Aaron Rodgers.
5. The person who visited Memorial Glade did not go at noon.
6. Chris Pine visited Sproul Plaza.

Goal: Determine each alumnus's landmark and the time of day they visited.""",

    """Math/probability:
Imagine there are three generative AI research teams:
1. Team A: Produces two text-to-image models (image-focused models).
2. Team B: Produces two text-to-text models (language-focused models).
3. Team C: Produces one text-to-image model (image-focused) and one text-to-text model (language-focused).

You randomly choose one of these teams and evaluate one of their models. The model happens to be a text-to-image model. What is the probability that the other model produced by the same team is also a text-to-image model?""",

    "Creative writing: Pretend you are Alan Turing. Write an elevator pitch for yourself in 150 words or less.",

    "Creative marketing: Brainstorm a name and slogan for an advertising company that uses generative AI to source its images.",

    """Technical Writing: How many grammatical/spelling errors are there in the passage below?

[Long passage about generative AI with intentional errors]""",

    """Reading comprehension:
[Passage about automation and efficiency]

Which of the following can be inferred from the passage about errors in manufacturing?
(A) They are an unavoidable problem in traditional manufacturing systems.
(B) They are the most important problem to fix through automation.
(C) They are an essential element for success when switching to automation from traditional manufacturing.
(D) They are a phenomenon found more often in traditional manufacturing than in automated manufacturing.
(E) They are an obstacle to increased efficiency and lower costs in traditional production.""",

    """Strategy: You are the Head of Strategy for ShopSmart, a mid-size retail chain specializing in affordable, everyday essentials. Your CEO is eager to integrate Generative AI into the company's operations to improve customer engagement and operational efficiency.

You have been tasked with developing a high-level plan for deploying Generative AI within the next 12 months. Outline your strategy by selecting one primary use case for Generative AI based on ShopSmart's priorities and justifying why:
a) Personalized marketing campaigns using AI-generated content.
b) Virtual shopping assistants to enhance online customer support.
c) AI-driven demand forecasting to optimize inventory.""",

    """Data Analysis: Using the provided csv file with a list of companies in the Bay Area, please tell us:
1. What is the median founding year?
2. What percentage of companies are in San Francisco?
3. How many companies are in Oakland?
4. How many companies are backed by Y Combinator and not in San Francisco?""",

    """Language Translation: Translate the following sentences into Spanish and Mandarin. Ensure the translations are accurate and maintain the meaning of the original text.
1. At Haas, learning happens both inside and outside the classroom.
2. Berkeley's campus is famous for its eucalyptus trees.
3. The rise of generative AI has sparked debates about intellectual property""",

    "Explain to a layperson (in less than 150 words) what vector embedding is.",

    "Visual Pattern Recognition: [Image will be provided]"
]

def save_answer(email, question_number, answer):
    conn = sqlite3.connect('data/course_answers.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO answers (email, question_number, answer, submitted_at)
        VALUES (?, ?, ?, ?)
    ''', (email, question_number, answer, datetime.now()))
    conn.commit()
    conn.close()

def get_user_answers(email):
    conn = sqlite3.connect('data/course_answers.db')
    df = pd.read_sql_query('''
        SELECT question_number, answer, submitted_at
        FROM answers
        WHERE email = ?
        ORDER BY question_number
    ''', conn, params=(email,))
    conn.close()
    return df

def get_last_answered_question(email):
    conn = sqlite3.connect('data/course_answers.db')
    c = conn.cursor()
    result = c.execute('''
        SELECT MAX(question_number) as last_question
        FROM answers
        WHERE email = ?
    ''', (email,)).fetchone()
    conn.close()
    return result[0] if result[0] is not None else -1

def main():
    st.title("Course Q&A Platform")
    
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    
    # Initialize database
    init_db()
    
    # Email-based authentication
    email = st.text_input("Enter your email address:")
    if not email:
        st.warning("Please enter your email address to continue.")
        return
    
    # Store user in database
    conn = sqlite3.connect('data/course_answers.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (email, created_at) VALUES (?, ?)',
              (email, datetime.now()))
    conn.commit()
    conn.close()

    # Get the last answered question for this user
    last_answered = get_last_answered_question(email)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous") and st.session_state.current_question > 0:
            st.session_state.current_question -= 1
    with col3:
        next_button = st.button("Next")
        if next_button:
            if st.session_state.current_question <= last_answered:
                if st.session_state.current_question < len(QUESTIONS) - 1:
                    st.session_state.current_question += 1
            else:
                st.error("Please submit an answer before moving to the next question.")
    
    # Display current question and answer box
    st.subheader(f"Question {st.session_state.current_question + 1}:")
    st.write(QUESTIONS[st.session_state.current_question])
    
    # Get existing answer if any
    existing_answers = get_user_answers(email)
    current_answer = ""
    if not existing_answers.empty:
        answer_row = existing_answers[existing_answers['question_number'] == st.session_state.current_question]
        if not answer_row.empty:
            current_answer = answer_row.iloc[0]['answer']
    
    # Answer input
    answer = st.text_area("Your Answer:", value=current_answer, height=200)
    
    if st.button("Submit Answer"):
        if answer.strip():
            if st.session_state.current_question <= last_answered + 1:
                save_answer(email, st.session_state.current_question, answer)
                st.success("Answer submitted successfully!")
                # Automatically move to next question if not on the last question
                if st.session_state.current_question < len(QUESTIONS) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                st.error("Please answer the questions in order.")
        else:
            st.error("Please provide an answer before submitting.")
    
    # Show progress
    progress = (last_answered + 2) / len(QUESTIONS) if last_answered < len(QUESTIONS) - 1 else 1.0
    st.progress(progress)
    
    # View all answers
    if st.checkbox("View all my answers"):
        answers_df = get_user_answers(email)
        if not answers_df.empty:
            for _, row in answers_df.iterrows():
                st.write(f"Question {row['question_number'] + 1}:")
                st.write(QUESTIONS[row['question_number']])
                st.write("Your Answer:")
                st.write(row['answer'])
                st.write("Submitted at:", row['submitted_at'])
                st.markdown("---")
        else:
            st.info("You haven't submitted any answers yet.")

if __name__ == "__main__":
    main() 