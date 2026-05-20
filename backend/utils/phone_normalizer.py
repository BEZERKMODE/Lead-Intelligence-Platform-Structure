import phonenumbers

class PhoneNormalizer:

    def normalize(
        self,
        phone
    ):

        parsed = phonenumbers.parse(
            phone,
            None
        )

        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )
