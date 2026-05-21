import re

from backend.services.twilio_lookup import TwilioLookup


class PhoneDiscoveryEngine:

    PHONE_REGEX = [

        r"\+91[\-\s]?[6-9]\d{9}",

        r"[6-9]\d{9}",

        r"\d{3,5}[\-\s]\d{6,8}"
    ]

    def discover(
        self,
        text
    ):

        numbers = set()

        for pattern in self.PHONE_REGEX:

            found = re.findall(
                pattern,
                text
            )

            for number in found:

                numbers.add(number)

        validated = []

        twilio = TwilioLookup()

        for number in numbers:

            result = twilio.validate_phone(
                number
            )

            if result.get("valid"):

                validated.append(number)

        return validated
