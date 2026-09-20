# Copyright © 2026 Chelsea Megan Woods
"""Minimal FastAPI surface for NovaAethrea memory operations."""

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any, Optional
from src.context_pack import build_context_pack

app = FastAPI(title="NovaAethrea Memory API", version="0.1.0")


class MemoryWrite(BaseModel):
    key: str
    value: Any
    namespace: str = Field(default="facts")


class MemoryRead(BaseModel):
    keys: list[str]
    namespace: str = "facts"


@app.get("/health")
def health():
    return {"status": "ok", "agent": "nova_aethrea"}


@app.post("/context-pack")
def context_pack(facts: Optional[dict] = None):
    return build_context_pack(facts=facts or {})
