import sys
import os
from datetime import datetime

def setup_logging():
	log_dir = "logs"
	os.makedirs(log_dir, exist_ok=True)
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	log_path = os.path.join(log_dir, f"daemon_{timestamp}.log")
	sys.stdout = open(log_path, "a")
	sys.stderr = sys.stdout
	print(f"[{datetime.now()}] [INFO] Logging started. Output redirected to {log_path}")


def log(message, level="INFO"):
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	formatted = f"[{timestamp}] [{level}] {message}"
	if level in {"ERROR", "CRITICAL"}:
		print(formatted, file=sys.stderr)
	else:
		print(formatted, file=sys.stdout)
