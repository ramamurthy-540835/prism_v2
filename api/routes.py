from fastapi import APIRouter, HTTPException
from kernel.core import PrismKernel

router = APIRouter()
kernel = PrismKernel()


def _task_from(payload: dict) -> str:
    task = payload.get("task") or payload.get("input") or payload.get("user_input")
    if not isinstance(task, str) or not task.strip():
        raise HTTPException(status_code=400, detail="task is required")
    return task


def _operation_from(payload: dict, default: str = "plan") -> str:
    return str(payload.get("operation") or payload.get("mode") or default)


@router.get("/health")
def health():
    return {"status": "ok", "service": "prism-v2-kernel"}


@router.get("/status")
def status():
    bridge = kernel.boot.bridge
    lakehouse = kernel.boot.lakehouse
    return {
        "status": "ok",
        "source": "prism_v2_kernel",
        "service": "prism-v2-kernel",
        "kernel": {
            "status": "ready" if kernel.boot.initialized else "booting",
            "apiStatus": "ready",
            "bridgeStatus": "connected" if not bridge.mock else "mock",
            "lakehouseStatus": "connected" if lakehouse.base_url else "local_rules",
            "bigQueryStatus": "via_lakehouse",
            "gcsArtifactStatus": "via_prism_v1",
        },
        "bridge": {
            "mode": "mock" if bridge.mock else "prism_v1_api",
            "baseUrlConfigured": bool(bridge.base_url),
        },
    }


@router.post("/run")
def run_task(payload: dict):
    task = _task_from(payload)
    operation = _operation_from(payload)
    context = payload.get("context") or {
        "prompt_uid": payload.get("prompt_uid") or payload.get("promptUid"),
        "version": payload.get("version"),
        "workspace_id": payload.get("workspace_id"),
        "project_name": payload.get("project_name"),
        "approval": payload.get("approval"),
        "approval_required": payload.get("approval_required") or payload.get("approval"),
    }
    return kernel.run(task, operation=operation, context=context)


@router.post("/intent")
def intent(payload: dict):
    task = _task_from(payload)
    parsed = kernel.boot.intent_parser.parse(task, operation=_operation_from(payload, "dry_run"))
    classified = kernel.boot.intent_classifier.classify(parsed)
    return {"status": "ok", "source": "prism_v2_kernel", "intent": classified}


@router.post("/graph")
def graph(payload: dict):
    task = _task_from(payload)
    parsed = kernel.boot.intent_parser.parse(task, operation=_operation_from(payload, "dry_run"))
    intent = kernel.boot.intent_classifier.classify(parsed)
    rules = kernel.boot.lakehouse.get_rules(intent)
    nodes = kernel.boot.graph_builder.build(intent, rules, payload.get("context") or payload)
    return {
        "status": "ok",
        "source": "prism_v2_kernel",
        "intent": intent,
        "graph": [node.to_dict() for node in nodes],
    }


@router.post("/route")
def route(payload: dict):
    task = _task_from(payload)
    parsed = kernel.boot.intent_parser.parse(task, operation=_operation_from(payload, "route"))
    intent = kernel.boot.intent_classifier.classify(parsed)
    rules = kernel.boot.lakehouse.get_rules(intent)
    nodes = kernel.boot.graph_builder.build(intent, rules, payload.get("context") or payload)
    routes = [
        {"node": node.id, "agent": node.agent, "model": kernel.boot.router.select(node.to_dict(), intent, rules)}
        for node in nodes
    ]
    return {
        "status": "ok",
        "source": "prism_v2_kernel",
        "modelRouter": {
            "recommendedModel": routes[0]["model"] if routes else "gemini-3.5-flash",
            "confidence": 0.72,
            "routingReason": "Selected through PRISM v2 model_router using graph node agent roles.",
            "routes": routes,
        },
    }


@router.post("/agents/run")
def run_agent(payload: dict):
    task = _task_from(payload)
    operation = _operation_from(payload, "plan")
    result = kernel.run(task, operation=operation, context=payload.get("context") or payload)
    return {
        "status": result.get("status", "ok"),
        "source": "prism_v2_kernel",
        "agents": result.get("results", []),
        "graph": result.get("graph", []),
    }


@router.get("/agents")
def agents():
    return {
        "status": "ok",
        "source": "prism_v2_kernel",
        "agents": [
            {"name": name, "status": "ready", "selected_model": kernel.boot.router.select({"agent": name})}
            for name in sorted(kernel.boot.agents.keys())
        ],
    }


@router.post("/lakehouse/ground")
def lakehouse_ground(payload: dict):
    task = _task_from(payload)
    parsed = kernel.boot.intent_parser.parse(task, operation=_operation_from(payload, "dry_run"))
    intent = kernel.boot.intent_classifier.classify(parsed)
    rules = kernel.boot.lakehouse.get_rules(intent)
    return {"status": "ok", "source": "prism_v2_kernel", "intent": intent, "lakehouse": rules}


@router.get("/runs")
def runs():
    return {
        "status": "ok",
        "source": "prism_v2_kernel",
        "runs": list(kernel.boot.state.memory.values())[-20:],
    }
