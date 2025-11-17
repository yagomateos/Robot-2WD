# 🤖 Robot 2WD ESP32 - Código Modularizado

## 📁 Estructura del Proyecto

```
esp32-robot-refactored/
├── src/
│   ├── main.py                  # 🚀 Punto de entrada principal
│   ├── config.py                # ⚙️ Configuración centralizada
│   ├── motor_controller.py      # 🔧 Control de motores L298N
│   ├── sensor_handler.py        # 📡 Sensor ultrasónico HC-SR04
│   ├── logger.py                # 📋 Sistema de logging
│   ├── security_manager.py      # 🔒 Gestión de seguridad y Safe Mode
│   ├── auto_mode.py             # 🤖 Modo automático con evasión
│   ├── wifi_manager.py          # 🌐 Gestión de conexión WiFi
│   └── http_server.py           # 🌐 Servidor HTTP con API REST
└── README.md
```

## 🎯 Ventajas de la Modularización

### ✅ Antes (Código Monolítico)
- ❌ Todo en un archivo de 300+ líneas
- ❌ Difícil de mantener y debuggear
- ❌ Imposible hacer tests unitarios
- ❌ Configuración hardcodeada
- ❌ Mezcla de responsabilidades

### ✅ Ahora (Código Modular)
- ✅ Cada módulo tiene una responsabilidad clara
- ✅ Fácil de mantener y extender
- ✅ Preparado para tests unitarios
- ✅ Configuración centralizada en `config.py`
- ✅ Reutilizable y escalable

## 📦 Módulos

### 1️⃣ `config.py`
**Configuración centralizada del sistema**
- Pines de hardware
- Credenciales WiFi
- Parámetros del servidor
- Configuración de seguridad
- Parámetros del modo automático

```python
# Cambiar credenciales WiFi aquí
WIFI_SSID = "Tu_WiFi"
WIFI_PASSWORD = "Tu_Password"
```

### 2️⃣ `motor_controller.py`
**Control de motores DC mediante L298N**

```python
motors = MotorController()
motors.forward()      # Adelante
motors.backward()     # Atrás
motors.turn_left()    # Izquierda
motors.turn_right()   # Derecha
motors.stop()         # Detener

# O ejecutar comando directo
motors.execute_command('F')  # F, B, L, R, S
```

### 3️⃣ `sensor_handler.py`
**Manejo del sensor ultrasónico HC-SR04**

```python
sensor = UltrasonicSensor()
distance = sensor.measure_distance_cm()  # Obtener distancia
has_obstacle = sensor.is_obstacle_detected(threshold_cm=20)
```

### 4️⃣ `logger.py`
**Sistema de logging con timestamps**

```python
logger = Logger()
logger.add("Mensaje de log")
uptime = logger.get_uptime_seconds()
all_logs = logger.get_all()
```

### 5️⃣ `security_manager.py`
**Gestión de seguridad y Safe Mode**

```python
security = SecurityManager(logger)
security.add_error(ip, "error_message")
if security.is_safe_mode_active():
    # Bloquear movimiento
security.deactivate_safe_mode()
```

### 6️⃣ `auto_mode.py`
**Modo automático con navegación autónoma**

```python
auto = AutoMode(motors, sensor, logger)
auto.enable()   # Activar
auto.disable()  # Desactivar

# En el loop principal
while True:
    auto.step()  # Ejecuta lógica de navegación
```

### 7️⃣ `wifi_manager.py`
**Gestión de conexión WiFi**

```python
wifi = WiFiManager(logger)
ip = wifi.connect()  # Conectar y obtener IP
if wifi.is_connected():
    print("IP:", wifi.get_ip())
```

### 8️⃣ `http_server.py`
**Servidor HTTP con API REST**

```python
server = HTTPServer(ip, motors, sensor, logger, security, auto_mode)
server.start()  # Inicia el servidor y loop principal
```

### 9️⃣ `main.py`
**Punto de entrada que orquesta todo**

```python
# Inicializa todos los módulos y arranca el sistema
main()
```

## 🚀 Instalación

### 1. Subir archivos al ESP32

