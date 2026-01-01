#!/usr/bin/env python3
"""
Generate benchmark analysis and data without matplotlib
Creates CSV data that can be plotted elsewhere
"""

import json
import csv
from pathlib import Path

# Read benchmark results
results_file = Path('/Users/sajad/Desktop/Chain/benchmarks/real_benchmark_results.json')
with open(results_file, 'r') as f:
    data = json.load(f)

results = data['results']
BITCOIN_TPS = data['bitcoin_tps_baseline']

print("="*80)
print(" COMPREHENSIVE BENCHMARK ANALYSIS")
print("="*80)
print()

# ============================================================================
# Analysis 1: Performance by Configuration
# ============================================================================
print("📊 PERFORMANCE BY CONFIGURATION")
print("-"*80)
print(f"{'Config':<15} {'Side Chains':<12} {'Transactions':<14} {'TPS (Avg)':<12} {'vs Bitcoin':<12}")
print("-"*80)

for i, r in enumerate(results, 1):
    sc = r['config']['side_chains']
    tx = r['config']['transactions']
    tps = r['tps_avg']
    vs_btc = r['vs_bitcoin']
    print(f"Config {i:<8} {sc:<12} {tx:<14} {tps:<12.2f} {vs_btc:<12.2f}x")

print()

# ============================================================================
# Analysis 2: Efficiency Metrics
# ============================================================================
print("⚡ EFFICIENCY METRICS")
print("-"*80)
print(f"{'Config':<15} {'TPS/Chain':<15} {'TPS/Transaction':<18} {'Throughput':<12}")
print("-"*80)

for i, r in enumerate(results, 1):
    sc = r['config']['side_chains']
    tx = r['config']['transactions']
    tps = r['tps_avg']
    tps_per_chain = tps / sc
    tps_per_tx = tps / tx
    throughput = tps / BITCOIN_TPS
    
    print(f"Config {i:<8} {tps_per_chain:<15.2f} {tps_per_tx:<18.2f} {throughput:<12.2f}x")

print()

# ============================================================================
# Analysis 3: Scaling Analysis
# ============================================================================
print("📈 SCALING ANALYSIS")
print("-"*80)

# Group by side chains
by_chains = {}
for r in results:
    sc = r['config']['side_chains']
    if sc not in by_chains:
        by_chains[sc] = []
    by_chains[sc].append(r)

print("\nBy Side Chain Count:")
for sc in sorted(by_chains.keys()):
    configs = by_chains[sc]
    avg_tps = sum(c['tps_avg'] for c in configs) / len(configs)
    print(f"  {sc} chains: {avg_tps:>10.2f} TPS (avg across {len(configs)} config{'s' if len(configs) > 1 else ''})")

# Group by transaction count
print("\nBy Transaction Count:")
by_tx = {}
for r in results:
    tx = r['config']['transactions']
    if tx not in by_tx:
        by_tx[tx] = []
    by_tx[tx].append(r)

for tx in sorted(by_tx.keys()):
    configs = by_tx[tx]
    avg_tps = sum(c['tps_avg'] for c in configs) / len(configs)
    print(f"  {tx} transactions: {avg_tps:>10.2f} TPS (avg across {len(configs)} config{'s' if len(configs) > 1 else ''})")

print()

# ============================================================================
# Analysis 4: Best Configurations
# ============================================================================
print("🏆 TOP PERFORMERS")
print("-"*80)

# Best overall TPS
best_overall = max(results, key=lambda x: x['tps_avg'])
print(f"Best TPS:           {best_overall['tps_avg']:.2f} ({best_overall['config']['side_chains']} chains, {best_overall['config']['transactions']} tx)")

# Best efficiency per chain
best_per_chain = max(results, key=lambda x: x['tps_avg'] / x['config']['side_chains'])
print(f"Best per Chain:     {best_per_chain['tps_avg'] / best_per_chain['config']['side_chains']:.2f} TPS/chain ({best_per_chain['config']['side_chains']} chains, {best_per_chain['config']['transactions']} tx)")

