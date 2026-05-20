# Lead Intelligence Platform

AI-powered enterprise lead discovery, enrichment, verification, scoring, and analytics platform built with FastAPI, React, PostgreSQL, Celery, Playwright, and AI-driven enrichment pipelines.

---

# Project Overview

Lead Intelligence Platform is designed to:

- discover business leads
- scrape company websites
- extract verified email addresses
- enrich lead data using enterprise APIs
- score and rank leads with AI
- export leads to CRM systems
- provide analytics dashboards
- support scalable asynchronous processing

The platform combines:

```text
SCRAPING + DATABASE ENRICHMENT + SMTP VERIFICATION + AI
```

to achieve high-quality lead intelligence.

---

# Features

## Lead Discovery

- Website crawling
- Contact page crawling
- Sitemap crawling
- Internal link extraction
- JavaScript rendering with Playwright

---

## Email Intelligence

- Regex-based extraction
- Obfuscated email detection
- SMTP verification
- MX record validation
- Catch-all detection
- AI-based best email ranking

---

## Enterprise Enrichment APIs

Integrated with:

- Apollo.io
- Hunter.io
- RocketReach
- People Data Labs

---

## AI Capabilities

- AI lead scoring
- Lead quality prediction
- Intelligent email ranking
- Outreach recommendation generation
- Semantic search with embeddings

---

# Backend Stack

| Technology | Purpose |
|---|---|
| FastAPI | API backend |
| PostgreSQL | Data storage |
| Redis | Task queue |
| Celery | Background jobs |
| SQLAlchemy | Database ORM |
| Playwright | Dynamic scraping |
| ChromaDB | Local vector search |
| Pinecone | Cloud vector search |

---

# Frontend Stack

| Technology | Purpose |
|---|---|
| React | Frontend UI |
| Axios | API requests |
| Chart.js | Analytics visualization |

---

# Architecture

```text
Frontend Dashboard
        ↓
FastAPI Backend
        ↓
Lead Processing Pipeline
        ↓
Website Scraper
        ↓
Apollo / Hunter / RocketReach
        ↓
SMTP Verification
        ↓
AI Lead Ranking
        ↓
PostgreSQL Database
        ↓
Analytics + CRM Export
```

---

# Project Structure

```text
lead-intelligence-platform/
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── scraper/
│   ├── vector_store/
│   ├── ml/
│   ├── middleware/
│   ├── utils/
│   ├── tests/
│   ├── docker/
│   ├── k8s/
│   └── app.py
│
├── frontend-react/
│
├── nginx/
│
├── docs/
│
├── scripts/
│
└── README.md
```

---

# Backend Modules

## API Layer

Handles:
- lead endpoints
- analytics endpoints
- exports
- integrations
- user management

Files:

```text
backend/api/
```

---

## Services Layer

Business logic:
- lead processing
- enrichment
- scoring
- CRM integration
- analytics

Files:

```text
backend/services/
```

---

## Scraper Layer

Responsible for:
- crawling websites
- extracting emails
- JavaScript rendering
- sitemap crawling
- proxy handling

Files:

```text
backend/scraper/
```

---

## Vector Store

Semantic AI search:
- embeddings
- RAG search
- vector similarity

Files:

```text
backend/vector_store/
```

---

## ML Layer

Machine learning:
- lead prediction
- classification
- recommendation engine

Files:

```text
backend/ml/
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-repo/lead-intelligence-platform.git
```

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\\Scripts\\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

# Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost/leads
REDIS_URL=redis://localhost:6379/0

OPENAI_API_KEY=YOUR_OPENAI_KEY

APOLLO_API_KEY=YOUR_APOLLO_KEY
HUNTER_API_KEY=YOUR_HUNTER_KEY
ROCKETREACH_API_KEY=YOUR_ROCKETREACH_KEY
```

---

# Run Backend

```bash
cd backend

uvicorn app:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

---

# Run Celery Worker

```bash
celery -A tasks worker --loglevel=info
```

---

# Frontend Setup

```bash
cd frontend-react

npm install

npm run dev
```

---

# Docker Deployment

## Build & Start Services

```bash
docker-compose up --build
```

---

# pgAdmin 4 Administration Console

The platform includes **pgAdmin 4** in the Docker Compose stack for easy database administration.

## Login Details

- **URL**: [http://localhost:5050](http://localhost:5050)
- **Default Email**: `admin@kinstechnology.com`
- **Default Password**: `supersecurepassword123`

## Auto-Imported Server Connection

A database connection named **Lead Intelligence Database** is pre-configured and automatically registered on the sidebar. You can connect immediately with the following parameters (internally pre-configured):

- **Host Name**: `postgres`
- **Port**: `5432`
- **Maintenance Database**: `lead_intel_db`
- **Username**: `lead_intel_user`
- **Password**: `supersecurepassword123`

---

# Kubernetes Deployment

Apply:

```bash
kubectl apply -f backend/k8s/
```

---

# API Endpoints

## Leads

```http
GET /leads
POST /leads
```

---

## Analytics

```http
GET /analytics/summary
```

---

## Apollo Lookup

```http
GET /apollo/{domain}
```

Example:

```http
GET /apollo/shopify.com
```

---

# Enterprise Email Discovery Flow

```text
Website URL
    ↓
Playwright Rendering
    ↓
Contact Page Crawl
    ↓
Regex Extraction
    ↓
Apollo API
    ↓
Hunter API
    ↓
RocketReach API
    ↓
SMTP Verification
    ↓
AI Ranking
    ↓
Best Verified Email
```

---

# Recommended Enterprise Stack

| Component | Tool |
|---|---|
| Scraping | Playwright |
| Backend | FastAPI |
| Queue | Celery |
| Database | PostgreSQL |
| Cache | Redis |
| Vector Search | Pinecone |
| AI | OpenAI |

---

# Future Improvements

- LinkedIn enrichment
- AI outreach automation
- CRM synchronization
- Email campaign engine
- Multi-tenant SaaS support
- Subscription billing
- Team collaboration
- Lead intent prediction
- Real-time dashboards

---

# Security Recommendations

- Rate limiting
- Proxy rotation
- CAPTCHA handling
- JWT authentication
- Encrypted secrets
- Audit logging
- HTTPS enforcement

---

# License

MIT License

---

# Author

Lead Intelligence Platform Team