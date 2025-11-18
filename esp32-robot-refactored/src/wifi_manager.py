"""
Gestor de conexión WiFi
"""
import network
import time
import config


class WiFiManager:
    """Gestor de conexión WiFi en modo cliente"""
    
    def __init__(self, logger):
        """
        Inicializa el gestor WiFi
        
        Args:
            logger (Logger): Sistema de logging
        """
        self.logger = logger
        self.sta = None
        self.ip = None
    
    def connect(self):
        """
        Conecta al WiFi configurado
        
        Returns:
            str: IP asignada, o None si falla la conexión
        """
        # Desactivar modo Access Point
        ap = network.WLAN(network.AP_IF)
        ap.active(False)
        
        # Activar modo Station (cliente)
        self.sta = network.WLAN(network.STA_IF)
        self.sta.active(True)

        # Configurar IP estática si está definida
        if hasattr(config, 'WIFI_STATIC_IP') and config.WIFI_STATIC_IP:
            self.sta.ifconfig(config.WIFI_STATIC_IP)
            print("📌 IP estática configurada:", config.WIFI_STATIC_IP[0])

        self.logger.add("Conectando a WiFi: {}".format(config.WIFI_SSID))
        print("\n" + "="*50)
        print("🌐 CONECTANDO A WIFI")
        print("="*50)
        print("SSID:", config.WIFI_SSID)
        print("Modo IP:", "ESTÁTICA" if hasattr(config, 'WIFI_STATIC_IP') and config.WIFI_STATIC_IP else "DHCP")
        print("Intentos máximos:", config.WIFI_CONNECT_ATTEMPTS)
        print("")

        # Intentar conexión
        self.sta.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        
        for attempt in range(config.WIFI_CONNECT_ATTEMPTS):
            if self.sta.isconnected():
                break
            
            print("Intento {}/{} -> {}".format(
                attempt + 1,
                config.WIFI_CONNECT_ATTEMPTS,
                "✓ Conectado" if self.sta.isconnected() else "⏳ Conectando..."
            ))
            
            time.sleep(0.5)
        
        # Verificar resultado
        if not self.sta.isconnected():
            print("\n❌ ERROR: No se pudo conectar al WiFi")
            print("Revisa:")
            print("  - SSID y contraseña correctos")
            print("  - WiFi en 2.4GHz (ESP32 no soporta 5GHz)")
            print("  - Señal WiFi disponible")
            print("")
            self.logger.add("ERROR: Conexión WiFi fallida")
            return None
        
        # Conexión exitosa
        self.ip = self.sta.ifconfig()[0]
        
        print("\n" + "="*50)
        print("✅ CONEXIÓN EXITOSA")
        print("="*50)
        print("IP asignada:", self.ip)
        print("Máscara:", self.sta.ifconfig()[1])
        print("Gateway:", self.sta.ifconfig()[2])
        print("DNS:", self.sta.ifconfig()[3])
        print("")
        
        self.logger.add("WiFi conectado - IP: {}".format(self.ip))
        
        return self.ip
    
    def disconnect(self):
        """Desconecta del WiFi"""
        if self.sta:
            self.sta.disconnect()
            self.sta.active(False)
            self.logger.add("WiFi desconectado")
    
    def is_connected(self):
        """
        Verifica si está conectado
        
        Returns:
            bool: True si está conectado
        """
        return self.sta and self.sta.isconnected()
    
    def get_ip(self):
        """
        Obtiene la IP asignada
        
        Returns:
            str: IP o None si no está conectado
        """
        return self.ip
