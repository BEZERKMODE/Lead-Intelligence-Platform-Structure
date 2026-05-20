import re
import requests

from bs4 import BeautifulSoup

EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

PHONE_REGEX = r"\+?\d[\d\s\-\(\)]{8,20}\d"

class CompanyContactScraper:

    def scrape_company_contacts(self, url):

        response = requests.get(
            url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(" ")

        emails = list(set(
            re.findall(EMAIL_REGEX, text)
        ))

        phones = list(set(
            re.findall(PHONE_REGEX, text)
        ))

        return {
            "website": url,
            "emails": emails,
            "phones": phones
        }
