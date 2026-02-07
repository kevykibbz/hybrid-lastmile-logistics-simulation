"""
Routing Module - Simple distance and travel time calculations

This module provides simplified routing logic without real-world GIS APIs.
Travel times are calculated using Euclidean distance and fixed vehicle speeds.

No optimization algorithms are used - vehicles simply move between defined points.
"""

import math
from data.facilities import get_facility_by_id


# ========================================
# DISTANCE CALCULATIONS
# ========================================

def euclidean_distance(coord1, coord2):
    """
    Calculate Euclidean distance between two coordinates.
    
    Args:
        coord1 (tuple): (x, y) coordinates of first point
        coord2 (tuple): (x, y) coordinates of second point
        
    Returns:
        float: Distance in abstract units
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_distance(origin_id, destination_id):
    """
    Get distance between two facilities.
    
    Args:
        origin_id (str): Origin facility ID
        destination_id (str): Destination facility ID
        
    Returns:
        float: Distance in abstract units
    """
    origin = get_facility_by_id(origin_id)
    destination = get_facility_by_id(destination_id)
    
    if origin is None or destination is None:
        raise ValueError(f"Invalid facility ID: {origin_id} or {destination_id}")
    
    return euclidean_distance(origin['coordinates'], destination['coordinates'])


# ========================================
# TRAVEL TIME CALCULATIONS
# ========================================

def calculate_travel_time(distance, speed):
    """
    Calculate travel time based on distance and speed.
    
    Args:
        distance (float): Distance in km
        speed (float): Speed in km/h
        
    Returns:
        float: Travel time in minutes
    """
    if speed <= 0:
        raise ValueError("Speed must be positive")
    
    time_hours = distance / speed
    time_minutes = time_hours * 60
    return time_minutes


def get_travel_time(origin_id, destination_id, vehicle_speed):
    """
    Get travel time between two facilities for a given vehicle speed.
    
    Args:
        origin_id (str): Origin facility ID
        destination_id (str): Destination facility ID
        vehicle_speed (float): Vehicle speed in km/h
        
    Returns:
        float: Travel time in minutes
    """
    distance = get_distance(origin_id, destination_id)
    return calculate_travel_time(distance, vehicle_speed)


# ========================================
# SIMPLE ROUTING LOGIC
# ========================================

def get_nearest_customer(hub_id, customer_ids):
    """
    Find the nearest customer to a hub from a list of candidates.
    
    This is a simple "nearest neighbor" heuristic, not an optimal route.
    
    Args:
        hub_id (str): Hub facility ID
        customer_ids (list): List of customer IDs to choose from
        
    Returns:
        str: Customer ID of nearest customer, or None if list is empty
    """
    if not customer_ids:
        return None
    
    min_distance = float('inf')
    nearest_customer = None
    
    for customer_id in customer_ids:
        distance = get_distance(hub_id, customer_id)
        if distance < min_distance:
            min_distance = distance
            nearest_customer = customer_id
    
    return nearest_customer


# REPORT_NOTE:
# Routing uses simple Euclidean distance and fixed speeds - no traffic modeling.
# This abstraction lets us focus on capacity and queueing effects rather than
# route optimization complexity. Real implementations would use road networks
# and dynamic routing APIs (e.g., Google Maps, OSRM).


# ========================================
# TRAVEL TIME MATRIX (OPTIONAL PRE-COMPUTATION)
# ========================================

def build_travel_time_matrix(facility_ids, vehicle_speed):
    """
    Pre-compute travel times between all facility pairs.
    
    This is optional - useful if many route queries are needed.
    
    Args:
        facility_ids (list): List of all facility IDs
        vehicle_speed (float): Default vehicle speed in km/h
        
    Returns:
        dict: Nested dictionary {origin: {destination: time}}
    """
    matrix = {}
    
    for origin_id in facility_ids:
        matrix[origin_id] = {}
        for destination_id in facility_ids:
            if origin_id == destination_id:
                matrix[origin_id][destination_id] = 0
            else:
                travel_time = get_travel_time(origin_id, destination_id, vehicle_speed)
                matrix[origin_id][destination_id] = travel_time
    
    return matrix
