"""
generate_figure1_architecture.py - Renders Figure 1 (System Architecture Diagram)
as an IEEE publication-quality vector graphic (PNG & PDF).
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'experiments_suite/results'))
os.makedirs(RESULTS_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Style helper
def draw_box(x, y, w, h, title, subtitle="", color="#EBF3FB", border_color="#1E6BB8", title_color="#0D3B66"):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=1.5,rounding_size=2", 
                                facecolor=color, edgecolor=border_color, linewidth=1.5, zorder=2)
    ax.add_patch(box)
    if subtitle:
        ax.text(x + w/2, y + h/2 + 2.5, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=title_color, zorder=3)
        ax.text(x + w/2, y + h/2 - 3.5, subtitle, ha='center', va='center', fontsize=7.5, color='#333333', style='italic', zorder=3)
    else:
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=title_color, zorder=3)

def draw_arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#2B3A42", mutation_scale=12), zorder=4)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 2, label, ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#2B3A42', zorder=5)

# --- 1. INPUT LAYER ---
draw_box(4, 76, 26, 16, "Security Event Logs & Provenance", "Events V, Timestamps tau, Constraints E", color="#F4F6F9", border_color="#5A6B7C", title_color="#2C3E50")

# --- 2. PREPROCESSING & MODELING ---
draw_box(37, 76, 26, 16, "Phase 1: Poset Indexing", "Acyclicity Check, Closure E+, P_free", color="#E8F4F8", border_color="#2980B9", title_color="#1B4F72")

# --- 3. BOUNDED SEARCH CORE ---
draw_box(70, 76, 26, 16, "Phase 2: Bounded A* Engine", "Admissible h(s) + Dominance Pruning", color="#EAF2F8", border_color="#2471A3", title_color="#154360")

# Arrows top row
draw_arrow(30, 84, 37, 84, "Raw Ingestion")
draw_arrow(63, 84, 70, 84, "Causal DAG G")

# --- Downward branching from Search Core ---
# Arrow down to Diversity
draw_arrow(78, 76, 32, 52, "Candidate Pool C_pool")
# Arrow down to Counterfactual
draw_arrow(88, 76, 82, 52, "Optimal pi*, Cost c*")

# --- 4. DIVERSITY BRANCH (LEFT) ---
draw_box(10, 36, 34, 16, "Phase 3: Diversity Selection", "Farthest-First Traversal on P_free\n(Maximizes d_free disagreement)", color="#E8F8F5", border_color="#1ABC9C", title_color="#117864")

# --- 5. COUNTERFACTUAL BRANCH (RIGHT) ---
draw_box(56, 36, 38, 16, "Phase 4: Counterfactual Flip-Cost", "Reverse Free Pairs (b, a) -> G_flip\nRe-search -> Delta = c_flip - c* (MAP Log-Ratio)", color="#FEF5E7", border_color="#F39C12", title_color="#B9770E")

# --- 6. OUTPUT STAGE ---
draw_box(25, 4, 50, 16, "Operational Forensic Outputs", "Ranked Diverse Candidate Timelines (K-Best)  |  Pairwise Sensitivity Matrix  |  Search Status (Exact / Bounded)", color="#F5EEF8", border_color="#8E44AD", title_color="#512E5F")

# Arrows into Output Stage
draw_arrow(27, 36, 40, 20, "Diverse Set S")
draw_arrow(75, 36, 60, 20, "Sensitivity Scores Delta_B")

plt.tight_layout()
fig.savefig(os.path.join(RESULTS_DIR, 'figure1_system_architecture.png'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(RESULTS_DIR, 'figure1_system_architecture.pdf'), bbox_inches='tight')
plt.close(fig)
print("Figure 1 generated successfully.")
