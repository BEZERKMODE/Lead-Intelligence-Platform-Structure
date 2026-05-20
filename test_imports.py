import sys
import traceback

print("Testing Application Imports...")
try:
    from backend.app import app
    print("SUCCESS: Application imported perfectly! No syntax errors found.")
except Exception as e:
    print("\n--- ERROR FOUND ---")
    traceback.print_exc()
    print("-------------------\n")
