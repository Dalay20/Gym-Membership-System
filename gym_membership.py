"""Gym membership system module with plan validation and feature selection."""
"""acorde al requerimiento 4, se asume que en el menu pueden haber dos compras, de dos o mas membresias, asi que se usa compras"""
from multiprocessing.pool import ApplyResult


"""se decidió crear las clases item y buyer debido al 4to requerimiento"""
class Item:

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

    def __init__(self, plan_name, additional_features, premium_membership_features):
            self.plan_name = plan_name
            self.additional_features = additional_features
            self.premium_membership_features = premium_membership_features

    def get_plan_cost(self):
        """Get the cost of a specific plan.

        Args:
            plan_name: Name of the membership plan.

        Returns:
            Cost of the plan, or 0 if plan not found.
        """
        if self.plan_name in self.plan:
            return self.plan[self.plan_name]['cost']
        return 0

    def get_features_cost(self):
        features_cost = 0
        for feature in self.additional_features:
            features_cost += self.get_feature_cost(feature)
        return features_cost

    def get_feature_cost(self, feature):
        return self.ADDITIONAL_FEATURES[feature]

    def calculate_total_membership_cost(self):
        base_plan_cost = self.get_plan_cost()
        features_cost = self.get_features_cost()
        cost = features_cost + base_plan_cost
        return cost


class Buyer:

    DISCOUNT_GROUP_MEMBERSHIP = 0.10
    NOTIFICATION_GROUP_MEMBERSHIP = f"Adquiere planes de membresía con tus amigos y recibe descuentos de: {DISCOUNT_GROUP_MEMBERSHIP * 100}%"

    def __init__(self, items):
            self.items = items

    def apply_discount(self, cost):
        return cost * self.DISCOUNT_GROUP_MEMBERSHIP

    def notify_discount(self):
        print(self.NOTIFICATION_GROUP_MEMBERSHIP)

    def count_membership(self):
        """
        Cuenta cuántas membresías de cada tipo hay en la compra.

        Args:
            buyer: Objeto Buyer que contiene una lista de items.

        Returns:
            dict: Diccionario con formato { 'NombrePlan': cantidad }
                  Ejemplo: { 'Premium': 2, 'Basic': 1 }
        """
        plan_counts = {}

        for item in self.items:
            if item.plan_name in plan_counts:
                plan_counts[item.plan_name] += 1
            else:
                plan_counts[item.plan_name] = 1

        return plan_counts

    def validate_discount_membership_group(self, plan_counts):
        valid_plans_discount_membership_group = []
        for plan in plan_counts:
            quantity = plan_counts[plan]
            if quantity > 1:
                valid_plans_discount_membership_group.append(plan)
        return valid_plans_discount_membership_group

    def calculate_costs(self):
        plan_counts = self.count_membership()
        valid_plans_discount_membership_group = self.validate_discount_membership_group(plan_counts)
        costs = {"Basic": 0.0, "Premium": 0.0, "Student":0.0, "Family":0.0}

        for item in self.items:
            item_total_membership_cost = item.calculate_total_membership_cost()
            if item.plan_name in costs:
                costs[item.plan_name] += item_total_membership_cost

        for plan_name in valid_plans_discount_membership_group:
            if plan_name in costs:
                discount_amount = self.apply_discount(costs[plan_name])
                costs[plan_name] -= discount_amount
        return costs

    def sum_costs(self, costs):
        total = 0.0
        for plan in costs:
            total += costs[plan]
        return total

    """otros requerimientos"""


def show_options():
    """Display available membership plans and additional features."""
    print("\n--- GYM MEMBERSHIP PLANS ---")
    for plan_name, details in Item.plan.items():
        print(f"===== {plan_name} Plan =====")
        print(f"Benefits: {details['benefits']}")
        print(f"Cost: ${details['cost']}")
        """permitir a usuario seleccionar lo mostrado y guardarlo , requirement ?"""
    print("\n--- ADDITIONAL FEATURES ---")
    for feature, cost in Item.ADDITIONAL_FEATURES.items():
        print(f"- {feature}: ${cost}")
    """Permitir a usuario seleccionar lo mostrado, requirement ?"""


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

    for item in features_input_list:
        clean_item = item.strip().lower()
        if clean_item in features_map:
            selected_valid_features.append(features_map[clean_item])
        elif clean_item:  # Si no está vacío pero no coincide
            invalid_features.append(item.strip())

    return selected_valid_features, invalid_features

def menu():
    print("=== BIENVENIDO AL SISTEMA DE MEMBRESÍAS DEL GYM ===")

    items = []

    while True:
        show_options()

        # Selección del plan
        plan_input = input("\nIngrese el nombre del plan que desea comprar: ")
        plan_name = validar_plan(plan_input)
        if not plan_name:
            print("Plan no válido. Intente nuevamente.")
            continue

        # Selección de features adicionales
        features_input = input("Ingrese features adicionales separados por coma (o presione Enter para none): ")
        features_list = [f.strip() for f in features_input.split(",")] if features_input else []
        valid_features, invalid_features = select_features(features_list)

        if invalid_features:
            print(f"Features inválidas ignoradas: {', '.join(invalid_features)}")

        # Crear item y agregar a la lista
        item = Item(plan_name, valid_features, premium_membership_features=[])
        items.append(item)

        print(f"\nPlan '{plan_name}' agregado con features: {', '.join(valid_features) if valid_features else 'ninguna'}.")

        # Preguntar al usuario qué desea hacer
        print("\n¿Qué desea hacer ahora?")
        print("1 - Agregar otro plan")
        print("2 - Calcular costos y finalizar compra")
        next_action = input("Ingrese opción (1 o 2): ").strip()

        if next_action == "2":
            break
        elif next_action != "1":
            print("Opción no válida, continuando con el menú...\n")

    if not items:
        print("No se seleccionó ninguna membresía. Saliendo del sistema.")
        return

    # Crear comprador y calcular costos
    buyer = Buyer(items)
    costs = buyer.calculate_costs()
    total = buyer.sum_costs(costs)

    # Mostrar resumen
    print("\n=== RESUMEN DE SU COMPRA ===")
    for plan, cost in costs.items():
        if cost > 0:
            print(f"{plan}: ${cost:.2f}")
    print(f"Total a pagar: ${total:.2f}")

    # Notificación de descuentos grupales
    if any(qty > 1 for qty in buyer.count_membership().values()):
        buyer.notify_discount()

    print("\n¡Gracias por su compra!")


if __name__ == "__main__":
    menu()
