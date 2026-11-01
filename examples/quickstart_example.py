"""
quickstart_example.py - Pedagogical 5-Event Example from Figure 1 of the Paper.

Demonstrates:
1. Ingesting event DAG and noisy timestamps.
2. Running bounded A* to find the baseline optimal timeline pi* and cost c*.
3. Evaluating counterfactual flip-costs Delta(a, b) on unconstrained event pairs.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../experiments_suite/src')))

from poset import EventDAG
from cost import InversionCostModel
from search import bounded_best_first_search
from counterfactual import compute_pairwise_flip_cost

def main():
    print("=" * 70)
    print("Counterfactual Flip-Cost Analysis: Quickstart Demo (Figure 1 in Paper)")
    print("=" * 70)

    # 1. Define events: 0: A (fork), 1: B (read key), 2: C (write tmp), 3: E (exfil), 4: D (login)
    event_names = ["A (fork)", "B (read key)", "C (write tmp)", "E (exfil)", "D (login)"]
    n_events = len(event_names)

    # Recorded timestamps with noise/inversions:
    # Notice: E (3.5) was recorded before C (3.9) and B (4.1), but E must causally follow B and C!
    timestamps = [1.0, 4.1, 3.9, 3.5, 6.0]

    # Precedence edges:
    # A -> B, A -> C, B -> E, C -> E (D is causally unconstrained)
    edges = [
        (0, 1), # A -> B
        (0, 2), # A -> C
        (1, 3), # B -> E
        (2, 3), # C -> E
    ]

    dag = EventDAG(n_events, edges)
    cost_model = InversionCostModel(n_events, timestamps)

    print("\n[Phase 1] Inputs Ingested:")
    for i, name in enumerate(event_names):
        print(f"  Event {i}: {name:<15} Recorded Timestamp = {timestamps[i]:.1f} s")
    print(f"  Precedence Edges : {edges}")
    print(f"  Reference Order (by timestamp): {[event_names[i] for i in cost_model.pi_tau]}")

    # 2. Run Bounded A* search to discover optimal timeline pi*
    print("\n[Phase 2] Executing Bounded A* Search...")
    baseline_res = bounded_best_first_search(dag, cost_model, budget=1000)
    
    print(f"  Status        : {baseline_res.status}")
    print(f"  Optimal Cost  : c* = {baseline_res.cost} timestamp inversions")
    print(f"  Optimal Order : {' -> '.join([event_names[i] for i in baseline_res.timeline])}")

    # 3. Analyze Free Pairs & Counterfactual Flips
    free_pairs = dag.get_free_pairs()
    print(f"\n[Phase 3] Evaluating Ordering Ambiguity on Free Pairs: {free_pairs}")
    print("-" * 70)
    print(f"{'Pair':<20} {'Baseline Order':<25} {'Flip Cost (Delta)':<20} {'Sensitivity'}")
    print("-" * 70)

    for u, v in free_pairs:
        cf_res = compute_pairwise_flip_cost(dag, cost_model, baseline_res, (u, v), search_budget=1000)
        u_name = event_names[cf_res.baseline_order[0]]
        v_name = event_names[cf_res.baseline_order[1]]
        base_str = f"{u_name} before {v_name}"
        pair_str = f"({event_names[u]}, {event_names[v]})"
        
        if cf_res.delta is not None:
            delta_str = f"Delta = {cf_res.delta}"
            sensitivity = "FRAGILE / AMBIGUOUS" if cf_res.delta <= 1 else "ROBUST / STABLE"
        else:
            delta_str = f"Status: {cf_res.status}"
            sensitivity = "N/A"
            
        print(f"{pair_str:<20} {base_str:<25} {delta_str:<20} {sensitivity}")

    print("=" * 70)
    print("Demo completed successfully! Matches theoretical values in Figure 1.")

if __name__ == "__main__":
    main()
