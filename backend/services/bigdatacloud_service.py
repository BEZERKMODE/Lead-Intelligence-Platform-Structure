import requests

from backend.config import settings


class BigDataCloudService:

    BASE_URL = "https://api.bigdatacloud.net/data"

    def india_location_mapper(self, company_name, city, state):
        if not settings.BIGDATACLOUD_API_KEY:
            return {"city": city, "state": state, "note": "BigDataCloud key not configured"}

        return {
            "city": city,
            "state": state,
            "country": "India",
            "source": "BigDataCloud"
        }

    def enrich_location(self, ip_address):
        if not settings.BIGDATACLOUD_API_KEY:
            return {"error": "BigDataCloud API key not configured"}

        try:
            response = requests.get(
                f"{self.BASE_URL}/ip-geolocation?ip={ip_address}&localityLanguage=en&key={settings.BIGDATACLOUD_API_KEY}",
                timeout=20
            )
            return response.json()
        except Exception as exc:
            return {"error": str(exc)}
