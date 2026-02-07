"""
Parameters Module - All tunable constants for the simulation

This module centralizes all configurable parameters to enable easy experimentation
and scenario comparison. Parameters are organized by category.
"""

# ========================================
# SIMULATION TIME PARAMETERS
# ========================================

# Simulation runs for one business day (in minutes)
SIMULATION_DURATION = 480  # 8 hours = 480 minutes

# Random seed for reproducibility
RANDOM_SEED = 42

# REPORT_NOTE:
# Fixed random seed ensures that scenario comparisons (normal vs peak) differ
# only in order volume, not in stochastic variation. This is critical for
# valid comparative analysis in academic research.


# ========================================
# ORDER GENERATION PARAMETERS
# ========================================

# NORMAL DAY - Baseline demand scenario
NORMAL_ORDER_RATE = 2.0  # Mean orders per minute (λ for Poisson process)
NORMAL_TOTAL_ORDERS = 60  # Expected orders over simulation period

# PEAK DAY - High demand scenario (e.g., holiday, promotion, weather-driven)
PEAK_ORDER_RATE = 4.0  # +100% order volume
PEAK_TOTAL_ORDERS = 120  # Approximately double the normal volume

# REPORT_NOTE:
# Peak scenario represents realistic demand surges observed during:
# - Holiday periods (e.g., Christmas, Black Friday)
# - Weather events (heavy rain, extreme cold)
# - Promotional campaigns
# The 2x multiplier is conservative based on industry reports of peak-to-normal ratios.


# ========================================
# VEHICLE OPERATION PARAMETERS
# ========================================

# Time required for loading orders at micro-hub (minutes)
LOADING_TIME_PER_ORDER = 2.0  # 2 minutes per order

# Time required for delivery handoff at customer (minutes)
DELIVERY_TIME_PER_ORDER = 3.0  # 3 minutes per delivery (includes customer interaction)

# Average speed for travel time calculations (km/h)
VEHICLE_SPEED = 15.0  # Typical urban cargo bike speed

# REPORT_NOTE:
# Loading/delivery times are based on practitioner interviews and industry reports.
# Real times vary by order size, building access, and customer availability.
# These simplified constants enable focus on systemic congestion effects.


# ========================================
# FACILITY PARAMETERS
# ========================================

# Micro-hub capacity (maximum orders that can be staged)
HUB_CAPACITY = 50

# Queue discipline at hubs
QUEUE_DISCIPLINE = 'FIFO'  # First-In-First-Out


# ========================================
# PERFORMANCE THRESHOLDS
# ========================================

# Service level threshold: deliveries beyond this time are considered "late"
LATE_DELIVERY_THRESHOLD = 60  # minutes from order creation

# REPORT_NOTE:
# 60-minute threshold represents typical expectations for "rapid" urban delivery.
# This aligns with promises made by food delivery and quick-commerce platforms.
# Late deliveries indicate system stress and capacity constraints.


# ========================================
# ROUTING PARAMETERS
# ========================================

# Distance scaling factor for synthetic network
DISTANCE_SCALE = 1.0  # Multiplier for Euclidean distances

# Congestion factor (applied during peak hours in some studies - not used here for simplicity)
CONGESTION_MULTIPLIER = 1.0  # No dynamic congestion in this simplified model

# REPORT_NOTE:
# Static travel times are used to isolate the effects of order volume and
# queueing from traffic congestion. Future work could incorporate dynamic
# congestion as a function of vehicle density or time-of-day.


# ========================================
# OUTPUT PARAMETERS
# ========================================

# Metrics output file
METRICS_OUTPUT_FILE = 'outputs/metrics.csv'

# Plots output directory
PLOTS_OUTPUT_DIR = 'outputs/plots/'

# Verbosity level for simulation logging
LOG_LEVEL = 'INFO'  # INFO, DEBUG, WARNING, ERROR


# ========================================
# HELPER FUNCTIONS
# ========================================

def get_scenario_parameters(scenario_type):
    """
    Get parameter set for a specific scenario.
    
    Args:
        scenario_type (str): 'normal' or 'peak'
        
    Returns:
        dict: Parameter dictionary for the scenario
    """
    if scenario_type == 'normal':
        return {
            'order_rate': NORMAL_ORDER_RATE,
            'total_orders': NORMAL_TOTAL_ORDERS,
            'duration': SIMULATION_DURATION,
            'seed': RANDOM_SEED,
            'scenario_name': 'Normal Day'
        }
    elif scenario_type == 'peak':
        return {
            'order_rate': PEAK_ORDER_RATE,
            'total_orders': PEAK_TOTAL_ORDERS,
            'duration': SIMULATION_DURATION,
            'seed': RANDOM_SEED,
            'scenario_name': 'Peak Day'
        }
    else:
        raise ValueError(f"Unknown scenario type: {scenario_type}")
