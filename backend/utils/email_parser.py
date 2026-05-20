class EmailParser:

    def parse(
        self,
        email
    ):

        username, domain = email.split("@")

        return {
            "username": username,
            "domain": domain
        }
