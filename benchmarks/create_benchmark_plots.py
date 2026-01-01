#!/usr/bin/env python3
"""
Comprehensive benchmark visualization showing relationship between
transaction count, side chain count, and performance
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# Read benchmark results
results_file = Path('/Users/sajad/Desktop/Chain/benchmarks/real_benchmark_results.json')
with open(results_file, 'r') as f:
    data = json.load(f)

results = data['results']
BITCOIN_TPS = data['bitcoin_tps_baseline']

# Extract data
side_chains = np.array([r['config']['side_chains'] for r in results])
transactions = np.array([r['config']['transactions'] for r in results])
tps_avg = np.array([r['tps_avg'] for r in results])
tps_min = np.array([r['tps_min'] for r in results])
tps_max = np.array([r['tps_max'] for r in results])
vs_bitcoin = np.array([r['vs_bitcoin'] for r in results])

# Output directory
img_dir = Path('/Users/sajad/Desktop/Chain/thesis_latex_sample/img')
img_dir.mkdir(exist_ok=True)

print("📊 Creating comprehensive benchmark visualizations...")
print(f"Data points: {len(results)}")
print()

# ============================================================================
# Plot 1: 3D Surface Plot - TPS vs Side Chains vs Transactions
# ============================================================================
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Create scatter plot
scatter = ax.scatter(side_chains, transactions, tps_avg, 
                    c=tps_avg, cmap='viridis', s=200, alpha=0.8,
                    edgecolors='black', linewidth=2)

# Add labels for each point
for i, (sc, tx, tps) in enumerate(zip(side_chains, transactions, tps_avg)):
    ax.text(sc, tx, tps, f'{tps:.0f}', fontsize=8, fontweight='bold')

ax.set_xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
ax.set_ylabel('Transaction Count', fontsize=12, fontweight='bold')
ax.set_zlabel('TPS (Avg)', fontsize=12, fontweight='bold')
ax.set_title('3D Performance: TPS vs Side Chains vs Transactions', 
             fontsize=14, fontweight='bold', pad=20)

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
cbar.set_label('TPS', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(img_dir / 'benchmark_3d_performance.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'benchmark_3d_performance.png'}")
plt.close()

# ============================================================================
# Plot 2: TPS vs Transaction Count (grouped by side chains)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

# Create scatter plot with different colors for each side chain count
unique_sc = sorted(set(side_chains))
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_sc)))

for i, sc in enumerate(unique_sc):
    mask = side_chains == sc
    ax.scatter(transactions[mask], tps_avg[mask], 
              s=300, alpha=0.7, c=[colors[i]], 
              label=f'{sc} chain{"s" if sc > 1 else ""}',
              edgecolors='black', linewidth=2)
    
    # Add connecting lines
    if sum(mask) > 1:
        sorted_indices = np.argsort(transactions[mask])
        sorted_tx = transactions[mask][sorted_indices]
        sorted_tps = tps_avg[mask][sorted_indices]
        ax.plot(sorted_tx, sorted_tps, '--', alpha=0.5, c=colors[i], linewidth=2)
    
    # Add value labels
    for tx, tps in zip(transactions[mask], tps_avg[mask]):
        ax.annotate(f'{tps:.0f}', (tx, tps), 
                   textcoords="offset points", xytext=(0, 10),
                   ha='center', fontsize=9, fontweight='bold')

ax.set_xlabel('Transaction Count', fontsize=13, fontweight='bold')
ax.set_ylabel('TPS (Avg)', fontsize=13, fontweight='bold')
ax.set_title('TPS vs Transaction Count (by Side Chain Count)', 
            fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='best', framealpha=0.9)
ax.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(img_dir / 'benchmark_tps_vs_transactions.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'benchmark_tps_vs_transactions.png'}")
plt.close()

# ============================================================================
# Plot 3: Efficiency Metrics - TPS per Side Chain
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# TPS per side chain
tps_per_chain = tps_avg / side_chains
colors_efficiency = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(results)))

bars1 = ax1.bar(range(len(results)), tps_per_chain, color=colors_efficiency, 
               alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_xlabel('Configuration', fontsize=12, fontweight='bold')
ax1.set_ylabel('TPS per Side Chain', fontsize=12, fontweight='bold')
ax1.set_title('Efficiency: TPS per Side Chain', fontsize=13, fontweight='bold')
ax1.set_xticks(range(len(results)))
ax1.set_xticklabels([f'{sc}ch\n{tx}tx' for sc, tx in zip(side_chains, transactions)], 
                    fontsize=9)
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars1, tps_per_chain)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
            f'{val:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# TPS per transaction
tps_per_tx = tps_avg / transactions

bars2 = ax2.bar(range(len(results)), tps_per_tx, color=colors_efficiency, 
               alpha=0.7, edgecolor='black', linewidth=2)
ax2.set_xlabel('Configuration', fontsize=12, fontweight='bold')
ax2.set_ylabel('TPS per Transaction', fontsize=12, fontweight='bold')
ax2.set_title('Efficiency: TPS per Transaction', fontsize=13, fontweight='bold')
ax2.set_xticks(range(len(results)))
ax2.set_xticklabels([f'{sc}ch\n{tx}tx' for sc, tx in zip(side_chains, transactions)], 
                    fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars2, tps_per_tx)):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(img_dir / 'benchmark_efficiency_metrics.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'benchmark_efficiency_metrics.png'}")
plt.close()

# ============================================================================
# Plot 4: Heatmap - Performance Matrix
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 8))

# Create a matrix for heatmap
unique_sc = sorted(set(side_chains))
unique_tx = sorted(set(transactions))

# Create matrix with NaN for missing combinations
matrix = np.full((len(unique_sc), len(unique_tx)), np.nan)

for r in results:
    sc_idx = unique_sc.index(r['config']['side_chains'])
    tx_idx = unique_tx.index(r['config']['transactions'])
    matrix[sc_idx, tx_idx] = r['tps_avg']

im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto', interpolation='nearest')

# Set ticks and labels
ax.set_xticks(range(len(unique_tx)))
ax.set_yticks(range(len(unique_sc)))
ax.set_xticklabels(unique_tx, fontsize=10)
ax.set_yticklabels(unique_sc, fontsize=10)

ax.set_xlabel('Transaction Count', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Side Chains', fontsize=12, fontweight='bold')
ax.set_title('Performance Heatmap: TPS across Configurations', 
            fontsize=14, fontweight='bold')

# Add text annotations
for i in range(len(unique_sc)):
    for j in range(len(unique_tx)):
        if not np.isnan(matrix[i, j]):
            text = ax.text(j, i, f'{matrix[i, j]:.0f}',
                         ha="center", va="center", color="black", 
                         fontsize=11, fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('TPS', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(img_dir / 'benchmark_heatmap.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'benchmark_heatmap.png'}")
plt.close()

# ============================================================================
# Plot 5: Scaling Analysis - Side Chains vs TPS (normalized by transactions)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

# Normalize TPS by transaction count to see true scaling
normalized_tps = tps_avg / (transactions / transactions[0])

ax.plot(side_chains, tps_avg, 'bo-', linewidth=2.5, markersize=12, 
       label='Actual TPS', alpha=0.7)
ax.plot(side_chains, normalized_tps, 'rs--', linewidth=2.5, markersize=10, 
       label='Normalized TPS (by tx count)', alpha=0.7)

# Add value labels
for sc, tps, norm_tps in zip(side_chains, tps_avg, normalized_tps):
    ax.annotate(f'{tps:.0f}', (sc, tps), 
               textcoords="offset points", xytext=(0, 10),
               ha='center', fontsize=9, fontweight='bold', color='blue')
    ax.annotate(f'{norm_tps:.0f}', (sc, norm_tps), 
               textcoords="offset points", xytext=(0, -15),
               ha='center', fontsize=9, fontweight='bold', color='red')

ax.set_xlabel('Number of Side Chains', fontsize=13, fontweight='bold')
ax.set_ylabel('TPS', fontsize=13, fontweight='bold')
ax.set_title('Scaling Analysis: Impact of Side Chain Count', 
            fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(img_dir / 'benchmark_scaling_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'benchmark_scaling_analysis.png'}")
plt.close()

# ============================================================================
# Plot 6: Comprehensive Multi-Panel Dashboard
# ============================================================================
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Panel 1: TPS by configuration
ax1 = fig.add_subplot(gs[0, 0])
bars = ax1.bar(range(len(results)), tps_avg, 
              color=plt.cm.viridis(np.linspace(0, 1, len(results))),
              alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_xlabel('Configuration', fontweight='bold')
ax1.set_ylabel('TPS', fontweight='bold')
ax1.set_title('TPS by Configuration', fontweight='bold', fontsize=12)
ax1.set_xticks(range(len(results)))
ax1.set_xticklabels([f'{sc}ch\n{tx}tx' for sc, tx in zip(side_chains, transactions)], 
                    fontsize=8)
ax1.grid(True, alpha=0.3, axis='y')

# Panel 2: Improvement vs Bitcoin
ax2 = fig.add_subplot(gs[0, 1])
colors_btc = ['green' if v > 1000 else 'orange' if v > 500 else 'blue' for v in vs_bitcoin]
bars = ax2.bar(range(len(results)), vs_bitcoin, color=colors_btc, 
              alpha=0.7, edgecolor='black', linewidth=2)
ax2.axhline(y=100, color='red', linestyle='--', linewidth=2, alpha=0.5, label='100x')
ax2.set_xlabel('Configuration', fontweight='bold')
ax2.set_ylabel('Improvement Factor', fontweight='bold')
ax2.set_title('Speedup vs Bitcoin', fontweight='bold', fontsize=12)
ax2.set_xticks(range(len(results)))
ax2.set_xticklabels([f'{sc}ch\n{tx}tx' for sc, tx in zip(side_chains, transactions)], 
                    fontsize=8)
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# Panel 3: Transaction count impact
ax3 = fig.add_subplot(gs[1, 0])
ax3.scatter(transactions, tps_avg, s=side_chains*50, alpha=0.6, 
           c=side_chains, cmap='plasma', edgecolors='black', linewidth=2)
for tx, tps, sc in zip(transactions, tps_avg, side_chains):
    ax3.annotate(f'{sc}ch', (tx, tps), fontsize=8, ha='center')
ax3.set_xlabel('Transaction Count', fontweight='bold')
ax3.set_ylabel('TPS', fontweight='bold')
ax3.set_title('TPS vs Transaction Count\n(bubble size = side chains)', 
             fontweight='bold', fontsize=12)
ax3.grid(True, alpha=0.3)

# Panel 4: Side chain impact
ax4 = fig.add_subplot(gs[1, 1])
ax4.scatter(side_chains, tps_avg, s=transactions*2, alpha=0.6, 
           c=transactions, cmap='coolwarm', edgecolors='black', linewidth=2)
for sc, tps, tx in zip(side_chains, tps_avg, transactions):
    ax4.annotate(f'{tx}tx', (sc, tps), fontsize=8, ha='center')
ax4.set_xlabel('Side Chain Count', fontweight='bold')
ax4.set_ylabel('TPS', fontweight='bold')
ax4.set_title('TPS vs Side Chain Count\n(bubble size = transactions)', 
             fontweight='bold', fontsize=12)
ax4.grid(True, alpha=0.3)

# Panel 5: Performance variance
ax5 = fig.add_subplot(gs[2, 0])
variance = [(r['tps_max'] - r['tps_min']) for r in results]
bars = ax5.bar(range(len(results)), variance, 
              color='coral', alpha=0.7, edgecolor='black', linewidth=2)
ax5.set_xlabel('Configuration', fontweight='bold')
ax5.set_ylabel('TPS Range (Max - Min)', fontweight='bold')
ax5.set_title('Performance Variance', fontweight='bold', fontsize=12)
ax5.set_xticks(range(len(results)))
ax5.set_xticklabels([f'{sc}ch\n{tx}tx' for sc, tx in zip(side_chains, transactions)], 
                    fontsize=8)
ax5.grid(True, alpha=0.3, axis='y')

# Panel 6: Summary statistics
ax6 = fig.add_subplot(gs[2, 1])
ax6.axis('off')

summary_text = f"""
BENCHMARK SUMMARY

