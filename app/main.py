from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psutil
import json

# Create FastAPI app instance
app = FastAPI()

# Path for Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Function to get system metrics
def get_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    io_counters = psutil.net_io_counters()

    return {
        'cpu_percent': cpu_percent,
        'memory_total': memory_info.total,
        'memory_used': memory_info.used,
        'memory_percent': memory_info.percent,
        'disk_total': disk_info.total,
        'disk_used': disk_info.used,
        'disk_percent': disk_info.percent,
        'io_sent': io_counters.bytes_sent,
        'io_recv': io_counters.bytes_recv
    }

# API endpoint to get system metrics
@app.get("/api/metrics")
async def metrics():
    return get_system_metrics()

# Home page that renders the HTML frontend
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
