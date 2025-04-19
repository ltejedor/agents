# mcp_server/queue.py
from collections import deque
from typing import Dict, Any, List

_QUEUE: "deque[Dict[str, Any]]" = deque()

def push(cmd: Dict[str, Any]) -> None:
    _QUEUE.append(cmd)

def pull(batch: int | None = None) -> List[Dict[str, Any]]:
    out = []
    while _QUEUE and (batch is None or len(out) < batch):
        out.append(_QUEUE.popleft())
    return out
