import json
import re
import os

workspace_dir = r"c:\Users\Admin$\Desktop\lead-intelligence-platform"
transcript_path = r"C:\Users\Admin$\.gemini\antigravity\brain\88c526d4-e523-4800-ae1c-36e45bda83fc\.system_generated\logs\transcript.jsonl"

last_user_message = ""
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get("type") == "USER_INPUT":
                last_user_message = data.get("content", "")
        except:
            pass

# The pattern is:
# # file/path
# 
# ```lang id="xxx"
# code
# ```
pattern = re.compile(r"#\s+([a-zA-Z0-9_./-]+)\n+```[a-zA-Z0-9_]+\s+id=\"[^\"]+\"\n(.*?)```", re.DOTALL)
matches = pattern.findall(last_user_message)

for filepath, code in matches:
    full_path = os.path.join(workspace_dir, filepath.strip())
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(code)

print(f"Extracted {len(matches)} files.")
