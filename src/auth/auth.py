from ..config import PASSWORD


def authenticate_user(email: str, password: str) -> tuple[bool, str]:
    """
    Authenticate a user with email and password.
    Returns a tuple of (success: bool, message: str)
    """
    if not email or not password:
        return False, "Please enter both email and password to continue."

    if password != PASSWORD:
        return False, "Incorrect password. Please try again."

    return True, "Authentication successful"
