"""
generate_additional_figures.py - Renders Figure 3 (Diversity vs Search Effort)
and conducts Scalability Benchmark (N=10 to 50) for Section 6.
"""

import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from poset import EventDAG
from cost import InversionCostModel
from search import bounded_best_first_search
from noise_models import generate_synthetic_incident, apply_gaussian_jitter_model

RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../results'))
os.makedirs(RESULTS_DIR, exist_ok=True)

def generate_figure3():
    # Data from Table 1 & Table 3
    methods = ['Score-only', 'Pool + Diverse', 'Flip-based Diverse']
    diversities = [0.060, 0.077, 0.145]
    expansions = [546, 547, 2186]
    
    fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=300)
    colors = ['#1f77b4', '#2ca02c', '#d62728']
    markers = ['o', 's', '^']
    
    for i, m in enumerate(methods):
        ax.scatter([diversities[i]], [expansions[i]], color=colors[i], marker=markers[i], s=120, label=m, zorder=5)
        ax.annotate(m, (diversities[i], expansions[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', fontsize=9)
        
    ax.plot(diversities, expansions, 'k--', alpha=0.5, zorder=3)
    ax.set_xlabel('Mean Candidate Diversity ($d_{free}$)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Search Expansions ($S$)', fontsize=11, fontweight='bold')
    ax.set_title('Figure 3: Trade-off Between Candidate Diversity and Search Effort', fontsize=11, fontweight='bold')
    ax.set_xlim(0.04, 0.17)
    ax.set_ylim(0, 2600)
    ax.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    
    fig.savefig(os.path.join(RESULTS_DIR, 'figure3_diversity_effort_tradeoff.png'), dpi=300)
    fig.savefig(os.path.join(RESULTS_DIR, 'figure3_diversity_effort_tradeoff.pdf'))
    plt.close(fig)
    print("Figure 3 saved successfully.")

def run_scalability_benchmark():
    print("\n--- Running Scalability Benchmark (N=10, 20, 30, 40, 50) ---")
    sizes = [10, 20, 30, 40, 50]
    runtimes = []
    expansions = []
    costs = []
    
    for n in sizes:
        times_n = []
        exp_n = []
        cost_n = []
        for s in range(15):
            dag, gt, tt = generate_synthetic_incident(n_events=n, edge_density=0.25, seed=s + 300)
            tr = apply_gaussian_jitter_model(dag, gt, tt, sigma=1.5)
            cm = InversionCostModel(n, tr.noisy_timestamps)
            
            t0 = time.perf_counter()
            res = bounded_best_first_search(dag, cm, budget=3000, pool_size=1)
            t1 = time.perf_counter()
            
            if res.timeline is not None:
                times_n.append((t1 - t0) * 1000)
                exp_n.append(res.expansions)
                cost_n.append(res.cost)
                
        runtimes.append(np.mean(times_n) if times_n else 0.0)
        expansions.append(np.mean(exp_n) if exp_n else 0.0)
        costs.append(np.mean(cost_n) if cost_n else 0.0)
        print(f"N={n}: Mean Runtime={runtimes[-1]:.2f} ms, Mean Expansions={expansions[-1]:.1f}, Mean Inversion Cost={costs[-1]:.2f}")
        
    # Plot Scalability Figure 4
    fig, ax1 = plt.subplots(figsize=(6, 4.2), dpi=300)
    ax2 = ax1.twinx()
    
    l1 = ax1.plot(sizes, runtimes, 'b-o', label='Runtime (ms)', linewidth=2)
    l2 = ax2.plot(sizes, expansions, 'r--s', label='Search Expansions', linewidth=2)
    
    ax1.set_xlabel('Event Count ($N$)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Mean Runtime (ms)', color='b', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Mean Search Expansions', color='r', fontsize=11, fontweight='bold')
    ax1.set_title('Figure 4: Computational Scalability Across Graph Dimensions ($N$)', fontsize=11, fontweight='bold')
    
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True)
    plt.tight_layout()
    
    fig.savefig(os.path.join(RESULTS_DIR, 'figure4_scalability_runtime.png'), dpi=300)
    fig.savefig(os.path.join(RESULTS_DIR, 'figure4_scalability_runtime.pdf'))
    plt.close(fig)
    print("Figure 4 saved successfully.")

if __name__ == "__main__":
    generate_figure3()
    run_scalability_benchmark()
