"""
Vehicle Module - Agent-based vehicle behavior processes

This module implements the AGENT-BASED MODEL (ABM) component of the hybrid simulation.
Each vehicle is an autonomous agent that:
- Makes decisions about which orders to deliver
- Responds to queue states at its hub
- Operates concurrently with other vehicle agents

Combined with SimPy's DES engine, this creates the hybrid DES+ABM architecture.
"""

import simpy
from data.parameters import (
    LOADING_TIME_PER_ORDER,
    DELIVERY_TIME_PER_ORDER
)
from simulation.routing import get_travel_time


# ========================================
# VEHICLE AGENT PROCESS
# ========================================

def vehicle_agent(env, vehicle, state):
    """
    Main process for vehicle agent behavior.
    
    This is the HYBRID MODEL in action:
    - DES component: SimPy process with timeouts and events
    - ABM component: Autonomous decision-making by vehicle agent
    
    Agent Behavior Loop:
    1. Check for orders at home hub (perception)
    2. Decide whether to take orders (decision)
    3. Load orders (action)
    4. Travel and deliver (action)
    5. Return to hub (action)
    6. Repeat
    
    Args:
        env (simpy.Environment): SimPy environment (DES)
        vehicle (Vehicle): Vehicle agent instance (ABM)
        state (SimulationState): Shared simulation state
        
    Yields:
        simpy.Timeout: Time delays for loading, travel, delivery
    """
    print(f"[ABM] {vehicle.id} starting at Hub {vehicle.base_hub}")
    
    while True:
        # AGENT PERCEPTION: Check environment state
        hub_queue = state.hub_queues.get(vehicle.base_hub, [])
        
        if len(hub_queue) > 0 and vehicle.is_available():
            # AGENT DECISION: Take orders up to capacity
            orders_to_deliver = []
            
            while len(orders_to_deliver) < vehicle.capacity and len(hub_queue) > 0:
                order_id = hub_queue.pop(0)  # FIFO queue discipline
                orders_to_deliver.append(order_id)
                vehicle.load_order(order_id)
            
            print(f"[ABM] t={env.now:.1f}: {vehicle.id} loading {len(orders_to_deliver)} orders")
            
            # DES EVENT: Loading time
            vehicle.state = 'LOADING'
            loading_time = LOADING_TIME_PER_ORDER * len(orders_to_deliver)
            yield env.timeout(loading_time)
            
            # Record pickup events
            for order_id in orders_to_deliver:
                state.metrics.record_pickup(order_id, env.now, vehicle.id)
            
            # AGENT ACTION: Deliver orders
            vehicle.state = 'DELIVERING'
            
            for order_id in orders_to_deliver:
                # Get customer location
                order_data = state.metrics.orders[order_id]
                customer_id = order_data['customer_id']
                
                # REPORT_NOTE: Simple routing - no optimization
                # Real systems use vehicle routing problem (VRP) algorithms
                # Here we use sequential nearest-neighbor for transparency
                
                # DES EVENT: Travel to customer
                current_location = vehicle.current_location
                travel_time = get_travel_time(current_location, customer_id, vehicle.speed)
                
                print(f"[ABM] t={env.now:.1f}: {vehicle.id} traveling to {customer_id} ({travel_time:.1f} min)")
                vehicle.state = 'TRAVELING'
                yield env.timeout(travel_time)
                
                # Update vehicle location
                vehicle.current_location = customer_id
                vehicle.total_distance_traveled += get_travel_time(current_location, customer_id, vehicle.speed) * vehicle.speed / 60
                
                # DES EVENT: Delivery time
                print(f"[ABM] t={env.now:.1f}: {vehicle.id} delivering {order_id}")
                vehicle.state = 'DELIVERING'
                yield env.timeout(DELIVERY_TIME_PER_ORDER)
                
                # Unload order
                vehicle.unload_order(order_id)
                
                # Record delivery event
                state.metrics.record_delivery(order_id, env.now)
            
            # AGENT ACTION: Return to hub
            return_travel_time = get_travel_time(vehicle.current_location, vehicle.base_hub, vehicle.speed)
            print(f"[ABM] t={env.now:.1f}: {vehicle.id} returning to Hub {vehicle.base_hub}")
            vehicle.state = 'TRAVELING'
            yield env.timeout(return_travel_time)
            
            vehicle.current_location = vehicle.base_hub
            vehicle.state = 'IDLE'
            
        else:
            # AGENT DECISION: Wait if no orders available
            vehicle.state = 'IDLE'
            yield env.timeout(1)  # Check again in 1 minute


