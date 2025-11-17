# ESP32 2WD Robot - Sistema de Control Inalámbrico

Proyecto de robot autónomo de dos ruedas (2WD) controlado por ESP32 con servidor HTTP embebido, telemetría en tiempo real y modo de navegación autónoma con evasión de obstáculos.

## Tabla de Contenidos

- [Características](#características)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Especificaciones de Hardware](#especificaciones-de-hardware)
- [Configuración de Pines](#configuración-de-pines)
- [API REST](#api-rest)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Sistema de Seguridad](#sistema-de-seguridad)
- [Troubleshooting](#troubleshooting)

## Características

### Control de Movimiento
- **Control manual bidireccional**: Adelante, atrás, izquierda, derecha y parada
- **Modo autónomo**: Navegación automática con evasión inteligente de obstáculos
- **Sensor de proximidad**: Detección ultrasónica de obstáculos hasta 400cm

### Conectividad
- **WiFi STA Mode**: Conexión a hotspot móvil para control remoto
- **API REST HTTP**: Endpoints JSON para control y telemetría
- **CORS habilitado**: Acceso desde cualquier origen para dashboard web
- **Socket no bloqueante**: Servidor HTTP con timeout de 0.1s para mantener responsividad

### Telemetría y Monitoreo
- **Métricas en tiempo real**: Distancia, estado de obstáculos, uptime del sistema
- **Sistema de logs**: Buffer circular de 50 entradas con timestamps
- **Telemetría de sensores**: Actualización continua de distancia en centímetros

### Seguridad
- **Safe Mode automático**: Activación tras 5 errores consecutivos
- **Logging de errores**: Registro de IP de origen y tipo de error
- **Rate limiting natural**: Protección contra comandos excesivos
- **Validación de parámetros**: Sanitización de entradas HTTP

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE (Dashboard)                  │
│              React + Vite (Puerto 5173)                 │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/JSON (WiFi 2.4GHz)
                     │
┌────────────────────▼────────────────────────────────────┐
│                 ESP32 (MicroPython)                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Servidor HTTP (Puerto 80)                   │  │
│  │  - Router de endpoints                           │  │
│  │  - Parseo de query params                        │  │
│  │  - Respuestas JSON con CORS                      │  │
│  └─────────┬────────────────────────────────────────┘  │
│            │                                            │
│  ┌─────────▼──────────┐  ┌──────────────────────────┐  │
│  │  Sistema de Logs   │  │  Sistema de Seguridad    │  │
│  │  - Buffer circular │  │  - Contador de fallos    │  │
│  │  - Timestamps      │  │  - Safe mode             │  │
│  └────────────────────┘  └──────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Modo Automático                       │  │
│  │  - Loop no bloqueante (200ms)                    │  │
│  │  - Lógica de evasión: Stop → Back → Left        │  │
│  │  - Distancia mínima configurable (20cm)         │  │
│  └─────────┬────────────────────────────────────────┘  │
│            │                                            │
│  ┌─────────▼──────────┐  ┌──────────────────────────┐  │
│  │  Control Motores   │  │  Sensor Ultrasónico      │  │
│  │  (Driver L298N)    │  │  (HC-SR04)               │  │
│  │  - IN1-IN4 (GPIO)  │  │  - TRIG: GPIO5           │  │
│  │  - 4 modos base    │  │  - ECHO: GPIO18          │  │
│  └────────┬───────────┘  └────────┬─────────────────┘  │
└───────────┼──────────────────────┼─────────────────────┘
            │                      │
      ┌─────▼──────┐         ┌────▼─────┐
      │  Motor L   │         │ HC-SR04  │
      │  Motor R   │         │ Sensor   │
      └────────────┘         └──────────┘
```

## Especificaciones de Hardware

### Microcontrolador
- **Modelo**: ESP32 DevKit
- **Firmware**: MicroPython v1.20+ (compatible)
- **Frecuencia**: 240 MHz (dual-core)
- **Flash**: 4MB (mínimo)
- **RAM**: 520KB SRAM

### Motor Driver
- **Modelo**: L298N Dual H-Bridge
- **Voltaje de entrada**: 5-35V DC
- **Corriente por canal**: 2A (máximo)
- **Lógica**: TTL 5V compatible con ESP32 3.3V

### Sensor Ultrasónico
- **Modelo**: HC-SR04
- **Rango de medición**: 2cm - 400cm
- **Precisión**: ±3mm
- **Ángulo de medición**: 15°
- **Frecuencia ultrasónica**: 40kHz

### Conectividad
- **WiFi**: 802.11 b/g/n (2.4 GHz únicamente)
- **Antena**: Integrada PCB
- **Potencia de transmisión**: 20.5 dBm (máximo)

## Configuración de Pines

### Control de Motores (L298N)

| Pin ESP32 | Función      | Driver L298N | Motor  |
|-----------|--------------|--------------|--------|
| GPIO 26   | IN1          | IN1          | Izq+   |
| GPIO 27   | IN2          | IN2          | Izq-   |
| GPIO 14   | IN3          | IN3          | Der+   |
| GPIO 12   | IN4          | IN4          | Der-   |

### Sensor Ultrasónico (HC-SR04)

| Pin ESP32 | Función      | HC-SR04      |
|-----------|--------------|--------------|
| GPIO 5    | TRIGGER      | TRIG         |
| GPIO 18   | ECHO         | ECHO         |
| GND       | Tierra       | GND          |
| 5V        | Alimentación | VCC          |

### Lógica de Control de Motores

| Comando   | IN1 | IN2 | IN3 | IN4 | Resultado       |
|-----------|-----|-----|-----|-----|-----------------|
| Forward   | 1   | 0   | 1   | 0   | Ambos adelante  |
| Backward  | 0   | 1   | 0   | 1   | Ambos atrás     |
| Left      | 0   | 1   | 1   | 0   | Giro izquierda  |
| Right     | 1   | 0   | 0   | 1   | Giro derecha    |
| Stop      | 0   | 0   | 0   | 0   | Motores parados |

## API REST

### Base URL
```
http://<ESP32_IP>
```

### Endpoints

#### `GET /`
Verificación de disponibilidad del servidor.

**Response:**
```
ESP32 Robot API OK
```

---

#### `GET /status`
Estado general del sistema.

**Response:**
```json
{
  "uptime": 3600,
  "wifi": "ok",
  "ip": "192.168.43.200"
}
```

**Campos:**
- `uptime` (int): Tiempo en segundos desde el arranque
- `wifi` (string): Estado de conexión WiFi
- `ip` (string): Dirección IP asignada

---

#### `GET /telemetry`
Telemetría de sensores y modo automático.

**Response:**
```json
{
  "uptime": 3600,
  "distance_cm": 15.3,
  "obstacle": true,
  "auto_enabled": false
}
```

**Campos:**
- `uptime` (int): Segundos desde arranque
- `distance_cm` (float): Distancia medida en centímetros (-1 si error)
- `obstacle` (bool): true si hay obstáculo dentro de min_distance
- `auto_enabled` (bool): Estado del modo automático

---

#### `GET /move?dir=<D>`
Control de movimiento del robot.

**Query Parameters:**
- `dir` (required): Dirección de movimiento
  - `F` - Forward (adelante)
  - `B` - Backward (atrás)
  - `L` - Left (izquierda)
  - `R` - Right (derecha)
  - `S` - Stop (parar)

**Response exitosa:**
```json
{
  "ok": true,
  "dir": "F"
}
```

**Errores:**
```json
// Missing parameter
{
  "error": "missing dir"
}

// Invalid direction
{
  "error": "invalid dir"
}

// Safe mode activo
{
  "error": "safe_mode"
}
```

**Ejemplo:**
```bash
curl "http://192.168.43.200/move?dir=F"
```

---

#### `GET /auto?enabled=<VALUE>`
Control del modo automático.

**Query Parameters:**
- `enabled` (required): Estado del modo automático
  - Valores true: `1`, `true`, `yes`, `on`
  - Valores false: `0`, `false`, `no`, `off`

**Response:**
```json
{
  "auto_enabled": true
}
```

**Ejemplo:**
```bash
# Activar modo automático
curl "http://192.168.43.200/auto?enabled=true"

# Desactivar modo automático
curl "http://192.168.43.200/auto?enabled=false"
```

---

#### `GET /logs`
Historial de eventos del sistema.

**Response:**
```json
{
  "logs": [
    "[0s] SERVER INICIADO",
    "[15s] MOVE F",
    "[20s] MOVE S",
    "[45s] AUTO ON",
    "[120s] ERROR de 192.168.43.100 -> invalid_dir:X"
  ]
}
```

**Características:**
- Buffer circular de 50 entradas
- Timestamps en segundos desde arranque
- Incluye comandos, errores y eventos de sistema

---

#### `GET /security`
Estado del sistema de seguridad.

**Response:**
```json
{
  "fail_count": 3,
  "safe_mode": false,
  "last_error": "invalid_dir:X",
  "last_ip": "192.168.43.100"
}
```

**Campos:**
- `fail_count` (int): Contador de errores acumulados
- `safe_mode` (bool): true si safe mode está activo (≥5 errores)
- `last_error` (string): Descripción del último error
- `last_ip` (string): IP que causó el último error

---

#### `GET /clear`
Resetear sistema de seguridad y safe mode.

**Response:**
```json
{
  "ok": true
}
```

**Efecto:**
- Resetea `fail_count` a 0
- Desactiva `safe_mode`
- Limpia `last_error` y `last_ip`

---

### Códigos de Estado HTTP

| Código | Significado              | Cuándo ocurre                    |
|--------|--------------------------|----------------------------------|
| 200    | OK                       | Petición exitosa                 |
| 400    | Bad Request              | Parámetros faltantes o inválidos |
| 403    | Forbidden                | Safe mode activo                 |
| 404    | Not Found                | Ruta no existe                   |

### Headers CORS

Todos los endpoints incluyen estos headers:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: *
```

## Instalación

### Requisitos Previos

1. **Hardware**
   - ESP32 DevKit
   - Cable USB-Micro USB
   - Robot 2WD con motores DC
   - Driver L298N
   - Sensor HC-SR04
   - Cables Dupont (M-M, M-F)
   - Batería/fuente de alimentación

2. **Software**
   - Python 3.7+ (para esptool)
   - Thonny IDE / uPyCraft / ampy
   - Firmware MicroPython para ESP32

### Paso 1: Flashear MicroPython

```bash
# Instalar esptool
pip install esptool

# Borrar flash del ESP32
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash

# Descargar firmware MicroPython
wget https://micropython.org/resources/firmware/ESP32_GENERIC-20240602-v1.23.0.bin

# Flashear firmware (ajustar puerto según tu sistema)
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20240602-v1.23.0.bin
```

**Ajustar puerto según sistema operativo:**
- Linux: `/dev/ttyUSB0` o `/dev/ttyACM0`
- macOS: `/dev/cu.usbserial-*` o `/dev/cu.SLAB_USBtoUART`
- Windows: `COM3`, `COM4`, etc.

### Paso 2: Subir Código al ESP32

**Opción A: Usando Thonny (Recomendado)**

1. Abrir Thonny IDE
2. Ir a: **Herramientas → Opciones → Intérprete**
3. Seleccionar: **MicroPython (ESP32)**
4. Elegir puerto serial correcto
5. Abrir `main_2wd.py`
6. Guardar como `main.py` en el ESP32 (no en computadora)

**Opción B: Usando ampy**

```bash
# Instalar ampy
pip install adafruit-ampy

# Subir archivo (ajustar puerto)
ampy --port /dev/ttyUSB0 put main_2wd.py /main.py

# Verificar que se subió
ampy --port /dev/ttyUSB0 ls
```

### Paso 3: Conexiones de Hardware

**Diagrama de Conexiones:**

```
ESP32                L298N               Motores
──────               ──────              ───────
GPIO26 ────────────→ IN1
GPIO27 ────────────→ IN2                Motor Izq
GPIO14 ────────────→ IN3
GPIO12 ────────────→ IN4                Motor Der

                     OUT1 ─────────────→ Motor Izq +
                     OUT2 ─────────────→ Motor Izq -
                     OUT3 ─────────────→ Motor Der +
                     OUT4 ─────────────→ Motor Der -

                     12V ──────────────→ Batería +
                     GND ──────────────→ Batería -

ESP32                HC-SR04
──────               ───────
GPIO5  ────────────→ TRIG
GPIO18 ────────────→ ECHO
5V     ────────────→ VCC
GND    ────────────→ GND
```

**Notas importantes:**
- **No conectar motores directamente al ESP32** (usar L298N)
- Tierra común entre ESP32 y L298N es **obligatoria**
- HC-SR04 necesita **5V**, no 3.3V
- Alimentación de motores separada de ESP32

## Configuración

### Configurar Credenciales WiFi

Editar en `main_2wd.py` (líneas 135-136):

```python
def iniciar_wifi_cliente():
    # ...
    ssid = "TU_HOTSPOT_SSID"      # ← Cambiar aquí
    pwd = "TU_PASSWORD"            # ← Cambiar aquí
    # ...
```

**Requisitos del hotspot:**
- Banda de frecuencia: **2.4 GHz** (ESP32 no soporta 5 GHz)
- Seguridad: WPA2 o WPA3
- DHCP habilitado

### Configurar Parámetros del Modo Automático

Editar en `main_2wd.py` (líneas 72-75):

```python
auto_mode = {
    "enabled": False,       # Estado inicial
    "min_distance": 20      # Distancia mínima en cm (ajustar según robot)
}
```

**Recomendaciones por velocidad del robot:**
- Robot lento (0.2 m/s): 15-20 cm
- Robot medio (0.5 m/s): 25-35 cm
- Robot rápido (1+ m/s): 40-50 cm

### Configurar Sistema de Seguridad

Editar en `main_2wd.py` (línea 91):

```python
if security["fail_count"] >= 5 and not security["safe_mode"]:
    # Cambiar '5' por el umbral deseado
```

## Uso

### Inicio del Sistema

1. **Encender el robot** (conectar batería)
2. **Reiniciar ESP32** (botón EN o desconectar/reconectar USB)
3. **Verificar conexión** mediante monitor serial:

```
Conectando a: TU_SSID
Intento 1 -> conectado: False
Intento 2 -> conectado: False
Intento 3 -> conectado: True
Conectado con IP: 192.168.43.200
API en: http://192.168.43.200
```

4. **Conectar dispositivo de control** a la misma red WiFi
5. **Probar API** con curl o navegador:

```bash
curl http://192.168.43.200/status
```

### Modo Manual

Control mediante peticiones HTTP a `/move`:

```bash
# Adelante
curl "http://192.168.43.200/move?dir=F"

# Atrás
curl "http://192.168.43.200/move?dir=B"

# Izquierda
curl "http://192.168.43.200/move?dir=L"

# Derecha
curl "http://192.168.43.200/move?dir=R"

# Parar
curl "http://192.168.43.200/move?dir=S"
```

### Modo Automático

Activar navegación autónoma:

```bash
# Activar
curl "http://192.168.43.200/auto?enabled=true"

# Desactivar
curl "http://192.168.43.200/auto?enabled=false"
```

**Comportamiento del modo automático:**

1. **Loop continuo** cada 200ms
2. **Lectura de sensor** ultrasónico
3. **Si distancia < min_distance:**
   - Parar (200ms)
   - Retroceder (400ms)
   - Girar izquierda (400ms)
   - Continuar adelante
4. **Si distancia ≥ min_distance:**
   - Continuar adelante

### Dashboard Web

El dashboard React proporciona control visual del robot.

**Instalación del dashboard:**

```bash
cd robot-dashboard

# Instalar dependencias
npm install

# Modo desarrollo
npm run dev
```

**Configurar IP del ESP32:**

Editar archivo de configuración en `robot-dashboard/src/config.js`:

```javascript
export const ROBOT_IP = "192.168.43.200"; // IP del ESP32
```

**Acceder al dashboard:**

```
http://localhost:5173
```

### Monitoreo y Debugging

**Ver logs en tiempo real:**

```bash
# Con jq para formato bonito
curl -s http://192.168.43.200/logs | jq

# Sin jq
curl http://192.168.43.200/logs
```

**Ver telemetría:**

```bash
# Monitoreo continuo con watch (Linux/macOS)
watch -n 1 'curl -s http://192.168.43.200/telemetry | jq'

# Monitoreo manual
while true; do curl -s http://192.168.43.200/telemetry | jq; sleep 1; done
```

**Estado de seguridad:**

```bash
curl -s http://192.168.43.200/security | jq
```

## Sistema de Seguridad

### Safe Mode

Protección automática contra errores repetidos.

**Activación:**
- Se activa tras **5 errores** consecutivos
- Bloquea endpoint `/move` (retorna `403 Forbidden`)
- Otros endpoints permanecen accesibles

**Causas de errores:**
- Parámetros faltantes en `/move`
- Direcciones inválidas (no F/B/L/R/S)
- Rutas no existentes (404)

**Desactivación:**

```bash
curl http://192.168.43.200/clear
```

**Verificar estado:**

```bash
curl http://192.168.43.200/security
```

### Logging de Eventos

Sistema de logs circular con 50 entradas máximas.

**Tipos de eventos registrados:**
- Inicio del servidor
- Comandos de movimiento
- Cambios de modo automático
- Errores de validación
- Activación/reset de safe mode

**Formato de log:**
```
[<uptime>s] <mensaje>
```

**Ejemplo:**
```json
{
  "logs": [
    "[0s] SERVER INICIADO",
    "[5s] MOVE F",
    "[8s] MOVE S",
    "[15s] AUTO ON",
    "[45s] ERROR de 192.168.43.100 -> invalid_dir:X",
    "[50s] SAFE MODE ACTIVADO",
    "[60s] SAFE MODE RESET"
  ]
}
```

## Troubleshooting

### ESP32 no se conecta a WiFi

**Síntomas:**
```
Conectando a: TU_SSID
Intento 1 -> conectado: False
...
Intento 40 -> conectado: False
NO conectado. Revisa el hotspot y 2.4GHz.
```

**Soluciones:**

1. **Verificar banda de frecuencia**
   - ESP32 solo soporta **2.4 GHz**
   - Desactivar 5 GHz en hotspot o forzar 2.4 GHz

2. **Verificar credenciales**
   - SSID correcto (sensible a mayúsculas)
   - Contraseña correcta

3. **Probar con hotspot móvil**
   - Crear hotspot desde smartphone
   - Nombre simple sin caracteres especiales

4. **Verificar antena**
   - ESP32 DevKit tiene antena PCB integrada
   - Mantener alejado de metal

### Sensor ultrasónico retorna -1.0

**Causas:**

1. **Timeout del sensor**
   - Objeto fuera de rango (>400cm)
   - Superficie absorbente de sonido (tela, espuma)

2. **Conexiones incorrectas**
   - Verificar TRIG → GPIO5
   - Verificar ECHO → GPIO18
   - Verificar VCC → 5V (no 3.3V)
   - Verificar GND común

3. **Interferencias**
   - Múltiples sensores ultrasónicos cercanos
   - Ruido eléctrico de motores

**Solución:**
```python
# En línea 48-49, aumentar timeout
duracion = time_pulse_us(ECHO, 1, 50000)  # De 30000 a 50000
```

### Motores no responden

**Diagnóstico:**

1. **Verificar alimentación**
   - L298N con LED encendido
   - Batería con carga suficiente (>6V)

2. **Verificar conexiones**
   ```bash
   # Test manual desde REPL de MicroPython
   from machine import Pin
   IN1 = Pin(26, Pin.OUT)
   IN1.value(1)  # Debe activar motor
   IN1.value(0)
   ```

3. **Verificar secuencia de pines**
   - IN1/IN2 controlan motor izquierdo
   - IN3/IN4 controlan motor derecho
   - Si gira al revés, invertir cables del motor

### Safe Mode se activa constantemente

**Causas:**

1. **Cliente enviando peticiones incorrectas**
   - Revisar logs: `curl http://IP/logs`
   - Identificar IP problemática en `/security`

2. **Dashboard con IP incorrecta**
   - Actualizar IP en configuración del dashboard
   - Verificar CORS habilitado

**Reset:**
```bash
curl http://IP/clear
```

### Dashboard no conecta con ESP32

**Checklist:**

1. **Mismo WiFi**
   - Dashboard y ESP32 en misma red

2. **IP correcta**
   - Verificar IP actual: `curl http://IP/status`
   - Actualizar en dashboard si cambió

3. **Firewall**
   - Desactivar temporalmente
   - Permitir puerto 80

4. **CORS**
   - Verificar headers en respuestas
   - Debería incluir `Access-Control-Allow-Origin: *`

### Modo automático errático

**Comportamiento esperado:**
- Medición cada 200ms
- Si obstáculo: Stop → Back (400ms) → Left (400ms)
- Si libre: Forward continuo

**Ajustes:**

1. **Distancia mínima muy baja**
   ```python
   auto_mode["min_distance"] = 30  # Aumentar de 20 a 30
   ```

2. **Velocidad muy alta**
   - Reducir voltaje de motores
   - Aumentar tiempos de maniobra:
   ```python
   time.sleep_ms(600)  # Línea 115: de 400 a 600
   ```

3. **Sensor mal calibrado**
   - Montar sensor perpendicular al suelo
   - Alejar de superficies metálicas

### Latencia alta en API

**Causas:**

1. **WiFi débil**
   - Acercar ESP32 al hotspot
   - Reducir interferencias

2. **Modo automático activo**
   - Tiene prioridad y puede retrasar respuestas
   - Desactivar para control manual fluido

**Optimización:**
```python
# Línea 104: Reducir frecuencia de auto mode
if time.ticks_diff(ahora, last_auto_check) < 500:  # De 200 a 500
```

### Logs saturados

**Síntoma:** Logs llenándose muy rápido

**Solución:**
```python
# Línea 82: Aumentar tamaño de buffer
if len(logs) > 100:  # De 50 a 100
```

## Especificaciones Técnicas

### Performance

| Métrica                    | Valor              |
|----------------------------|--------------------|
| Latencia API (promedio)    | 50-100ms           |
| Frecuencia modo auto       | 5 Hz (200ms)       |
| Frecuencia sensor          | Variable (on-demand)|
| Timeout socket             | 100ms              |
| Buffer de logs             | 50 entradas        |
| Max conexiones concurrentes| 1                  |

### Consumo Energético

| Componente     | Consumo        |
|----------------|----------------|
| ESP32 (WiFi)   | ~200mA @ 3.3V  |
| HC-SR04        | ~15mA @ 5V     |
| Motores (2x)   | 200-500mA @ 6V |
| **Total**      | ~400-700mA     |

### Memoria (ESP32)

| Recurso          | Uso estimado   |
|------------------|----------------|
| Código Python    | ~10 KB         |
| Variables globales| ~2 KB         |
| Stack servidor   | ~4 KB          |
| Buffer logs      | ~1 KB          |
| **Total RAM**    | ~17 KB / 520KB |

## Licencia

Este proyecto es de código abierto. Úsalo, modifícalo y compártelo libremente.

## Soporte

Para problemas, mejoras o consultas:
- Revisar sección [Troubleshooting](#troubleshooting)
- Verificar conexiones de hardware
- Consultar logs del sistema: `GET /logs`

---

**Documentación técnica versión 1.0**
*Última actualización: 2025*
