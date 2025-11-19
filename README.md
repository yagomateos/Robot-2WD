# Robot 2WD - ESP32 con Control Web

Sistema completo de robot de dos ruedas controlado por ESP32 con servidor HTTP embebido y dashboard web React para control remoto en tiempo real.

![ESP32](https://img.shields.io/badge/ESP32-MicroPython-blue)
![React](https://img.shields.io/badge/React-18.2.0-61dafb)
![License](https://img.shields.io/badge/license-Open%20Source-green)

## Descripción del Proyecto

Proyecto de robótica IoT que combina hardware (ESP32 + robot 2WD) con software (API REST + Dashboard web) para crear un robot controlable de forma remota a través de WiFi. El robot incluye sensores ultrasónicos para navegación autónoma y evasión de obstáculos.

## Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  📱 DASHBOARD WEB (React + Vite)                            │
│     - Control de movimiento                                 │
│     - Visualización de telemetría                           │
│     - Monitoreo de logs                                     │
│     - Panel de seguridad                                    │
│                                                              │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ HTTP/JSON (WiFi 2.4GHz)
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                                                              │
│  🤖 ESP32 ROBOT (MicroPython)                               │
│     - API REST HTTP                                         │
│     - Control de motores (L298N)                            │
│     - Sensor ultrasónico (HC-SR04)                          │
│     - Modo automático con evasión de obstáculos             │
│     - Sistema de logs y seguridad                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Componentes del Proyecto

### 🔧 ESP32 Robot (`/esp32-robot-refactored`)

Backend del robot implementado en MicroPython con servidor HTTP embebido.

**Características principales:**
- API REST completa con 8 endpoints
- Control de motores DC mediante driver L298N
- Sensor ultrasónico HC-SR04 para detección de obstáculos
- Modo automático con navegación autónoma
- Sistema de seguridad con Safe Mode
- Logging de eventos con timestamps
- CORS habilitado para acceso web

**Hardware:**
- ESP32 DevKit
- Driver de motores L298N
- Sensor ultrasónico HC-SR04
- 2 motores DC con reductora
- Batería/fuente de alimentación

**[📖 Ver documentación completa del ESP32](./esp32-robot-refactored/README.md)**

---

### 💻 Dashboard Web (`/robot-dashboard`)

Interfaz web desarrollada en React para control y monitoreo del robot.

**Características principales:**
- Control direccional (adelante, atrás, izquierda, derecha)
- Visualización de telemetría en tiempo real
- Monitoreo de distancia y detección de obstáculos
- Panel de logs del sistema
- Alertas de seguridad y Safe Mode
- Control de modo automático

**Tecnologías:**
- React 18.2.0
- Vite 4.3.0
- JavaScript ES6+

**[📖 Ver documentación del Dashboard](./robot-dashboard/README.md)**

---

## Inicio Rápido

### 1️⃣ Configurar el ESP32

```bash
cd esp32-robot-refactored

# Seguir instrucciones de instalación en el README
# 1. Flashear MicroPython
# 2. Subir archivos del directorio src/ al ESP32
# 3. Configurar credenciales WiFi en config.py
# 4. Reiniciar ESP32
```

### 2️⃣ Configurar el Dashboard

```bash
cd robot-dashboard

# Instalar dependencias
npm install

# Configurar IP del ESP32 en src/config.js
# export const ROBOT_IP = "192.168.43.200"

# Iniciar servidor de desarrollo
npm run dev
```

### 3️⃣ Conectar y Probar

1. **Encender el robot** y esperar a que se conecte al WiFi
2. **Anotar la IP** del ESP32 (aparece en monitor serial)
3. **Conectar tu dispositivo** a la misma red WiFi
4. **Abrir el dashboard** en `http://localhost:5173`
5. **Probar movimiento** y telemetría

## API REST

El ESP32 expone una API REST completa en el puerto 80:

| Endpoint       | Método | Descripción                           |
|----------------|--------|---------------------------------------|
| `/`            | GET    | Verificación del servidor             |
| `/status`      | GET    | Estado general del sistema            |
| `/telemetry`   | GET    | Telemetría de sensores                |
| `/move?dir=X`  | GET    | Control de movimiento (F/B/L/R/S)     |
| `/auto?enabled=X` | GET | Activar/desactivar modo automático |
| `/logs`        | GET    | Historial de eventos (últimos 50)     |
| `/security`    | GET    | Estado del sistema de seguridad       |
| `/clear`       | GET    | Reset de safe mode                    |

**Ejemplo de uso:**
```bash
# Obtener estado
curl http://192.168.43.200/status

# Mover adelante
curl "http://192.168.43.200/move?dir=F"

# Ver telemetría
curl http://192.168.43.200/telemetry
```

## Características Destacadas

### 🛡️ Sistema de Seguridad

- **Safe Mode automático**: Se activa tras 5 errores consecutivos
- **Logging de IP**: Registra la IP de origen de cada error
- **Bloqueo de movimiento**: Protege el robot en caso de fallos

### 🤖 Modo Automático

- **Navegación autónoma**: El robot avanza y evita obstáculos
- **Detección ultrasónica**: Mide distancia cada 200ms
- **Lógica de evasión**: Stop → Retroceso → Giro → Continuar
- **Distancia configurable**: Ajustable según velocidad del robot

### 📊 Telemetría en Tiempo Real

- **Uptime del sistema**: Tiempo desde el arranque
- **Distancia medida**: Lectura del sensor en centímetros
- **Detección de obstáculos**: Boolean basado en distancia mínima
- **Estado del modo auto**: Activo/inactivo

### 📝 Sistema de Logs

- **Buffer circular**: Últimas 50 entradas
- **Timestamps**: Segundos desde arranque
- **Eventos registrados**: Comandos, errores, cambios de modo

## Esquema de Conexiones

### Pines ESP32 → L298N (Motores)

```
ESP32          L298N
GPIO26    →    IN1 (Motor Izq +)
GPIO27    →    IN2 (Motor Izq -)
GPIO14    →    IN3 (Motor Der +)
GPIO12    →    IN4 (Motor Der -)
```

### Pines ESP32 → HC-SR04 (Sensor)

```
ESP32          HC-SR04
GPIO5     →    TRIG
GPIO18    →    ECHO
5V        →    VCC
GND       →    GND
```

## Requisitos del Sistema

### Hardware
- ESP32 DevKit (cualquier variante)
- Robot 2WD con motores DC
- Driver L298N Dual H-Bridge
- Sensor ultrasónico HC-SR04
- Batería 6-12V para motores
- Cables de conexión

### Software
- **Para ESP32:**
  - Python 3.7+ (esptool)
  - MicroPython firmware v1.20+
  - Thonny IDE o ampy

- **Para Dashboard:**
  - Node.js 14+
  - npm 6+

### Red
- WiFi 2.4 GHz (ESP32 no soporta 5 GHz)
- Hotspot móvil o router
- DHCP habilitado

## Configuración

### Configurar WiFi del ESP32

Editar `esp32-robot-refactored/src/config.py`:

```python
WIFI_SSID = "TU_SSID"           # ← Nombre de tu WiFi
WIFI_PASSWORD = "TU_PASSWORD"    # ← Contraseña
SECURITY_TOKEN = "tu-token-seguro-aqui"  # ← Token único y seguro
```

### Configurar IP en el Dashboard

Editar `robot-dashboard/src/config.js`:

```javascript
export const ROBOT_IP = "192.168.43.200"; // IP del ESP32
```

## Troubleshooting

### ESP32 no se conecta a WiFi
- Verificar que el WiFi sea **2.4 GHz** (no 5 GHz)
- Comprobar SSID y contraseña
- Probar con hotspot móvil

### Dashboard no conecta
- Verificar que ambos estén en la misma red
- Comprobar IP del ESP32 en `config.js`
- Desactivar firewall temporalmente

### Motores no responden
- Verificar conexiones de pines
- Comprobar alimentación del L298N
- Revisar polaridad de los motores

### Sensor retorna -1.0
- Verificar conexión VCC → 5V (no 3.3V)
- Comprobar TRIG → GPIO5, ECHO → GPIO18
- Verificar GND común entre ESP32 y sensor

**[📖 Ver guía completa de troubleshooting](./esp32-robot-refactored/README.md#troubleshooting)**

## Especificaciones Técnicas

| Característica              | Valor                  |
|-----------------------------|------------------------|
| Latencia API                | 50-100ms               |
| Frecuencia sensor           | 5 Hz (200ms)           |
| Alcance ultrasónico         | 2-400 cm               |
| Precisión sensor            | ±3mm                   |
| Consumo total               | ~400-700mA             |
| Max conexiones simultáneas  | 1                      |
| Buffer de logs              | 50 entradas            |
| Timeout socket              | 100ms                  |

## Estructura del Proyecto

```
Robot-2WD/
├── README.md                    # 📄 Este archivo
├── esp32-robot-refactored/      # 🔧 Backend ESP32
│   ├── src/                    # Código fuente MicroPython
│   │   ├── main.py            # Script principal
│   │   ├── config.py          # Configuración
│   │   ├── http_server.py     # Servidor HTTP
│   │   └── ...                # Otros módulos
│   ├── SETUP.md               # Guía de configuración segura
│   └── README.md              # Documentación técnica completa
├── robot-dashboard/            # 💻 Frontend React
│   ├── src/                   # Código fuente React
│   ├── package.json           # Dependencias npm
│   └── README.md              # Documentación del dashboard
└── .venv/                      # Entorno virtual Python (local)
```

## Roadmap

- [ ] Implementar PWM para control de velocidad
- [ ] Añadir más sensores (giroscopio, IR)
- [ ] Modo de patrulla automática
- [ ] Guardar configuración en EEPROM
- [ ] Implementar WebSocket para streaming de telemetría
- [ ] Añadir cámara con streaming de video
- [ ] App móvil nativa (React Native)

## Contribuir

Este es un proyecto de código abierto. Si quieres contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo licencia libre. Puedes usarlo, modificarlo y compartirlo libremente.

## Recursos Adicionales

### Documentación
- [📖 Documentación completa del ESP32](./esp32-robot-refactored/README.md)
- [📖 Guía de configuración segura](./esp32-robot-refactored/SETUP.md)
- [📖 Documentación del Dashboard](./robot-dashboard/README.md)

### Enlaces Útiles
- [MicroPython ESP32 Docs](https://docs.micropython.org/en/latest/esp32/quickref.html)
- [L298N Datasheet](https://www.sparkfun.com/datasheets/Robotics/L298_H_Bridge.pdf)
- [HC-SR04 Datasheet](https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf)
- [React Documentation](https://react.dev)

## Soporte

Para problemas, preguntas o sugerencias:
- Abre un **Issue** en GitHub
- Consulta la sección de **Troubleshooting** en los READMEs
- Revisa los **logs del sistema** para diagnóstico

---

**Proyecto desarrollado con ❤️ usando ESP32 y React**

*Última actualización: 2025*
