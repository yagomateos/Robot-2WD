"""
Configuración centralizada del robot ESP32
"""

# ===========================
# CONFIGURACIÓN DE PINES
# ===========================

# Pines del motor izquierdo (L298N IN1, IN2)
MOTOR_LEFT_PIN1 = 26
MOTOR_LEFT_PIN2 = 27

# Pines del motor derecho (L298N IN3, IN4)
MOTOR_RIGHT_PIN1 = 14
MOTOR_RIGHT_PIN2 = 12

# Pines del sensor ultrasónico HC-SR04
ULTRASONIC_TRIG = 5
ULTRASONIC_ECHO = 18

# ===========================
# CONFIGURACIÓN WIFI
# ===========================

# IMPORTANTE: Cambiar por tus credenciales
WIFI_SSID = "Galaxy S25 Ultra F1ED"
WIFI_PASSWORD = "5t85stns6eus2kr"

# Timeout de conexión WiFi (en intentos)
WIFI_CONNECT_ATTEMPTS = 40

# ===========================
# CONFIGURACIÓN DEL SERVIDOR
# ===========================

SERVER_PORT = 80
SOCKET_TIMEOUT = 0.1  # segundos

# ===========================
# CONFIGURACIÓN DE SEGURIDAD
# ===========================

# Número máximo de errores antes de activar Safe Mode
MAX_ERRORS_BEFORE_SAFE_MODE = 5

# Tamaño máximo del buffer de logs
MAX_LOG_ENTRIES = 50

# ===========================
# CONFIGURACIÓN MODO AUTOMÁTICO
# ===========================

# Distancia mínima de seguridad (cm)
AUTO_MIN_DISTANCE = 20

# Intervalo entre mediciones en modo auto (ms)
AUTO_CHECK_INTERVAL = 200

# Tiempos de maniobra de evasión (ms)
AUTO_STOP_TIME = 200
AUTO_BACKWARD_TIME = 400
AUTO_TURN_TIME = 400

# ===========================
# CONFIGURACIÓN DEL SENSOR
# ===========================

# Timeout de pulso del sensor ultrasónico (microsegundos)
ULTRASONIC_TIMEOUT = 30000
