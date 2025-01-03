import streamlit as st
from questions import QUESTIONS
from src.auth.auth import authenticate_user
from src.data.storage import (
    save_answer,
    get_user_answers,
    get_last_answered_question,
    save_playground_interaction,
    get_playground_interactions,
)
from src.ui.components import (
    display_question,
    display_navigation,
    display_progress,
    display_answer_history,
    display_playground_history,
)
from src.ai.playground import get_ai_response


def main():
    st.title("Berkeley Haas: AI For Business Leaders (EWMBA295T.6)")

    # Initialize session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "is_authenticated" not in st.session_state:
        st.session_state.is_authenticated = False
        st.session_state.user_email = None

    # Authentication - only show if not authenticated
    if not st.session_state.is_authenticated:
        email = st.text_input("Enter your email address:")
        password = st.text_input("Enter password:", type="password")

        is_authenticated, auth_message = authenticate_user(email, password)
        if is_authenticated:
            st.session_state.is_authenticated = True
            st.session_state.user_email = email
            st.rerun()  # Rerun to refresh the page without login fields
        else:
            st.warning(auth_message)
            return

    # Use stored email for all subsequent operations
    email = st.session_state.user_email

    # Get the last answered question for this user
    last_answered = get_last_answered_question(email)

    # Navigation
    nav_action = display_navigation(
        st.session_state.current_question, len(QUESTIONS), last_answered
    )
    if nav_action == "previous":
        st.session_state.current_question -= 1
        st.rerun()
    elif nav_action == "next":
        st.session_state.current_question += 1
        st.rerun()

    # Display current question
    current_question = QUESTIONS[st.session_state.current_question]
    display_question(current_question)

    # AI assistance selector
    ai_assistance = st.radio(
        "Select AI Assistance Level:",
        ["No AI Assistance", "Legacy AI Model", "Higher Capability Model"],
        key=f"ai_assistance_{st.session_state.current_question}",
    )

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
                if st.session_state.current_question < len(QUESTIONS) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                st.error("Please answer the questions in order.")
        else:
            st.error("Please provide an answer before submitting.")

    # Show progress
    display_progress(last_answered, len(QUESTIONS))

    # View all answers
    if st.checkbox("View all my answers"):
        display_answer_history(get_user_answers(email), QUESTIONS)

    # Add download button for answers
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

    # AI Playground
    if ai_assistance != "No AI Assistance":
        st.markdown("### AI Playground")
        prompt = st.text_area(
            "Enter your prompt:",
            height=100,
            key=f"prompt_{st.session_state.current_question}",
        )

        if st.button("Run", key=f"run_{st.session_state.current_question}"):
            if not prompt.strip():
                st.error("Please enter a prompt")
            else:
                try:
                    response_text, parameters = get_ai_response(prompt, ai_assistance)
                    st.markdown("### Response:")
                    st.write(response_text)

                    save_playground_interaction(
                        email,
                        st.session_state.current_question,
                        prompt,
                        parameters,
                        response_text,
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Add playground interactions download section
    st.markdown("### Download Playground History")
    download_options = st.radio(
        "Choose what to download:",
        ["My interactions only", "All interactions (admin only)"],
    )

    if st.button("Download Playground History"):
        interactions_df = get_playground_interactions(
            email if download_options == "My interactions only" else None
        )
        display_playground_history(interactions_df)

        if not interactions_df.empty:
            csv = interactions_df.to_csv(index=False)
            filename = f"playground_history{'_' + email if download_options == 'My interactions only' else '_all'}.csv"
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=filename,
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
