from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST
from uuid import uuid4

from models import User, Token
from secure import pwd_context



