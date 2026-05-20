from datetime import datetime
from datetime import timedelta

from jose import jwt

from passlib.context import CryptContext

from backend.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):

    return pwd_context.hash(password)

def verify_password(password, hashed_password):

    return pwd_context.verify(
        password,
        hashed_password
    )

def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.utcnow() + timedelta(hours=12)

    payload.update({
        "exp": expire
    })

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return token
