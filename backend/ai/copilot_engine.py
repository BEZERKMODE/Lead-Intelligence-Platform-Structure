class CopilotEngine:

    def query(
        self,
        prompt
    ):

        return {
            "query": prompt,
            "recommended_companies": [],
            "recommended_contacts": [],
            "ai_summary": "Top AI-ranked companies returned."
        }
