import requests

from backend.config import settings

class ApolloService:

    def search_people(
        self,
        company
    ):

        response = requests.post(
            "https://api.apollo.io/v1/mixed_people/search",
            json={
                "q_organization_name": company,
                "api_key": settings.APOLLO_API_KEY
            }
        )

        return response.json()
