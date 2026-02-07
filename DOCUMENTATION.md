# Hybrid Urban Logistics Simulation

## Overview

This project implements a **hybrid Discrete Event Simulation (DES) + Agent-Based Model (ABM)** for urban micro-hub logistics. The simulation models last-mile delivery operations under normal and peak demand conditions.

### Key Features

- **Discrete Event Simulation (DES)**: Using SimPy to model stochastic order arrivals, queueing, and time progression
- **Agent-Based Modeling (ABM)**: Vehicles as autonomous agents with individual capacity, state, and decision-making
- **Scenario Comparison**: Normal day vs. peak day demand analysis
- **Comprehensive Metrics**: Delivery times, late deliveries, vehicle utilization
- **Academic Visualizations**: Publication-ready plots for research reports

---

## Project Structure

```
hybrid_simulation/
│
├── data/
│   ├── facilities.py      # Warehouse, hubs, customers (synthetic data)
│   ├── fleet.py           # Vehicle agents and fleet definitions
│   └── parameters.py      # All tunable simulation parameters
│
├── simulation/
│   ├── environment.py     # SimPy environment and metrics collection
│   ├── orders.py          # Stochastic order generation (Poisson process)
│   ├── vehicles.py        # Vehicle agent behavior (ABM logic)
│   └── routing.py         # Simple distance/time calculations
│
├── experiments/
│   ├── run_normal_day.py  # Normal demand scenario
│   └── run_peak_day.py    # Peak demand scenario
│
├── outputs/
│   ├── metrics.csv        # Comparison metrics (generated)
│   ├── *.json             # Detailed results (generated)
│   └── plots/             # Visualization outputs (generated)
│
├── visualisation.py       # Plotting and chart generation
├── main.py                # Main entry point
└── README.md              # This file
```

---

## Installation & Setup

### Requirements

- Python 3.8+
- SimPy (Discrete Event Simulation library)
- Matplotlib (Visualization)
- NumPy (Numerical operations)

### Installation

```bash
# Navigate to project directory
cd hybrid_simulation

# Install dependencies
pip install simpy matplotlib numpy
```

---

## Running the Simulation

### Quick Start

Run the complete simulation study (both scenarios + visualizations):

```bash
python main.py
```

This will:
1. Execute the normal day scenario
2. Execute the peak day scenario
3. Generate comparison visualizations
4. Export metrics to CSV

### Run Individual Scenarios

**Normal Day Only:**
```bash
python experiments/run_normal_day.py
```

**Peak Day Only:**
```bash
python experiments/run_peak_day.py
```

### Generate Visualizations Only

If you've already run scenarios and just want to regenerate plots:

```bash
python visualisation.py
```

---

## Simulation Parameters

Key parameters can be modified in `data/parameters.py`:

| Parameter | Normal Day | Peak Day | Description |
|-----------|------------|----------|-------------|
| `ORDER_RATE` | 2.0/min | 4.0/min | Mean order arrival rate (λ) |
| `TOTAL_ORDERS` | 60 | 120 | Target number of orders |
| `SIMULATION_DURATION` | 480 min | 480 min | Simulation time (8 hours) |
| `FLEET_SIZE` | 6 vehicles | 6 vehicles | Number of delivery vehicles |
| `LATE_DELIVERY_THRESHOLD` | 60 min | 60 min | Service level target |
| `RANDOM_SEED` | 42 | 42 | For reproducibility |

**Note:** Fleet size is intentionally kept constant to observe capacity constraints under peak demand.

---

## Understanding the Hybrid Model

### Discrete Event Simulation (DES) Component

**What it does:**
- Models order arrivals as a Poisson process (stochastic)
- Manages simulation time progression
- Handles queueing at micro-hubs
- Schedules loading, travel, and delivery events

**SimPy processes:**
- `order_generator()`: Generates orders with exponential inter-arrival times
- `vehicle_agent()`: Each vehicle runs as a concurrent process

### Agent-Based Model (ABM) Component

**What it does:**
- Each vehicle is an autonomous agent
- Agents perceive their environment (check hub queues)
- Agents make decisions (which orders to take)
- Agents take actions (load, travel, deliver)

**Vehicle agent properties:**
- Capacity limits (5 orders per trip)
- State tracking (IDLE, LOADING, TRAVELING, DELIVERING)
- Individual performance metrics

### Why Hybrid?

| Pure DES | Pure ABM | Hybrid (DES+ABM) |
|----------|----------|------------------|
| ✓ Efficient time handling | ✓ Autonomous behavior | ✓ **Best of both** |
| ✓ Stochastic processes | ✓ Heterogeneous agents | ✓ Realistic + efficient |
| ✗ Limited autonomy | ✗ Complex time management | ✓ Emergent phenomena |

---

## Output Files

### Results (JSON)

Located in `outputs/`:

- `normal_day_results.json`: Detailed metrics for normal scenario
- `peak_day_results.json`: Detailed metrics for peak scenario

**Contents:**
- Order statistics
- Delivery times (average, max, min)
- Late delivery counts
- Vehicle utilization
- Full delivery time distributions

### Metrics (CSV)

`outputs/metrics.csv`: Comparison table for academic reports

| Metric | Normal Day | Peak Day | Change (%) |
|--------|------------|----------|------------|
| Average Delivery Time | ~ | ~ | ~ |
| Late Delivery Rate | ~ | ~ | ~ |
| ... | ... | ... | ... |

