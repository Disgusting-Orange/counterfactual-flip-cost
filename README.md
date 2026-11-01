# Counterfactual Flip-Cost Analysis: Quantifying Pairwise Ordering Ambiguity in Precedence-Constrained Security Timelines

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IEEE Access](https://img.shields.io/badge/Target-IEEE%20Access-orange.svg)](https://ieeeaccess.ieee.org/)

Official reference implementation, reproducibility benchmark suite, and LaTeX manuscript for the paper:
> **Counterfactual Flip-Cost Analysis: Quantifying Pairwise Ordering Ambiguity in Precedence-Constrained Security Timelines**  
> *Authors: Kamalesh N., Varun Dubey*  
> *School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, India*  
> *(Target Venue: IEEE Access)*

---

## 📌 Overview

Reconstructing cyber incident timelines from heterogeneous security logs is frequently undermined by timestamp distortions—such as per-core hardware clock drift, network transit latency, coarse millisecond quantisation, and adversary anti-forensic *timestomping*. While physical causality and system provenance enforce invariant Directed Acyclic Graph (DAG) precedence constraints, finding the minimal-inversion linear extension is **NP-complete** (Nearest-Neighbour Kendall-Tau Distance on Posets).

This repository introduces **Counterfactual Flip-Cost ($\Delta(a, b)$)**:
* Rather than trusting an arbitrary single optimal sequence $\pi^*$, we quantify the stability of individual pairwise decisions $(a \prec b)$ by measuring the marginal reconstruction penalty incurred when strictly forcing $b$ before $a$.
* **Theoretical Equivalence:** We prove that $\Delta(a, b)$ is mathematically identical to the **log-ratio of extremal Maximum A Posteriori (MAP) realizations** under a precedence-conditioned Mallows ranking model.
* **Algorithmic Engine:** Includes a budget-bounded A* search with an admissible heuristic $h(s)$ and exact subset-dominance pruning (matching brute-force search on 100% of test instances), plus farthest-first diversity traversal over unconstrained pairs ($P_{free}$).

---

## 🚀 Key Experimental Findings

1. **Exactness:** Bounded A* search matched global brute-force minimum cost on **60/60 benchmark instances (100%)**.
2. **Superiority over Probabilistic Baselines:** In single-incident investigations lacking recurring historical case-bases, process-mining marginal probability baselines fail (AUROC 0.58–0.60), whereas our Counterfactual Flip-Cost achieves **AUROC 0.801–0.856**.
3. **Severe Distortion Robustness:** Under high timestamp noise ($\sigma = 4.0$ s), the timestamp-margin heuristic collapses to 0.740, while Flip-Cost retains **0.801 AUROC** ($+0.061$ gain, 95% bootstrap CI $[+0.030, +0.092]$, $p < 0.001$).
4. **Sub-Second Scalability:** Scales to $N = 50$ events (search space $50! \approx 3 \times 10^{64}$) in **327 milliseconds** (average 1,530 expansions).

---

## 📂 Repository Structure

```
.
├── experiments_suite/
│   ├── src/
│   │   ├── poset.py              # Poset algebra, DAG transitive closure, reachability, P_free
│   │   ├── cost.py               # Kendall-tau inversion cost, admissible lower-bound h(s)
│   │   ├── search.py             # Bounded A* search with subset-dominance pruning
│   │   ├── diversity.py          # Farthest-First Candidate Selection on free pairs
│   │   ├── counterfactual.py     # Pairwise Flip-Cost Delta_B(a, b) computation
│   │   ├── baselines.py          # Timestamp Margin and Mallows Marginal Baselines
│   │   └── noise_models.py       # Gaussian jitter & PRISM 2026 Structured Clock Skew
│   ├── tests/
│   │   └── test_poset.py         # Unit tests & 100% brute-force exactness verification
│   ├── benchmarks/
│   │   ├── run_comprehensive_benchmark.py # Generates Tables 1, 2, 3 & Figure 2
│   │   └── generate_additional_figures.py # Generates Figures 3, 4 & N=10..50 scalability
│   └── results/                  # Generated CSVs and publication-grade vector plots (PDF/PNG)
│
├── ieee_manuscript/              # Camera-ready IEEE Access LaTeX package
│   ├── main.tex                  # Full IEEEtran LaTeX manuscript
│   ├── references.bib            # 30 verified IEEE citations
│   └── *.pdf / *.png             # High-resolution publication figures
│
├── paper_draft.md                # Markdown manuscript edition
└── README.md
```

---

## 🛠️ Quickstart & Reproducibility

### Prerequisites
Python 3.9+ with standard data science packages:
```bash
pip install numpy scipy matplotlib networkx scikit-learn
```

### 1. Run Unit Tests (Brute-Force Verification)
```bash
python experiments_suite/tests/test_poset.py
```

### 2. Run Comprehensive Benchmarks (Tables & AUROC)
```bash
python experiments_suite/benchmarks/run_comprehensive_benchmark.py
```

### 3. Run Scalability Benchmarks ($N=10$ to $50$)
```bash
python experiments_suite/benchmarks/generate_additional_figures.py
```

All output CSV tables and high-resolution PDF/PNG figures will be populated in `experiments_suite/results/`.

---

## 📖 Citation

```bibtex
@article{kamalesh2026flipcost,
  author    = {Kamalesh N. and Varun Dubey},
  title     = {Counterfactual Flip-Cost Analysis: Quantifying Pairwise Ordering Ambiguity in Precedence-Constrained Security Timelines},
  journal   = {IEEE Access},
  year      = {2026}
}
```

---

## 📄 License
This project is open-source under the MIT License.
