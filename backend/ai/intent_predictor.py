class IntentPredictor:

    def predict(
        self,
        company_data
    ):

        score = 0

        if company_data.get("funding"):
            score += 30

        if company_data.get("security_hiring"):
            score += 30

        if company_data.get("cloud_growth"):
            score += 20

        if company_data.get("uses_enterprise_tools"):
            score += 20

        return {
            "intent_score": min(score, 100)
        }