### Visualizations (PNG)

Located in `outputs/plots/`:

1. **scenario_comparison.png**: Bar charts comparing key metrics
2. **delivery_time_distribution.png**: Histograms of delivery times
3. **vehicle_utilization.png**: Per-vehicle delivery counts

All plots are 300 DPI, publication-ready.

---

## Key Assumptions

### Synthetic Data
- No real geospatial data (simplified coordinate system)
- Euclidean distances (no road networks)
- Fixed travel speeds (no traffic simulation)

### Routing
- Simple sequential delivery (no optimization)
- FIFO queue discipline at hubs
- No dynamic re-routing

### Vehicle Behavior
- Fixed capacity (5 orders)
- No battery/fuel constraints
- Instantaneous loading/unloading (simplified as time delays)

### Order Characteristics
- All orders identical (no size/priority variation)
- All customers equally likely (uniform distribution)
- Poisson arrival process (validated for service systems)

---

## Interpreting Results

### Expected Patterns

**Normal Day:**
- Average delivery time: 20-40 minutes
- Late delivery rate: <10%
- All orders delivered within simulation time

**Peak Day:**
- Average delivery time: 40-80 minutes (↑50-100%)
- Late delivery rate: 20-40% (↑200-400%)
- Some orders may remain undelivered (capacity exceeded)

### Key Insights for Report

1. **Queueing Effects**: Peak demand causes queue buildup at hubs
2. **Capacity Saturation**: Fixed fleet size becomes bottleneck
3. **Service Degradation**: Late deliveries increase non-linearly
4. **Vehicle Imbalance**: Some vehicles may be overutilized

### REPORT_NOTE Comments

Throughout the codebase, look for `# REPORT_NOTE:` comments. These provide:
- Assumptions and justifications
- Observed bottlenecks
- Academic context and citations
- Suggestions for Discussion/Validation sections

**Example:**
```python
# REPORT_NOTE:
# Peak scenario shows queue buildup at Hub H2 due to limited vehicle capacity.
# This supports discussion on urban congestion under demand surges.
```

---

## Extending the Model

### Easy Modifications

1. **Change Fleet Size**: Edit `NORMAL_FLEET` in `data/fleet.py`
2. **Adjust Demand**: Modify `ORDER_RATE` in `data/parameters.py`
3. **Add Customers**: Extend `CUSTOMERS` list in `data/facilities.py`
4. **Change Threshold**: Update `LATE_DELIVERY_THRESHOLD` in `data/parameters.py`

### Advanced Extensions

1. **Dynamic Routing**: Implement vehicle routing problem (VRP) solver
2. **Real Traffic**: Integrate Google Maps API for realistic travel times
3. **Battery Constraints**: Add range limits and charging stations
4. **Customer Behavior**: Model delivery time windows and priorities
5. **Hub Capacity**: Implement hub storage limitations
6. **Demand Forecasting**: Add predictive order arrival patterns

---

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'simpy'"**
- **Solution**: `pip install simpy matplotlib numpy`

**Issue: Runtime too long (>5 minutes)**
- **Solution**: Reduce `TOTAL_ORDERS` or `SIMULATION_DURATION` in `parameters.py`

**Issue: No plots generated**
- **Solution**: Check `outputs/plots/` directory exists, verify matplotlib backend

**Issue: All orders delivered on peak day (no capacity issues observed)**
- **Solution**: Increase `PEAK_ORDER_RATE` or decrease fleet size

---

## Academic Context

### Relevant Literature

This simulation approach draws from:

1. **Queueing Theory**: 
   - Poisson arrival processes (Erlang, 1909)
   - M/M/c queue models for service systems

2. **Urban Logistics**:
   - Micro-hub consolidation strategies
   - Last-mile delivery optimization

3. **Simulation Methodology**:
   - Discrete Event Simulation (Banks et al., 2010)
   - Agent-Based Modeling (Bonabeau, 2002)
   - Hybrid DES+ABM approaches (Brailsford et al., 2019)

### Validation Strategy

For academic rigor, consider:

1. **Face Validity**: Does behavior match real-world expectations?
2. **Sensitivity Analysis**: Test parameter variations
3. **Comparison**: Benchmark against analytical queueing models (M/M/c)
4. **Empirical Validation**: Compare with real delivery data (if available)

---

## Performance Characteristics

- **Runtime**: <30 seconds per scenario (120 orders, 6 vehicles)
- **Memory**: <50 MB
- **Scalability**: Linear in number of orders and vehicles

For larger experiments (1000+ orders), consider:
- Reducing logging verbosity
- Using NumPy arrays for metrics storage
- Parallelizing scenario runs

---

## License & Citation

**For Educational/Research Use Only**

If using this simulation in academic work, please cite:
- SimPy library: https://simpy.readthedocs.io/
- Your research paper/thesis

---

## Contact & Support

For questions about this simulation:
- Review REPORT_NOTE comments in source code
- Check parameters in `data/parameters.py`
- Examine experiment scripts in `experiments/`

**Happy Simulating! 🚲📦**

---

## Appendix: File Dependencies

```
main.py
├── experiments/run_normal_day.py
│   ├── data/* (facilities, fleet, parameters)
│   └── simulation/* (environment, orders, vehicles, routing)
├── experiments/run_peak_day.py
│   ├── data/*
│   └── simulation/*
└── visualisation.py
    └── outputs/*.json
```
