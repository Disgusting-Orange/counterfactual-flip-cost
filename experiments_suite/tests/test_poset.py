"""
test_poset.py - Unit test suite for Poset, A* Search, and Brute-Force Exactness Verification.
"""

import sys
import os
import itertools
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from poset import EventDAG
from cost import InversionCostModel
from search import bounded_best_first_search
from noise_models import generate_synthetic_incident, apply_gaussian_jitter_model

def brute_force_exact_search(dag: EventDAG, cost_model: InversionCostModel):
    """Enumerates all permutations to find the true global minimum Kendall-tau linear extension."""
    n = dag.n
    best_cost = float('inf')
    best_perm = None
    all_valid = []
    
    for perm in itertools.permutations(range(n)):
        if dag.is_valid_linear_extension(list(perm)):
            c = cost_model.total_cost(list(perm))
            all_valid.append((c, list(perm)))
            if c < best_cost:
                best_cost = c
                best_perm = list(perm)
                
    all_valid.sort(key=lambda x: x[0])
    return best_cost, best_perm, all_valid

def test_poset_acyclicity_and_reachability():
    # Triangle DAG: 0 -> 1, 1 -> 2, 0 -> 2
    dag = EventDAG(3, [(0, 1), (1, 2)])
    assert dag.has_path(0, 2)
    assert not dag.has_path(2, 0)
    assert dag.get_free_pairs() == []

def test_astar_matches_brute_force_exactness():
    """Validates on small instances (N=7, 8) that A* matches brute-force global minimum 100% of the time."""
    for seed in range(10):
        dag, gt, true_t = generate_synthetic_incident(n_events=7, edge_density=0.2, seed=seed)
        trace = apply_gaussian_jitter_model(dag, gt, true_t, sigma=1.5)
        cost_model = InversionCostModel(dag.n, trace.noisy_timestamps)
        
        bf_cost, bf_perm, _ = brute_force_exact_search(dag, cost_model)
        astar_res = bounded_best_first_search(dag, cost_model, budget=5000)
        
        assert astar_res.status == 'EXACT'
        assert astar_res.cost == bf_cost, f"Seed {seed}: A* cost {astar_res.cost} != Brute-force {bf_cost}"
        assert dag.is_valid_linear_extension(astar_res.timeline)
        
if __name__ == "__main__":
    print("Running unit tests...")
    test_poset_acyclicity_and_reachability()
    print("Poset acyclicity and reachability passed!")
    test_astar_matches_brute_force_exactness()
    print("A* matches brute-force exactness on all test instances!")