Total Configurations: {len(results)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PERFORMANCE:
• Best TPS: {max(tps_avg):.2f}
  ({side_chains[np.argmax(tps_avg)]} chains, {transactions[np.argmax(tps_avg)]} tx)

• Average TPS: {np.mean(tps_avg):.2f}
• Median TPS: {np.median(tps_avg):.2f}

IMPROVEMENT vs BITCOIN:
• Maximum: {max(vs_bitcoin):.2f}x
• Minimum: {min(vs_bitcoin):.2f}x
• Average: {np.mean(vs_bitcoin):.2f}x

CONFIGURATIONS:
• Side Chains: {min(side_chains)} - {max(side_chains)}
• Transactions: {min(transactions)} - {max(transactions)}

BEST EFFICIENCY:
• Per Chain: {max(tps_avg/side_chains):.2f} TPS/chain
• Per Transaction: {max(tps_avg/transactions):.2f} TPS/tx
"""

ax6.text(0.1, 0.5, summary_text, transform=ax6.transAxes,
        fontsize=10, verticalalignment='center', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Chain Blockchain - Comprehensive Benchmark Dashboard', 
            fontsize=16, fontweight='bold', y=0.995)

plt.savefig(img_dir / 'benchmark_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'benchmark_comprehensive_dashboard.png'}")
plt.close()

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("📊 VISUALIZATION COMPLETE")
print("="*70)
print(f"\nGenerated {6} comprehensive plots:")
print("  1. benchmark_3d_performance.png         - 3D visualization")
print("  2. benchmark_tps_vs_transactions.png    - TPS vs transaction count")
print("  3. benchmark_efficiency_metrics.png     - Efficiency analysis")
print("  4. benchmark_heatmap.png                - Performance heatmap")
print("  5. benchmark_scaling_analysis.png       - Scaling analysis")
print("  6. benchmark_comprehensive_dashboard.png - Complete dashboard")
print(f"\nAll plots saved to: {img_dir}/")
print("\n✅ Ready to include in your thesis!")

