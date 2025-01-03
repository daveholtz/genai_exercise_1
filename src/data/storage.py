import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any
from ..config import ANSWERS_FILE, PLAYGROUND_FILE


def save_answer(email: str, question_number: int, answer: str) -> None:
    """Save or update a user's answer to a question."""
    new_answer = pd.DataFrame(
        {
            "email": [email],
            "question_number": [question_number],
            "answer": [answer],
            "submitted_at": [datetime.now()],
        }
    )

    try:
        df = pd.read_csv(ANSWERS_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=["email", "question_number", "answer", "submitted_at"]
        )

    mask = (df["email"] == email) & (df["question_number"] == question_number)
    if mask.any():
        for col in df.columns:
            df.loc[mask, col] = new_answer[col].iloc[0]
    else:
        df = pd.concat([df, new_answer], ignore_index=True)

    df.to_csv(ANSWERS_FILE, index=False)


def get_user_answers(email: str) -> pd.DataFrame:
    """Retrieve all answers for a specific user."""
    try:
        df = pd.read_csv(ANSWERS_FILE)
        return df[df["email"] == email].sort_values("question_number")
    except FileNotFoundError:
        return pd.DataFrame(
            columns=["email", "question_number", "answer", "submitted_at"]
        )


def get_last_answered_question(email: str) -> int:
    """Get the last question number answered by the user."""
    df = get_user_answers(email)
    if df.empty:
        return -1
    return df["question_number"].max()


def save_playground_interaction(
    email: str,
    question_number: int,
    prompt: str,
    parameters: Dict[Any, Any],
    response: str,
) -> None:
    """Save a playground interaction."""
    interaction = {
        "email": email,
        "question_number": question_number,
        "prompt": prompt,
        "parameters": parameters,
        "response": response,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        with open(PLAYGROUND_FILE, "r") as f:
            interactions = json.load(f)
    except FileNotFoundError:
        interactions = []

    interactions.append(interaction)

    with open(PLAYGROUND_FILE, "w") as f:
        json.dump(interactions, f)


def get_playground_interactions(email: str = None) -> pd.DataFrame:
    """Retrieve playground interactions, optionally filtered by email."""
    try:
        with open(PLAYGROUND_FILE, "r") as f:
            interactions = json.load(f)

        df = pd.DataFrame(interactions)

        if email:
            df = df[df["email"] == email]

        params_df = pd.json_normalize(df["parameters"])
        df = pd.concat([df.drop("parameters", axis=1), params_df], axis=1)

        return df
    except FileNotFoundError:
        return pd.DataFrame()
