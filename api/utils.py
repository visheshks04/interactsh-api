from datetime import datetime
import re

def parse_interaction(interaction):
    match = re.search(r"from (\d+\.\d+\.\d+\.\d+) at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", interaction)
    
    if match:
        ip, timestamp_str = match.groups()
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return {"ip": ip, "timestamp": timestamp}
    else:
        return None