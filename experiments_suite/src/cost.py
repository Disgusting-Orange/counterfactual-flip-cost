"""
cost.py - Inversion metrics and admissible heuristics for Best-First Search.
"""

from typing import List, Dict, Set
from poset import EventDAG

class InversionCostModel:
    def __init__(self, n_events: int, timestamps: List[float]):
        self.n = n_events
        self.timestamps = list(timestamps)
        
        # Reference timestamp permutation: sort events by timestamp ascending
        # Deterministic tie-breaking by event index
        self.pi_tau = sorted(range(self.n), key=lambda x: (self.timestamps[x], x))
        self.tau_pos: Dict[int, int] = {v: i for i, v in enumerate(self.pi_tau)}
        
    def total_cost(self, permutation: List[int]) -> int:
        """
        Computes the exact Kendall-tau distance (number of inversions)
        between the given permutation and reference order pi_tau.
        """
        pos = {v: i for i, v in enumerate(permutation)}
        inversions = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                u = self.pi_tau[i]
                v = self.pi_tau[j]
                # In pi_tau, u appears before v. If in permutation pos[u] > pos[v], it's an inversion.
                if pos[u] > pos[v]:
                    inversions += 1
        return inversions

    def incremental_cost(self, placed_prefix: List[int], next_event: int) -> int:
        """
        Calculates the incremental inversions incurred by placing next_event
        immediately after placed_prefix.
        An inversion occurs for every event u in placed_prefix that has a later
        timestamp than next_event (tau_pos[u] > tau_pos[next_event]).
        """
        v_tau = self.tau_pos[next_event]
        incurred = 0
        for u in placed_prefix:
            if self.tau_pos[u] > v_tau:
                incurred += 1
        return incurred

    def compute_admissible_heuristic(self, dag: EventDAG, unplaced: Set[int]) -> int:
        """
        Admissible Lower Bound h(s):
        For any pair of unplaced events {u, v} in unplaced:
        If u precedes v in the DAG (u <_G v), then u MUST be placed before v in any
        valid completion. If tau_pos[u] > tau_pos[v], this pair will GUARANTEE an
        inversion in all valid linear extensions extending this state.
        Summing these unavoidable future inversions gives an admissible (never overestimating) h(s).
        """
        unplaced_list = list(unplaced)
        h = 0
        for i in range(len(unplaced_list)):
            u = unplaced_list[i]
            for j in range(i + 1, len(unplaced_list)):
                v = unplaced_list[j]
                if dag.has_path(u, v) and self.tau_pos[u] > self.tau_pos[v]:
                    h += 1
                elif dag.has_path(v, u) and self.tau_pos[v] > self.tau_pos[u]:
                    h += 1
        return h
