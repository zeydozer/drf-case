# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'drf_case_gunicorn'

# Server mechanics
preload_app = True
daemon = False
pidfile = '/tmp/gunicorn.pid'
user = 'app'
group = 'app'
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# SSL (if needed in future)
# keyfile = None
# certfile = None

def when_ready(server):
  server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
  worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
  server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
  server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
  worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
  worker.log.info("Worker aborted (pid: %s)", worker.pid)
