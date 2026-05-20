class CompanyClassifier:

    def classify(
        self,
        company
    ):

        industry = company.get("industry", "").lower()

        if "cybersecurity" in industry:
            return "Cybersecurity"

        if "fintech" in industry:
            return "FinTech"

        if "saas" in industry:
            return "SaaS"

        return "General"
