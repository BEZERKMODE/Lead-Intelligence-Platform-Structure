import requests

from backend.config import settings


class ApolloEnterprise:

    BASE_URL = "https://api.apollo.io/api/v1"

    def __init__(self):
        self.api_key = settings.APOLLO_API_KEY

    def search_company(self, domain):
        if not self.api_key:
            return {"error": "Apollo API key not configured"}

        payload = {
            "api_key": self.api_key,
            "domain": domain
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/mixed_companies/search",
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as exc:
            return {"error": str(exc)}

    def search_company_contacts(self, company_name):
        if not self.api_key:
            return {"error": "Apollo API key not configured"}

        payload = {
            "api_key": self.api_key,
            "company_name": company_name
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/mixed_contacts/search",
                json=payload,
                timeout=30
            )
            return response.json()
        except Exception as exc:
            return {"error": str(exc)}
