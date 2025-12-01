"""Pruebas para el `config_manager` y la carga opcional en `models.py`."""
import importlib
import models
import config_manager


def test_config_manager_loads_config():
    """Verifica que `config_manager.load_config()` devuelve un dict válido."""
    cfg = config_manager.load_config()
    assert isinstance(cfg, dict)
    # Debe contener claves principales
    assert 'plan' in cfg
    assert 'additional_features' in cfg


def test_models_apply_config():
    """Verifica que `models.Item` carga la configuración desde el archivo.

    Esto recarga el módulo `models` para forzar la lectura del config.
    """
    # Asegurar que load_config devuelve algo (ya hay config/config.json de ejemplo)
    cfg = config_manager.load_config()
    assert cfg is not None

    # Recargar models para que re-evalúe la carga de config
    importlib.reload(models)

    # Ahora Item.plan debería corresponder al plan definido en el config
    assert isinstance(models.Item.plan, dict)
    assert set(cfg['plan'].keys()) == set(models.Item.plan.keys())
