class LeadRanker:

    def rank(
        self,
        leads
    ):

        ranked = sorted(
            leads,
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        return ranked
