class LeadModel:
    def __init__(self, data):
        self.id = data.get('id')
        self.company_name = data.get('company_name', '')
        self.domain = data.get('domain', '')
        self.sector = data.get('sector', 'Unknown')
        self.location = data.get('location', 'Global')
        self.latitude = data.get('latitude', 0.0)
        self.longitude = data.get('longitude', 0.0)
        self.revenue = data.get('revenue', '$0M')
        self.employees = data.get('employees', '1-10')
        self.technologies = data.get('technologies', '') # comma separated
        self.contacts = data.get('contacts', '') # JSON or comma separated string
        self.priority_score = data.get('priority_score', 0)
        self.ai_match_rate = data.get('ai_match_rate', 0)
        self.growth_trend = data.get('growth_trend', 'Stable')
        self.status = data.get('status', 'New')
        self.last_scraped = data.get('last_scraped', '')
        self.notes = data.get('notes', '')
        self.security_score = data.get('security_score', 'A')
        self.subdomains = data.get('subdomains', '')
        self.vulnerabilities = data.get('vulnerabilities', '')
        self.phone = data.get('phone', '')

    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'domain': self.domain,
            'sector': self.sector,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'revenue': self.revenue,
            'employees': self.employees,
            'technologies': [t.strip() for t in self.technologies.split(',')] if self.technologies else [],
            'contacts': self.contacts,
            'priority_score': self.priority_score,
            'ai_match_rate': self.ai_match_rate,
            'growth_trend': self.growth_trend,
            'status': self.status,
            'last_scraped': self.last_scraped,
            'notes': self.notes,
            'security_score': self.security_score,
            'subdomains': [s.strip() for s in self.subdomains.split(',')] if self.subdomains else [],
            'vulnerabilities': [v.strip() for v in self.vulnerabilities.split(',')] if self.vulnerabilities else [],
            'phone': self.phone
        }
