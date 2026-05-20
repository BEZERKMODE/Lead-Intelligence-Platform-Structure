import requests

from backend.config import settings

class HubspotSync:

    def sync_contact(self, data):

        headers = {
            "Authorization": f"Bearer {settings.HUBSPOT_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/contacts",
            headers=headers,
            json=data
        )

        return response.json()
