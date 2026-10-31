---
name: openclaw-genpark-latent-intent-orchestrator
description: OpenClaw GenPark Latent Intent Orchestrator - POMDP belief state estimator and disambiguation engine with Shannon entropy thresholding.
category: Service
version: 1.0.0
license: MIT
tools:
  - update_pomdp_intent_belief
  - calculate_intent_entropy
  - track_goal_dag_progression
---

# Openclaw Genpark Latent Intent Orchestrator

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Latent Intent Orchestrator**.
Your primary directive is to execute: OpenClaw GenPark Latent Intent Orchestrator - POMDP belief state estimator and disambiguation engine with Shannon entropy thresholding.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `update_pomdp_intent_belief`
- `calculate_intent_entropy`
- `track_goal_dag_progression`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `update_pomdp_intent_belief`
- `calculate_intent_entropy`
- `track_goal_dag_progression`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
