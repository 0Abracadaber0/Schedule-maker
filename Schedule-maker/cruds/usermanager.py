import uuid
from typing import (
    Optional
)

from fastapi import (
    Depends,
    Request
)
from fastapi.security import (
    OAuth2PasswordRequestForm
)
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    models,
    exceptions
)

from secure import (
    SECRET,
    password_helper
)
from models import (
    User
)
from models import (
    get_user_db,
    db_get_by_username
)


class UserManager(IntegerIDMixin, BaseUserManager[User, uuid.uuid4]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        print(f'User {user.id} has registered')

    @staticmethod
    async def get_by_username(user_username: str) -> models.UP:
        """
        Get a user by username.
        :param user_username: username of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await db_get_by_username(user_username)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following an email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    yield UserManager(user_db, password_helper)
