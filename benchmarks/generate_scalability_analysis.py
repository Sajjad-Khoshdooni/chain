#!/usr/bin/env python3
"""
Generate comprehensive scalability analysis for thesis
Shows TPS scaling from 1 to 1000 side chains
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

# Configuration - Realistic Network Constraints
MAX_BLOCK_SIZE_MB = 1  # 1 MB blocks like Bitcoin
AVG_TX_SIZE_BYTES = 250  # Average transaction size
MASTER_BLOCK_TIME = 600  # 10 minutes in seconds
SIDE_BLOCK_TIME = 60  # 1 minute in seconds
BITCOIN_TPS = 7  # Bitcoin baseline

# Calculate maximum transactions per block based on block size
MAX_TX_PER_BLOCK = (MAX_BLOCK_SIZE_MB * 1024 * 1024) // AVG_TX_SIZE_BYTES
print(f"Max transactions per block (1MB / 250 bytes): {MAX_TX_PER_BLOCK}")

def calculate_theoretical_tps(num_side_chains):
    """
    Calculate realistic network TPS with block size constraints
    
    Formula: TPS = M/T_m + (N × S)/T_s
    
    Where:
        M = master chain tx/block (limited by block size)
        T_m = master block time (600s)
        N = number of side chains
        S = side chain tx/block (limited by block size)
        T_s = side chain block time (60s)
    """
    master_tps = MAX_TX_PER_BLOCK / MASTER_BLOCK_TIME
    side_tps = (num_side_chains * MAX_TX_PER_BLOCK) / SIDE_BLOCK_TIME
    total_tps = master_tps + side_tps
    
    return {
        'side_chains': num_side_chains,
        'master_tps': master_tps,
        'side_tps': side_tps,
        'total_tps': total_tps,
        'vs_bitcoin': total_tps / BITCOIN_TPS,
        'improvement_percent': (total_tps / BITCOIN_TPS - 1) * 100
    }

# Calculate for key configurations
configs = [1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000]
results = [calculate_theoretical_tps(n) for n in configs]

# Print results
print("\n" + "="*80)
print("REALISTIC NETWORK TPS SCALING (1MB blocks, 250 byte tx)")
print("="*80)
print(f"{'Chains':>8} | {'Master TPS':>12} | {'Side TPS':>12} | {'Total TPS':>12} | {'vs Bitcoin':>12}")
print("-"*80)

for r in results:
    print(f"{r['side_chains']:>8} | {r['master_tps']:>12.2f} | {r['side_tps']:>12.2f} | "
          f"{r['total_tps']:>12.2f} | {r['vs_bitcoin']:>12.2f}x")

print("="*80)

# Highlight key configurations
print("\n" + "="*80)
print("KEY FINDINGS:")
print("="*80)
print(f"1 chain:    {results[0]['total_tps']:>8.2f} TPS ({results[0]['vs_bitcoin']:>6.2f}x Bitcoin)")
print(f"           → Similar to Bitcoin with faster blocks")
print(f"10 chains:  {results[4]['total_tps']:>8.2f} TPS ({results[4]['vs_bitcoin']:>6.2f}x Bitcoin)")
print(f"           → Small scale deployment")
print(f"100 chains: {results[7]['total_tps']:>8.2f} TPS ({results[7]['vs_bitcoin']:>6.2f}x Bitcoin)")
print(f"           → Medium scale deployment")
print(f"1000 chains: {results[10]['total_tps']:>7.2f} TPS ({results[10]['vs_bitcoin']:>5.2f}x Bitcoin)")
print(f"           → Large scale deployment")
print("="*80)

# Create visualization
img_dir = Path('/Users/sajad/Desktop/Chain/thesis_latex_sample/img')
img_dir.mkdir(exist_ok=True)

# Plot 1: TPS vs Side Chains (Log scale for better visualization)
plt.figure(figsize=(12, 7))
side_chains = [r['side_chains'] for r in results]
total_tps = [r['total_tps'] for r in results]

plt.plot(side_chains, total_tps, 'b-o', linewidth=2.5, markersize=8, label='Chain Architecture')
plt.axhline(y=BITCOIN_TPS, color='r', linestyle='--', linewidth=2, label='Bitcoin (7 TPS)')

# Add annotations for key points
for i, r in enumerate([results[0], results[4], results[7], results[10]]):
    plt.annotate(f"{r['total_tps']:.0f} TPS\n({r['vs_bitcoin']:.0f}x)",
                xy=(r['side_chains'], r['total_tps']),
                xytext=(10, -15), textcoords='offset points',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

plt.xlabel('Number of Side Chains', fontsize=13, fontweight='bold')
plt.ylabel('Transactions Per Second (TPS)', fontsize=13, fontweight='bold')
plt.title('Blockchain Scalability: Parallel Side Chains Enable Linear TPS Growth', 
         fontsize=14, fontweight='bold')
plt.xscale('log')
plt.yscale('log')
plt.grid(True, alpha=0.3, which='both')
plt.legend(fontsize=12, loc='lower right')
plt.tight_layout()
plt.savefig(img_dir / 'scalability_1_to_1000_chains.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Saved: {img_dir / 'scalability_1_to_1000_chains.png'}")
plt.close()

# Plot 2: Linear Scale for smaller range (1-100 chains)
plt.figure(figsize=(12, 7))
small_range = results[:8]  # 1-100 chains
sc_small = [r['side_chains'] for r in small_range]
tps_small = [r['total_tps'] for r in small_range]

plt.plot(sc_small, tps_small, 'g-o', linewidth=3, markersize=10, label='Theoretical TPS')
plt.fill_between(sc_small, tps_small, alpha=0.3, color='green')
plt.axhline(y=BITCOIN_TPS, color='r', linestyle='--', linewidth=2, label='Bitcoin')

# Show linear scaling
z = np.polyfit(sc_small, tps_small, 1)
p = np.poly1d(z)
plt.plot(sc_small, p(sc_small), "r--", alpha=0.5, linewidth=2, 
        label=f'Linear Fit: y = {z[0]:.1f}x + {z[1]:.1f}')

plt.xlabel('Number of Side Chains', fontsize=13, fontweight='bold')
plt.ylabel('Transactions Per Second (TPS)', fontsize=13, fontweight='bold')
plt.title('Linear Horizontal Scalability (1-100 Side Chains)', 
         fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig(img_dir / 'linear_scalability_1_to_100.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'linear_scalability_1_to_100.png'}")
plt.close()

# Plot 3: Improvement Factor vs Bitcoin
plt.figure(figsize=(12, 7))
improvement = [r['vs_bitcoin'] for r in results]

bars = plt.bar(range(len(configs)), improvement, color='orange', alpha=0.8, edgecolor='black', linewidth=1.5)
plt.axhline(y=1, color='r', linestyle='--', linewidth=2, label='Bitcoin Baseline (1x)')

# Color code the bars
colors = ['lightcoral' if x < 20 else 'lightgreen' if x < 100 else 'darkgreen' for x in improvement]
for bar, color in zip(bars, colors):
    bar.set_color(color)

# Add value labels on bars
for i, (r, bar) in enumerate(zip(results, bars)):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{r["vs_bitcoin"]:.0f}x',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.xlabel('Side Chain Configuration', fontsize=13, fontweight='bold')
plt.ylabel('Performance vs Bitcoin (x times)', fontsize=13, fontweight='bold')
plt.title('Performance Improvement Over Bitcoin', fontsize=14, fontweight='bold')
plt.xticks(range(len(configs)), [f'{c}' for c in configs], rotation=45)
plt.yscale('log')
plt.grid(True, alpha=0.3, axis='y', which='both')
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig(img_dir / 'improvement_vs_bitcoin_all_configs.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: {img_dir / 'improvement_vs_bitcoin_all_configs.png'}")
plt.close()

# Save data as JSON
output = {
    'parameters': {
        'max_block_size_mb': MAX_BLOCK_SIZE_MB,
        'avg_tx_size_bytes': AVG_TX_SIZE_BYTES,
        'max_tx_per_block': MAX_TX_PER_BLOCK,
        'master_block_time': MASTER_BLOCK_TIME,
        'side_block_time': SIDE_BLOCK_TIME,
        'bitcoin_baseline_tps': BITCOIN_TPS
    },
    'results': results,
    'key_findings': {
        '1_chain': results[0],
        '10_chains': results[4],
        '100_chains': results[7],
        '1000_chains': results[10]
    }
}

with open('/Users/sajad/Desktop/Chain/benchmarks/scalability_analysis.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f"✓ Saved: scalability_analysis.json")

# Generate LaTeX table
latex_table = """\\begin{table}[h]
\\centering
\\caption{مقیاس‌پذیری شبکه: TPS تئوری برای 1 تا 1000 زنجیره جانبی}
\\label{tab:scalability-1-to-1000}
\\begin{tabular}{|c|c|c|c|c|}
\\hline
\\textbf{زنجیره‌های جانبی} & \\textbf{TPS زنجیره اصلی} & \\textbf{TPS زنجیره‌های جانبی} & \\textbf{TPS کل} & \\textbf{بهبود vs بیتکوین} \\\\ \\hline
"""

for r in [results[0], results[2], results[4], results[5], results[7], results[10]]:  # 1, 3, 10, 20, 100, 1000
    latex_table += f"{r['side_chains']} & {r['master_tps']:.2f} & {r['side_tps']:.2f} & {r['total_tps']:.2f} & {r['vs_bitcoin']:.0f}x \\\\ \\hline\n"

latex_table += """\\end{tabular}
\\end{table}
"""

with open('/Users/sajad/Desktop/Chain/benchmarks/scalability_table.tex', 'w') as f:
    f.write(latex_table)
print(f"✓ Saved: scalability_table.tex")

print("\n✅ Scalability analysis complete!")
print("\nKey Insight:")
print("  → 1 chain ≈ Bitcoin performance (just faster blocks)")
print("  → SCALABILITY comes from PARALLEL processing with multiple chains!")
print("  → Linear growth: ~70 TPS per additional side chain")
print("  → 1000 chains = 69,907 TPS (nearly 10,000x Bitcoin!)")


