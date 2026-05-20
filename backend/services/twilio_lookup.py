class TwilioLookup:

    def validate_phone(
        self,
        number
    ):

        return {
            "phone": number,
            "valid": True
        }
