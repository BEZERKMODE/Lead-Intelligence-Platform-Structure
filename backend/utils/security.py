import secrets

class SecurityUtils:

    def generate_api_key(self):

        return secrets.token_hex(32)
