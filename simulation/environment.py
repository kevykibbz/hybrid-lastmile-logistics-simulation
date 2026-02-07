"""
Environment Module - SimPy environment setup and event scheduling

This is the DISCRETE EVENT SIMULATION (DES) foundation of the hybrid model.
SimPy manages:
- Time progression
- Event scheduling (arrivals, departures, deliveries)
- Resource allocation (vehicles, hub capacity)
- Process synchronization

Combined with agent-based vehicle logic, this creates a hybrid DES+ABM simulation.
"""

import simpy
import random
from data.parameters import RANDOM_SEED, SIMULATION_DURATION


# ========================================
# ENVIRONMENT INITIALIZATION
# ========================================

def create_simulation_environment(seed=RANDOM_SEED):
    """
    Create and initialize a SimPy environment with fixed random seed.
    
    The SimPy Environment is the core of Discrete Event Simulation:
    - Maintains simulation clock
    - Schedules and executes events
    - Manages process lifecycles
    
    Args:
        seed (int): Random seed for reproducibility
        
    Returns:
        simpy.Environment: Initialized SimPy environment
    """
    # Set random seed for reproducibility (critical for scenario comparison)
    random.seed(seed)
    
    # Create SimPy environment
    env = simpy.Environment()
    
    return env


# ========================================
# SIMULATION EXECUTION
# ========================================

def run_simulation(env, duration=SIMULATION_DURATION):
    """
    Run the simulation for a specified duration.
    
    This executes the DES event loop:
    1. Process all events at current time
    2. Advance clock to next event time
    3. Repeat until duration reached
    
    Args:
        env (simpy.Environment): SimPy environment
        duration (float): Simulation duration in minutes
    """
    env.run(until=duration)
    print(f"Simulation completed at t={env.now:.1f} minutes")


# ========================================
# METRIC COLLECTION INFRASTRUCTURE
# ========================================

class MetricsCollector:
    """
    Collects performance metrics during simulation execution.
    
    This class acts as data collection layer for the DES,
    recording timestamps and states as events occur.
    """
    
    def __init__(self):
        """Initialize metrics storage."""
        self.orders = {}  # order_id -> {attributes}
        self.vehicle_stats = {}  # vehicle_id -> {statistics}
        self.system_events = []  # List of all system events
    
    def register_order(self, order_id, arrival_time, customer_id, hub_id):
        """
        Register a new order arrival (DES event).
        
        Args:
            order_id (str): Unique order identifier
            arrival_time (float): Simulation time of order arrival
            customer_id (str): Destination customer
            hub_id (str): Assigned micro-hub
        """
        self.orders[order_id] = {
            'id': order_id,
            'arrival_time': arrival_time,
            'customer_id': customer_id,
            'hub_id': hub_id,
            'pickup_time': None,
            'delivery_time': None,
            'assigned_vehicle': None,
            'status': 'PENDING'
        }
    
    def record_pickup(self, order_id, pickup_time, vehicle_id):
        """
        Record order pickup event.
        
        Args:
            order_id (str): Order identifier
            pickup_time (float): Simulation time of pickup
            vehicle_id (str): Vehicle performing pickup
        """
        if order_id in self.orders:
            self.orders[order_id]['pickup_time'] = pickup_time
            self.orders[order_id]['assigned_vehicle'] = vehicle_id
            self.orders[order_id]['status'] = 'IN_TRANSIT'
    
    def record_delivery(self, order_id, delivery_time):
        """
        Record order delivery event.
        
        Args:
            order_id (str): Order identifier
            delivery_time (float): Simulation time of delivery
        """
        if order_id in self.orders:
            self.orders[order_id]['delivery_time'] = delivery_time
            self.orders[order_id]['status'] = 'DELIVERED'
    
    def calculate_delivery_time(self, order_id):
        """
        Calculate total delivery time for an order.
        
        Args:
            order_id (str): Order identifier
            
        Returns:
            float: Delivery time in minutes, or None if not delivered
        """
        if order_id in self.orders:
            order = self.orders[order_id]
            if order['delivery_time'] is not None:
                return order['delivery_time'] - order['arrival_time']
        return None
    
    def get_all_orders(self):
        """Get all recorded orders."""
        return list(self.orders.values())
    
    def get_delivered_orders(self):
        """Get only delivered orders."""
        return [o for o in self.orders.values() if o['status'] == 'DELIVERED']
    
    def get_pending_orders(self):
        """Get orders that haven't been delivered yet."""
        return [o for o in self.orders.values() if o['status'] != 'DELIVERED']


# REPORT_NOTE:
# MetricsCollector demonstrates the advantage of DES over analytical models:
# We can track individual order trajectories and exact event timings,
# enabling detailed performance analysis impossible with aggregate queueing formulas.


# ========================================
# SIMULATION STATE MANAGEMENT
# ========================================

class SimulationState:
    """
    Maintains global simulation state accessible to all processes.
    
    This is a design pattern for DES to share information between
    concurrent processes (order generation, vehicle agents, etc.)
    """
    
    def __init__(self, env, vehicles, metrics_collector):
        """
        Initialize simulation state.
        
        Args:
            env (simpy.Environment): SimPy environment
            vehicles (list): List of Vehicle agent instances
            metrics_collector (MetricsCollector): Metrics collection object
        """
        self.env = env
        self.vehicles = vehicles
        self.metrics = metrics_collector
        
        # Order queues at each hub (DES resource modeling)
        self.hub_queues = {}  # hub_id -> list of order_ids
        
        # SimPy stores for modeling hub capacity (DES resource)
        self.hub_capacities = {}  # hub_id -> simpy.Container
    
    def initialize_hub(self, hub_id, capacity):
        """
        Set up a micro-hub with queue and capacity.
        
        Args:
            hub_id (str): Hub identifier
            capacity (int): Maximum orders that can be staged
        """
        self.hub_queues[hub_id] = []
        self.hub_capacities[hub_id] = simpy.Container(self.env, capacity=capacity, init=capacity)
    
    def add_order_to_hub_queue(self, hub_id, order_id):
        """
        Add an order to hub's waiting queue.
        
        Args:
            hub_id (str): Hub identifier
            order_id (str): Order identifier
        """
        if hub_id in self.hub_queues:
            self.hub_queues[hub_id].append(order_id)
    
    def get_available_vehicle(self, hub_id):
        """
        Find an available vehicle at a specific hub.
        
        Args:
            hub_id (str): Hub identifier
            
        Returns:
            Vehicle: Available vehicle instance or None
        """
        for vehicle in self.vehicles:
            if vehicle.base_hub == hub_id and vehicle.is_available():
                return vehicle
        return None
