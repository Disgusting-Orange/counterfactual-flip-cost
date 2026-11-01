"""
noise_models.py - Synthetic Event Generators and Realistic Distorted Noise Models.
"""

import numpy as np
import random
from typing import List, Tuple, Dict, Optional
from poset import EventDAG

class SyntheticIncidentTrace:
    def __init__(self, 
                 n_events: int, 
                 dag: EventDAG, 
                 ground_truth_order: List[int], 
                 true_timestamps: List[float], 
                 noisy_timestamps: List[float],
                 host_assignments: Optional[List[int]] = None):
        self.n = n_events
        self.dag = dag
        self.ground_truth_order = ground_truth_order
        self.true_timestamps = true_timestamps
        self.noisy_timestamps = noisy_timestamps
        self.host_assignments = host_assignments

def generate_synthetic_incident(
    n_events: int = 20, 
    edge_density: float = 0.25, 
    seed: Optional[int] = None
) -> Tuple[EventDAG, List[int], List[float]]:
    """
    Generates a ground-truth causal DAG and true timestamps.
    Ensures true precedence constraints are strictly acyclic.
    """
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
        
    ground_truth = list(range(n_events))
    random.shuffle(ground_truth)
    
    # Ground truth times spaced strictly monotonic according to ground truth order
    time_deltas = np.random.exponential(scale=2.0, size=n_events)
    true_times = np.cumsum(time_deltas)
    
    true_timestamps = [0.0] * n_events
    for rank, node in enumerate(ground_truth):
        true_timestamps[node] = float(true_times[rank])
        
    # Generate precedence edges consistent with ground_truth
    edges = []
    for i in range(n_events):
        u = ground_truth[i]
        for j in range(i + 1, n_events):
            v = ground_truth[j]
            if random.random() < edge_density:
                edges.append((u, v))
                
    dag = EventDAG(n_events, edges)
    return dag, ground_truth, true_timestamps

def apply_gaussian_jitter_model(
    dag: EventDAG,
    ground_truth: List[int],
    true_timestamps: List[float],
    sigma: float = 1.5,
    delay_prob: float = 0.1,
    delay_range: Tuple[float, float] = (3.0, 8.0)
) -> SyntheticIncidentTrace:
    """Noise Model 1: Uncorrelated Gaussian jitter with occasional positive delay bursts."""
    noisy_times = []
    for t in true_timestamps:
        jitter = np.random.normal(0, sigma)
        burst = random.uniform(*delay_range) if random.random() < delay_prob else 0.0
        noisy_times.append(max(0.0, float(t + jitter + burst)))
        
    return SyntheticIncidentTrace(
        n_events=dag.n,
        dag=dag,
        ground_truth_order=ground_truth,
        true_timestamps=true_timestamps,
        noisy_timestamps=noisy_times
    )

def apply_structured_skew_model(
    dag: EventDAG,
    ground_truth: List[int],
    true_timestamps: List[float],
    n_hosts: int = 4,
    max_offset: float = 4.0,
    quantization_step: float = 1.0
) -> SyntheticIncidentTrace:
    """
    Noise Model 2: Structured Multi-Source Clock Skew (Kimm et al., PRISM 2026).
    Simulates cross-host event merging with per-host clock offset,
    drift, and coarse millisecond/second timestamp quantization.
    """
    n = dag.n
    # Assign each event to an originating host
    hosts = [random.randint(0, n_hosts - 1) for _ in range(n)]
    
    # Per-host static clock offset and drift
    host_offsets = [random.uniform(-max_offset, max_offset) for _ in range(n_hosts)]
    host_drifts = [random.normalvariate(0, 0.05) for _ in range(n_hosts)]
    
    noisy_times = []
    for i in range(n):
        h = hosts[i]
        t = true_timestamps[i]
        t_skewed = t + host_offsets[h] + (t * host_drifts[h])
        # Apply quantization (e.g. 1.0 second or 100ms buckets)
        t_quantized = round(t_skewed / quantization_step) * quantization_step
        noisy_times.append(max(0.0, float(t_quantized)))
        
    return SyntheticIncidentTrace(
        n_events=n,
        dag=dag,
        ground_truth_order=ground_truth,
        true_timestamps=true_timestamps,
        noisy_timestamps=noisy_times,
        host_assignments=hosts
    )
