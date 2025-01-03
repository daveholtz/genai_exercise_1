import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any
from ..config import (
    S3_BUCKET,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    ANSWERS_PREFIX,
    PLAYGROUND_PREFIX,
)
import boto3
import io

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


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

    # Get existing answers if any
    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET, Key=f"{ANSWERS_PREFIX}{email}_answers.csv"
        )
        df = pd.read_csv(io.BytesIO(response["Body"].read()))
    except:
        df = pd.DataFrame(
            columns=["email", "question_number", "answer", "submitted_at"],
            dtype={
                "email": str,
                "question_number": int,
                "answer": str,
                "submitted_at": str,
            },
        )

    mask = (df["email"] == email) & (df["question_number"] == question_number)
    if mask.any():
        for col in df.columns:
            df.loc[mask, col] = new_answer[col].iloc[0]
    else:
        df = pd.concat([df, new_answer], ignore_index=True)

    # Save to S3
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=f"{ANSWERS_PREFIX}{email}_answers.csv",
        Body=csv_buffer.getvalue(),
    )


def get_user_answers(email: str) -> pd.DataFrame:
    """Retrieve all answers for a specific user."""
    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET, Key=f"{ANSWERS_PREFIX}{email}_answers.csv"
        )
        return pd.read_csv(io.BytesIO(response["Body"].read()))
    except:
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
    interaction = pd.DataFrame(
        [
            {
                "email": email,
                "question_number": question_number,
                "prompt": prompt,
                "parameters": json.dumps(parameters),  # Convert dict to JSON string
                "response": response,
                "timestamp": datetime.now().isoformat(),
            }
        ]
    )

    # Get existing interactions if any
    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET, Key=f"{PLAYGROUND_PREFIX}{email}_interactions.csv"
        )
        interactions = pd.read_csv(io.BytesIO(response["Body"].read()))
    except:
        interactions = pd.DataFrame(
            columns=[
                "email",
                "question_number",
                "prompt",
                "parameters",
                "response",
                "timestamp",
            ]
        )

    interactions = pd.concat([interactions, interaction], ignore_index=True)

    # Save to S3
    csv_buffer = io.StringIO()
    interactions.to_csv(csv_buffer, index=False)
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=f"{PLAYGROUND_PREFIX}{email}_interactions.csv",
        Body=csv_buffer.getvalue(),
    )


def get_playground_interactions(email: str = None) -> pd.DataFrame:
    """Retrieve playground interactions, optionally filtered by email."""
    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET, Key=f"{PLAYGROUND_PREFIX}{email}_interactions.csv"
        )
        df = pd.read_csv(io.BytesIO(response["Body"].read()))

        if email:
            df = df[df["email"] == email]

        # Convert JSON string back to dict and normalize
        df["parameters"] = df["parameters"].apply(json.loads)
        params_df = pd.json_normalize(df["parameters"].tolist())
        df = pd.concat([df.drop("parameters", axis=1), params_df], axis=1)

        return df
    except:
        return pd.DataFrame()
