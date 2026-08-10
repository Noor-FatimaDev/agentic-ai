# Day 8: AI Agents in LangGraph (DeepLearning.AI)

## Focus
Intro to LangGraph : moving from hand-rolled and Smolagents-based agent loops
to a graph-based framework for defining agent control flow.

## What I learned
- **Agent from scratch** : A basic agent loop inside LangGraph's
  graph structure to see the framework's primitives directly (nodes, edges, state)
  rather than through pre-built abstractions.
- **Essay-writing agent** : A multi-step agent that plans, drafts, critiques,
  and revises an essay, using agentic search tools to pull in supporting
  information mid-process.

## Core concepts covered
- **Nodes & edges** : control flow expressed explicitly as a graph instead of
  implicit in code structure (if/while logic).
- **State** : a shared object passed between nodes; each node reads and
  updates it, carrying context forward through the run.
- **Conditional edges** : routing to different nodes based on a previous
  step's outcome (retry, re-plan, continue), instead of always moving forward
  linearly.
- **Persistence / checkpointing** : saving graph state so a run can be paused
  and resumed rather than restarted from scratch.
- **Human-in-the-loop** : interrupting a run at a defined point for human
  review/input before the agent continues.
- **Streaming** : getting intermediate outputs as the agent runs, instead of
  waiting for the final result.
- **Agentic search tools** : giving the agent the ability to pull external
  information as part of its own reasoning steps.  

## How this connects to Days 4–7
Days 4–6 built a ReAct-style loop and CLI chatbot by hand; Day 7 rebuilt that
loop in Smolagents. Both were fundamentally linear - the agent's control flow
lived inside the code itself. LangGraph makes that control flow into an
explicit, inspectable graph, which is what enables cycles (retry/re-plan),
persistence, and clean interrupt points for human review - none of which are
straightforward to bolt onto a linear loop.