# REPORT_NOTE:
# The hybrid DES+ABM architecture provides several advantages:
#
# 1. DES Component (SimPy):
#    - Handles time progression and event scheduling
#    - Models stochastic processes (arrivals, travel times)
#    - Efficient simulation of queues and resources
#
# 2. ABM Component (Vehicle Agents):
#    - Captures heterogeneous behavior (different capacities, locations)
#    - Models autonomous decision-making
#    - Enables emergent system behavior from individual actions
#
# 3. Hybrid Benefits:
#    - More realistic than pure DES (captures agent autonomy)
#    - More efficient than pure ABM (uses DES for time management)
#    - Better representation of urban logistics (vehicles + system dynamics)


# ========================================
# MULTI-VEHICLE COORDINATION
# ========================================

def initialize_vehicle_agents(env, vehicles, state):
    """
    Start all vehicle agent processes concurrently.
    
    This demonstrates the DES capability to run multiple concurrent processes,
    each representing an autonomous agent.
    
    Args:
        env (simpy.Environment): SimPy environment
        vehicles (list): List of Vehicle instances
        state (SimulationState): Shared simulation state
    """
    for vehicle in vehicles:
        # Start each vehicle as a separate SimPy process
        # This creates concurrent agent behavior
        env.process(vehicle_agent(env, vehicle, state))
    
    print(f"[ABM] Initialized {len(vehicles)} vehicle agents")


# REPORT_NOTE:
# Multi-agent coordination emerges from individual agent behavior rather than
# centralized control. This is characteristic of ABM and reflects real-world
# distributed decision-making in urban logistics platforms (e.g., Uber, DoorDash).
# Emergent phenomena can include:
# - Queue formation at popular hubs
# - Uneven vehicle utilization
# - Spontaneous load balancing (or lack thereof)


# ========================================
# VEHICLE PERFORMANCE ANALYSIS
# ========================================

def analyze_vehicle_performance(vehicles):
    """
    Analyze vehicle utilization and performance.
    
    This post-simulation analysis reveals:
    - Which vehicles were most utilized
    - Whether capacity was balanced
    - Potential for fleet optimization
    
    Args:
        vehicles (list): List of Vehicle instances
        
    Returns:
        dict: Performance statistics per vehicle
    """
    performance = {}
    
    for vehicle in vehicles:
        performance[vehicle.id] = {
            'total_deliveries': vehicle.total_orders_delivered,
            'total_distance': vehicle.total_distance_traveled,
            'base_hub': vehicle.base_hub,
            'capacity': vehicle.capacity
        }
    
    return performance


def print_vehicle_summary(vehicles):
    """
    Print summary of vehicle performance.
    
    Args:
        vehicles (list): List of Vehicle instances
    """
    print("\n" + "="*60)
    print("VEHICLE PERFORMANCE SUMMARY")
    print("="*60)
    
    for vehicle in vehicles:
        print(f"{vehicle.id} (Hub {vehicle.base_hub}): "
              f"{vehicle.total_orders_delivered} deliveries, "
              f"{vehicle.total_distance_traveled:.1f} km")
    
    total_deliveries = sum(v.total_orders_delivered for v in vehicles)
    print(f"\nTotal deliveries: {total_deliveries}")
    print("="*60 + "\n")
