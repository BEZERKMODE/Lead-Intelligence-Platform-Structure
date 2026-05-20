class IntentEngine:

    def calculate_intent(
        self,
        signals
    ):

        score = 0

        if signals.get("funding_detected"):
            score += 30

        if signals.get("rapid_hiring"):
            score += 20

        if signals.get("cloud_growth"):
            score += 20

        if signals.get("security_hiring"):
            score += 30

        return min(score, 100)
