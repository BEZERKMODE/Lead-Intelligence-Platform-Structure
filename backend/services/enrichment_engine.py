import requests

from backend.config import settings

class EnrichmentEngine:

    def enrich_company(self, domain):

        headers = {
            "Cache-Control": "no-cache"
        }

        params = {
            "api_key": settings.APOLLO_API_KEY,
            "domain": domain
        }

        response = requests.get(
            "https://api.apollo.io/v1/organizations/enrich",
            headers=headers,
            params=params
        )

        return response.json()
