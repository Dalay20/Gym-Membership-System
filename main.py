"""Main module for gym membership system user interface."""
# Importamos tus funciones y datos desde tu archivo de lógica
from gym_membership import show_options, validar_plan, select_features


def main():
    """Main function to handle user interaction for membership selection."""
    print("--- Bienvenido al Sistema de Gestión de Membresías ---")

    # PARTE 1: Mostrar Opciones
    show_options()

    # PARTE 2: Selección de Plan
    # Usamos un bucle while para obligar al usuario a elegir algo válido
    selected_plan = None
    while selected_plan is None:
        plan_input = input("\nChoose membership plan: ")

        selected_plan = validar_plan(plan_input)

        if selected_plan is None:
            # Mensaje de error descriptivo
            print(f"Error: El plan '{plan_input}' no existe. Por favor intente de nuevo.")

    print(f"-> Plan seleccionado correctamente: {selected_plan}")

    # PARTE 3: Selección de Características
    print("\nEscriba las características adicionales que desea añadir, separadas por comas.")
    print("Ejemplo: Personal Training, Access to Pool")
    print("(Presione Enter si no desea ninguna)")

    features_input = input("Características: ")

    # Convertimos el string de entrada en una lista separando por comas
    features_list_raw = features_input.split(',')

    # Llamamos a tu función de validación que devuelve las dos listas
    valid_features, invalid_features = select_features(features_list_raw)

    # Manejo de errores
    if invalid_features:
        print("\n[!] Advertencia: Las siguientes características no fueron encontradas:")
        for inv in invalid_features:
            print(f"  - '{inv}'")
        print("El sistema continuará solo con las características válidas.")

    print(f"-> Features agregados: {valid_features}")

    # ---------------------------------------------------------
    # PARTE 4: Input de Miembros (Necesario para el Requisito 4 del siguiente compañero)
    # ---------------------------------------------------------
    try:
        num_members = int(input("\nIngrese el número de personas para la membresía: "))
        if num_members < 1:
            print("Error: El número de personas debe ser al menos 1.")
            return
    except ValueError:
        print("Error: Entrada inválida. Debe ingresar un número entero.")
        return

    # ---------------------------------------------------------
    # PUNTO DE INTEGRACIÓN (HAND-OFF)
    # ---------------------------------------------------------
    # Aquí es donde tu código termina y empieza el de tus compañeros.
    # Imprimimos los datos "limpios" para demostrar que tu parte funcionó.

    print("\n" + "="*40)
    print("RESUMEN DE DATOS VALIDADOS (LISTOS PARA CÁLCULO)")
    print("="*40)
    print(f"Plan Base:      {selected_plan}")
    print(f"Features:       {valid_features}")
    print(f"Miembros:       {num_members}")
    print("="*40)

    # --- AQUÍ LLAMARÍAS AL CÓDIGO DE TUS COMPAÑEROS ---
    # Ejemplo:
    # total = calcular_costo_total(selected_plan, valid_features, num_members)
    # print(f"El total a pagar es: {total}")


if __name__ == "__main__":
    main()
