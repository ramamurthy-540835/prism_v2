from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(slots=True)
class KernelRequest:
    task: str
    operation: str = "plan"
    context: dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: str(uuid4()))

@dataclass(slots=True)
class Intent:
    type: str
    priority: str
    operation: str
    raw_task: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "priority": self.priority, "operation": self.operation, "raw_task": self.raw_task, "metadata": self.metadata}

@dataclass(slots=True)
class GraphNode:
    id: str
    agent: str
    type: str
    operation: str
    depends_on: list[str] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "agent": self.agent, "type": self.type, "operation": self.operation, "depends_on": self.depends_on, "payload": self.payload}

@dataclass(slots=True)
class KernelResult:
    request_id: str
    status: str
    intent: dict[str, Any]
    graph: list[dict[str, Any]]
    results: list[dict[str, Any]]
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {"request_id": self.request_id, "status": self.status, "intent": self.intent, "graph": self.graph, "results": self.results, "created_at": self.created_at}
