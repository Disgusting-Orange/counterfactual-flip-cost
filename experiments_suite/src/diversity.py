"""
diversity.py - Diversity metrics and Farthest-First Candidate Selection.
"""

from typing import List, Tuple, Set
import numpy as np

def free_pair_disagreement_distance(
    pi_1: List[int], 
    pi_2: List[int], 
    free_pairs: List[Tuple[int, int]]
) -> float:
    """
    Computes normalized disagreement on unconstrained (free) pairs:
    d(pi_1, pi_2) = |{(u, v) in P_free : order disagrees}| / |P_free|
    """
    if not free_pairs:
        return 0.0
        
    pos1 = {v: i for i, v in enumerate(pi_1)}
    pos2 = {v: i for i, v in enumerate(pi_2)}
    
    disagreements = 0
    for u, v in free_pairs:
        order1 = pos1[u] < pos1[v]
        order2 = pos2[u] < pos2[v]
        if order1 != order2:
            disagreements += 1
            
    return disagreements / len(free_pairs)

def calculate_mean_diversity(candidates: List[List[int]], free_pairs: List[Tuple[int, int]]) -> float:
    """Computes the average pairwise diversity across a list of candidate timelines."""
    k = len(candidates)
    if k < 2 or not free_pairs:
        return 0.0
        
    total_dist = 0.0
    pairs_count = 0
    for i in range(k):
        for j in range(i + 1, k):
            total_dist += free_pair_disagreement_distance(candidates[i], candidates[j], free_pairs)
            pairs_count += 1
            
    return total_dist / pairs_count if pairs_count > 0 else 0.0

def farthest_first_selection(
    candidate_pool: List[Tuple[int, List[int]]], 
    k: int, 
    free_pairs: List[Tuple[int, int]]
) -> List[Tuple[int, List[int]]]:
    """
    Selects k diverse candidates from a pool using Farthest-First Traversal.
    Begins with the lowest-cost solution, then iteratively picks the candidate
    that maximizes the minimum distance to already selected candidates.
    """
    if not candidate_pool:
        return []
    if len(candidate_pool) <= k:
        return candidate_pool
        
    # Start with the best solution (first item, pool sorted by cost)
    selected = [candidate_pool[0]]
    remaining = candidate_pool[1:]
    
    while len(selected) < k and remaining:
        best_candidate = None
        max_min_dist = -1.0
        best_idx = -1
        
        for idx, cand in enumerate(remaining):
            # Compute distance to closest selected candidate
            min_dist = min(
                free_pair_disagreement_distance(cand[1], s[1], free_pairs)
                for s in selected
            )
            if min_dist > max_min_dist:
                max_min_dist = min_dist
                best_candidate = cand
                best_idx = idx
                
        if best_candidate is not None:
            selected.append(best_candidate)
            remaining.pop(best_idx)
        else:
            break
            
    return selected
