"""
Normal Day Experiment - Baseline demand scenario

This script runs the simulation under normal operating conditions:
- Baseline order arrival rate
- Standard fleet size
- Regular delivery time expectations

Results from this scenario establish the baseline performance metrics
for comparison with peak demand conditions.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import create_fleet, NORMAL_FLEET, MICRO_HUBS
from data.parameters import (
    get_scenario_parameters,
    HUB_CAPACITY,
    LATE_DELIVERY_THRESHOLD
)
from simulation import (
    create_simulation_environment,
    run_simulation,
    MetricsCollector,
    SimulationState,
    order_generator,
    initialize_vehicle_agents,
    analyze_vehicle_performance
)
import csv
import json


def run_normal_day_experiment():
    """
    Execute the normal day simulation scenario.
    
    Returns:
        dict: Simulation results and metrics
    """
    print("="*80)
    print("NORMAL DAY SCENARIO")
    print("="*80)
    
    # Get scenario parameters
    params = get_scenario_parameters('normal')
    print(f"\nScenario: {params['scenario_name']}")
    print(f"Order Rate: {params['order_rate']} orders/minute")
    print(f"Expected Orders: ~{params['total_orders']}")
    print(f"Duration: {params['duration']} minutes")
    print(f"Random Seed: {params['seed']}")
    print()
    
    # Create simulation environment (DES foundation)
    env = create_simulation_environment(seed=params['seed'])
    
    # Create fleet (ABM agents)
    vehicles = create_fleet(NORMAL_FLEET)
    print(f"Fleet: {len(vehicles)} vehicles")
    
    # Create metrics collector
    metrics = MetricsCollector()
    
    # Create simulation state
    state = SimulationState(env, vehicles, metrics)
    
    # Initialize hubs
    for hub in MICRO_HUBS:
        state.initialize_hub(hub['id'], HUB_CAPACITY)
    print(f"Initialized {len(MICRO_HUBS)} micro-hubs")
    print()
    
    # Start order generation process (DES)
    env.process(order_generator(
        env, 
        state, 
        params['order_rate'], 
        params['total_orders']
    ))
    
    # Start vehicle agents (ABM)
    initialize_vehicle_agents(env, vehicles, state)
    
    # Run simulation
    print("Starting simulation...\n")
    run_simulation(env, params['duration'])
    
    # Collect results
    results = calculate_metrics(state, params)
    
    # Print summary
    print_experiment_summary(results, vehicles)
    
    return results


def calculate_metrics(state, params):
    """
    Calculate performance metrics from simulation results.
    
    Args:
        state (SimulationState): Simulation state with metrics
        params (dict): Scenario parameters
        
    Returns:
        dict: Calculated metrics
    """
    delivered_orders = state.metrics.get_delivered_orders()
    all_orders = state.metrics.get_all_orders()
    
    # Calculate delivery times
    delivery_times = []
    late_deliveries = 0
    
    for order in delivered_orders:
        delivery_time = order['delivery_time'] - order['arrival_time']
        delivery_times.append(delivery_time)
        
        if delivery_time > LATE_DELIVERY_THRESHOLD:
            late_deliveries += 1
    
    # Calculate vehicle utilization
    vehicle_deliveries = {}
    for order in delivered_orders:
        vehicle_id = order['assigned_vehicle']
        if vehicle_id:
            vehicle_deliveries[vehicle_id] = vehicle_deliveries.get(vehicle_id, 0) + 1
    
    # Compile metrics
    results = {
        'scenario': params['scenario_name'],
        'total_orders_generated': len(all_orders),
        'total_orders_delivered': len(delivered_orders),
        'delivery_rate': len(delivered_orders) / len(all_orders) * 100 if all_orders else 0,
        'average_delivery_time': sum(delivery_times) / len(delivery_times) if delivery_times else 0,
        'max_delivery_time': max(delivery_times) if delivery_times else 0,
        'min_delivery_time': min(delivery_times) if delivery_times else 0,
        'late_deliveries': late_deliveries,
        'late_delivery_percentage': late_deliveries / len(delivered_orders) * 100 if delivered_orders else 0,
        'vehicle_deliveries': vehicle_deliveries,
        'delivery_times': delivery_times
    }
    
    return results


def print_experiment_summary(results, vehicles):
    """
    Print formatted summary of experiment results.
    
    Args:
        results (dict): Calculated metrics
        vehicles (list): Vehicle instances
    """
    print("\n" + "="*80)
    print("NORMAL DAY RESULTS")
    print("="*80)
    
    print(f"\nOrder Statistics:")
    print(f"  Total Generated: {results['total_orders_generated']}")
    print(f"  Total Delivered: {results['total_orders_delivered']}")
    print(f"  Delivery Rate: {results['delivery_rate']:.1f}%")
    
    print(f"\nDelivery Time Performance:")
    print(f"  Average: {results['average_delivery_time']:.1f} minutes")
    print(f"  Maximum: {results['max_delivery_time']:.1f} minutes")
    print(f"  Minimum: {results['min_delivery_time']:.1f} minutes")
    
    print(f"\nService Level:")
    print(f"  Late Deliveries (>{LATE_DELIVERY_THRESHOLD} min): {results['late_deliveries']}")
    print(f"  Late Delivery Rate: {results['late_delivery_percentage']:.1f}%")
    
    print(f"\nVehicle Utilization:")
    for vehicle_id, deliveries in sorted(results['vehicle_deliveries'].items()):
        print(f"  {vehicle_id}: {deliveries} deliveries")
    
    print("="*80)


def save_results(results, filename='outputs/normal_day_results.json'):
    """
    Save results to JSON file.
    
    Args:
        results (dict): Experiment results
        filename (str): Output file path
    """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Convert for JSON serialization
    results_copy = results.copy()
    results_copy['vehicle_deliveries'] = dict(results['vehicle_deliveries'])
    
    with open(filename, 'w') as f:
        json.dump(results_copy, f, indent=2)
    
    print(f"\nResults saved to {filename}")


if __name__ == '__main__':
    results = run_normal_day_experiment()
    save_results(results)
