"""
Facilities Module - Defines warehouse, micro-hubs, and customer locations

This module provides synthetic facility data for the urban logistics simulation.
No real-world GIS data is used - all locations and travel times are simplified.
"""

# ========================================
# WAREHOUSE DEFINITION
# ========================================

WAREHOUSE = {
    'id': 'W1',
    'name': 'Central Warehouse',
    'type': 'warehouse',
    'coordinates': (0, 0)  # Simplified coordinates (not real lat/lon)
}

# ========================================
# MICRO-HUBS DEFINITION
# ========================================

MICRO_HUBS = [
    {
        'id': 'H1',
        'name': 'Micro-Hub North',
        'type': 'micro_hub',
        'coordinates': (5, 10),
        'capacity': 50  # Max orders that can be staged here
    },
    {
        'id': 'H2',
        'name': 'Micro-Hub South',
        'type': 'micro_hub',
        'coordinates': (5, -10),
        'capacity': 50
    }
]

# ========================================
# CUSTOMER LOCATIONS
# ========================================

CUSTOMERS = [
    {'id': 'C1', 'name': 'Customer 1', 'hub': 'H1', 'coordinates': (6, 11)},
    {'id': 'C2', 'name': 'Customer 2', 'hub': 'H1', 'coordinates': (7, 12)},
    {'id': 'C3', 'name': 'Customer 3', 'hub': 'H1', 'coordinates': (4, 9)},
    {'id': 'C4', 'name': 'Customer 4', 'hub': 'H1', 'coordinates': (8, 13)},
    {'id': 'C5', 'name': 'Customer 5', 'hub': 'H1', 'coordinates': (5, 11)},
    {'id': 'C6', 'name': 'Customer 6', 'hub': 'H1', 'coordinates': (6, 10)},
    {'id': 'C7', 'name': 'Customer 7', 'hub': 'H1', 'coordinates': (7, 11)},
    {'id': 'C8', 'name': 'Customer 8', 'hub': 'H2', 'coordinates': (6, -11)},
    {'id': 'C9', 'name': 'Customer 9', 'hub': 'H2', 'coordinates': (7, -12)},
    {'id': 'C10', 'name': 'Customer 10', 'hub': 'H2', 'coordinates': (4, -9)},
    {'id': 'C11', 'name': 'Customer 11', 'hub': 'H2', 'coordinates': (8, -13)},
    {'id': 'C12', 'name': 'Customer 12', 'hub': 'H2', 'coordinates': (5, -11)},
    {'id': 'C13', 'name': 'Customer 13', 'hub': 'H2', 'coordinates': (6, -10)},
    {'id': 'C14', 'name': 'Customer 14', 'hub': 'H2', 'coordinates': (7, -11)},
    {'id': 'C15', 'name': 'Customer 15', 'hub': 'H2', 'coordinates': (8, -10)},
]

# ========================================
# HELPER FUNCTIONS
# ========================================

def get_facility_by_id(facility_id):
    """
    Retrieve a facility (warehouse, hub, or customer) by its ID.
    
    Args:
        facility_id (str): The ID of the facility
        
    Returns:
        dict: Facility information or None if not found
    """
    if facility_id == WAREHOUSE['id']:
        return WAREHOUSE
    
    for hub in MICRO_HUBS:
        if hub['id'] == facility_id:
            return hub
    
    for customer in CUSTOMERS:
        if customer['id'] == facility_id:
            return customer
    
    return None

def get_customers_by_hub(hub_id):
    """
    Get all customers assigned to a specific micro-hub.
    
    Args:
        hub_id (str): The ID of the micro-hub
        
    Returns:
        list: List of customer dictionaries
    """
    return [c for c in CUSTOMERS if c['hub'] == hub_id]
