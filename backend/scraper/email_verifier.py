import re
import socket
import smtplib
try:
    import dns.resolver
    dns_available = True
except ImportError:
    dns_available = False

class EmailVerifier:
    @staticmethod
    def is_valid_syntax(email):
        """Perform simple regex verification on email syntax."""
        pattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
        return re.match(pattern, email) is not None

    @staticmethod
    def get_mx_records(domain):
        """Query DNS records to find the mail servers (MX) for the domain."""
        if not dns_available:
            return [domain]
        try:
            records = dns.resolver.resolve(domain, 'MX')
            mx_hosts = [str(r.exchange).rstrip('.') for r in records]
            # Sort by preference/priority is managed automatically by dnspython,
            # but we can sort based on priority attribute if needed.
            sorted_records = sorted(records, key=lambda r: r.preference)
            return [str(r.exchange).rstrip('.') for r in sorted_records]
        except Exception:
            # Fallback to domain hostname itself if MX lookup fails
            return [domain]

    @staticmethod
    def verify_smtp_handshake(email):
        """
        Connect to mail exchange server and run simulated mail sending transaction.
        Returns:
            dict: { 'success': bool, 'status': str, 'code': int }
        """
        if not EmailVerifier.is_valid_syntax(email):
            return {"success": False, "status": "Invalid Syntax", "code": 400}

        domain = email.split('@')[1]
        mx_servers = EmailVerifier.get_mx_records(domain)

        if not mx_servers:
            return {"success": False, "status": "No Mail Exchange Servers Found", "code": 404}

        # Try connecting to the mail servers
        for mx in mx_servers:
            try:
                # 5-second socket timeout to prevent long hangs on unresponsive mailers
                server = smtplib.SMTP(timeout=5)
                server.connect(mx, 25)
                
                # Introduce ourselves to mail server
                server.helo(socket.gethostname())
                
                # Set sender address
                server.mail("verify-outreach@kinstechnology.com")
                
                # Run recipient check (RCPT TO)
                code, message = server.rcpt(email)
                server.quit()

                # SMTP code 250 represents successful transaction, mailbox exists
                # SMTP code 251 or 252 represents forwarding/unverifiable but mailbox active
                if code == 250:
                    return {"success": True, "status": "Verified Active", "code": code}
                elif code in [251, 252]:
                    return {"success": True, "status": "Forwarded/Active", "code": code}
                elif code == 550:
                    return {"success": False, "status": "Mailbox Does Not Exist (550)", "code": code}
                else:
                    return {"success": False, "status": f"Server Refused Connection ({code})", "code": code}

            except (socket.timeout, socket.error):
                # Try the next server in priority list
                continue
            except Exception as e:
                # Other SMTP/parsing errors, try next server
                continue

        # If all mail servers were unresponsive, mark as Unverifiable
        return {"success": False, "status": "Mail Servers Timeout/Unreachable", "code": 500}
