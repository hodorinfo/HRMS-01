import os

TEMPLATES_ROOT = "/home/hodorinfo4/Desktop/HRMS-01/HRMS_01/ui-service/templates/recruitment"

def main():
    for root, dirs, files in os.walk(TEMPLATES_ROOT):
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r') as file:
                    content = file.read()
                
                original = content
                
                filters_to_check = ["app_installed", "base64_encode", "fk_history"]
                needs_basefilters = any(f in content for f in filters_to_check)
                
                if needs_basefilters and "{% load basefilters" not in content:
                    content = "{% load basefilters %}\n" + content
                    
                if content != original:
                    with open(filepath, 'w') as file:
                        file.write(content)
                    print(f"Updated: {filepath}")

if __name__ == '__main__':
    main()