Usando **Thonny IDE**:
1. Conecta el ESP32
2. Abre Thonny y conecta al dispositivo
3. Sube TODOS los archivos de `src/` al ESP32
4. Renombra `main.py` a `boot.py` o configura para arranque automático

Usando **ampy**:
```bash
# Instalar ampy
pip install adafruit-ampy

# Subir todos los archivos
ampy --port /dev/ttyUSB0 put src/config.py
ampy --port /dev/ttyUSB0 put src/motor_controller.py
ampy --port /dev/ttyUSB0 put src/sensor_handler.py
ampy --port /dev/ttyUSB0 put src/logger.py
ampy --port /dev/ttyUSB0 put src/security_manager.py
ampy --port /dev/ttyUSB0 put src/auto_mode.py
ampy --port /dev/ttyUSB0 put src/wifi_manager.py
ampy --port /dev/ttyUSB0 put src/http_server.py
ampy --port /dev/ttyUSB0 put src/main.py
```

### 2. Configurar credenciales WiFi

Edita `config.py`:
```python
WIFI_SSID = "TU_WIFI"
WIFI_PASSWORD = "TU_PASSWORD"
```

### 3. Reiniciar ESP32

El robot arrancará automáticamente y:
1. ✅ Inicializará hardware
2. ✅ Conectará a WiFi
3. ✅ Iniciará servidor HTTP
4. ✅ Mostrará la IP en el monitor serial

## 🎨 Personalización

### Cambiar distancia mínima de evasión
```python
# En config.py
AUTO_MIN_DISTANCE = 30  # Cambiar de 20 a 30 cm
```

### Ajustar tiempos de maniobra
```python
# En config.py
AUTO_BACKWARD_TIME = 600  # Retroceder más tiempo
AUTO_TURN_TIME = 300      # Girar menos tiempo
```

### Cambiar pines de hardware
```python
# En config.py
MOTOR_LEFT_PIN1 = 26  # Cambiar según tu conexión
ULTRASONIC_TRIG = 5
```

## 🧪 Testing (Futuro)

La estructura modular permite tests unitarios:

```python
# test_motor_controller.py
def test_forward():
    motors = MotorController()
    motors.forward()
    assert motors.in1.value() == 1
    assert motors.in2.value() == 0

# test_sensor.py
def test_distance_measurement():
    sensor = UltrasonicSensor()
    distance = sensor.measure_distance_cm()
    assert distance > 0 or distance == -1
```

## 📊 Comparación de Tamaño

| Archivo | Líneas | Responsabilidad |
|---------|--------|-----------------|
| `config.py` | ~60 | Configuración |
| `motor_controller.py` | ~80 | Control motores |
| `sensor_handler.py` | ~60 | Sensores |
| `logger.py` | ~70 | Logging |
| `security_manager.py` | ~90 | Seguridad |
| `auto_mode.py` | ~100 | Navegación auto |
| `wifi_manager.py` | ~110 | WiFi |
| `http_server.py` | ~330 | API REST |
| `main.py` | ~70 | Orquestación |
| **TOTAL** | **~970** | **Modular** |

**Código original**: 1 archivo de ~330 líneas mezclando todo

## 🔄 Migración desde el código anterior

1. ✅ **Funcionalidad idéntica**: Todos los endpoints funcionan igual
2. ✅ **Compatible con el dashboard**: No requiere cambios en el frontend
3. ✅ **Misma API REST**: Endpoints y respuestas idénticas
4. ✅ **Mejor mantenibilidad**: Código más limpio y organizado

## 🎓 Próximos Pasos

1. **Añadir PWM para velocidad variable**
   - Modificar `motor_controller.py` con `PWM`
   
2. **Implementar WebSockets**
   - Nuevo módulo `websocket_server.py`
   
3. **Tests unitarios**
   - Carpeta `tests/` con pytest
   
4. **Configuración externa**
   - Leer `config.json` en lugar de hardcodear

## 📝 Licencia

Código abierto - Libre de usar y modificar

## 👨‍💻 Autor

Desarrollado con ❤️ por Yago Mateos
