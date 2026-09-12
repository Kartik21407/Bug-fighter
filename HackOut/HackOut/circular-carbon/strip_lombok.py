import os
import re

base_dir = r"c:\Users\Anuj\Desktop\HackOut\circular-carbon\backend\src\main\java"

for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".java"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                
            if "lombok" in content or "@Data" in content or "@RequiredArgsConstructor" in content:
                print(f"File needs lombok removal: {path}")
