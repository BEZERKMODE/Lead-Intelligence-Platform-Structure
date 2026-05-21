class DLPTargetEngine:

    TARGET_SIGNALS = [

        "Office365",
        "Google Workspace",
        "Remote Workforce",
        "Cloud Storage",
        "BYOD",
        "USB Usage",
        "Customer Data",
        "Healthcare Data",
        "Financial Data"
    ]

    @staticmethod
    def analyze(company):

        score = 0

        technologies = company.get(
            "technologies",
            []
        )

        for signal in DLPTargetEngine.TARGET_SIGNALS:

            if signal in technologies:
                score += 10

        if company.get("employees", 0) > 100:
            score += 20

        if company.get("multiple_branches"):
            score += 20

        return {
            "dlp_score": min(score, 100),

            "best_products": [

                "Forcepoint DLP",
                "Symantec DLP",
                "Microsoft Purview",
                "Trend Micro DLP",
                "Endpoint Protector"
            ]
        }
