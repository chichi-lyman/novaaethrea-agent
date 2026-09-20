# Copyright © 2026 Chelsea Megan Woods
from src.context_pack import build_context_pack, empty_envelope
from src.retry_handler import RetryHandler
import asyncio


def test_build_context_pack():
    pack = build_context_pack(facts={"k": "v"}, policy_grant="ALLOW")
    assert pack["facts"]["k"] == "v"
    assert pack["policy_grant"] == "ALLOW"
    assert "trace_id" in pack


def test_empty_envelope():
    env = empty_envelope(
        from_agent="nova_reign",
        to_agent="nova_aethrea",
        objective="load context",
    )
    assert env["from_agent"] == "nova_reign"
    assert env["policy"] == "ALLOW"


def test_retry_handler_success():
    async def ok():
        return {"ok": True}

    handler = RetryHandler(max_attempts=2)

    async def run():
        return await handler.run("test", ok)

    result = asyncio.get_event_loop().run_until_complete(run())
    assert result["status"] == "success"
