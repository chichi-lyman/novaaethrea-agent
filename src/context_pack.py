# Copyright © 2026 Chelsea Megan Woods
# Context pack builder for multi-agent memory handoffs

from __future__ import annotations

from typing import Any, Optional
from datetime import datetime, timezone
import uuid


def build_context_pack(
    *,
    facts: Optional[dict] = None,
    preferences: Optional[dict] = None,
    scenes: Optional[dict] = None,
    history_slice: Optional[list] = None,
    connector_health: Optional[dict] = None,
    policy_grant: str = "ALLOW",
    task_id: Optional[str] = None,
    trace_id: Optional[str] = None,
) -> dict[str, Any]:
    """Assemble a ContextPack compatible with schemas/mcp_memory.json."""
    return {
        "trace_id": trace_id or str(uuid.uuid4()),
        "task_id": task_id or str(uuid.uuid4()),
        "facts": facts or {},
        "preferences": preferences or {},
        "scenes": scenes or {},
        "history_slice": (history_slice or [])[-50:],
        "connector_health": connector_health or {},
        "policy_grant": policy_grant,
        "built_at": datetime.now(timezone.utc).isoformat(),
    }


def empty_envelope(
    *,
    from_agent: str,
    to_agent: str,
    objective: str,
    policy: str = "ALLOW",
    context_pack: Optional[dict] = None,
) -> dict[str, Any]:
    """Shared handoff envelope used across the Nova Umbrella pipeline."""
    return {
        "trace_id": str(uuid.uuid4()),
        "from_agent": from_agent,
        "to_agent": to_agent,
        "task_id": str(uuid.uuid4()),
        "objective": objective,
        "constraints": [],
        "inputs": {},
        "context_pack": context_pack or build_context_pack(),
        "policy": policy,
        "deadline_ms": None,
        "reply_channel": "orchestrator",
    }
