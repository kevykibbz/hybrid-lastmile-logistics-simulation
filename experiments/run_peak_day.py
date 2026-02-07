"""
Peak Day Experiment - High demand scenario

This script runs the simulation under peak demand conditions:
- Elevated order arrival rate (+100% compared to normal)
- Same fleet size (demonstrating capacity constraints)
- Same delivery time expectations

This scenario reveals system bottlenecks and capacity limitations
that emerge during demand surges.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data import create_fleet, PEAK_FLEET, MICRO_HUBS
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
import json


def run_peak_day_experiment():
    """
    Execute the peak day simulation scenario.
    
    Returns:
        dict: Simulation results and metrics
    """
    print("="*80)
    print("PEAK DAY SCENARIO")
    print("="*80)
    
    # Get scenario parameters
    params = get_scenario_parameters('peak')
    print(f"\nScenario: {params['scenario_name']}")
    print(f"Order Rate: {params['order_rate']} orders/minute")
    print(f"Expected Orders: ~{params['total_orders']}")
    print(f"Duration: {params['duration']} minutes")
    print(f"Random Seed: {params['seed']}")
    print()
    
    # REPORT_NOTE:
    # Same random seed as normal day ensures that differences in results
    # are due to order volume, not random variation. This is essential
    # for valid scenario comparison in academic research.
    
    # Create simulation environment (DES foundation)
    env = create_simulation_environment(seed=params['seed'])
    
    # Create fleet (ABM agents) - SAME SIZE AS NORMAL DAY
    vehicles = create_fleet(PEAK_FLEET)
    print(f"Fleet: {len(vehicles)} vehicles (UNCHANGED from normal day)")
    
    # REPORT_NOTE:
    # Keeping fleet size constant is intentional. This design reveals:
    # 1. How system degrades under resource constraints
    # 2. Where bottlenecks emerge (vehicles, hubs, routing)
    # 3. Capacity planning requirements for peak periods
    
    # Create metrics collector
    metrics = MetricsCollector()
    
    # Create simulation state
    state = SimulationState(env, vehicles, metrics)
    
    # Initialize hubs
    for hub in MICRO_HUBS:
        state.initialize_hub(hub['id'], HUB_CAPACITY)
    print(f"Initialized {len(MICRO_HUBS)} micro-hubs")
    print()
    
    # Start order generation process (DES) - HIGHER RATE
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
    
    # Analyze congestion points
    analyze_congestion(state, results)
    
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
    pending_orders = state.metrics.get_pending_orders()
    
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
    
    # Hub queue analysis
    hub_queue_lengths = {}
    for hub_id, queue in state.hub_queues.items():
        hub_queue_lengths[hub_id] = len(queue)
    
    # Compile metrics
    results = {
        'scenario': params['scenario_name'],
        'total_orders_generated': len(all_orders),
        'total_orders_delivered': len(delivered_orders),
        'total_orders_pending': len(pending_orders),
        'delivery_rate': len(delivered_orders) / len(all_orders) * 100 if all_orders else 0,
        'average_delivery_time': sum(delivery_times) / len(delivery_times) if delivery_times else 0,
        'max_delivery_time': max(delivery_times) if delivery_times else 0,
        'min_delivery_time': min(delivery_times) if delivery_times else 0,
        'late_deliveries': late_deliveries,
        'late_delivery_percentage': late_deliveries / len(delivered_orders) * 100 if delivered_orders else 0,
        'vehicle_deliveries': vehicle_deliveries,
        'delivery_times': delivery_times,
        'hub_queue_lengths': hub_queue_lengths
    }
    
    return results


def analyze_congestion(state, results):
    """
    Analyze where congestion and bottlenecks occurred.
    
    Args:
        state (SimulationState): Simulation state
        results (dict): Calculated metrics
    """
    print("\n" + "="*80)
    print("CONGESTION ANALYSIS")
    print("="*80)
    
    # Check for undelivered orders
    pending = results['total_orders_pending']
    if pending > 0:
        print(f"\n⚠️  BOTTLENECK DETECTED: {pending} orders undelivered at simulation end")
        print("   This indicates vehicle capacity insufficient for demand level")
        
        # REPORT_NOTE:
        # Undelivered orders signal that fleet size is the binding constraint.
        # Options to address this bottleneck:
        # 1. Increase fleet size
        # 2. Increase vehicle capacity
        # 3. Improve routing efficiency
        # 4. Add micro-hubs to reduce delivery distances
    
    # Check hub queues
    print(f"\nHub Queue Analysis:")
    for hub_id, queue_length in results['hub_queue_lengths'].items():
        if queue_length > 0:
            print(f"  {hub_id}: {queue_length} orders still queued")
            print(f"    → Hub experienced sustained queueing throughout simulation")
    
    # Check late deliveries
    late_pct = results['late_delivery_percentage']
    if late_pct > 20:
        print(f"\n⚠️  SERVICE LEVEL DEGRADATION: {late_pct:.1f}% of deliveries were late")
        print(f"   (Threshold: >{LATE_DELIVERY_THRESHOLD} minutes)")
        
        # REPORT_NOTE:
        # High late delivery rate indicates system operating beyond design capacity.
        # This validates the need for dynamic fleet sizing or demand management
        # during peak periods (e.g., surge pricing, delivery windows).
    
    # Vehicle utilization imbalance
    deliveries = list(results['vehicle_deliveries'].values())
    if deliveries:
        max_del = max(deliveries)
        min_del = min(deliveries)
        if max_del - min_del > 5:
            print(f"\n⚠️  UTILIZATION IMBALANCE: {max_del - min_del} delivery difference between vehicles")
            print("   Consider load balancing or dynamic vehicle reallocation")
    
    print("="*80)


def print_experiment_summary(results, vehicles):
    """
    Print formatted summary of experiment results.
    
    Args:
        results (dict): Calculated metrics
        vehicles (list): Vehicle instances
    """
    print("\n" + "="*80)
    print("PEAK DAY RESULTS")
    print("="*80)
    
    print(f"\nOrder Statistics:")
    print(f"  Total Generated: {results['total_orders_generated']}")
    print(f"  Total Delivered: {results['total_orders_delivered']}")
    print(f"  Still Pending: {results['total_orders_pending']}")
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


def save_results(results, filename='outputs/peak_day_results.json'):
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
    results_copy['hub_queue_lengths'] = dict(results.get('hub_queue_lengths', {}))
    
    with open(filename, 'w') as f:
        json.dump(results_copy, f, indent=2)
    
    print(f"\nResults saved to {filename}")


if __name__ == '__main__':
    results = run_peak_day_experiment()
    save_results(results)
