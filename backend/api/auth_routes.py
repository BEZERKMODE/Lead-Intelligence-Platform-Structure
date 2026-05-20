from fastapi import APIRouter

from backend.auth import create_access_token
from backend.auth import hash_password
from backend.auth import verify_password

router = APIRouter()

fake_users = {}

@router.post("/register")
def register(data: dict):

    email = data.get("email")

    password = hash_password(
        data.get("password")
    )

    fake_users[email] = password

    return {
        "status": "registered"
    }

@router.post("/login")
def login(data: dict):

    email = data.get("email")

    password = data.get("password")

    stored_password = fake_users.get(email)

    if not stored_password:

        return {
            "error": "Invalid user"
        }

    valid = verify_password(
        password,
        stored_password
    )

    if not valid:

        return {
            "error": "Invalid credentials"
        }

    token = create_access_token({
        "sub": email
    })

    return {
        "access_token": token
    }
