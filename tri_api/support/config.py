from decouple import config
from pydantic import BaseModel
from tri_api.support.enums import MongoOption


class Settings(BaseModel):
    """Server config settings."""

    root_url: str = config("ROOT_URL", default="http://localhost:8080")

    # Mongo Engine settings
    mongo_uri: str = (
        f"mongodb://{MongoOption.username.value}:{MongoOption.password.value}@{MongoOption.host.value}:{MongoOption.port.value}/"
    )

    # Security settings
    authorization_jwt_secret_key: str = config("AUTHORIZATION_JWT_SECRET_KEY")
    secret_salt: bytes = config("SECRET_SALT").encode()

    # Super User
    super_user_login_key: str = config("SUPER_USER_LOGIN_KEY")
    super_user_secret_key: str = config("SUPER_USER_SECRET_KEY")
    super_user_secret_token: str = config("SUPER_USER_SECRET_TOKEN")

    # FastMail SMTP server settings
    mail_console: bool = config("MAIL_CONSOLE", default=False, cast=bool)
    mail_server: str = config("MAIL_SERVER", default="smtp.myserver.io")
    mail_port: int = config("MAIL_PORT", default=587, cast=int)
    mail_username: str = config("MAIL_USERNAME", default="")
    mail_password: str = config("MAIL_PASSWORD", default="")
    mail_sender: str = config("MAIL_SENDER", default="noreply@myserver.io")


CONFIGURATION = Settings()
