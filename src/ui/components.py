import streamlit as st
from typing import Optional
import pandas as pd


def display_question(question: str) -> None:
    """Display a question with proper formatting for text and images."""
    if "![Image]" in question:
        parts = question.split("![Image]")

        # Display text part
        title_end = parts[0].find("\n")
        task_title = parts[0][:title_end].strip()
        task_content = parts[0][title_end:].strip()

        st.markdown(
            f"<h1 style='text-align: center;'>{task_title}</h1>", unsafe_allow_html=True
        )
        st.write(task_content)

        # Display image
        image_path = parts[1].strip()[1:-1]
        try:
            image_path = image_path.replace("(", "").replace(")", "").strip()
            st.image(image_path)
        except Exception as e:
            st.error(f"Could not load image: {image_path}")
            st.error(f"Error details: {str(e)}")
    else:
        title_end = question.find("\n")
        task_title = question[:title_end].strip()
        task_content = question[title_end:].strip()

        st.markdown(
            f"<h1 style='text-align: center;'>{task_title}</h1>", unsafe_allow_html=True
        )
        st.write(task_content)


def display_navigation(
    current_question: int, total_questions: int, last_answered: int
) -> Optional[str]:
    """Display navigation buttons and return navigation action if any."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("Previous") and current_question > 0:
            return "previous"

    with col3:
        if st.button("Next"):
            if current_question <= last_answered:
                if current_question < total_questions - 1:
                    return "next"
            else:
                st.error("Please submit an answer before moving to the next question.")

    return None


def display_progress(last_answered: int, total_questions: int) -> None:
    """Display progress bar."""
    progress = (
        (last_answered + 2) / total_questions
        if last_answered < total_questions - 1
        else 1.0
    )
    st.progress(progress)


def display_answer_history(answers_df: pd.DataFrame, questions: list[str]) -> None:
    """Display user's answer history."""
    if not answers_df.empty:
        for _, row in answers_df.iterrows():
            st.write(f"Question {row['question_number'] + 1}:")
            st.write(questions[row["question_number"]])
            st.write("Your Answer:")
            st.write(row["answer"])
            st.write("Submitted at:", row["submitted_at"])
            st.markdown("---")
    else:
        st.info("You haven't submitted any answers yet.")


def display_playground_history(interactions_df: pd.DataFrame) -> None:
    """Display playground interaction history."""
    if not interactions_df.empty:
        st.markdown("### Usage Summary")
        st.write(f"Total interactions: {len(interactions_df)}")
        st.write("Model usage distribution:")
        st.write(interactions_df["model"].value_counts())

        st.markdown("### Recent Interactions")
        st.dataframe(
            interactions_df[["timestamp", "question_number", "prompt", "response"]]
            .tail(5)
            .sort_values("timestamp", ascending=False)
        )
    else:
        st.info("No playground interactions found.")
