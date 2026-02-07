"""
Generate Conceptual Model Diagram for Hybrid DES+ABM Simulation

This script creates a visual representation of the simulation architecture
showing the interaction between DES and ABM components.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.lines as mlines

def create_conceptual_diagram():
    """Create and save conceptual model diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Hybrid DES + ABM Architecture', 
            fontsize=18, fontweight='bold', ha='center')
    ax.text(7, 9.0, 'Urban Micro-Hub Logistics Simulation', 
            fontsize=12, ha='center', style='italic', color='gray')
    
    # ============ DES LAYER (Left Side) ============
    des_box = FancyBboxPatch((0.5, 4.5), 5.5, 3.5, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='#2E86AB', facecolor='#E8F4F8', 
                             linewidth=2.5, alpha=0.9)
    ax.add_patch(des_box)
    
    ax.text(3.25, 7.7, 'DISCRETE EVENT SIMULATION', 
            fontsize=12, fontweight='bold', ha='center', color='#2E86AB')
    ax.text(3.25, 7.4, '(SimPy Framework)', 
            fontsize=9, ha='center', color='#2E86AB', style='italic')
    
    # DES Components
    des_components = [
        (1.2, 6.8, 'Stochastic Order\nGeneration'),
        (1.2, 6.0, 'Time Progression\n& Event Scheduling'),
        (1.2, 5.2, 'Hub Queueing\nManagement'),
        (5.0, 6.8, 'Poisson Process\nλ = 2.0-4.0/min'),
        (5.0, 6.0, 'SimPy\nEnvironment'),
        (5.0, 5.2, 'Metrics\nCollection'),
    ]
    
    for x, y, label in des_components:
        box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.45, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#2E86AB', facecolor='white', 
                            linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=8, ha='center', va='center')
    
    # ============ ABM LAYER (Right Side) ============
    abm_box = FancyBboxPatch((8, 4.5), 5.5, 3.5, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='#A23B72', facecolor='#F9E8F2', 
                             linewidth=2.5, alpha=0.9)
    ax.add_patch(abm_box)
    
    ax.text(10.75, 7.7, 'AGENT-BASED MODELING', 
            fontsize=12, fontweight='bold', ha='center', color='#A23B72')
    ax.text(10.75, 7.4, '(Vehicle Agents)', 
            fontsize=9, ha='center', color='#A23B72', style='italic')
    
    # ABM Components
    abm_components = [
        (8.8, 6.8, 'Vehicle State\nIDLE/LOADING/TRAVELING'),
        (8.8, 6.0, 'Capacity Limits\n(5 orders/vehicle)'),
        (8.8, 5.2, 'Autonomous\nDecision Logic'),
        (12.5, 6.8, 'Individual\nAgent Behavior'),
        (12.5, 6.0, '6 Independent\nVehicle Agents'),
        (12.5, 5.2, 'Emergent\nPatterns'),
    ]
    
    for x, y, label in abm_components:
        box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.45, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#A23B72', facecolor='white', 
                            linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, label, fontsize=8, ha='center', va='center')
    
    # ============ HYBRID INTEGRATION (Center) ============
    hybrid_box = FancyBboxPatch((5.5, 5.2), 3, 1.8, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='#F18F01', facecolor='#FFF4E6', 
                                linewidth=3, alpha=0.95)
    ax.add_patch(hybrid_box)
    
    ax.text(7, 6.7, '⚡ HYBRID INTEGRATION', 
            fontsize=11, fontweight='bold', ha='center', color='#F18F01')
    ax.text(7, 6.35, 'DES schedules events', 
            fontsize=8.5, ha='center')
    ax.text(7, 6.05, 'ABM agents respond', 
            fontsize=8.5, ha='center')
    ax.text(7, 5.75, 'System metrics collected', 
            fontsize=8.5, ha='center')
    ax.text(7, 5.45, 'Time-driven + Agent-driven', 
            fontsize=8.5, ha='center', style='italic', color='#F18F01')
    
    # ============ PHYSICAL NETWORK (Bottom) ============
    network_box = FancyBboxPatch((0.5, 0.5), 13, 3.2, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='#6A994E', facecolor='#F2F7EE', 
                                 linewidth=2.5, alpha=0.9)
    ax.add_patch(network_box)
    
    ax.text(7, 3.4, 'PHYSICAL NETWORK TOPOLOGY', 
            fontsize=12, fontweight='bold', ha='center', color='#6A994E')
    
    # Network Components with Icons
    # Warehouse
    warehouse = Circle((2, 2.3), 0.35, color='#BC4B51', alpha=0.8)
    ax.add_patch(warehouse)
    ax.text(2, 2.3, 'W1', fontsize=10, ha='center', va='center', 
            color='white', fontweight='bold')
    ax.text(2, 1.6, 'Warehouse', fontsize=9, ha='center', fontweight='bold')
    
    # Micro-Hubs
    for i, (x, label) in enumerate([(5, 'H1'), (9, 'H2')]):
        hub = patches.Rectangle((x-0.3, 2.0), 0.6, 0.6, 
                                color='#F18F01', alpha=0.8)
        ax.add_patch(hub)
        ax.text(x, 2.3, label, fontsize=9, ha='center', va='center', 
                color='white', fontweight='bold')
        ax.text(x, 1.6, 'Micro-Hub', fontsize=9, ha='center', fontweight='bold')
    
    # Customers (dots)
    customer_positions = [
        (3.5, 2.5), (4, 1.5), (6, 2.8), (6.5, 1.3),
        (7.5, 2.6), (8, 1.4), (10, 2.9), (10.5, 1.5),
        (11.5, 2.4), (12, 1.8)
    ]
    for x, y in customer_positions:
        customer = Circle((x, y), 0.12, color='#2E86AB', alpha=0.7)
        ax.add_patch(customer)
    
    ax.text(12, 1.0, 'C1-C15', fontsize=9, ha='center', 
            color='#2E86AB', fontweight='bold')
    ax.text(12, 0.75, 'Customers', fontsize=8, ha='center', color='#2E86AB')
    
    # Vehicle icon
    vehicle_icon = FancyBboxPatch((1.2, 1.0), 0.5, 0.3, 
                                  boxstyle="round,pad=0.02", 
                                  edgecolor='#A23B72', facecolor='#A23B72', 
                                  linewidth=2)
    ax.add_patch(vehicle_icon)
    ax.text(1.45, 1.15, '🚲', fontsize=12, ha='center', va='center')
    ax.text(1.45, 0.75, '6 Vehicles', fontsize=8, ha='center', fontweight='bold')
    ax.text(1.45, 0.6, 'Capacity: 5', fontsize=7, ha='center')
    
    # ============ ARROWS SHOWING FLOW ============
    arrow_style = "Simple,tail_width=1.5,head_width=8,head_length=8"
    
    # DES → Hybrid
    arrow1 = FancyArrowPatch((6, 6.1), (5.8, 6.1), 
                            arrowstyle=arrow_style, color='#2E86AB', 
                            linewidth=2, alpha=0.7)
    ax.add_patch(arrow1)
    
    # ABM → Hybrid
    arrow2 = FancyArrowPatch((8, 6.1), (8.2, 6.1), 
                            arrowstyle=arrow_style, color='#A23B72', 
                            linewidth=2, alpha=0.7)
    ax.add_patch(arrow2)
    
    # Hybrid → Network
    arrow3 = FancyArrowPatch((7, 5.2), (7, 3.8), 
                            arrowstyle=arrow_style, color='#F18F01', 
                            linewidth=2.5, alpha=0.8)
    ax.add_patch(arrow3)
    ax.text(7.5, 4.4, 'Executes\non Network', fontsize=8, 
            style='italic', color='#F18F01')
    
    # Network connections (dotted lines)
    for hub_x in [5, 9]:
        ax.plot([2, hub_x], [2.3, 2.3], 'k--', linewidth=1, alpha=0.3)
    
    # ============ LEGEND ============
    legend_elements = [
        mlines.Line2D([0], [0], color='#2E86AB', linewidth=3, label='DES Components'),
        mlines.Line2D([0], [0], color='#A23B72', linewidth=3, label='ABM Components'),
        mlines.Line2D([0], [0], color='#F18F01', linewidth=3, label='Hybrid Integration'),
        mlines.Line2D([0], [0], color='#6A994E', linewidth=3, label='Physical Network'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', 
             bbox_to_anchor=(0.02, 0.98), fontsize=9, framealpha=0.9)
    
    # ============ KEY FEATURES BOX ============
    features_text = (
        "Key Features:\n"
        "• SimPy for event scheduling\n"
        "• Poisson order arrivals\n"
        "• 6 autonomous vehicle agents\n"
        "• Real-time decision making\n"
        "• Emergent system behavior"
    )
    ax.text(13.2, 0.5, features_text, fontsize=7.5, 
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
           verticalalignment='bottom', horizontalalignment='right')
    
    plt.tight_layout()
    
    # Save figure
    output_path = 'outputs/plots/conceptual_model_diagram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Conceptual model diagram saved: {output_path}")
    
    plt.close()

if __name__ == "__main__":
    print("Generating conceptual model diagram...")
    create_conceptual_diagram()
    print("✅ Complete!")
