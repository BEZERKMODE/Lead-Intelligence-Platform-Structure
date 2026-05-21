import requests

from backend.config import settings


class ApolloProvider:

    BASE_URL = "https://api.apollo.io/api/v1"

    def search_companies(
        self,
        city,
        sector,
        country="India"
    ):

        payload = {

            "api_key": settings.APOLLO_API_KEY,

            "person_locations": [city],

            "organization_locations": [city],

            "organization_num_employees_ranges": [
                "11,50",
                "51,200",
                "201,500",
                "501,1000"
            ],

            "organization_industry_tag_ids": [
                sector
            ],

            "organization_locations_country": country
        }

        response = requests.post(
            f"{self.BASE_URL}/mixed_companies/search",
            json=payload,
            timeout=60
        )

        return response.json()
