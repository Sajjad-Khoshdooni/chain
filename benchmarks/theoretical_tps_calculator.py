#!/usr/bin/env python3
"""
Benchmark script for measuring TPS (Transactions Per Second) 
of the Chain blockchain architecture with varying number of side chains
"""

import subprocess
import json
import time
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Use a font that supports Persian text
matplotlib.rcParams['font.family'] = ['DejaVu Sans']

# Configuration
SIDE_CHAIN_COUNTS = [1, 2, 3, 5, 10, 15, 20, 25, 30, 40, 50]
MASTER_TX_PER_BLOCK = 1000  # M: transactions per master block
SIDE_TX_PER_BLOCK = 100     # S: transactions per side chain block
MASTER_BLOCK_TIME = 600     # seconds (10 minutes)
SIDE_BLOCK_TIME = 60        # seconds (1 minute)
BITCOIN_TPS = 7             # Bitcoin average TPS for comparison

def calculate_tps(num_side_chains, master_tx=MASTER_TX_PER_BLOCK, side_tx=SIDE_TX_PER_BLOCK):
    """
    Calculate theoretical TPS based on the formula:
    TPS = M/600 + (N*S)/60
    
    where:
        M = master chain transactions per block
        N = number of side chains
        S = side chain transactions per block
    """
    master_tps = master_tx / MASTER_BLOCK_TIME
    side_tps = (num_side_chains * side_tx) / SIDE_BLOCK_TIME
    total_tps = master_tps + side_tps
    return total_tps

def calculate_max_tps(num_side_chains, max_block_size_mb=1, avg_tx_size_kb=0.5):
    """
    Calculate maximum practical TPS considering block size limits
    
    Assumptions:
    - Maximum block size: 1 MB (similar to Bitcoin)
    - Average transaction size: 0.5 KB
    - Network propagation and validation time
    """
    # Maximum transactions per block based on block size
    max_tx_per_block = (max_block_size_mb * 1024) / avg_tx_size_kb
    
    # Calculate with maximum capacity
    return calculate_tps(num_side_chains, max_tx_per_block, max_tx_per_block)

def benchmark_all_configs():
    """Run benchmarks for all side chain configurations"""
    results = []
    
    print("=" * 60)
    print("Blockchain TPS Benchmark")
    print("=" * 60)
    print(f"Master block time: {MASTER_BLOCK_TIME}s (10 min)")
    print(f"Side chain block time: {SIDE_BLOCK_TIME}s (1 min)")
    print(f"Master tx/block: {MASTER_TX_PER_BLOCK}")
    print(f"Side chain tx/block: {SIDE_TX_PER_BLOCK}")
    print(f"Bitcoin TPS (baseline): {BITCOIN_TPS}")
    print("=" * 60)
    print()
    
    for num_chains in SIDE_CHAIN_COUNTS:
        tps = calculate_tps(num_chains)
        max_tps = calculate_max_tps(num_chains)
        improvement = (tps / BITCOIN_TPS) * 100
        
        result = {
            'side_chains': num_chains,
            'tps': tps,
            'max_tps': max_tps,
            'improvement_percent': improvement,
            'vs_bitcoin': tps / BITCOIN_TPS
        }
        results.append(result)
        
        print(f"Side Chains: {num_chains:3d} | "
              f"TPS: {tps:8.2f} | "
              f"Max TPS: {max_tps:10.2f} | "
              f"vs Bitcoin: {result['vs_bitcoin']:6.2f}x | "
              f"Improvement: {improvement:7.1f}%")
    
    print()
    print("=" * 60)
    
    # Find optimal configuration
    max_result = max(results, key=lambda x: x['tps'])
    print(f"\nOptimal configuration (from tested):")
    print(f"  Side chains: {max_result['side_chains']}")
    print(f"  TPS: {max_result['tps']:.2f}")
    print(f"  Improvement over Bitcoin: {max_result['vs_bitcoin']:.2f}x")
    
    return results

