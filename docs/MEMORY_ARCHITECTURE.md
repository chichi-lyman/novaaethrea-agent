# NovaAethrea Memory Architecture

© 2026 Chelsea Megan Woods · Nova Umbrella

## Role in the pipeline

```
Saphira → Aura → Agent Two → NovaReign → **NovaAethrea** → Agent Zero
```

NovaAethrea is the sole owner of long-horizon context and connector health. Specialists never hold persistent memory; they receive a **ContextPack** via the shared handoff envelope and return results that may be written back only under governance grant.

## Storage model

| Namespace     | Purpose                          | Persistence          |
|---------------|----------------------------------|----------------------|
| `facts`       | Stable user/system facts         | File JSON (swappable to SQLite/pgvector) |
| `preferences` | Tone, device, schedule prefs     | Same                 |
| `scenes`      | Named multi-step device scenes   | Same                 |
| `history`     | Recent task / scene audit slice  | Capped (last 200)    |

Primary implementation lives in `saphira-ai/src/memory/persistent_store.py` (singleton `persistent_memory`). This repository defines the **schemas and handoff contracts** so other agent repos can integrate without importing the main runtime.

## ContextPack

Every governance → memory → execution hop carries a ContextPack:

- `trace_id` / `task_id`
- `facts`, `preferences`, `scenes`, `history_slice`
- `connector_health` (status, last_success_ms, retries)
- `policy_grant` ∈ {ALLOW, REQUIRE_APPROVAL, DENY}

See `schemas/mcp_memory.json`.

## Retry / recovery

`src/retry_handler.py` provides exponential backoff with a simple circuit breaker. Connector failures never crash the pipeline; outcomes are recorded as `RetryOutcome` and surfaced in the ContextPack.

## Invariants

1. No external MCP call without a governance grant.
2. Specialists do not write persistent memory directly.
3. Commercial or messaging side-effects remain policy-gated upstream.
4. End users never see internal codenames or raw memory dumps.
