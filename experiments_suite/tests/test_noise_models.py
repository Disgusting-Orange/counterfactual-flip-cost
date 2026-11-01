"""
test_noise_models.py - Unit tests for Gaussian and PRISM 2026 Structured Clock Skew models.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from noise_models import (
    generate_synthetic_incident,
    apply_gaussian_jitter_model,
    apply_structured_skew_model
)

def test_ground_truth_incident_validity():
    dag, gt_order, true_times = generate_synthetic_incident(n_events=15, edge_density=0.2, seed=42)
    assert dag.n == 15
    assert len(gt_order) == 15
    assert dag.is_valid_linear_extension(gt_order)
    # Check true timestamps strictly monotonic along gt_order
    for i in range(len(gt_order) - 1):
        u = gt_order[i]
        v = gt_order[i + 1]
        assert true_times[u] < true_times[v]

def test_structured_clock_skew_model():
    dag, gt_order, true_times = generate_synthetic_incident(n_events=20, edge_density=0.2, seed=99)
    trace = apply_structured_skew_model(dag, gt_order, true_times, n_hosts=4, max_offset=4.0, quantization_step=1.0)
    assert len(trace.noisy_timestamps) == 20
    assert len(trace.host_assignments) == 20
    assert set(trace.host_assignments).issubset({0, 1, 2, 3})
    # Check all timestamps are multiples of 1.0 (quantized)
    for t in trace.noisy_timestamps:
        assert t >= 0.0
        assert round(t, 2) == round(t)
