import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import app

print("Registered Routes:")
for route in app.routes:
    print(f"Path: {route.path}, Name: {route.name}, Methods: {getattr(route, 'methods', None)}")
