class LinkedinScraper:

    def extract_company_profile(
        self,
        linkedin_url
    ):

        return {
            "linkedin_url": linkedin_url,
            "employees": [],
            "company_info": {}
        }
