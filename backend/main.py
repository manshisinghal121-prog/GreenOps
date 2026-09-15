from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .decision_engine import analyze_workload
from .models import WorkloadRequest
from .dashboard import get_dashboard_data


# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI(
    title="GreenOps API",
    description="AI-powered cloud cost and carbon optimizer",
    version="1.0.0"
)


# ==========================================
# ENABLE CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "GreenOps API is running!",
        "status": "online"
    }


# ==========================================
# ANALYZE WORKLOAD
# ==========================================

@app.post("/analyze")
def analyze(data: dict):

    result = analyze_workload(

        cpu_usage=data["cpu_usage"],

        ram_usage=data["ram_usage"],

        runtime_hours=data["runtime_hours"],

        hour=data["hour"],

        day_of_week=data["day_of_week"],

        workload_type=data["workload_type"],

        current_instance=data["current_instance"]
    )

    return result
@app.get("/dashboard")
def dashboard():

    return get_dashboard_data()