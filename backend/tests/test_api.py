import unittest
import sys
import os

# Add parent directory to path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app import create_app
from backend.database import init_db
from backend.ai_engine import AIEngine

class LeadPlatformTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test application context
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        
    def test_analytics_endpoint(self):
        response = self.client.get('/api/analytics')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('metrics', data)
        self.assertIn('total_leads', data['metrics'])
        
    def test_leads_list_endpoint(self):
        response = self.client.get('/api/leads')
        self.assertEqual(response.status_code, 200)
        leads = response.get_json()
        self.assertIsInstance(leads, list)
        if len(leads) > 0:
            self.assertIn('company_name', leads[0])
            self.assertIn('domain', leads[0])
            
    def test_ai_scoring_logic(self):
        # High Suitability sector with React/AWS stack
        match_rate = AIEngine.calculate_match_rate(
            sector="AI & Developer Tools",
            technologies="React, PyTorch, AWS, FastAPI",
            employees="100-250"
        )
        self.assertGreaterEqual(match_rate, 80)
        
        # Test Priority Score estimation
        priority = AIEngine.calculate_priority_score(match_rate, "High Growth")
        self.assertGreaterEqual(priority, match_rate)
        
    def test_outreach_email_generation(self):
        email = AIEngine.generate_outreach_email(
            company_name="Acme Corp",
            domain="acme.com",
            sector="Technology & SaaS",
            employees="100-250",
            technologies="Next.js, TailwindCSS, PostgreSQL",
            location="Chicago, IL",
            growth_trend="High Growth"
        )
        self.assertIn("Acme Corp", email)
        self.assertIn("KinsTechnology", email)
        self.assertIn("Suraj Singh Bartwal", email)
        self.assertIn("Technology & SaaS", email)

if __name__ == '__main__':
    unittest.main()
