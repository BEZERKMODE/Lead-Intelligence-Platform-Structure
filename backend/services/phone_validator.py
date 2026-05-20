import phonenumbers

class PhoneValidator:

    def validate_phone(self, number):

        try:

            parsed = phonenumbers.parse(
                number,
                None
            )

            return phonenumbers.is_valid_number(parsed)

        except Exception:

            return False
