import dns.resolver
import smtplib

class EmailValidator:

    def validate_email(self, email):

        try:

            domain = email.split("@")[1]

            mx_records = dns.resolver.resolve(
                domain,
                "MX"
            )

            mx_record = str(
                mx_records[0].exchange
            )

            server = smtplib.SMTP(timeout=10)

            server.connect(mx_record)

            server.helo("example.com")

            server.mail("verify@example.com")

            code, _ = server.rcpt(email)

            server.quit()

            return code == 250

        except Exception:

            return False
