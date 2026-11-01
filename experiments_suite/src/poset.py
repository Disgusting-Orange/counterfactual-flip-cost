"""
poset.py - Core mathematical abstractions for Precedence DAGs and Posets.
"""

import networkx as nx
from typing import List, Tuple, Set, Dict, Optional

class EventDAG:
    def __init__(self, n_events: int, edges: List[Tuple[int, int]]):
        self.n = n_events
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(self.n))
        self.graph.add_edges_from(edges)
        
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Precedence graph must be a Directed Acyclic Graph (DAG).")
            
        # Compute transitive closure for O(1) reachability lookups
        self._transitive_closure: nx.DiGraph = nx.transitive_closure(self.graph)
        self._descendants_cache: Dict[int, Set[int]] = {
            u: set(self._transitive_closure.successors(u)) for u in range(self.n)
        }
        self._ancestors_cache: Dict[int, Set[int]] = {
            u: set(self._transitive_closure.predecessors(u)) for u in range(self.n)
        }
        
        # Precompute in-degrees and predecessors for fast search expansion
        self.in_degrees = {u: self.graph.in_degree(u) for u in range(self.n)}
        self.predecessors = {u: set(self.graph.predecessors(u)) for u in range(self.n)}
        self.successors = {u: set(self.graph.successors(u)) for u in range(self.n)}
        
    def has_path(self, u: int, v: int) -> bool:
        """Returns True if u precedes v in the transitive closure (u <_G v)."""
        return v in self._descendants_cache[u]
        
    def get_free_pairs(self) -> List[Tuple[int, int]]:
        """
        Returns all unconstrained pairs (u, v) with u < v such that neither
        u precedes v nor v precedes u.
        """
        free_pairs = []
        for u in range(self.n):
            for v in range(u + 1, self.n):
                if not self.has_path(u, v) and not self.has_path(v, u):
                    free_pairs.append((u, v))
        return free_pairs

    def is_valid_linear_extension(self, permutation: List[int]) -> bool:
        """Verifies if a permutation satisfies all precedence constraints."""
        if len(permutation) != self.n or set(permutation) != set(range(self.n)):
            return False
        pos = {v: i for i, v in enumerate(permutation)}
        for u, v in self.graph.edges:
            if pos[u] >= pos[v]:
                return False
        return True

    def add_counterfactual_constraint(self, u: int, v: int) -> Optional['EventDAG']:
        """
        Attempts to add directed edge (u, v) representing the counterfactual constraint.
        If adding (u, v) creates a cycle (i.e., if v already precedes u), returns None.
        """
        if self.has_path(v, u):
            return None  # Infeasible counterfactual: violates existing causal chain
            
        new_edges = list(self.graph.edges) + [(u, v)]
        try:
            return EventDAG(self.n, new_edges)
        except ValueError:
            return None
