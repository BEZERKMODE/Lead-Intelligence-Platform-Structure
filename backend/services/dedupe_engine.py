from rapidfuzz import fuzz

class DedupeEngine:

    def is_duplicate(
        self,
        email_1,
        email_2
    ):

        similarity = fuzz.ratio(
            email_1,
            email_2
        )

        return similarity >= 90
