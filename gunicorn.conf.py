bind = "0.0.0.0:8080"  # Bind to all interfaces on port 8080
workers = 2  # Two worker processes, usually fine for small FastAPI apps
worker_class = "uvicorn.workers.UvicornWorker"  # ASGI-compatible worker
timeout = 30  # Seconds before killing a hung worker
loglevel = "info"

accesslog = "/var/log/fireguard/access.log"
errorlog = "/var/log/fireguard/error.log"
