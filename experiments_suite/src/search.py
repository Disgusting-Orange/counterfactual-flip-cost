"""
search.py - Bounded Best-First Search (A*) for Precedence-Constrained Inversion Minimization.
"""

import heapq
from typing import List, Tuple, Optional, Set, Dict
from poset import EventDAG
from cost import InversionCostModel

class SearchResult:
    def __init__(self, 
                 timeline: Optional[List[int]], 
                 cost: Optional[int], 
                 expansions: int, 
                 status: str,
                 pool: Optional[List[Tuple[int, List[int]]]] = None):
        self.timeline = timeline
        self.cost = cost
        self.expansions = expansions
        self.status = status  # 'EXACT', 'FEASIBLE', 'BUDGET_EXHAUSTED', 'INFEASIBLE'
        self.pool = pool if pool is not None else []

def bounded_best_first_search(
    dag: EventDAG,
    cost_model: InversionCostModel,
    budget: int = 1000,
    pool_size: int = 1,
    suboptimality_slack: Optional[int] = None
) -> SearchResult:
    """
    Finds the lowest-cost linear extension of DAG minimizing Kendall-tau distance
    to cost_model.pi_tau using A* search with dominance pruning.
    
    Dominance Property:
    For any partial prefix placing subset U of V, the cross-inversions between U and V \ U
    are invariant to the internal permutation of U. Therefore, for any subset U, only
    the minimal-cost prefix placing U needs to be retained.
    """
    n = dag.n
    # Priority queue stores tuples: (f, g, prefix, unplaced_set)
    initial_unplaced = frozenset(range(n))
    initial_h = cost_model.compute_admissible_heuristic(dag, set(initial_unplaced))
    
    # Priority queue: (f_score, -depth, g_score, counter, prefix, unplaced_frozen)
    counter = 0
    open_set = [(initial_h, 0, 0, counter, (), initial_unplaced)]
    
    # Best g-cost seen for each placed subset (dominance pruning for prefix subsets)
    best_g_for_subset: Dict[frozenset, int] = {frozenset(): 0}
    
    completed_solutions: List[Tuple[int, List[int]]] = []
    seen_permutations: Set[Tuple[int, ...]] = set()
    expansions = 0
    best_incumbent_cost = float('inf')
    
    while open_set and expansions < budget:
        f, neg_depth, g, _, prefix, unplaced = heapq.heappop(open_set)
        
        placed_set = frozenset(prefix)
        # Dominance check for partial states
        if len(prefix) < n and g > best_g_for_subset.get(placed_set, float('inf')):
            continue
            
        # Goal check
        if len(prefix) == n:
            if prefix not in seen_permutations:
                seen_permutations.add(prefix)
                completed_solutions.append((g, list(prefix)))
                if g < best_incumbent_cost:
                    best_incumbent_cost = g
                    
                if len(completed_solutions) >= pool_size:
                    completed_solutions.sort(key=lambda x: x[0])
                    return SearchResult(
                        timeline=completed_solutions[0][1],
                        cost=completed_solutions[0][0],
                        expansions=expansions,
                        status='EXACT',
                        pool=completed_solutions
                    )
            continue
            
        expansions += 1
        
        # Determine available candidates: unplaced nodes whose predecessors are all placed
        available = [u for u in unplaced if dag.predecessors[u].issubset(placed_set)]
        # Order available candidates by their timestamp position for strong guidance
        available.sort(key=lambda u: cost_model.tau_pos[u])
        
        for cand in available:
            new_prefix = prefix + (cand,)
            new_placed_set = frozenset(new_prefix)
            new_unplaced = unplaced - {cand}
            
            incremental = cost_model.incremental_cost(list(prefix), cand)
            new_g = g + incremental
            
            # Prune if this subset of nodes has already been produced with a lower cost
            if len(new_prefix) < n:
                # If pool_size == 1, strict dominance
                if pool_size == 1:
                    if new_g >= best_g_for_subset.get(new_placed_set, float('inf')):
                        continue
                else:
                    # Allow a slack of 2 for pool generation to retain diverse orderings
                    if new_g > best_g_for_subset.get(new_placed_set, float('inf')) + 2:
                        continue
                best_g_for_subset[new_placed_set] = min(best_g_for_subset.get(new_placed_set, float('inf')), new_g)
                
            h = cost_model.compute_admissible_heuristic(dag, set(new_unplaced))
            new_f = new_g + h
            
            counter += 1
            heapq.heappush(open_set, (new_f, -len(new_prefix), new_g, counter, new_prefix, new_unplaced))
            
    # Completed loop or budget reached
    if completed_solutions:
        # Sort solutions by cost
        completed_solutions.sort(key=lambda x: x[0])
        status = 'EXACT' if not open_set or completed_solutions[0][0] <= (open_set[0][0] if open_set else completed_solutions[0][0]) else 'FEASIBLE'
        return SearchResult(
            timeline=completed_solutions[0][1],
            cost=completed_solutions[0][0],
            expansions=expansions,
            status=status,
            pool=completed_solutions
        )
    else:
        return SearchResult(
            timeline=None,
            cost=None,
            expansions=expansions,
            status='BUDGET_EXHAUSTED',
            pool=[]
        )
