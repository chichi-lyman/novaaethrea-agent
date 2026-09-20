# Copyright © 2026 Chelsea Megan Woods
# NovaAethrea calm recovery / backoff for MCP and external connectors

from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable, Optional

logger = logging.getLogger("NovaAethrea.Retry")


class RetryHandler:
    """Exponential backoff with circuit awareness for connector calls."""

    def __init__(
        self,
        max_attempts: int = 4,
        base_delay_s: float = 0.25,
        max_delay_s: float = 8.0,
        circuit_threshold: int = 5,
    ):
        self.max_attempts = max_attempts
        self.base_delay_s = base_delay_s
        self.max_delay_s = max_delay_s
        self.circuit_threshold = circuit_threshold
        self._failures: dict[str, int] = {}

    def _circuit_open(self, connector: str) -> bool:
        return self._failures.get(connector, 0) >= self.circuit_threshold

    def record_success(self, connector: str) -> None:
        self._failures[connector] = 0

    def record_failure(self, connector: str) -> None:
        self._failures[connector] = self._failures.get(connector, 0) + 1

    async def run(
        self,
        connector: str,
        fn: Callable[[], Awaitable[Any]],
    ) -> dict[str, Any]:
        if self._circuit_open(connector):
            return {
                "connector": connector,
                "attempts": 0,
                "status": "circuit_open",
                "backoff_ms": 0,
                "last_error": "circuit open",
            }

        last_error: Optional[str] = None
        delay = self.base_delay_s
        for attempt in range(1, self.max_attempts + 1):
            try:
                result = await fn()
                self.record_success(connector)
                return {
                    "connector": connector,
                    "attempts": attempt,
                    "status": "success",
                    "backoff_ms": int(delay * 1000),
                    "last_error": None,
                    "result": result,
                }
            except Exception as e:
                last_error = str(e)
                self.record_failure(connector)
                logger.warning(
                    "Connector %s attempt %s failed: %s", connector, attempt, e
                )
                if attempt < self.max_attempts:
                    await asyncio.sleep(min(delay, self.max_delay_s))
                    delay *= 2

        return {
            "connector": connector,
            "attempts": self.max_attempts,
            "status": "exhausted",
            "backoff_ms": int(delay * 1000),
            "last_error": last_error,
        }
