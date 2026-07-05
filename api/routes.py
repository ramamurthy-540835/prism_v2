from fastapi import APIRouter, HTTPException
from kernel.core import PrismKernel

router = APIRouter()
kernel = PrismKernel()

@router.get("/health")
def health():
    return {"status": "ok", "service": "prism-v2-kernel"}

@router.post("/run")
def run_task(payload: dict):
    task = payload.get("task") or payload.get("input") or payload.get("user_input")
    if not isinstance(task, str) or not task.strip():
        raise HTTPException(status_code=400, detail="task is required")
    operation = payload.get("operation")
    return kernel.run(task, operation=operation, context=payload.get("context") or {})
