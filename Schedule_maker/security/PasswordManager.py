from passlib.context import CryptContext


from .pwd import pwd_context


class PasswordManager:
    def __init__(self, _pwd_context):
        self.pwd_context: CryptContext = _pwd_context

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


password_manager = PasswordManager(pwd_context)
