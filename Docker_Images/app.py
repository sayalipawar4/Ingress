import os
import socket
from flask import Flask, render_template

app = Flask(__name__)

def get_container_id():
    # Check if running in a Docker container
    try:
        with open("/proc/self/cgroup", "r") as f:
            for line in f:
                if "docker" in line or "kubepods" in line:
                    parts = line.strip().split("/")
                    if len(parts) > 2:
                        container_id = parts[-1]
                        # Extract short container ID (first 12 chars)
                        if len(container_id) > 12:
                            return container_id[:12]
                        return container_id
    except FileNotFoundError:
        # Not in a container (e.g., running on Mac/Windows)
        pass
    except Exception as e:
        pass
    
    # If not in container, return hostname
    try:
        return socket.gethostname()
    except:
        return "Host System"

def get_ip_address():
    try:
        # Try to get the actual network IP (not localhost)
        # Create a socket connection to an external address (doesn't actually connect)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # Connect to a public DNS server (doesn't send any data)
            s.connect(('8.8.8.8', 80))
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = None
        finally:
            s.close()
        
        if ip_address:
            return ip_address
        
        # Fallback: try getting hostname IP
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        if ip_address and ip_address != '127.0.0.1':
            return ip_address
            
    except Exception:
        pass
    
    return "127.0.0.1"

@app.route("/")
def home():
    container_id = get_container_id()
    ip_address = get_ip_address()
    return render_template("index.html", container_id=container_id, ip_address=ip_address)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
