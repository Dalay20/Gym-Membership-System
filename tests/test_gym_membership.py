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
