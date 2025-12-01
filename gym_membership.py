
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
