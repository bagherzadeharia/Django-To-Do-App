import subprocess
import sys

subprocess.run(
    [sys.executable, "manage.py", "makemigrations", "--check", "--dry-run"],
)

subprocess.run(
    [sys.executable, "manage.py", "migrate"],
    check=True,
)

subprocess.run(sys.argv[1:], check=True)