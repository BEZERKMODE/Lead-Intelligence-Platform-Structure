import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)
try:
    response = client.get("/api/leads/scrape-stream?domain=dtdc.com")
    print("STATUS CODE:", response.status_code)
    print("HEADERS:", response.headers)
    print("CONTENT:", response.content)
except Exception as e:
    import traceback
    traceback.print_exc()
