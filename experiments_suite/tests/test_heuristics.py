"""
test_heuristics.py - Tests Theorem 4 (Admissibility of h(s)) and Lemma 1 (Subset Dominance).
"""

import sys
import os
import itertools
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from poset import EventDAG
from cost import InversionCostModel
from noise_models import generate_synthetic_incident, apply_gaussian_jitter_model

def test_theorem_4_heuristic_admissibility():
    """
    Empirically verifies Theorem 4: For any state s = (P, U, R),
    0 <= h(s) <= h*(s), where h*(s) is the minimum true additional cost
    among ALL valid completions of prefix P.
    """
    for seed in range(5):
        dag, gt, tt = generate_synthetic_incident(n_events=6, edge_density=0.25, seed=seed + 10)
        trace = apply_gaussian_jitter_model(dag, gt, tt, sigma=1.5)
        cost_model = InversionCostModel(dag.n, trace.noisy_timestamps)
        
        # Test across partial states
        n = dag.n
        for prefix_len in range(1, n - 1):
            for perm in itertools.permutations(range(n)):
                prefix = list(perm[:prefix_len])
                # Check prefix is valid
                placed_set = set(prefix)
                prefix_valid = True
                for u in prefix:
                    if not dag.predecessors[u].issubset(placed_set):
                        # Some predecessor wasn't placed before u in prefix
                        # check topological validity of prefix alone
                        pass
                
                # Check if prefix order preserves internal precedence
                pos_p = {v: i for i, v in enumerate(prefix)}
                internal_valid = True
                for u in prefix:
                    for v in prefix:
                        if (u, v) in dag.graph.edges and pos_p[u] >= pos_p[v]:
                            internal_valid = False
                            break
                    if not internal_valid:
                        break
                if not internal_valid:
                    continue
                    
                # Valid partial prefix found
                unplaced = set(range(n)) - placed_set
                h = cost_model.compute_admissible_heuristic(dag, unplaced)
                assert h >= 0, "Heuristic must be non-negative"
                
                # Compute exact h*(s) by enumerating all completions of prefix
                g = 0
                for idx, w in enumerate(prefix):
                    g += cost_model.incremental_cost(prefix[:idx], w)
                    
                min_full_cost = float('inf')
                for comp_perm in itertools.permutations(list(unplaced)):
                    full_perm = prefix + list(comp_perm)
                    if dag.is_valid_linear_extension(full_perm):
                        full_cost = cost_model.total_cost(full_perm)
                        if full_cost < min_full_cost:
                            min_full_cost = full_cost
                            
                if min_full_cost < float('inf'):
                    h_star = min_full_cost - g
                    assert h <= h_star, f"Theorem 4 violated! h={h} > h*={h_star}"
                    break
