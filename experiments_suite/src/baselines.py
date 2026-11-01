"""
baselines.py - Baseline sensitivity metrics (Timestamp Margin and Probabilistic Marginals).
"""

from typing import List, Tuple, Dict, Optional
import numpy as np

def compute_timestamp_margin(u: int, v: int, timestamps: List[float]) -> float:
    """
    Computes absolute timestamp difference: |tau(u) - tau(v)|.
    Heuristic hypothesis: Events further apart in recorded time are less ambiguous.
    """
    return abs(timestamps[u] - timestamps[v])

def compute_mallows_pair_probability(
    u: int, 
    v: int, 
    candidate_pool: List[Tuple[int, List[int]]], 
    theta: float = 0.5
) -> float:
    """
    Computes empirical marginal probability P(u < v) under a Mallows model
    estimated over the candidate pool:
    P(u < v) = sum_{pi with u < v} exp(-theta * c(pi)) / sum_{pi} exp(-theta * c(pi))
    """
    if not candidate_pool:
        return 0.5
        
    weights = []
    indicators = []
    
    for cost, timeline in candidate_pool:
        w = np.exp(-theta * cost)
        weights.append(w)
        pos = {node: i for i, node in enumerate(timeline)}
        indicators.append(1.0 if pos[u] < pos[v] else 0.0)
        
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.5
        
    weighted_prob = sum(w * ind for w, ind in zip(weights, indicators)) / total_weight
    return float(weighted_prob)
