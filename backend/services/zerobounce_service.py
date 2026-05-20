import requests

from backend.config import settings

class ZeroBounceService:

    def validate_email(
        self,
        email
    ):

        response = requests.get(
            "https://api.zerobounce.net/v2/validate",
            params={
                "api_key": settings.ZEROBOUNCE_API_KEY,
                "email": email
            }
        )

        return response.json()
