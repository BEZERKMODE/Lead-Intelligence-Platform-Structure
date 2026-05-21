class CybersecurityOpportunityEngine:

    HIGH_VALUE_TECH = [

        "AWS",
        "Azure",
        "Google Cloud",
        "Kubernetes",
        "Office365",
        "Docker",
        "Cisco",
        "VMware"
    ]

    SECURITY_GAPS = [

        "No WAF",
        "No DLP",
        "No Email Security",
        "No Endpoint Protection",
        "Weak SPF",
        "Weak DMARC"
    ]

    @staticmethod
    def calculate(company):

        score = 0

        technologies = company.get(
            "technologies",
            []
        )

        for tech in technologies:

            if tech in CybersecurityOpportunityEngine.HIGH_VALUE_TECH:
                score += 10

        if company.get("employee_count", 0) > 200:
            score += 20

        if company.get("uses_cloud"):
            score += 15

        if company.get("remote_workforce"):
            score += 10

        if company.get("multiple_locations"):
            score += 15

        return {
            "opportunity_score": min(score, 100),
            "recommended_services": [

                "DLP",
                "Email Security",
                "Firewall",
                "Endpoint Protection",
                "Cloud Security",
                "VAPT",
                "SOC Monitoring"
            ]
        }
