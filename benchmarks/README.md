# Benchmark Scripts and Data

This directory contains all benchmark-related files for the Chain blockchain project.

## 📊 Data Files

### Raw Results
- **`real_benchmark_results.json`** - Real measured performance data from Rust implementation
- **`benchmark_results.json`** - Theoretical benchmark results
- **`theoretical_max_tps_analysis.json`** - Theoretical maximum TPS analysis based on system constraints

### Processed Data
- **`benchmark_data_for_plotting.csv`** - CSV export of benchmark data for external plotting tools
- **`benchmark_data_latex.tex`** - LaTeX table of benchmark data for thesis
- **`benchmark_table.tex`** - LaTeX table for theoretical results
- **`real_benchmark_table.tex`** - LaTeX table for real results

## 🐍 Python Scripts

### Analysis Scripts (Working ✅)
- **`analyze_benchmark_data.py`** - Comprehensive analysis of benchmark data
  - Generates performance metrics
  - Creates efficiency analysis
  - Exports CSV and LaTeX tables
  - ✅ **Status**: Working correctly

- **`compare_results.py`** - Compare theoretical vs real performance
  - Shows the difference between predicted and actual TPS
  - Generates comparison markdown report
  - ✅ **Status**: Working correctly

- **`calculate_max_tps_cap.py`** - Calculate theoretical maximum TPS
  - Analyzes system constraints (CPU, network, disk, block size)
  - Identifies bottlenecks
  - Calculates scaling potential
  - ✅ **Status**: Working correctly

- **`generate_report.py`** - Generate comprehensive benchmark report
  - Creates markdown summary of all results
  - ASCII charts for quick visualization
  - ✅ **Status**: Working correctly

### Benchmark Runner
- **`real_benchmark.py`** - Runs actual benchmarks on Rust implementation
  - Builds the project in release mode
  - Runs multiple configurations
  - Measures real TPS performance
  - ⚠️ **Note**: Requires Rust toolchain and takes time to run

### Visualization Scripts (Matplotlib Issues ⚠️)
- **`create_benchmark_plots.py`** - Create comprehensive visualization plots
  - 3D performance plots
  - Heatmaps
  - Efficiency metrics
  - ⚠️ **Status**: Requires matplotlib backend configuration (crashes on some systems)

- **`visualize_real_results.py`** - Generate visualizations from real results
  - TPS vs side chains plots
  - Improvement comparisons
  - ⚠️ **Status**: Requires matplotlib backend configuration (crashes on some systems)

- **`theoretical_tps_calculator.py`** - Theoretical calculations with plots
  - Calculate theoretical TPS
  - Generate comparison plots
  - ⚠️ **Status**: Requires matplotlib backend configuration (crashes on some systems)

### Fixing Matplotlib Issues
If the plotting scripts crash (exit code 139), try:
```bash
# Option 1: Install backend dependencies
brew install python-tk

# Option 2: Use a different backend
export MPLBACKEND=Agg

# Option 3: Run in a virtual environment with proper matplotlib setup
python3 -m venv venv
source venv/bin/activate
pip install matplotlib numpy
```

## 📝 Generated Reports

- **`BENCHMARK_ANALYSIS.md`** - Comprehensive analysis report
- **`REAL_BENCHMARK_REPORT.md`** - Real performance measurements report
- **`THEORETICAL_VS_REAL_COMPARISON.md`** - Comparison between theoretical and real results

## 🚀 Quick Start

### Run Analysis (No dependencies needed)
```bash
cd benchmarks

# Analyze existing benchmark data
python3 analyze_benchmark_data.py

# Compare theoretical vs real
python3 compare_results.py

# Calculate maximum TPS potential
python3 calculate_max_tps_cap.py

# Generate comprehensive report
python3 generate_report.py
```

### Run New Benchmarks (Requires Rust)
```bash
cd benchmarks

# Run real benchmarks (takes 5-10 minutes)
./real_benchmark.py
```

### Create Visualizations (Requires matplotlib)
```bash
cd benchmarks

# Create all plots
python3 create_benchmark_plots.py

# Create real results visualizations
python3 visualize_real_results.py

# Run theoretical calculator with plots
python3 theoretical_tps_calculator.py
```

## 📈 Key Results

Based on the current benchmark data:

- **Best Performance**: 44,824.87 TPS (1 side chain, 50 transactions)
- **Peak Improvement**: 6,403.55x faster than Bitcoin
- **Scalability**: Performance scales with side chain count
- **Theoretical Maximum**: Up to 6,996.99 TPS (100 chains, single node)

## 🔗 Integration with Thesis

The LaTeX tables and generated reports are designed for direct inclusion in the thesis:

1. **LaTeX Tables**: Copy from `.tex` files to thesis chapters
2. **CSV Data**: Import into thesis plotting tools
3. **Markdown Reports**: Use for documentation and analysis sections

## 📂 File Organization

```
benchmarks/
├── README.md                              # This file
├── Data Files/
│   ├── real_benchmark_results.json        # Real measurements
│   ├── benchmark_results.json             # Theoretical results
│   ├── theoretical_max_tps_analysis.json  # Max TPS analysis
│   ├── benchmark_data_for_plotting.csv    # CSV export
│   ├── benchmark_data_latex.tex           # LaTeX table
│   ├── benchmark_table.tex                # LaTeX theoretical
│   └── real_benchmark_table.tex           # LaTeX real
├── Scripts/
│   ├── analyze_benchmark_data.py          # ✅ Working
│   ├── compare_results.py                 # ✅ Working
│   ├── calculate_max_tps_cap.py           # ✅ Working
│   ├── generate_report.py                 # ✅ Working
│   ├── real_benchmark.py                  # Requires Rust
│   ├── create_benchmark_plots.py          # ⚠️ Matplotlib
│   ├── visualize_real_results.py          # ⚠️ Matplotlib
│   └── theoretical_tps_calculator.py      # ⚠️ Matplotlib
└── Reports/
    ├── BENCHMARK_ANALYSIS.md              # Analysis report
    ├── REAL_BENCHMARK_REPORT.md           # Real results
    └── THEORETICAL_VS_REAL_COMPARISON.md  # Comparison
```

## 🛠️ Maintenance

All file paths have been updated to use the `benchmarks/` directory structure. 
The scripts now correctly reference:
- Input data from `benchmarks/`
- Output files to `benchmarks/`
- Thesis images to `../thesis_latex_sample/img/`

## 📊 Output Locations

- **CSV/JSON Data**: `benchmarks/` directory
- **LaTeX Tables**: `benchmarks/` directory  
- **Markdown Reports**: `benchmarks/` directory
- **Plot Images**: `thesis_latex_sample/img/` directory (for thesis integration)


