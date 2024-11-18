import bcrypt
from tri_api.support.config import CONFIGURATION


def hash_password(password: str) -> str:
    """Return a salted password hash."""
    return bcrypt.hashpw(
        password.encode(),
        CONFIGURATION.secret_salt,
    ).decode()