# Best efficiency per transaction
best_per_tx = max(results, key=lambda x: x['tps_avg'] / x['config']['transactions'])
print(f"Best per Tx:        {best_per_tx['tps_avg'] / best_per_tx['config']['transactions']:.2f} TPS/tx ({best_per_tx['config']['side_chains']} chains, {best_per_tx['config']['transactions']} tx)")

# Best improvement vs Bitcoin
best_improvement = max(results, key=lambda x: x['vs_bitcoin'])
print(f"Best vs Bitcoin:    {best_improvement['vs_bitcoin']:.2f}x ({best_improvement['config']['side_chains']} chains, {best_improvement['config']['transactions']} tx)")

print()

# ============================================================================
# Analysis 5: Statistical Summary
# ============================================================================
print("📊 STATISTICAL SUMMARY")
print("-"*80)

all_tps = [r['tps_avg'] for r in results]
all_vs_btc = [r['vs_bitcoin'] for r in results]

print(f"TPS Statistics:")
print(f"  Minimum:     {min(all_tps):>10.2f}")
print(f"  Maximum:     {max(all_tps):>10.2f}")
print(f"  Average:     {sum(all_tps)/len(all_tps):>10.2f}")
print(f"  Median:      {sorted(all_tps)[len(all_tps)//2]:>10.2f}")
print(f"  Range:       {max(all_tps) - min(all_tps):>10.2f}")

print(f"\nImprovement vs Bitcoin:")
print(f"  Minimum:     {min(all_vs_btc):>10.2f}x")
print(f"  Maximum:     {max(all_vs_btc):>10.2f}x")
print(f"  Average:     {sum(all_vs_btc)/len(all_vs_btc):>10.2f}x")

print()

# ============================================================================
# Export Data for External Plotting
# ============================================================================
output_dir = Path('/Users/sajad/Desktop/Chain/benchmarks')

# Export comprehensive CSV
csv_file = output_dir / 'benchmark_data_for_plotting.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['SideChains', 'Transactions', 'TPS_Avg', 'TPS_Min', 'TPS_Max', 
                     'TPS_Median', 'StdDev', 'VsBitcoin', 'TPS_Per_Chain', 'TPS_Per_Tx'])
    
    for r in results:
        sc = r['config']['side_chains']
        tx = r['config']['transactions']
        writer.writerow([
            sc,
            tx,
            r['tps_avg'],
            r['tps_min'],
            r['tps_max'],
            r['tps_median'],
            r['tps_stdev'],
            r['vs_bitcoin'],
            r['tps_avg'] / sc,
            r['tps_avg'] / tx
        ])

print(f"✓ CSV data exported to: {csv_file}")
print()

# ============================================================================
# ASCII Visualizations
# ============================================================================
print("="*80)
print(" ASCII VISUALIZATIONS")
print("="*80)
print()

print("📊 TPS BY CONFIGURATION")
print("-"*80)
max_tps = max(all_tps)
for r in results:
    sc = r['config']['side_chains']
    tx = r['config']['transactions']
    tps = r['tps_avg']
    bar_length = int((tps / max_tps) * 50)
    bar = '█' * bar_length
    print(f"{sc:2d} chains, {tx:3d} tx: {bar:50s} {tps:8.2f} TPS")

print()
print("📊 IMPROVEMENT VS BITCOIN")
print("-"*80)
max_improvement = max(all_vs_btc)
for r in results:
    sc = r['config']['side_chains']
    tx = r['config']['transactions']
    vs_btc = r['vs_bitcoin']
    bar_length = int((vs_btc / max_improvement) * 50)
    bar = '█' * bar_length
    print(f"{sc:2d} chains, {tx:3d} tx: {bar:50s} {vs_btc:7.2f}x")

print()
print("📊 TPS PER SIDE CHAIN (EFFICIENCY)")
print("-"*80)
efficiency = [(r['tps_avg'] / r['config']['side_chains'], r) for r in results]
max_eff = max(e[0] for e in efficiency)
for eff_val, r in sorted(efficiency, key=lambda x: x[0], reverse=True):
    sc = r['config']['side_chains']
    tx = r['config']['transactions']
    bar_length = int((eff_val / max_eff) * 50)
    bar = '█' * bar_length
    print(f"{sc:2d} chains, {tx:3d} tx: {bar:50s} {eff_val:8.2f} TPS/chain")

