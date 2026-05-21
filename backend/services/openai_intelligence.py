import openai

from backend.config import settings


class OpenAIIntelligence:

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key

    def analyze_company(self, data):
        if not self.api_key:
            return {"warning": "OpenAI API key not configured"}

        prompt = (
            "Analyze this company profile for India cybersecurity and buying intent. "
            f"Company: {data.get('company_name')}\n"
            f"Domain: {data.get('domain')}\n"
            f"Technologies: {data.get('technologies')}\n"
            f"Apollo data: {data.get('apollo')}\n"
            "Provide a short summary with sector, intent, and recommendation."
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity GTM intelligence assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.2
            )
            return {
                "analysis": response.choices[0].message.content.strip()
            }
        except Exception as exc:
            return {"error": str(exc)}
