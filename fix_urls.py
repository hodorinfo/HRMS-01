import os, re

TEMPLATES_ROOT = "/home/hodorinfo4/Desktop/HRMS-01/HRMS_01/ui-service/templates/recruitment"

def fix_template(filepath):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    original = content

    # Fix `<a#"?{{pd}}...` to `<a href="#?{{pd}}...`
    content = re.sub(r'<a#"\?([^"]+)"', r'<a href="#?\1"', content)

    # Fix `<a/recruitment/.../""` to `<a href="/recruitment/.../"`
    content = re.sub(r'<a(/recruitment/[^"]+/)""', r'<a href="\1"', content)

    # Fix `href=""/recruitment/.../""` to `href="/recruitment/.../"`
    content = re.sub(r'href=""(/recruitment/[^"]+)""', r'href="\1"', content)

    # Fix `<formaction="/recruitment...` to `<form action="/recruitment...`
    content = re.sub(r'<formaction="(/recruitment/[^"]+)"', r'<form action="\1"', content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

changed = 0
for root, dirs, files in os.walk(TEMPLATES_ROOT):
    for fname in files:
        if fname.endswith(".html"):
            fpath = os.path.join(root, fname)
            if fix_template(fpath):
                changed += 1

print(f"Fixed {changed} templates.")
