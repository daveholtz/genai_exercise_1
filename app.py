import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
from questions import QUESTIONS

def save_answer(email, question_number, answer):
    # Create a new answer as a DataFrame directly
    new_answer = pd.DataFrame({
        "email": [email],
        "question_number": [question_number],
        "answer": [answer],
        "submitted_at": [datetime.now()]
    })

    # Load existing answers or create new DataFrame
    try:
        df = pd.read_csv("answers.csv")
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=["email", "question_number", "answer", "submitted_at"]
        )

    # Update/append the answer
    mask = (df["email"] == email) & (df["question_number"] == question_number)
    if mask.any():
        # Update existing row
        for col in df.columns:
            df.loc[mask, col] = new_answer[col].iloc[0]
    else:
        # Append new row using concat with explicit dtypes
        df = pd.concat([df, new_answer], ignore_index=True)

    # Save to CSV
    df.to_csv("answers.csv", index=False)


def get_user_answers(email):
    try:
        df = pd.read_csv("answers.csv")
        return df[df["email"] == email].sort_values("question_number")
    except FileNotFoundError:
        return pd.DataFrame(
            columns=["email", "question_number", "answer", "submitted_at"]
        )


def get_last_answered_question(email):
    df = get_user_answers(email)
    if df.empty:
        return -1
    return df["question_number"].max()


def main():
    st.title("Course Q&A Platform")

    # Initialize session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    # Email-based authentication
    email = st.text_input("Enter your email address:")
    if not email:
        st.warning("Please enter your email address to continue.")
        return

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

    # Display current question number and task title in large format
    current_question = QUESTIONS[st.session_state.current_question]
    
    # Check if the question contains an image marker
    if "![Image]" in current_question:
        # Split the question into text and image parts
        parts = current_question.split("![Image]")
        
        # Display the text part
        title_end = parts[0].find('\n')
        task_title = parts[0][:title_end].strip()
        task_content = parts[0][title_end:].strip()
        
        st.markdown(f"<h1 style='text-align: center;'>{task_title}</h1>", unsafe_allow_html=True)
        st.write(task_content)
        
        # Extract and display the image
        image_path = parts[1].strip()[1:-1]  # Remove parentheses but keep the full path
        try:
            # Make sure we're using the correct path separator and clean the path
            image_path = image_path.replace('(', '').replace(')', '').strip()
            st.write(f"Debug: Attempting to load image from: {image_path}")  # Debug line
            st.image(image_path)
        except Exception as e:
            st.error(f"Could not load image: {image_path}")
            st.error(f"Error details: {str(e)}")
    else:
        # Original handling for non-image questions
        title_end = current_question.find('\n')
        task_title = current_question[:title_end].strip()
        task_content = current_question[title_end:].strip()
        
        st.markdown(f"<h1 style='text-align: center;'>{task_title}</h1>", unsafe_allow_html=True)
        st.write(task_content)

    # Get existing answer if any
    existing_answers = get_user_answers(email)
    current_answer = ""
    if not existing_answers.empty:
        answer_row = existing_answers[
            existing_answers["question_number"] == st.session_state.current_question
        ]
        if not answer_row.empty:
            current_answer = answer_row.iloc[0]["answer"]

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
    progress = (
        (last_answered + 2) / len(QUESTIONS)
        if last_answered < len(QUESTIONS) - 1
        else 1.0
    )
    st.progress(progress)

    # View all answers
    if st.checkbox("View all my answers"):
        answers_df = get_user_answers(email)
        if not answers_df.empty:
            for _, row in answers_df.iterrows():
                st.write(f"Question {row['question_number'] + 1}:")
                st.write(QUESTIONS[row["question_number"]])
                st.write("Your Answer:")
                st.write(row["answer"])
                st.write("Submitted at:", row["submitted_at"])
                st.markdown("---")
        else:
            st.info("You haven't submitted any answers yet.")

    # Add download button at the bottom
    if st.checkbox("Download my answers"):
        user_answers = get_user_answers(email)
        if not user_answers.empty:
            csv = user_answers.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"answers_{email}.csv",
                mime="text/csv",
            )
        else:
            st.info("No answers to download yet.")


if __name__ == "__main__":
    main()
