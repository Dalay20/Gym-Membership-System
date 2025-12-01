"""Unit tests for gym membership system."""
from gym_membership import validar_plan, select_features, get_plan_cost, show_options, plan


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
    from gym_membership import Buyer

    b = Buyer([])

    # Total just above 200 -> discount 20
    discounted_250 = b.apply_special_discount(250)
    assert discounted_250 == 230
    assert b.special_discount_amount == 20.0

    # Total above 400 -> discount 50
    discounted_450 = b.apply_special_discount(450)
    assert discounted_450 == 400
    assert b.special_discount_amount == 50.0


def test_premium_features_surcharge():
    """Test 15% surcharge when premium features are included."""
    from gym_membership import Item, Buyer

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