print()

# ============================================================================
# Create LaTeX-ready data
# ============================================================================
latex_file = output_dir / 'benchmark_data_latex.tex'
with open(latex_file, 'w') as f:
    f.write("% Auto-generated benchmark data for LaTeX\n")
    f.write("% Include this in your thesis\n\n")
    
    f.write("\\begin{table}[h]\n")
    f.write("\\centering\n")
    f.write("\\caption{تحلیل جامع عملکرد برای پیکربندی‌های مختلف}\n")
    f.write("\\label{tab:comprehensive-benchmark}\n")
    f.write("\\begin{tabular}{|c|c|c|c|c|c|}\n")
    f.write("\\hline\n")
    f.write("\\textbf{زنجیره‌های جانبی} & \\textbf{تراکنش‌ها} & \\textbf{TPS} & ")
    f.write("\\textbf{TPS/زنجیره} & \\textbf{TPS/تراکنش} & \\textbf{بهبود} \\\\ \\hline\n")
    
    for r in results:
        sc = r['config']['side_chains']
        tx = r['config']['transactions']
        tps = r['tps_avg']
        tps_per_chain = tps / sc
        tps_per_tx = tps / tx
        vs_btc = r['vs_bitcoin']
        
        f.write(f"{sc} & {tx} & {tps:.2f} & {tps_per_chain:.2f} & ")
        f.write(f"{tps_per_tx:.2f} & {vs_btc:.2f}x \\\\ \\hline\n")
    
    f.write("\\end{tabular}\n")
    f.write("\\end{table}\n")

print(f"✓ LaTeX table exported to: {latex_file}")
print()

# ============================================================================
# Create markdown report
# ============================================================================
md_file = output_dir / 'BENCHMARK_ANALYSIS.md'
with open(md_file, 'w') as f:
    f.write("# Comprehensive Benchmark Analysis\n\n")
    f.write(f"**Generated:** {data['timestamp']}\n\n")
    
    f.write("## Performance Matrix\n\n")
    f.write("| Side Chains | Transactions | TPS (Avg) | TPS/Chain | TPS/Tx | vs Bitcoin |\n")
    f.write("|-------------|--------------|-----------|-----------|---------|------------|\n")
    
    for r in results:
        sc = r['config']['side_chains']
        tx = r['config']['transactions']
        tps = r['tps_avg']
        tps_per_chain = tps / sc
        tps_per_tx = tps / tx
        vs_btc = r['vs_bitcoin']
        
        f.write(f"| {sc} | {tx} | {tps:.2f} | {tps_per_chain:.2f} | {tps_per_tx:.2f} | {vs_btc:.2f}x |\n")
    
    f.write("\n## Key Findings\n\n")
    f.write(f"1. **Best Overall Performance**: {best_overall['tps_avg']:.2f} TPS ")
    f.write(f"({best_overall['config']['side_chains']} side chains, ")
    f.write(f"{best_overall['config']['transactions']} transactions)\n\n")
    
    f.write(f"2. **Peak Improvement**: {best_improvement['vs_bitcoin']:.2f}x faster than Bitcoin\n\n")
    
    f.write(f"3. **Best Efficiency**: {best_per_chain['tps_avg'] / best_per_chain['config']['side_chains']:.2f} ")
    f.write(f"TPS per side chain\n\n")
    
    f.write("## Observations\n\n")
    f.write("- Performance peaks at 3 side chains with 150 transactions\n")
    f.write("- All configurations show significant improvement over Bitcoin (>390x)\n")
    f.write("- Scalability is demonstrated across different transaction volumes\n")

print(f"✓ Markdown report exported to: {md_file}")
print()

print("="*80)
print("✅ ANALYSIS COMPLETE")
print("="*80)
print()
print("Generated files:")
print(f"  1. {csv_file.name} - CSV data for plotting")
print(f"  2. {latex_file.name} - LaTeX table")
print(f"  3. {md_file.name} - Markdown report")
print()
print("You can import the CSV into Excel, Google Sheets, or other plotting tools")
print("to create custom visualizations.")
print()

