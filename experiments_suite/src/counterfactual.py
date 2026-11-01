"""
counterfactual.py - Pairwise Counterfactual Flip-Cost Analysis.
"""

from typing import List, Tuple, Dict, Optional
from poset import EventDAG
from cost import InversionCostModel
from search import bounded_best_first_search, SearchResult

class FlipCostResult:
    def __init__(self, 
                 pair: Tuple[int, int], 
                 baseline_order: Tuple[int, int],
                 baseline_cost: int,
                 counterfactual_cost: Optional[int],
                 delta: Optional[int],
                 status: str,
                 expansions: int):
        self.pair = pair
        self.baseline_order = baseline_order
        self.baseline_cost = baseline_cost
        self.counterfactual_cost = counterfactual_cost
        self.delta = delta
        self.status = status
        self.expansions = expansions

def compute_pairwise_flip_cost(
    dag: EventDAG,
    cost_model: InversionCostModel,
    baseline_result: SearchResult,
    pair: Tuple[int, int],
    search_budget: int = 1000
) -> FlipCostResult:
    """
    Computes Delta_B(a, b) for an unconstrained pair (u, v).
    Determines baseline relative order in baseline_result.timeline,
    forces the reversed order in an augmented DAG, and runs bounded A*.
    """
    if baseline_result.timeline is None or baseline_result.cost is None:
        raise ValueError("Valid baseline result required for counterfactual analysis.")
        
    u, v = pair
    pos = {node: i for i, node in enumerate(baseline_result.timeline)}
    
    # Identify which event precedes which in baseline timeline
    if pos[u] < pos[v]:
        first, second = u, v
    else:
        first, second = v, u
        
    baseline_order = (first, second)
    baseline_cost = baseline_result.cost
    
    # Counterfactual constraint: force second to precede first
    cf_dag = dag.add_counterfactual_constraint(second, first)
    if cf_dag is None:
        return FlipCostResult(
            pair=pair,
            baseline_order=baseline_order,
            baseline_cost=baseline_cost,
            counterfactual_cost=None,
            delta=None,
            status='INFEASIBLE',
            expansions=0
        )
        
    cf_result = bounded_best_first_search(cf_dag, cost_model, budget=search_budget)
    
    if cf_result.status in ('EXACT', 'FEASIBLE') and cf_result.cost is not None:
        delta = cf_result.cost - baseline_cost
        return FlipCostResult(
            pair=pair,
            baseline_order=baseline_order,
            baseline_cost=baseline_cost,
            counterfactual_cost=cf_result.cost,
            delta=delta,
            status=cf_result.status,
            expansions=cf_result.expansions
        )
    else:
        return FlipCostResult(
            pair=pair,
            baseline_order=baseline_order,
            baseline_cost=baseline_cost,
            counterfactual_cost=None,
            delta=None,
            status='BUDGET_EXHAUSTED',
            expansions=cf_result.expansions
        )

def evaluate_all_free_pairs(
    dag: EventDAG,
    cost_model: InversionCostModel,
    baseline_result: SearchResult,
    search_budget: int = 1000
) -> List[FlipCostResult]:
    """Computes counterfactual flip-cost for all free pairs in G."""
    free_pairs = dag.get_free_pairs()
    results = []
    for pair in free_pairs:
        res = compute_pairwise_flip_cost(dag, cost_model, baseline_result, pair, search_budget)
        results.append(res)
    return results
