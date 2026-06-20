import os
import re

target_dirs = [
    "candidate", "dashboard", "linkedin", "offerletter", "pipeline", 
    "settings", "skill_zone", "skill_zone_cand", "stage", "survey"
]
loose_files = [
    "rating_input.html", "select2.js", "survey_form.html", "survey_preview_form.html"
]

base_dir = "/home/hodorinfo4/Desktop/horilla/horilla-hr/recruitment"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    for td in target_dirs:
        # Match python render/template strings: "candidate/...
        content = re.sub(f'"{td}/', f'"recruitment/{td}/', content)
        content = re.sub(f"'{td}/", f"'recruitment/{td}/", content)

    for lf in loose_files:
        content = re.sub(f'"{lf}"', f'"recruitment/{lf}"', content)
        content = re.sub(f"'{lf}'", f"'recruitment/{lf}'", content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.py') or file.endswith('.html'):
            filepath = os.path.join(root, file)
            process_file(filepath)

print("Done updating template paths.")
