"""Interactive menu for gym membership purchase system."""
from models import Item, Buyer
from utils import (show_options, validar_plan, select_features,
                   validate_plan_availability)


def menu():
    """Interactive menu for gym membership selection and purchase.

    Returns:
        float: Total cost if confirmed and valid, -1 if cancelled or invalid.
    """
    print("=== BIENVENIDO AL SISTEMA DE MEMBRESÍAS DEL GYM ===")

    items = []

    while True:
        show_options()

        # Selección del plan (Requirement 7: Validate availability)
        plan_input = input("\nIngrese el nombre del plan que desea comprar: ")
        plan_name = validar_plan(plan_input)
        if not plan_name:
            print(f"ERROR: El plan '{plan_input}' no es válido.")
            print("Por favor, seleccione uno de los planes disponibles listados arriba.")
            continue

        # Requirement 7: Validate plan availability (más descriptivo)
        from utils import check_plan_availability

        available, reason = check_plan_availability(plan_name)
        if not available:
            print(f"ERROR: El plan '{plan_name}' no está disponible actualmente.")
            if reason:
                print(f"Razón: {reason}.")
            print("Por favor, seleccione otro plan.")
            continue

        # Selección de features adicionales (Requirement 7: Validate availability)
        features_input = input(
            "Ingrese features adicionales separados por coma "
            "(o presione Enter para none): "
        )
        features_list = [f.strip() for f in features_input.split(",")] if features_input else []
        valid_features, invalid_features = select_features(features_list)

        # Requirement 7 & 10: Display error for unavailable features (más descriptivo)
        if invalid_features:
            print("\nADVERTENCIA: Las siguientes características no están disponibles:")
            from utils import check_feature_availability
            for inv_feat in invalid_features:
                available_feat, reason_feat = check_feature_availability(inv_feat)
                if reason_feat:
                    print(f"  - '{inv_feat}': {reason_feat}")
                else:
                    print(f"  - '{inv_feat}'")
            print("Las características inválidas serán ignoradas.")
            print("Continuando solo con las características válidas...")

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

    # Requirement 10: Handle case when no items selected
    if not items:
        print("\nERROR: No se seleccionó ninguna membresía.")
        print("No se puede procesar una compra sin al menos un plan.")
        print("Saliendo del sistema.")
        return -1  # Requirement 9: Return -1 for invalid input

    # Requirement 10: Error handling for calculation
    try:
        # Crear comprador y calcular costos
        buyer = Buyer(items)
        costs = buyer.calculate_costs()
        total = buyer.sum_costs(costs)

        # Requirement 8: Display summary for user confirmation
        print("\n" + "="*50)
        print("=== RESUMEN DE SU COMPRA ===")
        print("="*50)

        # Show selected memberships and features
        print("\nMembresías seleccionadas:")
        for idx, item in enumerate(items, 1):
            print(f"\n  {idx}. Plan: {item.plan_name}")
            if item.additional_features:
                feat_list = ', '.join(item.additional_features)
                print(f"     Características adicionales: {feat_list}")
            if item.premium_membership_features:
                prem_list = ', '.join(item.premium_membership_features)
                print(f"     Características premium: {prem_list}")

        # Show cost breakdown
        print("\nDesglose de costos:")
        for plan_name, cost in costs.items():
            if cost > 0:
                print(f"  {plan_name}: ${cost:.2f}")

        # Mostrar subtotal y recargos/descuentos
        subtotal_before_adjustments = (
            buyer.sum_costs(costs) +
            buyer.special_discount_amount -
            buyer.premium_surcharge_amount
        )

        if buyer.premium_surcharge_amount > 0 or buyer.special_discount_amount > 0:
            print(f"\n  Subtotal: ${subtotal_before_adjustments:.2f}")

            if buyer.premium_surcharge_amount > 0:
                print(f"  Recargo Premium (15%): +${buyer.premium_surcharge_amount:.2f}")

            if buyer.special_discount_amount > 0:
                print(f"  Descuento especial: -${buyer.special_discount_amount:.2f}")

        print("\n" + "="*50)
        print(f"  TOTAL A PAGAR: ${total:.2f}")
        print("="*50)

        # Notificación de descuentos grupales
        if any(qty > 1 for qty in buyer.count_membership().values()):
            print("\n💡 ", end="")
            buyer.notify_discount()

        # Requirement 8: User confirmation before finalizing
        print("\n¿Desea confirmar esta compra?")
        print("1 - Sí, confirmar y finalizar")
        print("2 - No, cancelar compra")

        confirmation = input("Ingrese su opción (1 o 2): ").strip()

        if confirmation == "1":
            print("\n✅ ¡Compra confirmada!")
            print("¡Gracias por su compra!")
            return total  # Requirement 9: Return positive integer (total cost)

        # Requirement 9: Return -1 if cancelled
        print("\n❌ Compra cancelada.")
        print("No se realizó ningún cargo.")
        return -1

    except ValueError as e:
        # Requirement 10: Handle calculation errors gracefully
        print(f"\nERROR DE CÁLCULO: {str(e)}")
        print("No se pudo procesar la compra debido a un error en los cálculos.")
        print("Por favor, contacte al administrador del sistema.")
        return -1
    except (KeyError, AttributeError, TypeError) as e:
        # Requirement 10: Handle unexpected errors
        print(f"\nERROR INESPERADO: {str(e)}")
        print("Ocurrió un error al procesar su compra.")
        print("Por favor, intente nuevamente o contacte al soporte técnico.")
        return -1


if __name__ == "__main__":
    menu()
