import json
import time
import os
import subprocess
import shlex
from datetime import datetime

# KONFIGURASI FILE
COMMAND_FILE = "command.json"
STATUS_FILE = "status.json"
RESULT_FILE = "result.json"

def get_tool_command(tool_id, target):
    """Mapping 53 fitur ke perintah CLI asli."""
    cmd_map = {
        # VULNERABILITY ANALYSIS
        "01": f"nmap --script vuln {target}",
        "03": f"nuclei -u {target}",
        # WEB EXPLOITATION
        "09": f"sqlmap -u {target} --batch --random-agent",
        "10": f"nikto -h {target}",
        "13": f"curl -I {target}/etc/passwd",
        "14": f"curl -I {target}/../../etc/passwd",
        # NETWORK & SERVER
        "21": f"nmap -sV {target}",
        "22": f"whatweb {target}",
        "24": f"dig {target} ANY",
        "25": f"subfinder -d {target}",
        # DATABASE & CLOUD
        "40": f"httpx -u {target} -path /.env,.git/config -status-code",
        "43": f"httpx -u {target} -path /.git/config -status-code",
    }
    # Fallback ke nmap jika ID belum terdaftar detailnya
    return cmd_map.get(tool_id, f"nmap -F {target}")

def start_engine():
    print("💎 PINGKI ELITE ENGINE v12.0 - REAL EXECUTION ACTIVE 💎")
    with open(STATUS_FILE, "w") as f: json.dump({"state": "idle"}, f)

    while True:
        if os.path.exists(COMMAND_FILE):
            try:
                with open(COMMAND_FILE, "r") as f:
                    cmd_data = json.load(f)
                
                if cmd_data.get("status") == "trigger":
                    with open(STATUS_FILE, "w") as f:
                        json.dump({"state": "running", "last_log": f"Executing {cmd_data['tool_name']}..."}, f)
                    
                    raw_cmd = get_tool_command(cmd_data['tool_id'], cmd_data['target'])
                    print(f"[>] Running: {raw_cmd}")

                    # Eksekusi Subprocess
                    process = subprocess.Popen(
                        shlex.split(raw_cmd),
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                    )
                    
                    output_log = [f"root@termux:~# {raw_cmd}", "-"*40]
                    for line in process.stdout:
                        output_log.append(line.strip())
                    process.wait()

                    with open(RESULT_FILE, "w") as f: json.dump({"output": "\n".join(output_log)}, f)
                    with open(STATUS_FILE, "w") as f: json.dump({"state": "done"}, f)
                    with open(COMMAND_FILE, "w") as f: json.dump({"status": "idle"}, f)
                    print("[✓] Execution Finished.")
                    
            except Exception as e:
                print(f"[!] Engine Error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    start_engine()
