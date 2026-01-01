#!/usr/bin/env python3
"""
Generate visualizations from real benchmark results
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Read real benchmark results
results_file = Path('/Users/sajad/Desktop/Chain/benchmarks/real_benchmark_results.json')
with open(results_file, 'r') as f:
    data = json.load(f)

results = data['results']
BITCOIN_TPS = data['bitcoin_tps_baseline']

# Extract data
side_chains = [r['config']['side_chains'] for r in results]
tps_avg = [r['tps_avg'] for r in results]
tps_min = [r['tps_min'] for r in results]
tps_max = [r['tps_max'] for r in results]
vs_bitcoin = [r['vs_bitcoin'] for r in results]
transactions = [r['config']['transactions'] for r in results]

# Output directory
img_dir = Path('/Users/sajad/Desktop/Chain/thesis_latex_sample/img')
img_dir.mkdir(exist_ok=True)

print("📊 Generating visualization plots from real benchmark data...")

# Plot 1: TPS vs Number of Side Chains (with error bars)
plt.figure(figsize=(10, 6))
errors = [(r['tps_avg'] - r['tps_min'], r['tps_max'] - r['tps_avg']) for r in results]
plt.errorbar(side_chains, tps_avg, yerr=np.array(errors).T, 
             fmt='bo-', linewidth=2, markersize=8, capsize=5, capthick=2,
             label='Real Measured TPS')
plt.axhline(y=BITCOIN_TPS, color='r', linestyle='--', linewidth=2, label='Bitcoin TPS')
plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
plt.ylabel('Transactions Per Second (TPS)', fontsize=12, fontweight='bold')
plt.title('Real Blockchain Performance: TPS vs Side Chains', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.yscale('log')  # Log scale to better show the range
plt.tight_layout()
plt.savefig(img_dir / 'real_tps_vs_sidechains.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'real_tps_vs_sidechains.png'}")
plt.close()

# Plot 2: Improvement Factor vs Bitcoin (bar chart)
plt.figure(figsize=(10, 6))
colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
bars = plt.bar(range(len(side_chains)), vs_bitcoin, color=colors, alpha=0.7)
plt.axhline(y=1, color='r', linestyle='--', linewidth=2, label='Bitcoin Baseline')
plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
plt.ylabel('Improvement Factor (vs Bitcoin)', fontsize=12, fontweight='bold')
plt.title('Real Performance Improvement over Bitcoin', fontsize=14, fontweight='bold')
plt.xticks(range(len(side_chains)), side_chains)
plt.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, vs_bitcoin)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'{val:.0f}x', ha='center', va='bottom', fontweight='bold')

plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig(img_dir / 'real_improvement_vs_bitcoin.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'real_improvement_vs_bitcoin.png'}")
plt.close()

# Plot 3: TPS with min/max range visualization
plt.figure(figsize=(10, 6))
x_pos = np.arange(len(side_chains))

# Plot the range as shaded area
for i in range(len(side_chains)):
    plt.plot([x_pos[i], x_pos[i]], [tps_min[i], tps_max[i]], 
             'k-', alpha=0.3, linewidth=2)

plt.plot(x_pos, tps_avg, 'go-', linewidth=2, markersize=10, label='Average TPS')
plt.plot(x_pos, tps_min, 'b^--', linewidth=1, markersize=6, label='Minimum TPS')
plt.plot(x_pos, tps_max, 'rv--', linewidth=1, markersize=6, label='Maximum TPS')

plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
plt.ylabel('Transactions Per Second (TPS)', fontsize=12, fontweight='bold')
plt.title('TPS Performance Range (Real Measurements)', fontsize=14, fontweight='bold')
plt.xticks(x_pos, side_chains)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(img_dir / 'real_tps_range.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'real_tps_range.png'}")
plt.close()

# Plot 4: Throughput vs Total Transactions
plt.figure(figsize=(10, 6))
plt.scatter(transactions, tps_avg, s=200, c=side_chains, cmap='viridis', 
           alpha=0.6, edgecolors='black', linewidth=2)
plt.colorbar(label='Number of Side Chains')

# Add labels for each point
for i, (tx, tps, sc) in enumerate(zip(transactions, tps_avg, side_chains)):
    plt.annotate(f'{sc} chains', (tx, tps), 
                xytext=(5, 5), textcoords='offset points',
                fontsize=9, fontweight='bold')

plt.xlabel('Total Transactions', fontsize=12, fontweight='bold')
plt.ylabel('Average TPS', fontsize=12, fontweight='bold')
plt.title('Throughput vs Transaction Count', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(img_dir / 'real_throughput_vs_transactions.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'real_throughput_vs_transactions.png'}")
plt.close()

# Plot 5: Comparative bar chart (Bitcoin vs Chain at different scales)
plt.figure(figsize=(12, 6))
x = np.arange(len(side_chains))
width = 0.35

bitcoin_values = [BITCOIN_TPS] * len(side_chains)
chain_values = tps_avg

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left plot: Absolute values
ax1.bar(x - width/2, bitcoin_values, width, label='Bitcoin', color='orange', alpha=0.7)
ax1.bar(x + width/2, chain_values, width, label='Chain (Real)', color='green', alpha=0.7)
ax1.set_xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
ax1.set_ylabel('TPS (Log Scale)', fontsize=12, fontweight='bold')
ax1.set_title('Absolute TPS Comparison', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(side_chains)
ax1.set_yscale('log')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Right plot: Improvement factors
colors = ['#27ae60' if v > 1000 else '#3498db' for v in vs_bitcoin]
bars = ax2.bar(x, vs_bitcoin, color=colors, alpha=0.7)
ax2.axhline(y=100, color='orange', linestyle='--', linewidth=2, label='100x improvement')
ax2.set_xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
ax2.set_ylabel('Improvement Factor', fontsize=12, fontweight='bold')
ax2.set_title('Performance Gain vs Bitcoin', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(side_chains)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, val in zip(bars, vs_bitcoin):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
             f'{val:.0f}x', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(img_dir / 'real_comparison_bitcoin_vs_chain.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'real_comparison_bitcoin_vs_chain.png'}")
plt.close()

# Plot 6: Scalability trend line
plt.figure(figsize=(10, 6))
plt.plot(side_chains, tps_avg, 'bo-', linewidth=2, markersize=10, label='Real Measured TPS')

# Add polynomial trend line
z = np.polyfit(side_chains, tps_avg, 2)
p = np.poly1d(z)
x_trend = np.linspace(min(side_chains), max(side_chains), 100)
plt.plot(x_trend, p(x_trend), 'r--', linewidth=2, alpha=0.7, label='Trend (polynomial fit)')

plt.fill_between(side_chains, tps_min, tps_max, alpha=0.2, color='blue', label='Performance range')

plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
plt.ylabel('TPS', fontsize=12, fontweight='bold')
plt.title('Scalability Trend Analysis', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(img_dir / 'real_scalability_trend.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'real_scalability_trend.png'}")
plt.close()

# Summary statistics plot
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: TPS by configuration
ax1.barh(range(len(side_chains)), tps_avg, color='steelblue', alpha=0.7)
ax1.set_yticks(range(len(side_chains)))
ax1.set_yticklabels([f'{sc} chains' for sc in side_chains])
ax1.set_xlabel('Average TPS', fontweight='bold')
ax1.set_title('TPS by Configuration', fontweight='bold')
ax1.grid(True, alpha=0.3, axis='x')

# Plot 2: Improvement factors
ax2.barh(range(len(side_chains)), vs_bitcoin, color='forestgreen', alpha=0.7)
ax2.set_yticks(range(len(side_chains)))
ax2.set_yticklabels([f'{sc} chains' for sc in side_chains])
ax2.set_xlabel('Improvement Factor vs Bitcoin', fontweight='bold')
ax2.set_title('Speedup over Bitcoin', fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

# Plot 3: Performance variance
variance = [(r['tps_max'] - r['tps_min']) / r['tps_avg'] * 100 for r in results]
ax3.bar(range(len(side_chains)), variance, color='coral', alpha=0.7)
ax3.set_xticks(range(len(side_chains)))
ax3.set_xticklabels([f'{sc}' for sc in side_chains])
ax3.set_xlabel('Number of Side Chains', fontweight='bold')
ax3.set_ylabel('Variance (%)', fontweight='bold')
ax3.set_title('Performance Stability', fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: Efficiency (TPS per side chain)
efficiency = [tps / sc for tps, sc in zip(tps_avg, side_chains)]
ax4.plot(side_chains, efficiency, 'ro-', linewidth=2, markersize=8)
ax4.set_xlabel('Number of Side Chains', fontweight='bold')
ax4.set_ylabel('TPS per Side Chain', fontweight='bold')
ax4.set_title('Efficiency Analysis', fontweight='bold')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(img_dir / 'real_comprehensive_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'real_comprehensive_analysis.png'}")
plt.close()

print("\n✅ All visualization plots generated successfully!")
print(f"\n📁 Plots saved to: {img_dir}/")
print("\n📋 Generated plots:")
print("  1. real_tps_vs_sidechains.png           - TPS performance with error bars")
print("  2. real_improvement_vs_bitcoin.png       - Improvement factors")
print("  3. real_tps_range.png                    - Performance ranges")
print("  4. real_throughput_vs_transactions.png   - Throughput analysis")
print("  5. real_comparison_bitcoin_vs_chain.png  - Side-by-side comparison")
print("  6. real_scalability_trend.png            - Scalability trend analysis")
print("  7. real_comprehensive_analysis.png       - Multi-panel comprehensive view")

