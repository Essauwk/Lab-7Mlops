"""
Multi-Agent Orchestration Engine with LangGraph
Advanced workflow orchestrator for coordinated multi-agent systems with
state management, conditional routing, and persistent checkpointing.
Author: Reem Arafa | Version: 2.0
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict
from agents import (
    load_memory,
    route_from_router,
    router_node,
    researcher_node,
    save_memory_node,
    supervisor_node,
    writer_node,
)


class State(TypedDict):
    topic: str
    research: list
    draft: str
    iterations: int
    need_more: bool


def build_graph() -> StateGraph:
    graph = StateGraph(State)
    graph.add_node("load_memory", load_memory)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("router", router_node)
    graph.add_node("writer", writer_node)
    graph.add_node("save_memory", save_memory_node)

    graph.add_edge(START, "load_memory")
    graph.add_edge("load_memory", "supervisor")
    graph.add_edge("supervisor", "researcher")
    graph.add_edge("researcher", "router")
    graph.add_conditional_edges(
        "router",
        route_from_router,
        {
            "researcher": "researcher",
            "writer": "writer",
        },
    )
    graph.add_edge("writer", "save_memory")
    graph.add_edge("save_memory", END)

    return graph


if __name__ == "__main__":
    g = build_graph()
    initial_state = {"topic": "LangGraph multi-agent demo", "research": [], "draft": "", "iterations": 0, "need_more": True}
    checkpointer = MemorySaver()
    app = g.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "lab7-demo"}}
    run_log = Path(__file__).resolve().parent / "run_log.txt"
    buffer = StringIO()

    class Tee:
        def __init__(self, *streams):
            self.streams = streams

        def write(self, text):
            for stream in self.streams:
                stream.write(text)

        def flush(self):
            for stream in self.streams:
                stream.flush()

    with redirect_stdout(Tee(sys.stdout, buffer)):
        print("Invoking graph...\n")
        result = app.invoke(initial_state, config=config)
        print("\n=== Run complete ===")
        print("Final state:\n", result)

    with run_log.open("w", encoding="utf-8") as f:
        f.write(buffer.getvalue())
