import requests

from bs4 import BeautifulSoup

class AIWebScraper:

    def scrape_page(self, url):

        response = requests.get(
            url,
            timeout=30
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.title.text if soup.title else None

        return {
            "url": url,
            "title": title,
            "content_length": len(soup.text)
        }
