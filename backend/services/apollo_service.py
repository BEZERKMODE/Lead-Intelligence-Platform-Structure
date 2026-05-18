import requests
from backend.config import Config

class ApolloService:
    """
    Apollo.io Intelligence Service
    - organizations/enrich: works on all plans — returns real company data
    - mixed_people/search: requires paid plan — falls back to simulation
    """

    @staticmethod
    def enrich_organization(domain: str):
        """
        Fetch real company data from Apollo using domain.
        Returns dict with: name, industry, employees, city, country, revenue,
        technologies, linkedin_url, phone, founded_year.
        """
        api_key = Config.APOLLO_API_KEY
        if not api_key or api_key.strip() in ('', 'YOUR_APOLLO_API_KEY'):
            return None

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key
        }
        try:
            r = requests.get(
                "https://api.apollo.io/v1/organizations/enrich",
                params={"domain": domain},
                headers=headers,
                timeout=10
            )
            if r.status_code == 200:
                org = r.json().get("organization", {})
                # Extract real technologies
                techs = [t.get("name") for t in org.get("current_technologies", []) if t.get("name")][:8]
                tech_str = ", ".join(techs) if techs else ""

                # Build location from city + country
                city = org.get("city", "")
                country = org.get("country", "")
                location_parts = [p for p in [city, country] if p]
                location = ", ".join(location_parts) if location_parts else ""

                # Format revenue
                revenue_raw = org.get("organization_revenue_printed") or org.get("annual_revenue_printed") or ""
                employees_raw = org.get("estimated_num_employees")
                employees_str = str(employees_raw) if employees_raw else ""

                return {
                    "company_name": org.get("name", ""),
                    "industry": org.get("industry", ""),
                    "employees": employees_str,
                    "location": location,
                    "revenue": revenue_raw,
                    "technologies": tech_str,
                    "linkedin_url": org.get("linkedin_url", ""),
                    "phone": org.get("sanitized_phone", ""),
                    "founded_year": org.get("founded_year", ""),
                    "description": org.get("short_description", ""),
                    "keywords": org.get("keywords", [])[:10],
                    "org_id": org.get("id", "")
                }
            else:
                print(f"[!] Apollo org enrich returned {r.status_code} for {domain}")
                return None
        except Exception as e:
            print(f"[!] Apollo org enrich exception: {e}")
            return None

    @staticmethod
    def search_company(domain: str):
        """Search for people at a company by domain."""
        api_key = Config.APOLLO_API_KEY
        if not api_key or api_key.strip() in ('', 'YOUR_APOLLO_API_KEY'):
            return ApolloService._mock_contacts(domain)

        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key
        }

        # Try people search endpoints (requires paid plan)
        for endpoint in [
            "https://api.apollo.io/v1/mixed_people/search",
            "https://api.apollo.io/v1/people/search"
        ]:
            try:
                r = requests.post(
                    endpoint,
                    json={"q_organization_domains": [domain], "page": 1, "per_page": 5},
                    headers=headers,
                    timeout=10
                )
                if r.status_code == 200 and r.json().get("people"):
                    print(f"[+] Apollo people found at {endpoint} for {domain}")
                    return r.json()
            except Exception as e:
                print(f"[!] {endpoint} error: {e}")

        # Fallback to simulation
        print(f"[!] Apollo people search unavailable for {domain}. Using smart simulation.")
        return ApolloService._mock_contacts(domain)

    @staticmethod
    def _mock_contacts(domain: str):
        return {
            "people": [
                {"name": "Sarah Jenkins", "email": f"sarah.j@{domain}", "title": "Director of IT Operations"},
                {"name": "David Miller",  "email": f"d.miller@{domain}", "title": "Chief Information Security Officer (CISO)"},
                {"name": "James Vance",   "email": f"jvance@{domain}",  "title": "VP of Infrastructure Security"}
            ]
        }

    @staticmethod
    def extract_emails(domain: str):
        data = ApolloService.search_company(domain)
        return [
            {"name": p.get("name"), "email": p.get("email"), "title": p.get("title")}
            for p in data.get("people", [])
            if p.get("email")
        ]
