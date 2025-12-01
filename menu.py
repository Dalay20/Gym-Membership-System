"""Interactive menu for gym membership purchase system."""
from models import Item, Buyer
from utils import show_options, validar_plan, select_features


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

    print(f"Total a pagar: ${total:.2f}")

    # Notificación de descuentos grupales
    if any(qty > 1 for qty in buyer.count_membership().values()):
        buyer.notify_discount()

    print("\n¡Gracias por su compra!")


if __name__ == "__main__":
    menu()
