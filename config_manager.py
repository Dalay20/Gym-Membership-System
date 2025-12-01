"""Carga opcional de configuración desde `config/config.json`.

La carga es opcional: si no existe el archivo o hay errores,
se devuelve None y el sistema usa la configuración embebida.
"""
import json
import os
from typing import Optional, Dict


def load_config() -> Optional[Dict]:
    """Carga y devuelve la configuración como dict si existe.

    Busca `config/config.json` en la raíz del proyecto. Si el archivo no existe
    o no es válido, devuelve None.
    """
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return None
        return data
    except (json.JSONDecodeError, OSError, ValueError):
        return None


if __name__ == "__main__":
    cfg = load_config()
    print("Loaded config:" if cfg else "No config found")
