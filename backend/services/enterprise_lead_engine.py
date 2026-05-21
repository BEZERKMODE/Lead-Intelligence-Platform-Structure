import re
import dns.resolver
import smtplib
import requests

from bs4 import BeautifulSoup

from backend.services.apollo_enterprise import ApolloEnterprise
from backend.services.technology_detector import TechnologyDetector
from backend.services.openai_intelligence import OpenAIIntelligence
from backend.services.bigdatacloud_service import BigDataCloudService
from backend.services.ipinfo_service import IPInfoService
from backend.config import settings


class EnterpriseLeadEngine:

    EMAIL_REGEX = (
        r"[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}"
    )

    PHONE_REGEX = (
        r"(?:\+91[\-\s]?)?"
        r"(?:0)?"
        r"[6789]\d{9}"
    )

    IMPORTANT_PAGES = [
        "",
        "/contact",
        "/contact-us",
        "/about",
        "/team",
        "/support",
        "/company",
        "/careers",
        "/privacy-policy"
    ]

    def __init__(self):
        self.apollo = ApolloEnterprise()
        self.tech = TechnologyDetector()
        self.ai = OpenAIIntelligence()
        self.geo = BigDataCloudService()
        self.ipinfo = IPInfoService()

    def scrape_website(self, domain):
        found_emails = set()
        found_phones = set()

        for page in self.IMPORTANT_PAGES:
            try:
                url = f"https://{domain}{page}"
                response = requests.get(
                    url,
                    timeout=20,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(" ")

                emails = re.findall(self.EMAIL_REGEX, text)
                phones = re.findall(self.PHONE_REGEX, text)

                for email in emails:
                    if any(x in email.lower() for x in [".png", ".jpg", ".jpeg", ".css", ".js"]):
                        continue
                    found_emails.add(email.lower())

                for phone in phones:
                    phone = phone.replace(" ", "").replace("-", "")
                    if len(phone) >= 10:
                        found_phones.add(phone)
            except Exception:
                continue

        return {"emails": list(found_emails), "phones": list(found_phones)}

    def smtp_validate(self, email):
        try:
            domain = email.split("@")[1]
            mx_records = dns.resolver.resolve(domain, "MX")
            mx_record = str(mx_records[0].exchange)
            server = smtplib.SMTP(timeout=10)
            server.connect(mx_record)
            server.helo("example.com")
            server.mail("verify@example.com")
            code, _ = server.rcpt(email)
            server.quit()
            return code == 250
        except Exception:
            return False

    def zerobounce_validate(self, email):
        response = requests.get(
            "https://api.zerobounce.net/v2/validate",
            params={
                "api_key": settings.ZEROBOUNCE_API_KEY,
                "email": email
            },
            timeout=30
        )
        return response.json()

    def score_email(self, smtp_valid, zb_status):
        score = 0
        if smtp_valid:
            score += 50
        if zb_status == "valid":
            score += 50
        return score

    def analyze_company(self, company_name, domain, city, state):
        website_data = self.scrape_website(domain)
        technologies = self.tech.detect_stack(f"https://{domain}")
        apollo_company = self.apollo.search_company(domain)
        apollo_people = self.apollo.search_company_contacts(company_name)

        validated_emails = []
        for email in website_data["emails"]:
            smtp_valid = self.smtp_validate(email)
            zb = self.zerobounce_validate(email)
            final_score = self.score_email(smtp_valid, zb.get("status"))
            validated_emails.append({
                "email": email,
                "smtp_valid": smtp_valid,
                "zerobounce": zb,
                "confidence_score": final_score
            })

        geo = self.geo.india_location_mapper(company_name, city, state)
        ai_analysis = self.ai.analyze_company({
            "company_name": company_name,
            "domain": domain,
            "technologies": technologies,
            "apollo": apollo_company
        })

        return {
            "company_name": company_name,
            "domain": domain,
            "geo": geo,
            "emails": validated_emails,
            "phones": website_data["phones"],
            "technologies": technologies,
            "apollo_company": apollo_company,
            "apollo_people": apollo_people,
            "ai_analysis": ai_analysis
        }
