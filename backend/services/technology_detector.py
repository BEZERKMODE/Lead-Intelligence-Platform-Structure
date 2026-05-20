import requests

class TechnologyDetector:

    def detect_stack(self, website):

        technologies = []

        try:

            response = requests.get(
                website,
                timeout=20
            )

            content = response.text.lower()

            if "aws" in content:
                technologies.append("AWS")

            if "cloudflare" in content:
                technologies.append("Cloudflare")

            if "react" in content:
                technologies.append("React")

            if "hubspot" in content:
                technologies.append("HubSpot")

            if "google-analytics" in content:
                technologies.append("Google Analytics")

            return {
                "website": website,
                "technologies": technologies
            }

        except Exception as e:

            return {
                "error": str(e)
            }
