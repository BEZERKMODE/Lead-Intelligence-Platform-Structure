import time
import random
from backend.config import settings

class AIEngine:
    @staticmethod
    def calculate_match_rate(sector, technologies, employees):
        # A simple deterministic rule-based ML simulation
        # High value indicators: SaaS/Tech/AI sectors, cloud hosting, payment portals
        score = 65 # baseline
        
        techs_lower = [t.lower().strip() for t in technologies.split(',')] if technologies else []
        
        # Sector weighting
        if sector in ['Technology & SaaS', 'AI & Developer Tools', 'Finance & Fintech']:
            score += 15
        elif sector in ['Design & SaaS']:
            score += 10
            
        # Tech stack weighting
        high_value_techs = ['react', 'next.js', 'aws', 'postgresql', 'stripe', 'pytorch', 'kubernetes', 'go']
        for tech in techs_lower:
            if tech in high_value_techs:
                score += 3
                
        # Size weighting
        if employees in ['100-250', '250-500', '500-1,000']:
            score += 8
        elif employees in ['1,000-5,000', '5,000-10,000']:
            score += 5
            
        # Cap at 99
        return min(max(score, 45), 99)

    @staticmethod
    def calculate_priority_score(match_rate, growth_trend):
        # Base priority score matches the match rate, plus growth bonus
        score = match_rate
        if growth_trend == 'High Growth':
            score += 5
        elif growth_trend == 'Declining':
            score -= 15
        return min(max(score, 10), 100)

    @staticmethod
    def detect_growth_trend(employees, domain):
        # Simple simulation based on domain length or employees
        if 'ai' in domain or 'app' in domain or employees in ['50-100', '100-250', '500-1,000']:
            return "High Growth"
        return "Stable"

    @staticmethod
    def generate_outreach_email(company_name, domain, sector, employees, technologies, location, growth_trend, notes=""):
        # Returns a highly customized, extremely professional, personalized email template for KinsTechnology
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
        
    @staticmethod
    def mock_rag_search(query):
        # Simulates vector search matching technologies
        recommendations = {
            "analytics": ["Mixpanel", "Amplitude", "Google Analytics 4"],
            "hosting": ["Vercel", "Netlify", "AWS Amplify"],
            "database": ["PostgreSQL", "Supabase", "MongoDB Atlas"],
            "payments": ["Stripe Billing", "Adyen", "Paddle"]
        }
        
        q_lower = query.lower()
        for key, recs in recommendations.items():
            if key in q_lower:
                return {
                    "query": query,
                    "matches": recs,
                    "confidence": 0.94,
                    "explanation": f"Matched vector lookup for developer stack recommendations under Category '{key.capitalize()}'"
                }
                
        return {
            "query": query,
            "matches": ["AWS Cloudfront", "Vercel SDK", "Retool Dashboards"],
            "confidence": 0.72,
            "explanation": "Default vector recommendations for fast-growing SaaS setups"
        }

    @staticmethod
    def geocode_location(location):
        if not location:
            return 37.7749, -122.4194 # San Francisco fallback
            
        location_lower = location.lower().strip()
        
        # 1. Attempt Nominatim OpenStreetMap API with strict user-agent and timeout safeguards
        import urllib.request
        import urllib.parse
        import json
        
        try:
            # Format and quote the query parameters correctly
            url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location)}&format=json&limit=1"
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'KinsTechnologyPreSalesOutreachSuite/2.4.0 (suraj@kinstechnology.com)'
                }
            )
            with urllib.request.urlopen(req, timeout=4) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                if res_data and len(res_data) > 0:
                    lat = float(res_data[0]['lat'])
                    lon = float(res_data[0]['lon'])
                    return lat, lon
        except Exception as e:
            # Gracefully log geocoder exception and fall back to local high-fidelity database
            print(f"[!] Nominatim API geocoding failed: {str(e)}. Using fallback database.")
            
        # 2. Comprehensive global local database fallback
        geo_db = {
            "san francisco": (37.7749, -122.4194),
            "new york": (40.7128, -74.0060),
            "london": (51.5074, -0.1278),
            "paris": (48.8566, 2.3522),
            "stockholm": (59.3293, 18.0686),
            "berlin": (52.5200, 13.4050),
            "tokyo": (35.6762, 139.6503),
            "sydney": (-33.8688, 151.2093),
            "toronto": (43.6532, -79.3832),
            "chicago": (41.8781, -87.6298),
            "mumbai": (19.0760, 72.8777),
            "delhi": (28.6139, 77.2090),
            "bangalore": (12.9716, 77.5946),
            "india": (20.5937, 78.9629),
            "singapore": (1.3521, 103.8198),
            "dublin": (53.3498, -6.2603),
            "amsterdam": (52.3676, 4.9041),
            "seattle": (47.6062, -122.3321),
            "austin": (30.2672, -97.7431),
            "boston": (42.3601, -71.0589),
            "los angeles": (34.0522, -118.2437)
        }
        
        for city, coords in geo_db.items():
            if city in location_lower:
                return coords
                
        # If no match is found, return a randomized slight offset of a default location to prevent exact stacking on the map
        import random
        return 30.0 + random.uniform(-10.0, 10.0), 0.0 + random.uniform(-30.0, 30.0)
