import requests

class GeoScraper:

    def discover_companies(
        self,
        keyword,
        location
    ):

        query = f"{keyword} companies in {location}"

        return {
            "query": query,
            "companies_found": []
        }
