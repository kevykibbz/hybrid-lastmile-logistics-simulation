"""
Orders Module - Stochastic order generation process

This is a core DISCRETE EVENT SIMULATION (DES) component.
Orders arrive according to a Poisson process, creating arrival events
that trigger subsequent vehicle dispatch and delivery processes.

The stochastic arrival process models real-world demand uncertainty.
"""

import random
import simpy
from data.facilities import CUSTOMERS, get_customers_by_hub
from data.parameters import NORMAL_ORDER_RATE, PEAK_ORDER_RATE


# ========================================
# ORDER GENERATION (DES PROCESS)
# ========================================

def order_generator(env, state, order_rate, total_orders):
    """
    Generate orders stochastically using Poisson arrival process.
    
    This is a SimPy process - a generator function that yields events.
    It represents the DES paradigm of modeling arrival processes.
    
    Poisson Process Properties:
    - Inter-arrival times are exponentially distributed
    - Mean arrival rate = λ (orders per minute)
    - Independent arrivals (memoryless property)
    
    Args:
        env (simpy.Environment): SimPy environment
        state (SimulationState): Shared simulation state
        order_rate (float): Mean arrival rate (λ) in orders per minute
        total_orders (int): Maximum number of orders to generate
    
    Yields:
        simpy.Timeout: Waits for next arrival time
    """
    order_count = 0
    
    print(f"[DES] Starting order generation process: λ={order_rate} orders/min, target={total_orders}")
    
    while order_count < total_orders:
        # Calculate inter-arrival time using exponential distribution
        # This is the standard stochastic model for Poisson processes
        inter_arrival_time = random.expovariate(order_rate)
        
        # DES event: Wait until next order arrives
        yield env.timeout(inter_arrival_time)
        
        # Generate new order
        order_count += 1
        order_id = f"O{order_count:03d}"
        
        # Randomly assign customer (uniform distribution)
        customer = random.choice(CUSTOMERS)
        customer_id = customer['id']
        hub_id = customer['hub']
        
        # Record order arrival event in metrics
        state.metrics.register_order(
            order_id=order_id,
            arrival_time=env.now,
            customer_id=customer_id,
            hub_id=hub_id
        )
        
        # Add order to hub queue
        state.add_order_to_hub_queue(hub_id, order_id)
        
        if order_count % 20 == 0:
            print(f"[DES] t={env.now:.1f}: Order {order_id} arrived (Hub: {hub_id}, Customer: {customer_id}) [Total: {order_count}]")
    
    print(f"[DES] Order generation complete: {order_count} orders created")


# REPORT_NOTE:
# Poisson arrival process is validated by decades of research in:
# - Queueing theory (Erlang, Little's Law)
# - Call center operations
# - Retail checkout modeling
# - Emergency service arrivals
# 
# For urban logistics, Poisson captures the randomness of individual customer
# orders while maintaining statistical regularity at the aggregate level.


# ========================================
# ORDER ATTRIBUTES
# ========================================

class Order:
    """
    Order object with attributes.
    
    While not strictly necessary for this simulation (we track orders in metrics),
    this class structure would be useful for more complex order attributes
    (e.g., priority, size, special requirements).
    """
    
    def __init__(self, order_id, arrival_time, customer_id, hub_id):
        """
        Initialize an order.
        
        Args:
            order_id (str): Unique identifier
            arrival_time (float): Simulation time of order creation
            customer_id (str): Destination customer
            hub_id (str): Assigned micro-hub
        """
        self.id = order_id
        self.arrival_time = arrival_time
        self.customer_id = customer_id
        self.hub_id = hub_id
        self.status = 'PENDING'
        self.assigned_vehicle = None
        self.pickup_time = None
        self.delivery_time = None
    
    def __repr__(self):
        return f"Order({self.id}, {self.status}, Hub:{self.hub_id}, Customer:{self.customer_id})"


# ========================================
# HELPER FUNCTIONS
# ========================================

def calculate_expected_orders(order_rate, duration):
    """
    Calculate expected number of orders for given rate and duration.
    
    For a Poisson process: E[N(t)] = λ * t
    
    Args:
        order_rate (float): Arrival rate (λ) in orders per minute
        duration (float): Time period in minutes
        
    Returns:
        float: Expected number of orders
    """
    return order_rate * duration


def validate_order_rate(order_rate, duration):
    """
    Validate that order rate is reasonable for simulation.
    
    Args:
        order_rate (float): Arrival rate in orders per minute
        duration (float): Simulation duration in minutes
        
    Returns:
        bool: True if valid, False otherwise
    """
    if order_rate <= 0:
        print(f"Warning: Invalid order rate {order_rate}")
        return False
    
    expected_orders = calculate_expected_orders(order_rate, duration)
    if expected_orders < 10:
        print(f"Warning: Very few orders expected ({expected_orders:.1f})")
    
    return True
