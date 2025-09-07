# Configuración de Gunicorn para Render
import os

# Puerto - Render requiere que se use la variable PORT
port = os.environ.get('PORT', 5000)
bind = f"0.0.0.0:{port}"

# Workers - Reducir para plan free
workers = 1

# Timeout
timeout = 30

# Logs
accesslog = "-"
errorlog = "-"

# Preload app
preload_app = True

# Worker class
worker_class = "sync"

# Max requests
max_requests = 1000
max_requests_jitter = 100

# Keep alive
keepalive = 2
