"""
Fleet Module - Defines vehicle specifications and fleet composition

This module represents the AGENT-BASED component of the hybrid simulation.
Each vehicle acts as an autonomous agent with:
- Individual capacity limits
- State tracking (idle, traveling, delivering)
- Simple decision logic for order selection
"""

# ========================================
# VEHICLE TYPE DEFINITIONS
# ========================================

# Small electric cargo bikes - typical for last-mile urban delivery
VEHICLE_TYPES = {
    'CARGO_BIKE': {
        'type': 'cargo_bike',
        'capacity': 5,  # Maximum number of orders per trip
        'speed': 15,  # km/h (simplified - real speed varies by congestion)
        'description': 'Electric cargo bike for urban last-mile delivery'
    }
}

# ========================================
# FLEET COMPOSITION
# ========================================

# NORMAL DAY FLEET
# This fleet size is designed for baseline order volumes
NORMAL_FLEET = [
    {'id': 'V1', 'type': 'CARGO_BIKE', 'base_hub': 'H1'},
    {'id': 'V2', 'type': 'CARGO_BIKE', 'base_hub': 'H1'},
    {'id': 'V3', 'type': 'CARGO_BIKE', 'base_hub': 'H1'},
    {'id': 'V4', 'type': 'CARGO_BIKE', 'base_hub': 'H2'},
    {'id': 'V5', 'type': 'CARGO_BIKE', 'base_hub': 'H2'},
    {'id': 'V6', 'type': 'CARGO_BIKE', 'base_hub': 'H2'},
]

# PEAK DAY FLEET
# Same fleet used during peak demand - this is intentional to show capacity constraints
PEAK_FLEET = NORMAL_FLEET

# REPORT_NOTE:
# Fleet size remains constant between scenarios. This design choice allows us to
# observe system behavior under resource constraints during demand surges.
# Peak scenarios reveal bottlenecks and queue buildup when vehicles become saturated.


# ========================================
# VEHICLE CLASS (AGENT REPRESENTATION)
# ========================================

class Vehicle:
    """
    Agent-Based Model (ABM) component: Vehicle Agent
    
    Each vehicle is an autonomous agent that:
    - Tracks its own state (idle, traveling, delivering)
    - Makes decisions about which orders to pick up next
    - Has individual capacity and performance characteristics
    
    This class bridges DES (SimPy events) with ABM (agent behavior).
    """
    
    def __init__(self, vehicle_id, vehicle_type, base_hub):
        """
        Initialize a vehicle agent.
        
        Args:
            vehicle_id (str): Unique identifier (e.g., 'V1')
            vehicle_type (str): Type key from VEHICLE_TYPES (e.g., 'CARGO_BIKE')
            base_hub (str): Home hub ID where vehicle starts/returns
        """
        self.id = vehicle_id
        self.type = vehicle_type
        self.base_hub = base_hub
        
        # Get specifications from vehicle type
        specs = VEHICLE_TYPES[vehicle_type]
        self.capacity = specs['capacity']
        self.speed = specs['speed']
        
        # Agent state variables
        self.current_location = base_hub  # Current position (hub or customer ID)
        self.current_load = []  # List of order IDs currently carried
        self.state = 'IDLE'  # IDLE, LOADING, TRAVELING, DELIVERING
        
        # Performance tracking
        self.total_orders_delivered = 0
        self.total_distance_traveled = 0
        self.total_time_busy = 0
    
    def is_available(self):
        """Check if vehicle can accept new orders."""
        return self.state == 'IDLE' and len(self.current_load) < self.capacity
    
    def has_capacity(self):
        """Check if vehicle has space for more orders."""
        return len(self.current_load) < self.capacity
    
    def load_order(self, order_id):
        """
        Load an order onto the vehicle (agent decision).
        
        Args:
            order_id (str): Order identifier to load
        """
        if self.has_capacity():
            self.current_load.append(order_id)
            return True
        return False
    
    def unload_order(self, order_id):
        """
        Unload an order at delivery point.
        
        Args:
            order_id (str): Order identifier to unload
        """
        if order_id in self.current_load:
            self.current_load.remove(order_id)
            self.total_orders_delivered += 1
            return True
        return False
    
    def __repr__(self):
        return f"Vehicle({self.id}, {self.state}, load={len(self.current_load)}/{self.capacity})"


# ========================================
# HELPER FUNCTIONS
# ========================================

def create_fleet(fleet_config):
    """
    Instantiate vehicle agents from configuration.
    
    Args:
        fleet_config (list): List of vehicle configuration dicts
        
    Returns:
        list: List of Vehicle agent instances
    """
    vehicles = []
    for config in fleet_config:
        vehicle = Vehicle(
            vehicle_id=config['id'],
            vehicle_type=config['type'],
            base_hub=config['base_hub']
        )
        vehicles.append(vehicle)
    return vehicles

def get_vehicles_at_hub(vehicles, hub_id):
    """
    Get all vehicles currently at a specific hub.
    
    Args:
        vehicles (list): List of Vehicle instances
        hub_id (str): Hub identifier
        
    Returns:
        list: Vehicles at the specified hub
    """
    return [v for v in vehicles if v.current_location == hub_id]
