from urllib.parse import urlparse

class DomainTools:

    def extract_domain(
        self,
        url
    ):

        parsed = urlparse(url)

        return parsed.netloc
