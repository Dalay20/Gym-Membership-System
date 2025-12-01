# Gym-Membership-System

Proyecto de ejemplo para la gestión de membresías de un gimnasio.

Instalación y pruebas
---------------------

Instalar dependencias y ejecutar la suite de tests:

```bash
pip install -r requirements.txt
PYTHONPATH=. pytest -q
```

Uso
---

- Ejecuta `python main.py` para iniciar el menú interactivo.

Configuración (opcional)
------------------------

El proyecto soporta una configuración externa opcional en `config/config.json`.
Si existe, el sistema cargará automáticamente los planes, características y mapas
de disponibilidad desde ese archivo al importar `models.py`. Si el archivo no
existe o es inválido, el proyecto seguirá usando la configuración embebida.

Estructura mínima de `config/config.json`:

```json
{
	"plan": { "Basic": { "benefits": "...", "cost": 25 } },
	"additional_features": { "Personal Training": 30 },
	"premium_features": { "Exclusive Gym Facilities": 100 },
	"plan_available": { "Premium": false },
	"feature_available": { "Personal Training": true }
}
```

Uso práctico:

- Para deshabilitar temporalmente un plan o feature, añade la clave correspondiente
	en `plan_available` o `feature_available` y pon su valor en `false`.
- No es necesario reiniciar nada adicional: la configuración se carga al importar
	`models.py` (por ejemplo al ejecutar `main.py` o al correr tests con
	`PYTHONPATH=.`).

Ejemplo de comandos:

```bash
# Ejecutar tests (incluir la raíz en PYTHONPATH para importaciones locales)
PYTHONPATH=. pytest -q

# Ejecutar el menú interactivo
python main.py

# Ejecutar el paylint
cd /workspaces/Gym-Membership-System && pylint *.py --disable=C0111,C0103
```
