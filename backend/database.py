import sqlite3
import os
import sys
from datetime import datetime

# Ensure parent directory is in sys.path so 'backend' package imports work seamlessly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Ensure static uploads folder exists
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create leads table with security columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            domain TEXT NOT NULL UNIQUE,
            sector TEXT,
            location TEXT,
            latitude REAL,
            longitude REAL,
            revenue TEXT,
            employees TEXT,
            technologies TEXT,
            contacts TEXT,
            priority_score INTEGER,
            ai_match_rate INTEGER,
            growth_trend TEXT,
            status TEXT DEFAULT 'New',
            last_scraped TEXT,
            notes TEXT,
            security_score TEXT DEFAULT 'A',
            subdomains TEXT,
            vulnerabilities TEXT,
            phone TEXT
        )
    ''')
    
    # Run dynamic migrations to add new columns if table already exists
    for col, type_name in [('security_score', 'TEXT DEFAULT "A"'), ('subdomains', 'TEXT'), ('vulnerabilities', 'TEXT'), ('phone', 'TEXT')]:
        try:
            cursor.execute(f"ALTER TABLE leads ADD COLUMN {col} {type_name}")
        except sqlite3.OperationalError:
            pass # Column already exists
    
    # Check if table is empty, if so, seed it with premium leads
    cursor.execute('SELECT COUNT(*) FROM leads')
    count = cursor.fetchone()[0]
    
    if count == 0:
        seed_leads = [
            (
                "Stripe", "stripe.com", "Finance & Fintech", "San Francisco, CA", 
                37.7749, -122.4194, "$14B", "5,000-10,000",
                "React, AWS, Redis, Ruby, PostgreSQL, Stripe Billing", 
                "collins@stripe.com (Patrick Collins, CEO), patrick@stripe.com (Patrick Collison, Co-founder)", 
                96, 98, "High Growth", "SQL", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Top tier target. High fit for core CRM integration. Needs custom outreach for enterprise billing features."
            ),
            (
                "Vercel", "vercel.com", "Technology & SaaS", "New York, NY", 
                40.7128, -74.0060, "$150M", "500-1,000",
                "Next.js, React, Node.js, AWS, TailwindCSS, MongoDB", 
                "guillermo@vercel.com (Guillermo Rauch, CEO)", 
                88, 92, "High Growth", "Enriched", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "High growth hosting/frontend tool. Good fit for cloud developer toolkit. Already utilizing advanced webhooks."
            ),
            (
                "Canva", "canva.com", "Design & SaaS", "Sydney, Australia", 
                -33.8688, 151.2093, "$2B", "1,000-5,000",
                "React, Java, AWS, Kubernetes, Cloudflare, Swift", 
                "melanie@canva.com (Melanie Perkins, CEO), cliff@canva.com (Cliff Obrecht, COO)", 
                91, 95, "High Growth", "Contacted", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Excellent fit for marketing team asset synchronization. Reach out regarding new visual collaboration integrations."
            ),
            (
                "Spotify", "spotify.com", "Entertainment & Media", "Stockholm, Sweden", 
                59.3293, 18.0686, "$12B", "5,000-10,000",
                "Python, Java, Google Cloud, PostgreSQL, Docker, C++", 
                "daniel@spotify.com (Daniel Ek, CEO)", 
                78, 80, "Stable", "New", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Large enterprise, long sales cycle. Potential expansion into audio advertising platforms."
            ),
            (
                "Hugging Face", "huggingface.co", "AI & Developer Tools", "Paris, France", 
                48.8566, 2.3522, "$50M", "100-250",
                "Python, PyTorch, Svelte, AWS, TailwindCSS, PostgreSQL", 
                "clement@huggingface.co (Clement Delangue, CEO)", 
                94, 97, "High Growth", "SQL", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Major AI catalyst. High priority developer partnership candidate. Monitor active repo expansions."
            ),
            (
                "Linear", "linear.app", "Technology & SaaS", "San Francisco, CA", 
                37.7749, -122.4300, "$20M", "50-100",
                "React, Next.js, GraphQL, PostgreSQL, Node.js", 
                "karri@linear.app (Karri Saarinen, CEO)", 
                89, 94, "High Growth", "Enriched", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Extremely fast-growing project management tool. Seeded prospect with potential high-tier plan requirements."
            ),
            (
                "Monzo", "monzo.com", "Finance & Fintech", "London, UK", 
                51.5074, -0.1278, "$400M", "1,000-5,000",
                "Go, Cassandra, AWS, Kubernetes, React, Python", 
                "tsal@monzo.com (TS Anil, CEO)", 
                84, 86, "High Growth", "New", 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Digital-first bank. High potential for automated compliance workflows and customer communication tooling."
            )
        ]
        
        cursor.executemany('''
            INSERT INTO leads (
                company_name, domain, sector, location, 
                latitude, longitude, revenue, employees, 
                technologies, contacts, priority_score, 
                ai_match_rate, growth_trend, status, 
                last_scraped, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_leads)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
