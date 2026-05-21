from backend.services.hunter_service import HunterService
from backend.services.zerobounce_service import ZeroBounceService


class EmailAccuracyEngine:

    def verify(self, domain):

        hunter = HunterService()

        results = hunter.find_emails(domain)

        valid = []

        validator = ZeroBounceService()

        for email in results.get(
            "data",
            {}
        ).get(
            "emails",
            []
        ):

            check = validator.validate_email(
                email["value"]
            )

            if check.get("status") == "valid":

                valid.append({

                    "email": email["value"],

                    "confidence":
                        email.get(
                            "confidence",
                            0
                        )
                })

        return sorted(
            valid,
            key=lambda x: x["confidence"],
            reverse=True
        )
