# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkLatentIntentOrchestrator

client = OpenClawGenParkLatentIntentOrchestrator()

TOOLS = [
    {
        "name": "update_pomdp_intent_belief",
        "description": "Updates belief state over latent user dialogue intents given observed tokens.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prior_belief": {"type": "object"},
                "observed_tokens": {"type": "array", "items": {"type": "string"}},
                "observation_likelihoods": {"type": "object"}
            },
            "required": ["prior_belief", "observed_tokens", "observation_likelihoods"]
        }
    },
    {
        "name": "calculate_intent_entropy",
        "description": "Calculates Shannon entropy to determine if agent should ask clarifying question.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "belief_distribution": {"type": "object"},
                "ambiguity_threshold": {"type": "number"}
            },
            "required": ["belief_distribution"]
        }
    },
    {
        "name": "track_goal_dag_progression",
        "description": "Evaluates goal DAG to identify ready unblocked subgoals for agent execution.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "goal_dag": {"type": "object"},
                "completed_subgoals": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["goal_dag", "completed_subgoals"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "update_pomdp_intent_belief":
            res = client.update_pomdp_intent_belief(args["prior_belief"], args["observed_tokens"], args["observation_likelihoods"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "calculate_intent_entropy":
            res = client.calculate_intent_entropy(args["belief_distribution"], args.get("ambiguity_threshold"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "track_goal_dag_progression":
            res = client.track_goal_dag_progression(args["goal_dag"], args["completed_subgoals"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
