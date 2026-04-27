"""
Intelligent Multi-Agent System: Core Agent Implementations
Specialized agent nodes for research, writing, and coordination.
Author: Reem Arafa | Version: 2.0
"""

import json
from pathlib import Path
from typing_extensions import TypedDict

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "memory.json"

class State(TypedDict):
    """Shared workflow state persisted across all agent operations."""
    topic: str
    research: list
    draft: str
    iterations: int
    need_more: bool


def load_memory(state: State) -> dict:
    print("[load_memory] checking for memory file...")
    if MEMORY_FILE.exists():
        with MEMORY_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for k in ("research", "draft", "iterations"):
            if k in data and data[k] is not None:
                state[k] = data[k]
        print(f"[load_memory] loaded memory from {MEMORY_FILE}")
    else:
        print("[load_memory] no memory found, starting fresh")
    return state


def supervisor_node(state: State) -> dict:
    print("[supervisor] initializing task and routing")
    if not state.get("topic"):
        state["topic"] = "LangGraph multi-agent demo"
    state.setdefault("research", [])
    state.setdefault("draft", "")
    state.setdefault("iterations", 0)
    state.setdefault("need_more", True)
    print(f"[supervisor] topic={state['topic']}")
    return state


def researcher_node(state: State) -> dict:
    it = state.get("iterations", 0)
    print(f"[researcher] running iteration {it}")
    fact = f"Fact about '{state['topic']}' - item {it + 1}"
    state.setdefault("research", []).append(fact)
    state["iterations"] = it + 1
    print(f"[researcher] found: {fact}")
    return state


def decision_node(state: State) -> dict:
    it = state.get("iterations", 0)
    need_more = it < 2
    state["need_more"] = need_more
    print(f"[decision] iterations={it}, need_more={need_more}")
    return state


def writer_node(state: State) -> dict:
    print("[writer] composing draft from research items")
    items = state.get("research", [])
    draft = "\n".join(f"- {s}" for s in items)
    draft = f"Summary for topic: {state.get('topic')}\n" + draft
    state["draft"] = draft
    print("[writer] draft composed")
    return state


def save_memory_node(state: State) -> dict:
    print(f"[save_memory] persisting memory to {MEMORY_FILE}")
    tosave = {"research": state.get("research", []), "draft": state.get("draft", ""), "iterations": state.get("iterations", 0)}
    with MEMORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(tosave, f, indent=2)
    print("[save_memory] memory saved")
    return state


def router_node(state: State) -> dict:
    print("[router] routing based on decision")
    return decision_node(state)


def route_from_router(state: State) -> str:
    destination = "researcher" if state.get("need_more") else "writer"
    print(f"[router] conditional edge -> {destination}")
    return destination