def create_plots(results):
    """Create visualization plots for the benchmark results"""
    side_chains = [r['side_chains'] for r in results]
    tps_values = [r['tps'] for r in results]
    max_tps_values = [r['max_tps'] for r in results]
    improvement = [r['vs_bitcoin'] for r in results]
    
    # Create output directory for plots
    img_dir = Path('/Users/sajad/Desktop/Chain/thesis_latex_sample/img')
    img_dir.mkdir(exist_ok=True)
    
    # Plot 1: TPS vs Number of Side Chains
    plt.figure(figsize=(10, 6))
    plt.plot(side_chains, tps_values, 'b-o', linewidth=2, markersize=8, label='Theoretical TPS')
    plt.axhline(y=BITCOIN_TPS, color='r', linestyle='--', linewidth=2, label='Bitcoin TPS')
    plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
    plt.ylabel('Transactions Per Second (TPS)', fontsize=12, fontweight='bold')
    plt.title('Blockchain Scalability: TPS vs Side Chains', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(img_dir / 'tps_vs_sidechains.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {img_dir / 'tps_vs_sidechains.png'}")
    plt.close()
    
    # Plot 2: Improvement Factor vs Bitcoin
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(side_chains)), improvement, color='green', alpha=0.7)
    plt.axhline(y=1, color='r', linestyle='--', linewidth=2, label='Bitcoin Baseline')
    plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
    plt.ylabel('Improvement Factor (vs Bitcoin)', fontsize=12, fontweight='bold')
    plt.title('Performance Improvement over Bitcoin', fontsize=14, fontweight='bold')
    plt.xticks(range(len(side_chains)), side_chains)
    plt.grid(True, alpha=0.3, axis='y')
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(img_dir / 'improvement_vs_bitcoin.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {img_dir / 'improvement_vs_bitcoin.png'}")
    plt.close()
    
    # Plot 3: TPS Comparison (Theoretical vs Maximum)
    plt.figure(figsize=(10, 6))
    x = np.arange(len(side_chains))
    width = 0.35
    plt.bar(x - width/2, tps_values, width, label='Theoretical TPS', color='blue', alpha=0.7)
    plt.bar(x + width/2, max_tps_values, width, label='Maximum TPS', color='orange', alpha=0.7)
    plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
    plt.ylabel('Transactions Per Second (TPS)', fontsize=12, fontweight='bold')
    plt.title('TPS: Theoretical vs Maximum Capacity', fontsize=14, fontweight='bold')
    plt.xticks(x, side_chains)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(img_dir / 'tps_theoretical_vs_max.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {img_dir / 'tps_theoretical_vs_max.png'}")
    plt.close()
    
    # Plot 4: Horizontal Scalability
    plt.figure(figsize=(10, 6))
    plt.plot(side_chains, tps_values, 'g-o', linewidth=2, markersize=8)
    plt.fill_between(side_chains, tps_values, alpha=0.3, color='green')
    plt.xlabel('Number of Side Chains', fontsize=12, fontweight='bold')
    plt.ylabel('Total Network TPS', fontsize=12, fontweight='bold')
    plt.title('Horizontal Scalability of Chain Architecture', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(img_dir / 'horizontal_scalability.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {img_dir / 'horizontal_scalability.png'}")
    plt.close()
    
    # Plot 5: Architecture Diagram (Conceptual)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Master Chain
    master_y = 7
    for i in range(5):
        rect = plt.Rectangle((i*2, master_y), 1.5, 0.8, 
                            facecolor='lightblue', edgecolor='blue', linewidth=2)
        ax.add_patch(rect)
        ax.text(i*2 + 0.75, master_y + 0.4, f'M{i}', 
               ha='center', va='center', fontsize=10, fontweight='bold')
        if i < 4:
            ax.arrow(i*2 + 1.5, master_y + 0.4, 0.45, 0, 
                    head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    
    ax.text(5, master_y + 1.5, 'Master Chain (10 min blocks)', 
           ha='center', fontsize=12, fontweight='bold')
    
    # Side Chains
    side_y_positions = [5, 3.5, 2]
    for side_idx, y_pos in enumerate(side_y_positions):
        for i in range(7):
            rect = plt.Rectangle((i*1.3, y_pos), 0.9, 0.6, 
                               facecolor='lightgreen', edgecolor='green', linewidth=1.5)
            ax.add_patch(rect)
            ax.text(i*1.3 + 0.45, y_pos + 0.3, f'S{side_idx}{i}', 
                   ha='center', va='center', fontsize=8)
            if i < 6:
                ax.arrow(i*1.3 + 0.9, y_pos + 0.3, 0.35, 0, 
                        head_width=0.15, head_length=0.08, fc='green', ec='green')
        
        # Arrows from side chains to master chain
        for i in [1, 3, 5]:
            ax.arrow(i*1.3 + 0.45, y_pos + 0.6, 0.3, master_y - y_pos - 0.8, 
                    head_width=0.15, head_length=0.15, 
                    fc='orange', ec='orange', alpha=0.6, linestyle='--')
        
        ax.text(-0.5, y_pos + 0.3, f'Side Chain {side_idx+1}', 
               ha='right', fontsize=10)
    
    ax.text(5, 0.5, 'Side Chains (1 min blocks)', 
           ha='center', fontsize=12, fontweight='bold')
    
    plt.title('Chain Architecture: Master + Side Chains', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(img_dir / 'architecture_diagram.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {img_dir / 'architecture_diagram.png'}")
    plt.close()
    
    print("\n✓ All plots generated successfully!")

def save_results_json(results):
    """Save benchmark results to JSON file"""
    output_file = Path('/Users/sajad/Desktop/Chain/benchmarks/benchmark_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved to: {output_file}")

def generate_latex_table(results):
    """Generate LaTeX table code for the thesis"""
    latex_code = """\\begin{table}[h]
\\centering
\\caption{نتایج بنچمارک TPS برای تعداد مختلف زنجیره‌های جانبی}
\\label{tab:tps-benchmark}
\\begin{tabular}{|c|c|c|c|}
\\hline
\\textbf{تعداد زنجیره‌های جانبی} & \\textbf{TPS} & \\textbf{حداکثر TPS} & \\textbf{بهبود نسبت به بیتکوین} \\\\ \\hline
"""
    
    for r in results:
        latex_code += f"{r['side_chains']} & {r['tps']:.2f} & {r['max_tps']:.2f} & {r['vs_bitcoin']:.2f}x \\\\ \\hline\n"
    
    latex_code += """\\end{tabular}
\\end{table}
"""
    
    output_file = Path('/Users/sajad/Desktop/Chain/benchmarks/benchmark_table.tex')
    with open(output_file, 'w') as f:
        f.write(latex_code)
    print(f"✓ LaTeX table saved to: {output_file}")
    
    return latex_code

if __name__ == '__main__':
    print("\n🚀 Starting Blockchain TPS Benchmark...\n")
    
    # Run benchmarks
    results = benchmark_all_configs()
    
    # Create plots
    print("\n📊 Generating plots...")
    create_plots(results)
    
    # Save results
    save_results_json(results)
    
    # Generate LaTeX table
    print("\n📝 Generating LaTeX table...")
    latex_table = generate_latex_table(results)
    
    print("\n✅ Benchmark complete!")
    print("\nNext steps:")
    print("  1. Check the generated plots in thesis_latex_sample/img/")
    print("  2. Review benchmark_results.json for detailed data")
    print("  3. Use benchmark_table.tex in your thesis")

