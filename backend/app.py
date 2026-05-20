import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from backend.api.routes import router

app = FastAPI(
    title="Enterprise Lead Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    from sqlalchemy import text
    from backend.database import Base, engine, SessionLocal
    
    try:
        with engine.begin() as conn:
            if "sqlite" not in engine.url.drivername:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    except Exception as e:
        print(f"Warning: Could not create pgvector extension: {e}")
        
    try:
        from backend.models.company import Company
        from backend.models.contact import Contact
        from backend.models import LeadModel, TenantModel, WorkflowRun
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables initialized successfully!")
        
        # Seed premium data if the table is empty to give a spectacular first impression
        db = SessionLocal()
        try:
            if db.query(LeadModel).count() == 0:
                print("[Seeder] Database is empty. Seeding gorgeous pre-sales outreach profiles...")
                
                stripe_lead = LeadModel(
                    company_name="Stripe",
                    domain="stripe.com",
                    sector="Finance & Fintech",
                    location="South San Francisco, CA",
                    latitude=37.7749,
                    longitude=-122.4194,
                    revenue="$14.3B",
                    employees="8,000+",
                    technologies="React, Ruby on Rails, AWS, Stripe Billing, Redis, Kubernetes",
                    contacts="John Collison <john@stripe.com> (Co-Founder) | Patrick Collison <patrick@stripe.com> (CEO) [VERIFIED]",
                    priority_score=92,
                    ai_match_rate=95,
                    growth_trend="High Growth",
                    status="New",
                    security_score="A",
                    subdomains="api.stripe.com, dashboard.stripe.com, checkout.stripe.com, status.stripe.com",
                    vulnerabilities="Minor: SPF softfail policy active, Missing secure cookie headers on status subdomain",
                    phone="+1 (650) 555-0199",
                    notes="Premium enterprise scale payment provider. Heavy cloud footprint. Highly suitable target for cybersecurity perimeter hygiene review."
                )
                
                vercel_lead = LeadModel(
                    company_name="Vercel",
                    domain="vercel.com",
                    sector="AI & Developer Tools",
                    location="New York, NY",
                    latitude=40.7128,
                    longitude=-74.0060,
                    revenue="$80M",
                    employees="450",
                    technologies="Next.js, React, Node.js, AWS, TailwindCSS, PostgreSQL",
                    contacts="Guillermo Rauch <rauchg@vercel.com> (CEO) [VERIFIED] | Lee Robinson <lee@vercel.com> (VP of DevExp) [VERIFIED]",
                    priority_score=88,
                    ai_match_rate=90,
                    growth_trend="High Growth",
                    status="Enriched",
                    security_score="B",
                    subdomains="api.vercel.com, status.vercel.com, git.vercel.com",
                    vulnerabilities="Missing DMARC policy (spoofing risk), TLS 1.1 enabled on legacy CDN nodes",
                    phone="+1 (212) 555-0145",
                    notes="Developer tool and hosting platform. Heavy integration with GitHub and AWS networks. Ideal target for pre-sales outreach."
                )
                
                linear_lead = LeadModel(
                    company_name="Linear",
                    domain="linear.app",
                    sector="Design & SaaS",
                    location="London, UK",
                    latitude=51.5074,
                    longitude=-0.1278,
                    revenue="$12M",
                    employees="60",
                    technologies="React, TypeScript, Node.js, PostgreSQL, GCP, TailwindCSS",
                    contacts="Karri Saarinen <karri@linear.app> (CEO) [VERIFIED] | Jori Lallo <jori@linear.app> (Co-Founder) [VERIFIED]",
                    priority_score=84,
                    ai_match_rate=82,
                    growth_trend="High Growth",
                    status="SQL",
                    security_score="A",
                    subdomains="api.linear.app, dev.linear.app, web.linear.app",
                    vulnerabilities="Minor: SPF softfail policy active",
                    phone="+44 20 7946 0958",
                    notes="Premium issue tracker for modern tech companies. Clean, fast software stack. Great candidate for standard CRM sync."
                )
                
                db.add(stripe_lead)
                db.add(vercel_lead)
                db.add(linear_lead)
                db.commit()
                print("[Seeder] Successfully seeded 3 gorgeous accounts into database!")
        finally:
            db.close()
            
    except Exception as e:
        print(f"Error initializing database tables or seeding: {e}")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=5003, reload=True)
