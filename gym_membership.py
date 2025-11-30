"""Gym membership system module with plan validation and feature selection."""

plan = {
    "Basic": {
        "benefits": 'Access to standard gym equipment and locker room.',
        "cost": 25
    },
    "Premium": {
        "benefits": 'Includes Basic + Sauna access and free towel service.',
        "cost": 30
    },
    "Student": {
        "benefits": 'Access to standard gym equipment and locker room + early hours access.',
        "cost": 20
    },
    "Family": {
        "benefits": 'Access for up to 4 family members + Pool access.',
        "cost": 40
    }
}

ADDITIONAL_FEATURES = {
    'Personal Training': 30,
    'Group Classes': 20,
    'Access to Pool': 15,
    'Specialized Program': 40
}

def show_options():
    """Display available membership plans and additional features."""
    print("\n--- GYM MEMBERSHIP PLANS ---")
    for plan_name, details in plan.items():
        print(f"===== {plan_name} Plan =====")
        print(f"Benefits: {details['benefits']}")
        print(f"Cost: ${details['cost']}")

    print("\n--- ADDITIONAL FEATURES ---")
    for feature, cost in ADDITIONAL_FEATURES.items():
        print(f"- {feature}: ${cost}")

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

    if normalized_plan in plan:
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
    features_map = {k.lower(): k for k in ADDITIONAL_FEATURES}

    for item in features_input_list:
        clean_item = item.strip().lower()
        if clean_item in features_map:
            selected_valid_features.append(features_map[clean_item])
        elif clean_item:  # Si no está vacío pero no coincide
            invalid_features.append(item.strip())

    return selected_valid_features, invalid_features


def get_plan_cost(plan_name):
    """Get the cost of a specific plan.

    Args:
        plan_name: Name of the membership plan.

    Returns:
        Cost of the plan, or 0 if plan not found.
    """
    if plan_name in plan:
        return plan[plan_name]['cost']
    return 0
