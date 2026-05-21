SECTOR_KEYWORDS = {

    "FinTech": [
        "bank",
        "finance",
        "insurance",
        "payments",
        "nbfc"
    ],

    "Healthcare": [
        "hospital",
        "pharma",
        "medical",
        "diagnostics"
    ],

    "SaaS": [
        "software",
        "cloud",
        "platform",
        "saas"
    ],

    "Cybersecurity": [
        "security",
        "soc",
        "firewall",
        "endpoint"
    ],

    "Manufacturing": [
        "factory",
        "industrial",
        "manufacturing"
    ],

    "Retail": [
        "ecommerce",
        "retail",
        "shopping"
    ]
}


class SectorClassifier:

    @staticmethod
    def classify(text):

        text = text.lower()

        matches = {}

        for sector, keywords in SECTOR_KEYWORDS.items():

            score = 0

            for keyword in keywords:

                if keyword in text:
                    score += 1

            matches[sector] = score

        return sorted(
            matches.items(),
            key=lambda x: x[1],
            reverse=True
        )[0]
