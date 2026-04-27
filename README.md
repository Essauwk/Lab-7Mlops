# Intelligent Research & Writing Agent System

A sophisticated multi-agent orchestration system powered by LangGraph that simulates collaborative research and writing workflows.

## Architecture

- **Agents**: Research specialist (`researcher`) and Writing specialist (`writer`)
- **Supervisor/Router**: Task coordinator (`supervisor`) initializes workflows; decision engine (`router`) evaluates readiness
- **Memory & State**: Checkpoint persistence via `MemorySaver` with thread-based sessions, plus local state snapshots in `memory.json`
- **Workflow**: Smart conditional routing using `need_more` flag to iteratively refine research before writer delegation

Example run log saved at `run_log.txt` demonstrates full agent collaboration.

Run:

```bash
pip install -r requirements.txt
python main.py
```
