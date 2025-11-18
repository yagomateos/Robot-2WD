# 🔧 Guía de Configuración Segura - ESP32 Robot

## ⚠️ IMPORTANTE: Configuración de Credenciales

Este proyecto requiere configuración local de credenciales WiFi que **NO deben ser compartidas** en el repositorio Git.

## 📋 Pasos de Configuración

### 1. Crear archivo de configuración local

```bash
cd esp32-robot-refactored/src
cp config_template.py config.py
```

### 2. Editar config.py con tus credenciales

Abre `config.py` y actualiza las siguientes líneas:

```python
# ANTES (template):
WIFI_SSID = "TU_WIFI_SSID"
WIFI_PASSWORD = "TU_WIFI_PASSWORD"

# DESPUÉS (tus valores reales):
WIFI_SSID = "MiRedWiFi"
WIFI_PASSWORD = "miPassword123"
```

### 3. Verificar que config.py NO esté en Git

El archivo `.gitignore` ya incluye esta regla:

```
esp32-robot-refactored/src/config.py
```

Verifica que el archivo no aparezca en `git status`:

```bash
git status
# config.py NO debe aparecer en la lista
```

## 🔒 Seguridad

### ✅ Buenas prácticas implementadas:

- ✅ `config.py` en `.gitignore`
- ✅ `config_template.py` como ejemplo sin credenciales reales
- ✅ Documentación de configuración segura

### ⚠️ ADVERTENCIA: Historial de Git

**IMPORTANTE:** Las credenciales WiFi estuvieron previamente en el repositorio Git. Aunque el archivo ha sido removido, **las credenciales siguen en el historial de commits**.

#### Riesgos:

- Si el repositorio es público, las credenciales están expuestas
- El historial de Git mantiene todas las versiones anteriores
- Cualquier persona con acceso al repositorio puede ver el historial

#### Soluciones recomendadas:

1. **Si el repo es privado y solo tú tienes acceso:** No hay problema inmediato
2. **Si el repo es público o compartido:** Debes limpiar el historial

### Limpiar credenciales del historial de Git

**Opción 1: Git filter-branch (destructivo)**

```bash
# ADVERTENCIA: Esto reescribe el historial de Git
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch esp32-robot-refactored/src/config.py" \
  --prune-empty --tag-name-filter cat -- --all

# Forzar push (solo si estás seguro)
git push origin --force --all
```

**Opción 2: BFG Repo-Cleaner (más rápido)**

```bash
# Instalar BFG
brew install bfg  # macOS
# o descargar de https://rtyley.github.io/bfg-repo-cleaner/

# Limpiar archivo
bfg --delete-files config.py

# Limpiar y forzar push
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push origin --force --all
```

**Opción 3: Crear repositorio nuevo (más seguro)**

Si las credenciales son críticas, considera crear un nuevo repositorio desde el estado actual.

## 🔐 Cambiar Credenciales WiFi Expuestas

Si tus credenciales WiFi estaban en un repositorio público:

1. **Cambiar la contraseña de tu red WiFi** desde el router
2. Actualizar `config.py` con la nueva contraseña
3. Limpiar el historial de Git (ver arriba)

## 📝 Configuración para Desarrollo

### Variables configurables en config.py:

```python
# Pines del hardware
MOTOR_LEFT_PIN1 = 26
MOTOR_LEFT_PIN2 = 27
MOTOR_RIGHT_PIN1 = 14
MOTOR_RIGHT_PIN2 = 12
ULTRASONIC_TRIG = 5
ULTRASONIC_ECHO = 18

# WiFi
WIFI_SSID = "TU_SSID"
WIFI_PASSWORD = "TU_PASSWORD"
WIFI_CONNECT_ATTEMPTS = 40

# Servidor HTTP
SERVER_PORT = 80
SOCKET_TIMEOUT = 0.1

# Seguridad
MAX_ERRORS_BEFORE_SAFE_MODE = 5
MAX_LOG_ENTRIES = 50

# Modo Automático
AUTO_MIN_DISTANCE = 20  # cm
AUTO_CHECK_INTERVAL = 200  # ms
AUTO_STOP_TIME = 200
AUTO_BACKWARD_TIME = 400
AUTO_TURN_TIME = 400

# Sensor
ULTRASONIC_TIMEOUT = 30000  # microsegundos
```

## 🚀 Despliegue al ESP32

Una vez configurado `config.py`, puedes subir los archivos al ESP32:

```bash
# Usando ampy (ejemplo)
ampy --port /dev/ttyUSB0 put esp32-robot-refactored/src/config.py

# O usando tu herramienta preferida (Thonny, mpremote, etc.)
```

## ❓ Solución de Problemas

### "ModuleNotFoundError: No module named 'config'"

- Verifica que `config.py` existe en `esp32-robot-refactored/src/`
- Verifica que lo hayas subido al ESP32

### "Config.py aparece en git status"

- Verifica que `.gitignore` contiene la línea correcta
- Ejecuta: `git rm --cached esp32-robot-refactored/src/config.py`

### "WiFi no conecta"

- Verifica SSID y contraseña en `config.py`
- Verifica que tu ESP32 soporte la banda de tu WiFi (2.4GHz, no 5GHz)

## 📚 Más Información

- [Documentación del proyecto](../README.md)
- [Arquitectura del sistema](./README.md)
- [Guía de contribución](../CONTRIBUTING.md)

---

**Última actualización:** 2025-01-18
