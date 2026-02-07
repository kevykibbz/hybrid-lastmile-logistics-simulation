"""
Visualization Module - Generate plots for simulation results

This module creates publication-ready visualizations for the final report:
- Comparison charts (normal vs peak scenarios)
- Distribution plots (delivery times)
- Vehicle utilization analysis

All plots follow academic standards with clear labels and legends.
"""

import matplotlib.pyplot as plt
import matplotlib
import os
import json
import numpy as np

# Use non-interactive backend for server environments
matplotlib.use('Agg')


# ========================================
# COMPARISON PLOTS
# ========================================

def plot_scenario_comparison(normal_results, peak_results, output_dir='outputs/plots'):
    """
    Create bar chart comparing key metrics between scenarios.
    
    This is the primary visualization for scenario comparison,
    showing how system performance degrades under peak demand.
    
    Args:
        normal_results (dict): Normal day metrics
        peak_results (dict): Peak day metrics
        output_dir (str): Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Metrics to compare
    metrics = {
        'Average Delivery Time (min)': [
            normal_results['average_delivery_time'],
            peak_results['average_delivery_time']
        ],
        'Max Delivery Time (min)': [
            normal_results['max_delivery_time'],
            peak_results['max_delivery_time']
        ],
        'Late Delivery Rate (%)': [
            normal_results['late_delivery_percentage'],
            peak_results['late_delivery_percentage']
        ],
        'Delivery Rate (%)': [
            normal_results['delivery_rate'],
            peak_results['delivery_rate']
        ]
    }
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Scenario Comparison: Normal Day vs Peak Day', fontsize=16, fontweight='bold')
    
    scenarios = ['Normal Day', 'Peak Day']
    colors = ['#4CAF50', '#F44336']  # Green for normal, red for peak
    
    # Plot each metric
    for idx, (metric_name, values) in enumerate(metrics.items()):
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]
        
        bars = ax.bar(scenarios, values, color=colors, alpha=0.7, edgecolor='black')
        ax.set_ylabel(metric_name, fontsize=11, fontweight='bold')
        ax.set_title(metric_name, fontsize=12)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(output_dir, 'scenario_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved scenario comparison plot: {output_path}")
    plt.close()
    
    # REPORT_NOTE:
    # This visualization immediately reveals the impact of demand surges:
    # - Increased delivery times (capacity saturation)
    # - Higher late delivery rates (service degradation)
    # - Potential decrease in delivery rate (unserved orders)
    # These patterns validate the need for adaptive capacity planning.


# ========================================
# DELIVERY TIME DISTRIBUTIONS
# ========================================

def plot_delivery_time_distribution(normal_results, peak_results, output_dir='outputs/plots'):
    """
    Create histogram comparing delivery time distributions.
    
    This shows not just average performance but the full distribution,
    revealing tail behavior and outliers.
    
    Args:
        normal_results (dict): Normal day metrics
        peak_results (dict): Peak day metrics
        output_dir (str): Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Delivery Time Distributions', fontsize=16, fontweight='bold')
    
    # Normal day distribution
    normal_times = normal_results.get('delivery_times', [])
    if normal_times:
        ax1.hist(normal_times, bins=20, color='#4CAF50', alpha=0.7, edgecolor='black')
        ax1.axvline(np.mean(normal_times), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(normal_times):.1f} min')
        ax1.axvline(60, color='orange', linestyle=':', linewidth=2, label='Late Threshold: 60 min')
        ax1.set_xlabel('Delivery Time (minutes)', fontsize=11)
        ax1.set_ylabel('Frequency', fontsize=11)
        ax1.set_title('Normal Day', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
    
    # Peak day distribution
    peak_times = peak_results.get('delivery_times', [])
    if peak_times:
        ax2.hist(peak_times, bins=20, color='#F44336', alpha=0.7, edgecolor='black')
        ax2.axvline(np.mean(peak_times), color='red', linestyle='--', linewidth=2, label=f'Mean: {np.mean(peak_times):.1f} min')
        ax2.axvline(60, color='orange', linestyle=':', linewidth=2, label='Late Threshold: 60 min')
        ax2.set_xlabel('Delivery Time (minutes)', fontsize=11)
        ax2.set_ylabel('Frequency', fontsize=11)
        ax2.set_title('Peak Day', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(output_dir, 'delivery_time_distribution.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved delivery time distribution plot: {output_path}")
    plt.close()


# ========================================
# VEHICLE UTILIZATION
# ========================================

def plot_vehicle_utilization(normal_results, peak_results, output_dir='outputs/plots'):
    """
    Create bar chart showing vehicle utilization differences.
    
    This reveals whether vehicles are evenly loaded or if some
    are overutilized while others are idle.
    
    Args:
        normal_results (dict): Normal day metrics
        peak_results (dict): Peak day metrics
        output_dir (str): Directory to save plots
    """
    os.makedirs(output_dir, exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Vehicle Utilization', fontsize=16, fontweight='bold')
    
    # Normal day
    normal_vehicles = normal_results.get('vehicle_deliveries', {})
    if normal_vehicles:
        vehicles = sorted(normal_vehicles.keys())
        deliveries = [normal_vehicles[v] for v in vehicles]
        
        ax1.bar(vehicles, deliveries, color='#4CAF50', alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Vehicle ID', fontsize=11)
        ax1.set_ylabel('Number of Deliveries', fontsize=11)
        ax1.set_title('Normal Day', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add mean line
        mean_deliveries = np.mean(deliveries)
        ax1.axhline(mean_deliveries, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_deliveries:.1f}')
        ax1.legend()
    
    # Peak day
    peak_vehicles = peak_results.get('vehicle_deliveries', {})
    if peak_vehicles:
        vehicles = sorted(peak_vehicles.keys())
        deliveries = [peak_vehicles[v] for v in vehicles]
        
        ax2.bar(vehicles, deliveries, color='#F44336', alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Vehicle ID', fontsize=11)
        ax2.set_ylabel('Number of Deliveries', fontsize=11)
        ax2.set_title('Peak Day', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add mean line
        mean_deliveries = np.mean(deliveries)
        ax2.axhline(mean_deliveries, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_deliveries:.1f}')
        ax2.legend()
    
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(output_dir, 'vehicle_utilization.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved vehicle utilization plot: {output_path}")
    plt.close()
    
    # REPORT_NOTE:
    # Uneven vehicle utilization suggests spatial demand imbalances.
    # This could inform:
    # - Micro-hub placement optimization
    # - Dynamic vehicle reallocation strategies
    # - Fleet sizing by geographic zone


# ========================================
# MAIN VISUALIZATION FUNCTION
# ========================================

def generate_all_plots(normal_results_file, peak_results_file, output_dir='outputs/plots'):
    """
    Generate all visualization plots from result files.
    
    This is the main entry point for creating visualization suite.
    
    Args:
        normal_results_file (str): Path to normal day results JSON
        peak_results_file (str): Path to peak day results JSON
        output_dir (str): Directory to save plots
    """
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80 + "\n")
    
    # Load results
    with open(normal_results_file, 'r') as f:
        normal_results = json.load(f)
    
    with open(peak_results_file, 'r') as f:
        peak_results = json.load(f)
    
    print(f"Loaded results:")
    print(f"  Normal Day: {normal_results_file}")
    print(f"  Peak Day: {peak_results_file}\n")
    
    # Generate plots
    plot_scenario_comparison(normal_results, peak_results, output_dir)
    plot_delivery_time_distribution(normal_results, peak_results, output_dir)
    plot_vehicle_utilization(normal_results, peak_results, output_dir)
    
    print(f"\n✓ All plots saved to: {output_dir}")
    print("="*80)


# ========================================
# SAVE METRICS TO CSV
# ========================================

def save_metrics_to_csv(normal_results, peak_results, output_file='outputs/metrics.csv'):
    """
    Save comparison metrics to CSV file for report tables.
    
    Args:
        normal_results (dict): Normal day metrics
        peak_results (dict): Peak day metrics
        output_file (str): Output CSV file path
    """
    import csv
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['Metric', 'Normal Day', 'Peak Day', 'Change (%)', 'Change (Absolute)'])
        
        # Metrics comparison
        metrics = [
            ('Total Orders Generated', 'total_orders_generated', ''),
            ('Total Orders Delivered', 'total_orders_delivered', ''),
            ('Delivery Rate (%)', 'delivery_rate', '%'),
            ('Average Delivery Time (min)', 'average_delivery_time', ' min'),
            ('Max Delivery Time (min)', 'max_delivery_time', ' min'),
            ('Late Deliveries', 'late_deliveries', ''),
            ('Late Delivery Rate (%)', 'late_delivery_percentage', '%'),
        ]
        
        for metric_name, key, unit in metrics:
            normal_val = normal_results.get(key, 0)
            peak_val = peak_results.get(key, 0)
            
            if normal_val > 0:
                change_pct = ((peak_val - normal_val) / normal_val) * 100
            else:
                change_pct = 0
            
            change_abs = peak_val - normal_val
            
            writer.writerow([
                metric_name,
                f"{normal_val:.2f}{unit}",
                f"{peak_val:.2f}{unit}",
                f"{change_pct:+.1f}%",
                f"{change_abs:+.2f}"
            ])
    
    print(f"\n✓ Metrics saved to CSV: {output_file}")


if __name__ == '__main__':
    # Example usage
    generate_all_plots(
        'outputs/normal_day_results.json',
        'outputs/peak_day_results.json'
    )
