import smtplib

class SMTPChecker:

    def check(
        self,
        host
    ):

        try:

            server = smtplib.SMTP(
                host,
                timeout=10
            )

            server.quit()

            return True

        except Exception:

            return False
