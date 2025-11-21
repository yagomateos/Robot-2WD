# Tests para ESP32 Robot

Este directorio contiene tests unitarios para el proyecto ESP32 Robot 2WD.

## Instalación de Dependencias

Instala las dependencias de testing:

```bash
cd /Users/yagomateos/Proyectos/Robot-2WD/esp32-robot-refactored
pip install -r requirements-test.txt
```

O si usas un entorno virtual:

```bash
cd /Users/yagomateos/Proyectos/Robot-2WD/esp32-robot-refactored
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements-test.txt
```

## Ejecutar los Tests

**Ejecutar todos los tests:**
```bash
python -m pytest tests/ -v
```

**Ejecutar tests con cobertura:**
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

**Ejecutar un archivo de tests específico:**
```bash
python -m pytest tests/test_motor_controller.py -v
```

**Ejecutar un test específico:**
```bash
python -m pytest tests/test_motor_controller.py::test_motor_forward -v
```

## Estructura de Tests

```
tests/
├── __init__.py                  # Paquete de tests
├── conftest.py                  # Configuración de pytest y mocks
├── test_motor_controller.py     # Tests para motor_controller.py
├── test_sensor_handler.py       # Tests para sensor_handler.py
├── test_logger.py               # Tests para logger.py
├── test_security_manager.py     # Tests para security_manager.py
├── test_auto_mode.py            # Tests para auto_mode.py
└── test_http_server.py          # Tests para http_server.py
```

## Mocks de Hardware

Los tests utilizan mocks para simular el hardware de MicroPython:

- **`machine.Pin`**: Simulación de pines GPIO
- **`machine.time_pulse_us`**: Simulación de medición de pulsos del sensor
- **`machine.reset`**: Simulación de reinicio del ESP32
- **`socket`**: Simulación de sockets de red
- **`time`**: Simulación de funciones de tiempo de MicroPython

Estos mocks están definidos en `conftest.py` y se aplican automáticamente a todos los tests.

## Cobertura de Tests

Los tests cubren:

### ✅ motor_controller.py (11 tests)
- Inicialización de pines
- Movimientos: forward, backward, turn_left, turn_right, stop
- Ejecución de comandos válidos e inválidos
- Validación de tipos de entrada

### ✅ sensor_handler.py (13 tests)
- Medición de distancia en diferentes rangos
- Manejo de timeouts
- Valores fuera de rango
- Errores de hardware
- Detección de obstáculos

### ✅ logger.py (8 tests)
- Agregar logs con timestamps
- Buffer circular
- Formato JSON
- Cálculo de uptime
- Limpieza de logs

### ✅ security_manager.py (8 tests)
- Conteo de errores
- Activación/desactivación de Safe Mode
- Reset de contadores
- Formato JSON

### ✅ auto_mode.py (9 tests)
- Activación/desactivación
- Navegación sin obstáculos
- Maniobra de evasión
- Control de frecuencia
- Ajuste de distancia mínima

### ✅ http_server.py (10 tests)
- Parseo de paths HTTP
- Extracción de query parameters
- Escape de strings para JSON
- Rate limiting por IP
- Validación de paths

## Notas Importantes

1. **No se requiere hardware**: Los tests se ejecutan completamente en Python estándar usando mocks.

2. **Configuración**: Los tests usan `config_template.py` como base de configuración.

3. **Aislamiento**: Cada test es independiente y no afecta a otros tests.

4. **Cobertura**: Se recomienda mantener una cobertura de código superior al 80%.

## Solución de Problemas

**Error de importación de módulos:**
```bash
# Asegúrate de ejecutar pytest desde el directorio raíz del proyecto
cd /Users/yagomateos/Proyectos/Robot-2WD/esp32-robot-refactored
python -m pytest tests/
```

**Tests fallan por dependencias:**
```bash
# Reinstala las dependencias
pip install -r requirements-test.txt
```
