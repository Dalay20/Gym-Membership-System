"""Gym membership system module with plan validation and feature selection.

Note: According to requirement 4, the menu can handle multiple membership purchases.
Classes Item and Buyer were created to fulfill the 4th requirement.
"""


class Item:
    """Represents a membership item with plan and features."""

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

    PREMIUM_FEATURES = {
        'Exclusive Gym Facilities': 100,
        'Specialized Training Programs': 80
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
        """Calculate total cost of all features (normal and premium)."""
        features_cost = 0
        # Sumar features adicionales normales
        for feature in self.additional_features:
            features_cost += self.get_feature_cost(feature)
        # Sumar features premium
        for feature in self.premium_membership_features:
            features_cost += self.get_feature_cost(feature)
        return features_cost

    def get_feature_cost(self, feature):
        """Get the cost of a specific feature."""
        if feature in self.ADDITIONAL_FEATURES:
            return self.ADDITIONAL_FEATURES[feature]
        if feature in self.PREMIUM_FEATURES:
            return self.PREMIUM_FEATURES[feature]
        return 0

    def calculate_total_membership_cost(self):
        """Calculate the total cost including plan and all features."""
        base_plan_cost = self.get_plan_cost()
        features_cost = self.get_features_cost()
        cost = features_cost + base_plan_cost
        return cost


class Buyer:
    """Represents a buyer with multiple membership items and discount logic."""

    DISCOUNT_GROUP_MEMBERSHIP = 0.10
    NOTIFICATION_GROUP_MEMBERSHIP = (
        f"Adquiere planes de membresía con tus amigos y recibe "
        f"descuentos de: {DISCOUNT_GROUP_MEMBERSHIP * 100}%"
    )

    def __init__(self, items):
        self.items = items
        self.special_discount_amount = 0.0
        self.premium_surcharge_amount = 0.0

    def apply_discount(self, cost):
        """Calculate the group membership discount amount."""
        return cost * self.DISCOUNT_GROUP_MEMBERSHIP

    def notify_discount(self):
        """Display group membership discount notification."""
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
        """Identify plans that qualify for group discounts (quantity > 1)."""
        valid_plans_discount_membership_group = []
        for plan_name in plan_counts:
            quantity = plan_counts[plan_name]
            if quantity > 1:
                valid_plans_discount_membership_group.append(plan_name)
        return valid_plans_discount_membership_group

    def calculate_costs(self):
        """Calculate costs per plan type with group discounts applied."""
        plan_counts = self.count_membership()
        valid_plans = self.validate_discount_membership_group(plan_counts)
        costs = {"Basic": 0.0, "Premium": 0.0, "Student": 0.0, "Family": 0.0}

        for item in self.items:
            item_total_membership_cost = item.calculate_total_membership_cost()
            if item.plan_name in costs:
                costs[item.plan_name] += item_total_membership_cost

        for plan_name in valid_plans:
            if plan_name in costs:
                discount_amount = self.apply_discount(costs[plan_name])
                costs[plan_name] -= discount_amount
        return costs

    def sum_costs(self, costs):
        """Sum all costs and apply premium surcharge and special discounts."""
        total = 0.0
        for plan_name in costs:
            total += costs[plan_name]

        # Aplicar recargo premium del 15% si hay features premium
        if self.has_premium_features():
            self.premium_surcharge_amount = total * 0.15
            total += self.premium_surcharge_amount

        # Aplicar descuentos especiales basados en el coste total
        discounted_total = self.apply_special_discount(total)
        return discounted_total

    def apply_special_discount(self, total):
        """Aplica descuentos especiales fijos según el total.

        Reglas:
        - Si el coste total supera 400$, resta 50$.
        - Si el coste total supera 200$, resta 20$.

        Se almacena el monto descontado en `self.special_discount_amount`.
        """
        self.special_discount_amount = 0.0
        if total > 400:
            self.special_discount_amount = 50.0
        elif total > 200:
            self.special_discount_amount = 20.0

        return max(0.0, total - self.special_discount_amount)

    def has_premium_features(self):
        """Verifica si algún item tiene features premium."""
        for item in self.items:
            for feature in item.premium_membership_features:
                if feature in Item.PREMIUM_FEATURES:
                    return True
        return False


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


# Exponer `plan` y `get_plan_cost` para compatibilidad con los tests
plan = Item.plan


def get_plan_cost(plan_name):
    """Return the cost for a given plan name or 0 if not found."""
    if plan_name in plan:
        return plan[plan_name]["cost"]
    return 0

def menu():
    """Interactive menu for gym membership selection and purchase."""
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
        features_input = input(
            "Ingrese features adicionales separados por coma "
            "(o presione Enter para none): "
        )
        features_list = [f.strip() for f in features_input.split(",")] if features_input else []
        valid_features, invalid_features = select_features(features_list)

        if invalid_features:
            print(f"Features inválidas ignoradas: {', '.join(invalid_features)}")

        # Separar features normales de premium
        normal_features = [f for f in valid_features if f in Item.ADDITIONAL_FEATURES]
        premium_features = [f for f in valid_features if f in Item.PREMIUM_FEATURES]

        # Crear item y agregar a la lista
        item = Item(plan_name, normal_features, premium_features)
        items.append(item)

        features_msg = []
        if normal_features:
            features_msg.append(f"Normal: {', '.join(normal_features)}")
        if premium_features:
            features_msg.append(f"Premium: {', '.join(premium_features)}")

        print(f"\nPlan '{plan_name}' agregado.")
        if features_msg:
            print(f"Features: {' | '.join(features_msg)}")
        else:
            print("Features: ninguna")

        # Preguntar al usuario qué desea hacer
        print("\n¿Qué desea hacer ahora?")
        print("1 - Agregar otro plan")
        print("2 - Calcular costos y finalizar compra")
        next_action = input("Ingrese opción (1 o 2): ").strip()

        if next_action == "2":
            break
        if next_action != "1":
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
    for plan_name, cost in costs.items():
        if cost > 0:
            print(f"{plan_name}: ${cost:.2f}")

    # Mostrar subtotal y recargos/descuentos
    subtotal_before_adjustments = (
        buyer.sum_costs(costs) +
        buyer.special_discount_amount -
        buyer.premium_surcharge_amount
    )

    if buyer.premium_surcharge_amount > 0 or buyer.special_discount_amount > 0:
        print(f"\nSubtotal: ${subtotal_before_adjustments:.2f}")

        if buyer.premium_surcharge_amount > 0:
            print(f"Recargo Premium (15%): +${buyer.premium_surcharge_amount:.2f}")

        if buyer.special_discount_amount > 0:
            print(f"Descuento especial: -${buyer.special_discount_amount:.2f}")

    print(f"Total a pagar: ${total:.2f}")    # Notificación de descuentos grupales
    if any(qty > 1 for qty in buyer.count_membership().values()):
        buyer.notify_discount()

    print("\n¡Gracias por su compra!")


if __name__ == "__main__":
    menu()
