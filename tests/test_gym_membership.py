"""Unit tests for gym membership system."""
from gym_membership import (
    validar_plan, select_features, get_plan_cost,
    show_options, plan, Item, Buyer
)


def test_validar_plan():
    """Test plan validation function."""
    assert validar_plan("Basic") == "Basic"
    assert validar_plan("basic") == "Basic"
    assert validar_plan("  premium ") == "Premium"
    assert validar_plan("") is None
    assert validar_plan("unknown") is None


def test_select_features():
    """Test feature selection and validation."""
    valid, invalid = select_features(["Personal Training", "unknown", "  access to pool  "])
    assert "Personal Training" in valid
    assert "Access to Pool" in valid
    assert any(i.lower() == "unknown" for i in invalid)


def test_get_plan_cost():
    """Test getting plan cost by name."""
    assert get_plan_cost("Basic") == plan["Basic"]["cost"]
    assert get_plan_cost("Nope") == 0


def test_show_options_outputs(capsys):
    """Test that show_options displays correct information."""
    show_options()
    captured = capsys.readouterr()
    assert "GYM MEMBERSHIP PLANS" in captured.out
    assert "ADDITIONAL FEATURES" in captured.out


def test_apply_special_discount():
    """Test special discount application on Buyer."""
    buyer = Buyer([])

    # Total just above 200 -> discount 20
    discounted_250 = buyer.apply_special_discount(250)
    assert discounted_250 == 230
    assert buyer.special_discount_amount == 20.0

    # Total above 400 -> discount 50
    discounted_450 = buyer.apply_special_discount(450)
    assert discounted_450 == 400
    assert buyer.special_discount_amount == 50.0


def test_premium_features_surcharge():
    """Test 15% surcharge when premium features are included."""
    # Item con features premium
    item_with_premium = Item("Basic", [], ["Exclusive Gym Facilities"])
    buyer_premium = Buyer([item_with_premium])

    costs = buyer_premium.calculate_costs()
    total = buyer_premium.sum_costs(costs)

    # Basic (25) + Exclusive Gym Facilities (100) = 125
    # 15% surcharge = 125 * 0.15 = 18.75
    # Total = 125 + 18.75 = 143.75
    assert buyer_premium.premium_surcharge_amount == 18.75
    assert total == 143.75

    # Item sin features premium
    item_no_premium = Item("Basic", ["Personal Training"], [])
    buyer_no_premium = Buyer([item_no_premium])

    costs_no_premium = buyer_no_premium.calculate_costs()
    total_no_premium = buyer_no_premium.sum_costs(costs_no_premium)

    # No debe haber recargo premium
    assert buyer_no_premium.premium_surcharge_amount == 0.0
    assert total_no_premium == 55  # 25 + 30

def test_item_cost_calculation():
    """Test detailed cost calculation for a single item."""
    # Plan Family (40) + Group Classes (20) + Exclusive Facilities (100)
    # Total esperado: 160
    item = Item("Family", ["Group Classes"], ["Exclusive Gym Facilities"])
    assert item.get_plan_cost() == 40
    assert item.get_feature_cost("Group Classes") == 20
    assert item.get_feature_cost("Exclusive Gym Facilities") == 100
    assert item.get_feature_cost("Feature Inexistente") == 0
    assert item.calculate_total_membership_cost() == 160

def test_group_discount_logic():
    """Test 10% discount when buying more than one of the same plan."""
    # Escenario 1: 2 planes Basic.
    # Costo: 25 + 25 = 50. Descuento 10% = 5. Total esperado = 45.
    item1 = Item("Basic", [], [])
    item2 = Item("Basic", [], [])
    buyer = Buyer([item1, item2])
    costs = buyer.calculate_costs()
    # Verifica que el costo almacenado para 'Basic' ya tenga el descuento aplicado
    assert costs["Basic"] == 45.0
    # Escenario 2: 1 Basic y 1 Premium. No hay descuento grupal.
    # Costo: 25 + 30 = 55.
    item3 = Item("Basic", [], [])
    item4 = Item("Premium", [], [])
    buyer_mixed = Buyer([item3, item4])
    costs_mixed = buyer_mixed.calculate_costs()
    assert costs_mixed["Basic"] == 25.0
    assert costs_mixed["Premium"] == 30.0


def test_buyer_utility_methods():
    """Test helper methods for counting and validating groups."""
    item1 = Item("Basic", [], [])
    item2 = Item("Basic", [], [])
    item3 = Item("Student", [], [])
    buyer = Buyer([item1, item2, item3])
    # Probar conteo
    counts = buyer.count_membership()
    assert counts["Basic"] == 2
    assert counts["Student"] == 1
    # Probar identificación de grupos válidos para descuento
    valid_groups = buyer.validate_discount_membership_group(counts)
    assert "Basic" in valid_groups
    assert "Student" not in valid_groups


def test_has_premium_features():
    """Test detection of premium features in the buyer's cart."""
    # Caso False
    item_normal = Item("Basic", ["Pool Access"], [])
    buyer_normal = Buyer([item_normal])
    assert buyer_normal.has_premium_features() is False
    # Caso True
    item_premium = Item("Basic", [], ["Specialized Training Programs"])
    buyer_premium = Buyer([item_premium])
    assert buyer_premium.has_premium_features() is True


def test_integration_surcharge_and_special_discount():
    """
    Test complex scenario: Surcharge AND Special Discount applied together.
    Order of operations: Sum -> Surcharge (15%) -> Special Discount (-$20/-$50).
    """
    # Configuración para superar los $200 pero tener features premium
    # Plan Family (40) + Specialized Program (80) + Specialized Program (80) = 200
    # Usamos 2 items para no complicar la lógica de items individuales
    item1 = Item("Family", [], ["Specialized Training Programs"]) # 40 + 80 = 120
    item2 = Item("Family", [], ["Specialized Training Programs"]) # 40 + 80 = 120
    # Subtotal Base: 240
    # Descuento Grupal (Family x2): 10% de 240 = 24.
    # Nuevo Subtotal: 216
    buyer = Buyer([item1, item2])
    costs = buyer.calculate_costs()
    assert costs["Family"] == 216.0
    # Ahora probamos sum_costs que aplica el recargo y el descuento especial
    total_final = buyer.sum_costs(costs)
    # Cálculos esperados:
    # 1. Base con descuento grupal: 216
    # 2. Recargo Premium 15% (porque tiene Specialized Training):
    #    216 * 0.15 = 32.4
    #    Subtotal + Recargo = 216 + 32.4 = 248.4
    # 3. Descuento Especial:
    #    Total > 200 (248.4 > 200), entonces resta $20.
    #    248.4 - 20 = 228.4
    assert buyer.premium_surcharge_amount == 32.4
    assert buyer.special_discount_amount == 20.0
    assert round(total_final, 2) == 228.4
