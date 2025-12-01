"""Gym membership system module with plan validation and feature selection.

Note: According to requirement 4, the menu can handle multiple membership purchases.
Classes Item and Buyer were created to fulfill the 4th requirement.

This module re-exports all functionality from models, utils, and menu modules
for backward compatibility.
"""

# Import all classes and functions from organized modules
from models import Item, Buyer
from utils import validar_plan, select_features, show_options, get_plan_cost
from menu import menu

# Re-export for backward compatibility
plan = Item.plan

__all__ = [
    'Item',
    'Buyer',
    'validar_plan',
    'select_features',
    'show_options',
    'get_plan_cost',
    'menu',
    'plan'
]


# No ejecutar menu() automáticamente cuando se importa el módulo
# Solo ejecutar si se ejecuta directamente este archivo
if __name__ == "__main__":
    menu()
