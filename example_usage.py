# -*- coding: utf-8 -*-
from client import OpenClawGenParkLatentIntentOrchestrator

orchestrator = OpenClawGenParkLatentIntentOrchestrator()

# 1. POMDP Belief Update
prior = {"PURCHASE_COMPUTE": 0.33, "CANCEL_SUBSCRIPTION": 0.33, "QUERY_INVOICE": 0.34}
tokens = ["refund", "billing", "charge"]
likelihoods = {
    "PURCHASE_COMPUTE": {"refund": 0.01, "billing": 0.20, "charge": 0.30},
    "CANCEL_SUBSCRIPTION": {"refund": 0.40, "billing": 0.50, "charge": 0.30},
    "QUERY_INVOICE": {"refund": 0.10, "billing": 0.80, "charge": 0.70}
}
post = orchestrator.update_pomdp_intent_belief(prior, tokens, likelihoods)
print(f"Top Intent: {post['top_intent']} (Confidence: {post['top_intent_confidence']})")

# 2. Ambiguity Entropy Check
entropy = orchestrator.calculate_intent_entropy(post['posterior_belief'], ambiguity_threshold=1.1)
print(f"\nEntropy: {entropy['entropy_bits']} bits -> {entropy['recommended_action']}")

# 3. Goal DAG Progression
dag = {
    "AUTH_USER": [],
    "FETCH_INVOICE": ["AUTH_USER"],
    "DISPUTE_CHARGE": ["FETCH_INVOICE"],
    "NOTIFY_SUPPORT": ["DISPUTE_CHARGE"]
}
prog = orchestrator.track_goal_dag_progression(dag, completed_subgoals=["AUTH_USER"])
print(f"\nGoal DAG Progress: {prog['completion_percentage']}% completed, Ready to execute: {prog['ready_to_execute']}")
