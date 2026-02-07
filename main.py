"""
Main Entry Point - Hybrid Urban Logistics Simulation

This is the primary script to run the complete simulation study:
1. Execute normal day scenario
2. Execute peak day scenario
3. Generate comparison visualizations
4. Export metrics for report

The simulation demonstrates a HYBRID DISCRETE EVENT SIMULATION (DES) +
AGENT-BASED MODEL (ABM) approach to urban micro-hub logistics.
"""

import os
import sys
import json
from experiments.run_normal_day import run_normal_day_experiment, save_results as save_normal
from experiments.run_peak_day import run_peak_day_experiment, save_results as save_peak
from visualisation import generate_all_plots, save_metrics_to_csv
from simulation.vehicles import print_vehicle_summary


def main():
    """
    Main execution function - runs complete simulation study.
    """
    print("\n" + "="*80)
    print(" HYBRID URBAN LOGISTICS SIMULATION ".center(80, "="))
    print(" Discrete Event Simulation + Agent-Based Modeling ".center(80, " "))
    print("="*80 + "\n")
    
    # Create output directories
    os.makedirs('outputs/plots', exist_ok=True)
    
    print("This simulation will:")
    print("  1. Run NORMAL DAY scenario (baseline demand)")
    print("  2. Run PEAK DAY scenario (high demand)")
    print("  3. Generate comparison visualizations")
    print("  4. Export metrics for academic report\n")
    
    input("Press Enter to start simulation...")
    print()
    
    # ========================================
    # SCENARIO 1: NORMAL DAY
    # ========================================
    print("\n" + "█"*80)
    print(" SCENARIO 1: NORMAL DAY ".center(80, " "))
    print("█"*80 + "\n")
    
    normal_results = run_normal_day_experiment()
    save_normal(normal_results, 'outputs/normal_day_results.json')
    
    print("\n✓ Normal Day scenario complete")
    print("  Press Enter to continue to Peak Day scenario...")
    input()
    
    # ========================================
    # SCENARIO 2: PEAK DAY
    # ========================================
    print("\n" + "█"*80)
    print(" SCENARIO 2: PEAK DAY ".center(80, " "))
    print("█"*80 + "\n")
    
    peak_results = run_peak_day_experiment()
    save_peak(peak_results, 'outputs/peak_day_results.json')
    
    print("\n✓ Peak Day scenario complete")
    print("  Press Enter to generate visualizations...")
    input()
    
    # ========================================
    # GENERATE VISUALIZATIONS
    # ========================================
    print("\n" + "█"*80)
    print(" VISUALIZATION GENERATION ".center(80, " "))
    print("█"*80 + "\n")
    
    generate_all_plots(
        'outputs/normal_day_results.json',
        'outputs/peak_day_results.json',
        'outputs/plots'
    )
    
    # Save CSV metrics
    save_metrics_to_csv(
        normal_results,
        peak_results,
        'outputs/metrics.csv'
    )
    
    # ========================================
    # SUMMARY REPORT
    # ========================================
    print("\n" + "="*80)
    print(" SIMULATION STUDY COMPLETE ".center(80, "="))
    print("="*80 + "\n")
    
    print_summary_comparison(normal_results, peak_results)
    
    print("\n" + "="*80)
    print("OUTPUT FILES GENERATED:")
    print("="*80)
    print("\n📊 Results:")
    print("  - outputs/normal_day_results.json")
    print("  - outputs/peak_day_results.json")
    print("  - outputs/metrics.csv")
    print("\n📈 Visualizations:")
    print("  - outputs/plots/scenario_comparison.png")
    print("  - outputs/plots/delivery_time_distribution.png")
    print("  - outputs/plots/vehicle_utilization.png")
    print("\n" + "="*80)
    
    print("\n✓ All outputs ready for academic report")
    print("✓ Review REPORT_NOTE comments in source code for insights\n")
    
    # REPORT_NOTE:
    # Key findings to discuss in report:
    # 1. HYBRID MODELING APPROACH:
    #    - DES (SimPy) handles time progression and stochastic arrivals
    #    - ABM (Vehicle agents) models autonomous decision-making
    #    - Combination provides richer insights than either alone
    #
    # 2. SCENARIO COMPARISON:
    #    - Peak demand reveals system bottlenecks
    #    - Late deliveries increase under capacity constraints
    #    - Queueing effects amplified by fixed fleet size
    #
    # 3. VALIDATION & LIMITATIONS:
    #    - Synthetic data limits real-world applicability
    #    - Static routing ignores real-time optimization
    #    - No dynamic pricing or demand management
    #
    # 4. FUTURE WORK:
    #    - Incorporate real traffic data
    #    - Implement vehicle routing optimization
    #    - Model customer behavior responses
    #    - Test dynamic fleet sizing strategies


def print_summary_comparison(normal_results, peak_results):
    """
    Print side-by-side comparison of scenarios.
    
    Args:
        normal_results (dict): Normal day metrics
        peak_results (dict): Peak day metrics
    """
    print("SCENARIO COMPARISON SUMMARY")
    print("-" * 80)
    print(f"{'Metric':<40} {'Normal Day':>15} {'Peak Day':>15} {'Change':>10}")
    print("-" * 80)
    
    metrics = [
        ('Orders Generated', 'total_orders_generated', ''),
        ('Orders Delivered', 'total_orders_delivered', ''),
        ('Delivery Rate (%)', 'delivery_rate', '%'),
        ('Avg Delivery Time (min)', 'average_delivery_time', ' min'),
        ('Max Delivery Time (min)', 'max_delivery_time', ' min'),
        ('Late Deliveries', 'late_deliveries', ''),
        ('Late Delivery Rate (%)', 'late_delivery_percentage', '%'),
    ]
    
    for metric_name, key, unit in metrics:
        normal_val = normal_results.get(key, 0)
        peak_val = peak_results.get(key, 0)
        
        if normal_val > 0:
            change = ((peak_val - normal_val) / normal_val) * 100
            change_str = f"{change:+.1f}%"
        else:
            change_str = "N/A"
        
        print(f"{metric_name:<40} {normal_val:>14.1f}{unit:>1} {peak_val:>14.1f}{unit:>1} {change_str:>10}")
    
    print("-" * 80)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulation interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
