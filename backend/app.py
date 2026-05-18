import os
import sys

# Ensure parent directory is in sys.path so 'backend' package imports work seamlessly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask_cors import CORS
from backend.config import Config
from backend.database import init_db
from backend.api.routes import api_bp

def create_app():
    # Make sure database is initialized on startup
    init_db()
    
    # Establish templates & static files relative to backend folder
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')
                
    app.config.from_object(Config)
    CORS(app) # Enable Cross-Origin Resource Sharing
    
    # Register endpoints blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Main dashboard route
    @app.route('/')
    def index():
        return render_template('index.html')
        
    # Top-level Apollo.io lookup endpoint mapping — path: allows dots in domain names
    @app.route('/apollo/<path:domain>')
    def apollo_top_level(domain):
        from backend.services.apollo_service import ApolloService
        from flask import jsonify
        org_data = ApolloService.enrich_organization(domain) or {}
        contacts = ApolloService.extract_emails(domain)
        return jsonify({
            "domain": domain,
            "organization": org_data,
            "contacts": contacts
        })
        
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5001))
    print(f"[*] Lead Intelligence Platform starting on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
