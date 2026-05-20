import json
import os
import re

transcript_path = r"c:\Users\Admin$\.gemini\antigravity\brain\757b7d29-b820-4cbe-bb94-7a4dfd0c2cc4\.system_generated\logs\transcript.jsonl"
workspace = r"c:\Users\Admin$\Desktop\lead-intelligence-platform"

def process_transcript():
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT":
                    content = data.get("content", "")
                    if "# PART " in content:
                        print("Found part in user input!")
                        extract_files(content)
            except Exception as e:
                pass

def extract_files(content):
    # Match patterns like:
    # # backend/app.py
    # 
    # ```python id="1m2g4v"
    # code
    # ```
    
    # Split by "# " which precedes the filepath
    parts = content.split("\n# ")
    for part in parts:
        if part.strip().startswith("PART"):
            continue
            
        lines = part.strip().split("\n")
        if not lines:
            continue
            
        filename = lines[0].strip()
        # Some lines might not be filenames, check if it has a slash or extension
        if "/" not in filename and "." not in filename:
            continue
            
        # extract code block
        code_match = re.search(r'```[a-z]*.*?\n(.*?)```', part, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
            
            # fix imports for python files in backend
            if filename.startswith("backend/") and filename.endswith(".py"):
                # Apply the backend. prefix to specific modules
                code = re.sub(r'from api\.', 'from backend.api.', code)
                code = re.sub(r'from services\.', 'from backend.services.', code)
                code = re.sub(r'from models\.', 'from backend.models.', code)
                code = re.sub(r'from auth ', 'from backend.auth ', code)
                code = re.sub(r'from celery_worker ', 'from backend.celery_worker ', code)
                code = re.sub(r'from config ', 'from backend.config ', code)
                code = re.sub(r'from database ', 'from backend.database ', code)
                
                # Apply Suraj Singh Bartwal personalization constraint if it's personalization_engine
                if "personalization_engine.py" in filename:
                    code = code.replace("I noticed {company} is growing rapidly.", "I noticed {company} is growing rapidly. I'm Suraj Singh Bartwal with the KinsTechnology CyberSecurity Pre-Sales Outreach Team.")
                
                # Handle SentenceTransformer fallback in embeddings.py
                if "embeddings.py" in filename:
                    code = code.replace("self.model = SentenceTransformer(\n            \"all-MiniLM-L6-v2\"\n        )", "try:\n            self.model = SentenceTransformer(\"all-MiniLM-L6-v2\")\n        except:\n            self.model = None")
                    code = code.replace("vector = self.model.encode(text)\n\n        return vector.tolist()", "if self.model:\n            return self.model.encode(text).tolist()\n        return [0.0]*384")
                    
            full_path = os.path.join(workspace, filename.replace('/', os.sep))
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, "w", encoding="utf-8") as out_f:
                out_f.write(code + "\n")
            print(f"Created {full_path}")

if __name__ == "__main__":
    process_transcript()
