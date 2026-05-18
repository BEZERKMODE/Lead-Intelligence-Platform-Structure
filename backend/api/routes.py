from flask import Blueprint, jsonify, request, Response, stream_with_context
import json
import csv
import io
from datetime import datetime
import random
from backend.database import get_db_connection
from backend.models import LeadModel
from backend.scraper.scraper import LeadScraper
from backend.ai_engine import AIEngine

api_bp = Blueprint('api', __name__)

@api_bp.route('/leads', methods=['GET'])
def get_leads():
    # Parsing query params
    search = request.args.get('search', '').strip()
    sector = request.args.get('sector', '').strip()
    status = request.args.get('status', '').strip()
    sort_by = request.args.get('sort_by', 'priority_score').strip()
    order = request.args.get('order', 'desc').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM leads WHERE 1=1"
    params = []
    
    if search:
        query += " AND (company_name LIKE ? OR domain LIKE ? OR technologies LIKE ? OR location LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param, search_param])
        
    if sector:
        query += " AND sector = ?"
        params.append(sector)
        
    if status:
        query += " AND status = ?"
        params.append(status)
        
    # Security check for sorting columns
    allowed_sort = ['id', 'company_name', 'domain', 'priority_score', 'ai_match_rate', 'status', 'revenue']
    if sort_by not in allowed_sort:
        sort_by = 'priority_score'
        
    if order not in ['asc', 'desc']:
        order = 'desc'
        
    query += f" ORDER BY {sort_by} {order.upper()}"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    leads = [LeadModel(dict(row)).to_dict() for row in rows]
    return jsonify(leads)

@api_bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"error": "Lead not found"}), 404
        
    return jsonify(LeadModel(dict(row)).to_dict())

@api_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.json or {}
    domain = data.get('domain', '').strip().lower()
    company_name = data.get('company_name', '').strip()
    
    if not domain:
        return jsonify({"error": "Domain is required"}), 400
        
    if not company_name:
        company_name = domain.split('.')[0].capitalize()
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if duplicate
    cursor.execute("SELECT id FROM leads WHERE domain = ?", (domain,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": f"Lead for domain '{domain}' already exists"}), 400
        
    sector = data.get('sector', 'Unknown')
    location = data.get('location', 'Global')
    latitude = float(data.get('latitude', 0.0))
    longitude = float(data.get('longitude', 0.0))
    if latitude == 0.0 and longitude == 0.0:
        latitude, longitude = AIEngine.geocode_location(location)
    revenue = data.get('revenue', '$0M')
    employees = data.get('employees', '1-10')
    technologies = data.get('technologies', '')
    contacts = data.get('contacts', '')
    priority_score = int(data.get('priority_score', 0))
    ai_match_rate = int(data.get('ai_match_rate', 0))
    growth_trend = data.get('growth_trend', 'Stable')
    status = data.get('status', 'New')
    notes = data.get('notes', '')
    last_scraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO leads (
            company_name, domain, sector, location, latitude, longitude,
            revenue, employees, technologies, contacts, priority_score,
            ai_match_rate, growth_trend, status, last_scraped, notes, phone
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        company_name, domain, sector, location, latitude, longitude,
        revenue, employees, technologies, contacts, priority_score,
        ai_match_rate, growth_trend, status, last_scraped, notes, data.get('phone', '')
    ))
    
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"success": True, "lead_id": new_id}), 201

@api_bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    data = request.json or {}
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Lead not found"}), 404
        
    # Prepare updating statement dynamically
    fields = []
    params = []
    
    allowed_fields = [
        'company_name', 'sector', 'location', 'latitude', 'longitude',
        'revenue', 'employees', 'technologies', 'contacts', 'priority_score',
        'ai_match_rate', 'growth_trend', 'status', 'notes',
        'security_score', 'subdomains', 'vulnerabilities', 'phone'
    ]
    
    for field in allowed_fields:
        if field in data:
            fields.append(f"{field} = ?")
            params.append(data[field])
            
    if not fields:
        conn.close()
        return jsonify({"error": "No update fields provided"}), 400
        
    params.append(lead_id)
    update_query = f"UPDATE leads SET {', '.join(fields)} WHERE id = ?"
    
    cursor.execute(update_query, params)
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})

