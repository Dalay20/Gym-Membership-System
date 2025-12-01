"""Validation and utility functions for gym membership system."""
from models import Item


def validar_plan(plan_input):
    """Validate and normalize plan input.

    Args:
        plan_input: The plan name entered by the user.

    Returns:
        Normalized plan name if valid, None otherwise.
    """
    if not plan_input:
        return None

    normalized_plan = plan_input.strip().capitalize()

    if normalized_plan in Item.plan:
        return normalized_plan
    return None


def select_features(features_input_list):
    """Validate and select features from user input list.

    Args:
        features_input_list: List of feature names entered by the user.

    Returns:
        Tuple of (valid_features, invalid_features).
    """
    selected_valid_features = []
    invalid_features = []

    # Mapeo insensible a mayúsculas para facilitar la búsqueda
    features_map = {k.lower(): k for k in Item.ADDITIONAL_FEATURES}
    features_map.update({k.lower(): k for k in Item.PREMIUM_FEATURES})

    for item in features_input_list:
        clean_item = item.strip().lower()
        if clean_item in features_map:
            selected_valid_features.append(features_map[clean_item])
        elif clean_item:  # Si no está vacío pero no coincide
            invalid_features.append(item.strip())

    return selected_valid_features, invalid_features


def show_options():
    """Display available membership plans and additional features."""
    print("\n--- GYM MEMBERSHIP PLANS ---")
    for plan_name, details in Item.plan.items():
        print(f"===== {plan_name} Plan =====")
        print(f"Benefits: {details['benefits']}")
        print(f"Cost: ${details['cost']}")
    print("\n--- ADDITIONAL FEATURES ---")
    for feature, cost in Item.ADDITIONAL_FEATURES.items():
        print(f"- {feature}: ${cost}")

    print("\n--- PREMIUM MEMBERSHIP FEATURES (15% surcharge applied) ---")
    for feature, cost in Item.PREMIUM_FEATURES.items():
        print(f"- {feature}: ${cost}")


def get_plan_cost(plan_name):
    """Return the cost for a given plan name or 0 if not found."""
    if plan_name in Item.plan:
        return Item.plan[plan_name]["cost"]
    return 0


def validate_plan_availability(plan_name):
    """Validate that a membership plan is available.

    Args:
        plan_name: The plan name to check.

    Returns:
        bool: True if plan is available, False otherwise.
    """
    return plan_name in Item.plan


def check_plan_availability(plan_name):
    """Check plan availability and provide a reason when unavailable.

    Returns:
        tuple: (available: bool, reason: str|None)
    """
    if not plan_name:
        return False, "Nombre de plan vacío"
    if plan_name in Item.plan:
        # Si existe una mapping de disponibilidad, respetarla; por defecto True
        available = getattr(Item, 'PLAN_AVAILABLE', {}).get(plan_name, True)
        if available:
            return True, None
        return False, "El plan está marcado como no disponible"
    return False, "El plan no existe"


def validate_feature_availability(feature_name):
    """Validate that a feature is available.

    Args:
        feature_name: The feature name to check.

    Returns:
        bool: True if feature is available, False otherwise.
    """
    return (feature_name in Item.ADDITIONAL_FEATURES or
            feature_name in Item.PREMIUM_FEATURES)


def check_feature_availability(feature_name):
    """Check feature availability and provide a reason when unavailable.

    Returns:
        tuple: (available: bool, reason: str|None)
    """
    if not feature_name:
        return False, "Nombre de característica vacío"
    # Por compatibilidad, asumimos que ADDITIONAL_FEATURES y PREMIUM_FEATURES
    # contienen valores de coste (int). La disponibilidad se puede controlar
    # opcionalmente desde Item.FEATURE_AVAILABLE (dict de bool).
    if (feature_name in Item.ADDITIONAL_FEATURES or
            feature_name in Item.PREMIUM_FEATURES):
        available = getattr(Item, 'FEATURE_AVAILABLE', {}).get(feature_name, True)
        if available:
            return True, None
        return False, "La característica está marcada como no disponible"
    return False, "La característica no existe"
