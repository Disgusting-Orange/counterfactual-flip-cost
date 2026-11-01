"""
test_counterfactual.py - Unit tests for counterfactual flip-cost computation and status handling.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from poset import EventDAG
from cost import InversionCostModel
from search import bounded_best_first_search
from counterfactual import compute_pairwise_flip_cost

def test_counterfactual_flip_cost_properties():
    # Chain: 0 -> 1 -> 2, plus independent node 3
    dag = EventDAG(4, [(0, 1), (1, 2)])
    # 0, 1, 2 timestamps: 1.0, 2.0, 3.0; node 3 timestamp: 1.5
    timestamps = [1.0, 2.0, 3.0, 1.5]
    cost_model = InversionCostModel(4, timestamps)
    
    baseline = bounded_best_first_search(dag, cost_model, budget=500)
    assert baseline.status == 'EXACT'
    
    # 1. Test unconstrained pair (0, 3)
    res_03 = compute_pairwise_flip_cost(dag, cost_model, baseline, (0, 3), search_budget=500)
    assert res_03.delta is not None
    assert res_03.delta >= 0
    assert res_03.status in ('EXACT', 'FEASIBLE')
    
    # 2. Test causally constrained pair (0, 2): reversal is impossible
    res_02 = compute_pairwise_flip_cost(dag, cost_model, baseline, (0, 2), search_budget=500)
    assert res_02.status == 'INFEASIBLE'
    assert res_02.delta is None
