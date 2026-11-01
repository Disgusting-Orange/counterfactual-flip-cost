# Counterfactual Flip-Cost Analysis: Quantifying Pairwise Ordering Ambiguity in Precedence-Constrained Security Timelines

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![IEEE Access](https://img.shields.io/badge/Target-IEEE%20Access-orange.svg)](https://ieeeaccess.ieee.org/)
[![Tests CI](https://img.shields.io/badge/tests-6%20passed-brightgreen.svg)]()

Official reference implementation, reproducibility benchmark suite, and complete camera-ready LaTeX source for the paper:
> **Counterfactual Flip-Cost Analysis: Quantifying Pairwise Ordering Ambiguity in Precedence-Constrained Security Timelines**  
> *Authors: Kamalesh N., Varun Dubey*  
> *School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, India*  
> *(Target Venue: IEEE Access)*

---

## 📌 Section V Paper Claims & Codebase Verification

As stated in **Section V (Experimental Setup)** of the manuscript:
> *"All benchmarking code, synthetic poset generators, noise distortion models, and unit test suites are open-sourced for reproducibility at [https://github.com/Disgusting-Orange/counterfactual-flip-cost](https://github.com/Disgusting-Orange/counterfactual-flip-cost)."*

This repository fulfills every claim made in the paper:

| Paper Claim in Section V | Source Location in Repository | Description / Capabilities |
| :--- | :--- | :--- |
| **Synthetic Poset Generators** | [`experiments_suite/src/noise_models.py`](experiments_suite/src/noise_models.py) | Generates ground-truth DAGs with tunable edge densities ($p_{edge} \in [0.15, 0.35]$) and exponential inter-event intervals ($\lambda = 0.5$). |
| **Noise Distortion Model 1** | [`experiments_suite/src/noise_models.py`](experiments_suite/src/noise_models.py) | Uncorrelated Gaussian timestamp jitter ($\sigma \in \{1.0, 1.5, 2.0, 4.0\}$ s), burst delays, and missing record drops. |
| **Noise Distortion Model 2** | [`experiments_suite/src/noise_models.py`](experiments_suite/src/noise_models.py) | **Kimm et al. (PRISM 2026)** multi-source structured clock skew ($M=4$ distributed hosts, asymmetric offsets $[-4, 4]$ s, drift, 1-second quantisation). |
| **Bounded A* Engine** | [`experiments_suite/src/search.py`](experiments_suite/src/search.py) | Bounded search with admissible heuristic $h(s)$ and exact subset-dominance pruning (Theorem 4 & Lemma 1). |
| **Counterfactual Sensitivity** | [`experiments_suite/src/counterfactual.py`](experiments_suite/src/counterfactual.py) | Computes $\Delta_B(a, b) = c_{flip} - c^*$ with explicit unverified status $\bot$ upon budget exhaustion. |
| **Diversity Selection** | [`experiments_suite/src/diversity.py`](experiments_suite/src/diversity.py) | Farthest-first traversal over unconstrained free pairs ($P_{free}$). |
| **Unit Test Suites** | [`experiments_suite/tests/`](experiments_suite/tests/) | **100% Passing:** Poset acyclicity, 60/60 brute-force exactness, heuristic admissibility (Theorem 4), noise models, and flip-costs. |
| **Camera-Ready LaTeX Source** | [`paper/`](paper/) | Complete IEEE Access LaTeX source (`main.tex`), class files (`ieeeaccess.cls`, `IEEEtran.cls`), and all 8 vector figures (`figures/*.pdf`, `*.tex`). |

---

## 🚀 Key Experimental Findings

1. **Exactness:** Bounded A* search matched global brute-force minimum cost on **60/60 benchmark instances (100%)**.
2. **Superiority over Probabilistic Baselines:** In single-incident investigations lacking recurring historical case-bases, process-mining marginal probability baselines fail (AUROC 0.58–0.60), whereas our Counterfactual Flip-Cost achieves **AUROC 0.801–0.856**.
3. **Severe Distortion Robustness:** Under high timestamp noise ($\sigma = 4.0$ s), the timestamp-margin heuristic collapses to 0.740, while Flip-Cost retains **0.801 AUROC** ($+0.061$ gain, 95% bootstrap CI $[+0.030, +0.092]$, $p < 0.001$).
4. **Sub-Second Scalability:** Scales to $N = 50$ events (search space $50! \approx 3 \times 10^{64}$) in **327 milliseconds** (average 1,530 expansions).

---

## 📂 Repository Layout

```
.
├── paper/                        # Complete IEEE Access Camera-Ready LaTeX Package
│   ├── main.tex                  # The exact 10-page IEEE Access manuscript
│   ├── ieeeaccess.cls            # Official IEEE Access document class
│   ├── IEEEtran.cls              # IEEEtran class
│   ├── figures/                  # All 8 publication figures (.pdf and .tex source)
│   └── *.png                     # IEEE Access banner and branding logos
│
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
│   │   ├── test_poset.py         # Unit tests & 100% brute-force exactness verification
│   │   ├── test_heuristics.py    # Theorem 4 admissibility verification (0 <= h <= h*)
│   │   ├── test_noise_models.py  # Gaussian and PRISM 2026 model tests
│   │   └── test_counterfactual.py# Flip-cost and status handling tests
│   ├── benchmarks/
│   │   ├── run_comprehensive_benchmark.py # Generates Tables 1, 2, 3 & Figure 6
│   │   └── generate_additional_figures.py # Generates Figure 5, 8 & N=10..50 scalability
│   └── results/                  # Generated CSVs and publication-grade vector plots (PDF/PNG)
│
├── examples/
│   └── quickstart_example.py     # 1-second reproduction of Figure 1 (5-event toy example)
│
├── .github/workflows/ci.yml      # Automated GitHub Actions test runner
├── requirements.txt              # Standard Python dependencies
├── setup.py                      # Package installation config (pip install -e .)
├── LICENSE                       # MIT License
└── README.md
```

---

## 🛠️ Quickstart & Reproducibility

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Disgusting-Orange/counterfactual-flip-cost.git
cd counterfactual-flip-cost
pip install -r requirements.txt
```

### 2. Run the 1-Second Quickstart Demo (Figure 1 in Paper)
Reproduces the 5-event scenario showing $c^* = 2$, fragile flip $\Delta(C, B) = 1$, and robust flip $\Delta(A, D) = 4$:
```bash
python examples/quickstart_example.py
```

### 3. Run the Full Unit Test Suite (6 Tests)
```bash
pytest experiments_suite/tests/
```

### 4. Run Comprehensive Paper Benchmarks
```bash
python experiments_suite/benchmarks/run_comprehensive_benchmark.py
python experiments_suite/benchmarks/generate_additional_figures.py
```

---

## 📖 Citation

```bibtex
@article{kamalesh2026flipcost,
  author    = {Kamalesh N. and Varun Dubey},
  title     = {Counterfactual Flip-Cost Analysis: Quantifying Pairwise Ordering Ambiguity in Precedence-Constrained Security Timelines},
  journal   = {IEEE Access},
  volume    = {12},
  year      = {2026}
}
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
