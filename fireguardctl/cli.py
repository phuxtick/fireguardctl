#!/usr/bin/env python3

import argparse
import requests
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Send Fireguard status update.")
    parser.add_argument("--hostname", required=True, help="Hostname")
    parser.add_argument("--location", required=True, help="Location/group")
    parser.add_argument("--service", action='append', help="Service status in the form name=state", required=True)
    parser.add_argument("--url", default="http://localhost:8080/api/status", help="API endpoint URL")
    args = parser.parse_args()

    # Build services dictionary
    services = {}
    for svc in args.service:
        try:
            name, state = svc.split("=")
            services[name.strip()] = state.strip().lower()
        except ValueError:
            print(f"Invalid service format: {svc} (use name=state)")
            return

    payload = {
        "hostname": args.hostname,
        "location": args.location,
        "services": services,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        r = requests.post(args.url, json=payload)
        print(f"Status sent: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error sending status: {e}")

if __name__ == "__main__":
    main()
