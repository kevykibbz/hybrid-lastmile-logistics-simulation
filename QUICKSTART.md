# Quick Start Guide

## Running Your First Simulation

### Step 1: Install Dependencies

```bash
cd hybrid_simulation
pip install -r requirements.txt
```

This installs:
- `simpy` - Discrete Event Simulation library
- `matplotlib` - For generating plots
- `numpy` - For numerical operations

### Step 2: Run the Complete Study

```bash
python main.py
```

This will:
1. ✓ Run normal day scenario (~15-20 seconds)
2. ✓ Run peak day scenario (~15-20 seconds)
3. ✓ Generate comparison plots
4. ✓ Export metrics to CSV

**Total runtime: < 1 minute**

### Step 3: View Results

**Generated Files:**

```
outputs/
├── normal_day_results.json      # Detailed metrics
├── peak_day_results.json        # Detailed metrics  
├── metrics.csv                  # Comparison table
└── plots/
    ├── scenario_comparison.png          # ← USE IN REPORT
    ├── delivery_time_distribution.png   # ← USE IN REPORT
    └── vehicle_utilization.png          # ← USE IN REPORT
```

---

## Alternative: Run Scenarios Individually

### Normal Day Only
```bash
python experiments/run_normal_day.py
```

### Peak Day Only
```bash
python experiments/run_peak_day.py
```

### Regenerate Plots Only
```bash
python visualisation.py
```

---

## Understanding the Output

### Console Output

You'll see:
- `[DES]` tags → Discrete Event Simulation events (order arrivals)
- `[ABM]` tags → Agent-Based Model events (vehicle actions)

Example:
```
[DES] t=8.6: Order O020 arrived (Hub: H1, Customer: C5)
[ABM] t=8.7: V1 delivering O001
```

### Key Metrics

After each scenario, you'll see:

```
Order Statistics:
  Total Generated: 60
  Total Delivered: 60
  Delivery Rate: 100.0%

Delivery Time Performance:
  Average: 45.2 minutes
  Maximum: 98.5 minutes

Service Level:
  Late Deliveries (>60 min): 12
  Late Delivery Rate: 20.0%
```

---

## Customizing Parameters

Edit `data/parameters.py`:

```python
# Increase peak demand
PEAK_ORDER_RATE = 6.0  # Default: 4.0

# Change fleet size (in data/fleet.py)
NORMAL_FLEET = [...add more vehicles...]

# Adjust service level threshold
LATE_DELIVERY_THRESHOLD = 90  # Default: 60 minutes
```

After editing, re-run:
```bash
python main.py
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'simpy'"

**Fix:**
```bash
pip install simpy matplotlib numpy
```

### Runtime Too Long

**Fix:** Reduce order volume in `data/parameters.py`:
```python
NORMAL_TOTAL_ORDERS = 30  # Default: 60
PEAK_TOTAL_ORDERS = 60    # Default: 120
```

### No Plots Generated

**Fix:** Check matplotlib backend:
```python
import matplotlib
matplotlib.use('Agg')  # Already set in visualisation.py
```

### All Orders Delivered on Peak Day (Too Easy)

**Fix:** Make peak scenario harder:
```python
# In data/parameters.py
PEAK_ORDER_RATE = 8.0  # Increase from 4.0

# OR in data/fleet.py - reduce fleet size
PEAK_FLEET = NORMAL_FLEET[:4]  # Use only 4 vehicles
```

---

## Next Steps

1. **Review Code Comments** → Look for `# REPORT_NOTE:` sections
2. **Analyze Plots** → Use for report Discussion section
3. **Experiment** → Modify parameters and re-run
4. **Extract Insights** → Compare normal vs peak behavior

---

## For Your Report

### Results Section

Use these outputs:
- `outputs/metrics.csv` → Table of metrics
- `outputs/plots/*.png` → Insert figures

### Discussion Section

Key points from `REPORT_NOTE` comments:

1. **Hybrid Approach Benefits:**
   - DES handles time progression efficiently
   - ABM captures vehicle autonomy realistically
   - Together = more realistic than pure DES or pure ABM

2. **Peak Demand Insights:**
   - Queue buildup at micro-hubs
   - Vehicle capacity becomes bottleneck
   - Late deliveries increase non-linearly

3. **Validation:**
   - Fixed random seed ensures reproducibility
   - Poisson process validated by queueing theory
   - Parameters based on industry reports

### Limitations Section

Mention:
- Synthetic data (not real geospatial)
- No route optimization
- Static routing (no real-time updates)
- Simplified vehicle behavior

### Future Work

Suggest:
- Integrate real traffic data
- Implement VRP optimization
- Add battery/charging constraints
- Model dynamic pricing

---

## Getting Help

1. Check `README.md` for detailed documentation
2. Review `REPORT_NOTE` comments in source code
3. Look at example outputs in `outputs/` folder

**Happy Simulating! 🚲📦**
