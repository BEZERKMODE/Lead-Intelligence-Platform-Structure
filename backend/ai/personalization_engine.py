class PersonalizationEngine:

    def generate_email(
        self,
        first_name,
        company
    ):

        return f"""
Hi {first_name},

I noticed {company} is growing rapidly.

We help companies improve lead intelligence,
contact enrichment, and AI-driven outreach.

Would you like a quick demo?

Best Regards,
Suraj Singh Bartwal
KinsTechnology CyberSecurity Pre-Sales Outreach Team
"""

    @staticmethod
    def generate_outreach_email(company_name, domain, sector, employees, technologies, location, growth_trend, notes=""):
        size_label = "SMB"
        if employees:
            if '5,000' in employees or '10,000' in employees or '1,000' in employees:
                size_label = "Enterprise"
            elif '250' in employees or '500' in employees:
                size_label = "Mid-Market"
                
        email_body = f"""Subject: External Security & Digital Perimeter Review for {company_name}

I hope this message finds you well.

Our analysts at KinsTechnology recently profiled the external digital perimeter for {company_name} ({domain}). As an organization classified under the {sector} sector with an estimated size of {size_label} ({employees}), we've mapped several exposure points regarding active hosts, pre-sales intelligence vectors, and perimeter hygiene.

We would love to share our gathered visual intelligence report with your IT team. Would you be open to a 10-minute brief assessment review next Tuesday?

Best Regards,
Suraj Singh Bartwal
KinsTechnology CyberSecurity Pre-Sales Outreach Team"""
        return email_body.strip()
