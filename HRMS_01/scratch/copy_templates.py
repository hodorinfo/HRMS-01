import os
import shutil

monolith_dir = "/home/hodorinfo4/Desktop/horilla/horilla-hr"
dest_dir = "/home/hodorinfo4/Desktop/HRMS-01/HRMS_01/ui-service/templates"

# We want to find files loaded by the dashboard views.
# Let's search for files matching specific names.
search_names = [
    "dashboard_shift", "shift_request", "work_type", 
    "overtime", "validate", "allocation", "feedback", "asset"
]

print("Scanning monolith templates...")
copied_count = 0
for root, dirs, files in os.walk(monolith_dir):
    for f in files:
        if f.endswith(".html"):
            for name in search_names:
                if name in f.lower():
                    # Let's copy it to a matching structure or dest_dir
                    rel_path = os.path.relpath(root, monolith_dir)
                    # Find if it is in a templates folder
                    parts = rel_path.split(os.sep)
                    if "templates" in parts:
                        idx = parts.index("templates")
                        sub_path = os.path.join(*parts[idx+1:])
                    else:
                        sub_path = f
                    
                    target_path = os.path.join(dest_dir, sub_path)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(os.path.join(root, f), target_path)
                    print(f"Copied {f} to {target_path}")
                    copied_count += 1

print(f"Done copying {copied_count} templates.")
