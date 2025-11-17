"""
Robot 2WD ESP32 - Sistema Principal
Punto de entrada de la aplicación
"""

# Importar módulos del sistema
from motor_controller import MotorController
from sensor_handler import UltrasonicSensor
from logger import Logger
from security_manager import SecurityManager
from auto_mode import AutoMode
from wifi_manager import WiFiManager
from http_server import HTTPServer


def main():
    """Función principal de inicio"""
    
    print("\n" + "="*50)
    print("🤖 ROBOT 2WD ESP32 - INICIANDO")
    print("="*50)
    print("")
    
    # 1. Inicializar Logger
    print("📋 Inicializando Logger...")
    logger = Logger()
    logger.add("Sistema iniciado")
    
    # 2. Inicializar Hardware
    print("🔧 Inicializando Hardware...")
    motors = MotorController()
    logger.add("Motores inicializados")
    
    sensor = UltrasonicSensor()
    logger.add("Sensor ultrasónico inicializado")
    
    # 3. Inicializar Sistemas
    print("⚙️ Inicializando Sistemas...")
    security = SecurityManager(logger)
    logger.add("Sistema de seguridad inicializado")
    
    auto_mode = AutoMode(motors, sensor, logger)
    logger.add("Modo automático inicializado")
    
    # 4. Conectar WiFi
    print("🌐 Conectando a WiFi...")
    wifi = WiFiManager(logger)
    ip = wifi.connect()
    
    if ip is None:
        logger.add("❌ FALLO CRÍTICO: No se pudo conectar a WiFi")
        print("\n❌ ERROR CRÍTICO: Conexión WiFi fallida")
        print("El robot no puede iniciar sin conexión WiFi.")
        print("Revisa la configuración en config.py")
        return
    
    # 5. Iniciar Servidor HTTP
    print("🚀 Iniciando Servidor HTTP...")
    server = HTTPServer(ip, motors, sensor, logger, security, auto_mode)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupción detectada")
        logger.add("Sistema detenido por usuario")
        motors.stop()
        wifi.disconnect()
        print("✅ Robot detenido correctamente")
    except Exception as e:
        print("\n\n❌ ERROR:", str(e))
        logger.add("ERROR CRÍTICO: " + str(e))
        motors.stop()
        wifi.disconnect()


# Ejecutar aplicación
if __name__ == "__main__":
    main()
