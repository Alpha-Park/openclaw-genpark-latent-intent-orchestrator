# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Latent Intent Orchestrator - POMDP Belief State Estimator & Disambiguation Engine
Standard Library only: math, typing.
Calculates POMDP Bayesian belief state updating over latent dialogue intents, evaluates
intent distribution Shannon entropy to trigger disambiguation queries, and tracks multi-turn goal DAGs.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkLatentIntentOrchestrator:
    def __init__(self, ambiguity_entropy_threshold: float = 1.2):
        self.entropy_thresh = ambiguity_entropy_threshold

    def update_pomdp_intent_belief(self, prior_belief: Dict[str, float],
                                   observed_tokens: List[str],
                                   observation_likelihoods: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """
        Updates belief state over discrete latent intent states given observed dialogue tokens:
        b'(s) = [ prod_{o in tokens} P(o | s) * b(s) ] / P(o | b)
        """
        states = list(prior_belief.keys())
        unnormalized = {}

        for s in states:
            prior_s = prior_belief[s]
            # Product of observation likelihoods
            p_obs_given_s = 1.0
            for tok in observed_tokens:
                p_tok = observation_likelihoods.get(s, {}).get(tok.lower(), 0.05) # smoothing floor
                p_obs_given_s *= p_tok
            unnormalized[s] = prior_s * p_obs_given_s

        total_mass = sum(unnormalized.values())
        if total_mass <= 0:
            posterior = {s: 1.0 / len(states) for s in states}
        else:
            posterior = {s: round(v / total_mass, 4) for s, v in unnormalized.items()}

        sorted_intents = sorted(posterior.items(), key=lambda x: x[1], reverse=True)

        return {
            "prior_belief": prior_belief,
            "observed_tokens": observed_tokens,
            "posterior_belief": posterior,
            "top_intent": sorted_intents[0][0],
            "top_intent_confidence": sorted_intents[0][1],
            "all_ranked_intents": [{"intent": i, "confidence": c} for i, c in sorted_intents]
        }

    def calculate_intent_entropy(self, belief_distribution: Dict[str, float],
                                 ambiguity_threshold: float = None) -> Dict[str, Any]:
        """
        Calculates Shannon entropy H(b) = -sum(p_i * log2(p_i)) over intent distribution.
        If entropy exceeds ambiguity_threshold, triggers active clarification.
        """
        thresh = ambiguity_threshold if ambiguity_threshold is not None else self.entropy_thresh
        probs = list(belief_distribution.values())
        total = sum(probs)
        if total <= 0:
            return {"entropy_bits": 0.0, "verdict": "EMPTY_DISTRIBUTION"}

        norm_p = [p / total for p in probs]
        entropy_h = -sum(p * math.log2(p) for p in norm_p if p > 0)

        is_ambiguous = entropy_h >= thresh

        if is_ambiguous:
            action = "ASK_DISAMBIGUATION_QUESTION"
            reason = f"Intent uncertainty {entropy_h:.3f} bits exceeds tolerance threshold {thresh:.3f} bits"
        else:
            action = "PROCEED_TO_AUTONOMOUS_EXECUTION"
            reason = f"Confidence sufficiently concentrated ({entropy_h:.3f} bits <= {thresh:.3f} bits)"

        return {
            "entropy_bits": round(entropy_h, 4),
            "ambiguity_threshold": thresh,
            "is_ambiguous": is_ambiguous,
            "recommended_action": action,
            "rationale": reason
        }

    def track_goal_dag_progression(self, goal_dag: Dict[str, List[str]],
                                   completed_subgoals: List[str]) -> Dict[str, Any]:
        """
        Evaluates goal dependency graph (subgoal -> [prerequisites]) to identify
        ready unblocked subgoals vs blocked subgoals.
        """
        done = set(completed_subgoals)
        ready = []
        blocked = []

        for goal_id, prereqs in goal_dag.items():
            if goal_id in done:
                continue
            # Check if all prereqs completed
            unmet = [p for p in prereqs if p not in done]
            if not unmet:
                ready.append(goal_id)
            else:
                blocked.append({"goal_id": goal_id, "unmet_prerequisites": unmet})

        total_goals = len(goal_dag)
        completion_pct = (len(done) / max(1, total_goals)) * 100.0

        return {
            "total_goals_count": total_goals,
            "completed_goals_count": len(done),
            "completion_percentage": round(completion_pct, 1),
            "ready_to_execute": ready,
            "blocked_goals": blocked,
            "is_all_goals_complete": len(done) >= total_goals
        }
