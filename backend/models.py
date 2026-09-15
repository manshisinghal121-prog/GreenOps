from pydantic import BaseModel


class WorkloadRequest(BaseModel):
    cpu_usage: float
    ram_usage: float
    runtime_hours: float
    hour: int
    day_of_week: int
    workload_type: str
    current_instance: str