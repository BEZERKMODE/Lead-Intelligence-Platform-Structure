import requests

from backend.config import settings

class HunterService:

    def find_emails(
        self,
        domain
    ):

        response = requests.get(
            "https://api.hunter.io/v2/domain-search",
            params={
                "domain": domain,
                "api_key": settings.HUNTER_API_KEY
            }
        )

        return response.json()
