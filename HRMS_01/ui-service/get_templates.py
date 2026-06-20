import os
import re

URLS_FILE = "/home/hodorinfo4/Desktop/horilla/horilla-hr/recruitment/urls.py"
VIEWS_DIR = "/home/hodorinfo4/Desktop/horilla/horilla-hr/recruitment/views"

with open(URLS_FILE, "r") as f:
    urls_content = f.read()

url_patterns = re.findall(r'path\(\s*\"([^\"]+)\"\s*,\s*([a-zA-Z0-9_\.]+)', urls_content)

templates_map = {}
for root, _, files in os.walk(VIEWS_DIR):
    for f in files:
        if f.endswith(".py"):
            with open(os.path.join(root, f), "r") as pyf:
                content = pyf.read()
                defs = re.split(r"def ", content)
                for d in defs[1:]:
                    func_name = d.split("(")[0].strip()
                    renders = re.findall(r"render\s*\(\s*[^,]+,\s*[\"']([^\"']+)\.html[\"']", d)
                    if renders:
                        templates_map[func_name] = renders[0] + ".html"
                    else:
                        template_responses = re.findall(r"TemplateResponse\s*\(\s*[^,]+,\s*[\"']([^\"']+)\.html[\"']", d)
                        if template_responses:
                            templates_map[func_name] = template_responses[0] + ".html"

print("--- MAPPINGS ---")
for url, func_path in url_patterns:
    func_name = func_path.split(".")[-1]
    if func_name in templates_map:
        print(f"{url} -> {templates_map[func_name]}")
    else:
        print(f"{url} -> {func_name} (No direct template found)")
