import requests

from backend.config import settings


class IPInfoService:

    BASE_URL = "https://ipinfo.io"

    def __init__(self):
        self.token = settings.IPINFO_API_TOKEN

    def fetch_ip_data(self, ip_address):
        if not self.token:
            return {"error": "IPInfo API token not configured"}

        try:
            response = requests.get(
                f"{self.BASE_URL}/{ip_address}/json",
                params={"token": self.token},
                timeout=20
            )
            return response.json()
        except Exception as exc:
            return {"error": str(exc)}
