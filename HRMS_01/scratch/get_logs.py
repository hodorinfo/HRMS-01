import subprocess
res = subprocess.run(["docker", "compose", "logs", "ui-service", "--tail=50"], capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)