@api_bp.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@api_bp.route('/leads/scrape-stream')
def scrape_stream():
    domain = request.args.get('domain', '').strip()
    if not domain:
        return Response("data: {\"error\": \"Domain is required\"}\n\n", mimetype='text/event-stream')
        
    @stream_with_context
    def generate():
        log_queue = []
        def log_cb(msg, category):
            log_queue.append((msg, category))
            
        # Run enrichment
        try:
            # We want to yield the logs real-time as they are collected
            def yielding_callback(msg, category):
                data = json.dumps({"log": msg, "category": category})
                yield f"data: {data}\n\n"
                
            yield f"data: {json.dumps({'log': f'⚡ Launching scraping cluster for {domain}', 'category': 'start'})}\n\n"
            
            # Since the lead scraper does time.sleep and yields progress,
            # we capture the output.
            # To integrate seamlessly, we feed LeadScraper the callback
            enriched = LeadScraper.enrich_domain(domain, log_callback=yielding_callback)
            
            # Save or Update inside DB
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM leads WHERE domain = ?", (domain,))
            existing = cursor.fetchone()
            
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if existing:
                lead_id = existing[0]
                cursor.execute('''
                    UPDATE leads SET
                        company_name = ?, sector = ?, location = ?, latitude = ?, longitude = ?,
                        revenue = ?, employees = ?, technologies = ?, contacts = ?,
                        priority_score = ?, ai_match_rate = ?, growth_trend = ?,
                        status = ?, last_scraped = ?, notes = ?,
                        security_score = ?, subdomains = ?, vulnerabilities = ?, phone = ?
                    WHERE id = ?
                ''', (
                    enriched['company_name'], enriched['sector'], enriched['location'],
                    enriched['latitude'], enriched['longitude'], enriched['revenue'],
                    enriched['employees'], enriched['technologies'], enriched['contacts'],
                    enriched['priority_score'], enriched['ai_match_rate'], enriched['growth_trend'],
                    enriched['status'], now_str, enriched['notes'],
                    enriched['security_score'], enriched['subdomains'], enriched['vulnerabilities'],
                    enriched.get('phone', ''),
                    lead_id
                ))
            else:
                cursor.execute('''
                    INSERT INTO leads (
                        company_name, domain, sector, location, latitude, longitude,
                        revenue, employees, technologies, contacts, priority_score,
                        ai_match_rate, growth_trend, status, last_scraped, notes,
                        security_score, subdomains, vulnerabilities, phone
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    enriched['company_name'], enriched['domain'], enriched['sector'],
                    enriched['location'], enriched['latitude'], enriched['longitude'],
                    enriched['revenue'], enriched['employees'], enriched['technologies'],
                    enriched['contacts'], enriched['priority_score'], enriched['ai_match_rate'],
                    enriched['growth_trend'], enriched['status'], now_str, enriched['notes'],
                    enriched['security_score'], enriched['subdomains'], enriched['vulnerabilities'],
                    enriched.get('phone', '')
                ))
                lead_id = cursor.lastrowid
                
            conn.commit()
            conn.close()
            
            # Send final lead data
            yield f"data: {json.dumps({'log': '✅ Lead information saved to local sqlite database.', 'category': 'success', 'lead_id': lead_id})}\n\n"
            yield f"data: {json.dumps({'complete': True, 'lead_id': lead_id})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'log': f'❌ Scraping failed: {str(e)}', 'category': 'error'})}\n\n"
            
    return Response(generate(), mimetype='text/event-stream')

@api_bp.route('/leads/<int:lead_id>/email', methods=['POST'])
def generate_email(lead_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"error": "Lead not found"}), 404
        
    lead = dict(row)
    email = AIEngine.generate_outreach_email(
        company_name=lead['company_name'],
        domain=lead['domain'],
        sector=lead['sector'],
        employees=lead['employees'],
        technologies=lead['technologies'],
        location=lead['location'],
        growth_trend=lead['growth_trend'],
        notes=lead['notes']
    )
    
    return jsonify({"email": email})

@api_bp.route('/leads/<int:lead_id>/sync', methods=['POST'])
def sync_crm(lead_id):
    target_crm = request.json.get('crm', 'Salesforce').strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT company_name, domain FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({"error": "Lead not found"}), 404
        
    # Mark lead status as SQL or similar upon sync
    cursor.execute("UPDATE leads SET status = 'SQL' WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    
    # Simulate a highly premium CRM integration token response
    crm_id = f"0018W{random.randint(10000, 99999)}A{random.choice(['A','B','C'])}Q"
    return jsonify({
        "success": True,
        "message": f"Successfully pushed {row['company_name']} ({row['domain']}) to {target_crm}.",
        "crm_record_id": crm_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@api_bp.route('/leads/import', methods=['POST'])
def import_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400
        
    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        
        imported_count = 0
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for row in reader:
            domain = row.get('domain', '').strip().lower()
            if not domain:
                continue
                
            # Skip duplicates
            cursor.execute("SELECT id FROM leads WHERE domain = ?", (domain,))
            if cursor.fetchone():
                continue
                
            company_name = row.get('company_name', '').strip() or domain.split('.')[0].capitalize()
            sector = row.get('sector', 'Unknown').strip()
            location = row.get('location', 'Global').strip()
            revenue = row.get('revenue', '$0M').strip()
            employees = row.get('employees', '1-10').strip()
            technologies = row.get('technologies', '').strip()
            contacts = row.get('contacts', '').strip()
            
            lat, lng = AIEngine.geocode_location(location)
            cursor.execute('''
                INSERT INTO leads (
                    company_name, domain, sector, location, latitude, longitude,
                    revenue, employees, technologies, contacts, priority_score,
                    ai_match_rate, growth_trend, status, last_scraped, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 'Stable', 'New', '', 'Imported via bulk CSV loader.')
            ''', (company_name, domain, sector, location, lat, lng, revenue, employees, technologies, contacts))
            imported_count += 1
            
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "imported_count": imported_count})
    except Exception as e:
        return jsonify({"error": f"Failed to parse CSV: {str(e)}"}), 400

@api_bp.route('/analytics', methods=['GET'])
def get_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. High level statistics
    cursor.execute("SELECT COUNT(*) FROM leads")
    total_leads = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM leads WHERE priority_score >= 80")
    highly_qualified = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(priority_score) FROM leads WHERE priority_score > 0")
    avg_score = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM leads WHERE status = 'SQL'")
    synced_crm_count = cursor.fetchone()[0]
    
    # 2. Sector splits
    cursor.execute("SELECT sector, COUNT(*) as count FROM leads GROUP BY sector ORDER BY count DESC")
    sector_split = {row['sector']: row['count'] for row in cursor.fetchall()}
    
    # 3. Status Funnel
    cursor.execute("SELECT status, COUNT(*) as count FROM leads GROUP BY status")
    status_funnel = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # 4. Key Technologies
    cursor.execute("SELECT technologies FROM leads WHERE technologies != ''")
    tech_counts = {}
    for row in cursor.fetchall():
        tech_list = [t.strip() for t in row['technologies'].split(',')]
        for tech in tech_list:
            if tech:
                tech_counts[tech] = tech_counts.get(tech, 0) + 1
                
    sorted_techs = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:6]
    top_techs = {k: v for k, v in sorted_techs}
    
    conn.close()
    
    return jsonify({
        "metrics": {
            "total_leads": total_leads,
            "highly_qualified": highly_qualified,
            "avg_priority_score": round(avg_score, 1),
            "synced_crm_count": synced_crm_count
        },
        "sector_split": sector_split,
        "status_funnel": status_funnel,
        "top_technologies": top_techs
    })

@api_bp.route('/apollo/<path:domain>', methods=['GET'])
def apollo_lookup(domain):
    from backend.services.apollo_service import ApolloService
    results = ApolloService.extract_emails(domain)
    return jsonify({
        "domain": domain,
        "results": results
    })
