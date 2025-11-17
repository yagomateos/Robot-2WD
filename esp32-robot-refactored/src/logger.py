"""
Sistema de logging con buffer circular
"""
import time
import config


class Logger:
    """Sistema de logging con timestamps y buffer circular"""
    
    def __init__(self):
        """Inicializa el logger"""
        self.logs = []
        self.start_time = time.ticks_ms()
    
    def get_uptime_seconds(self):
        """
        Obtiene el tiempo de actividad del sistema en segundos
        
        Returns:
            int: Segundos desde el inicio
        """
        return time.ticks_diff(time.ticks_ms(), self.start_time) // 1000
    
    def add(self, message):
        """
        Añade una entrada al log
        
        Args:
            message (str): Mensaje a registrar
        """
        # Limitar el tamaño del buffer (buffer circular)
        if len(self.logs) >= config.MAX_LOG_ENTRIES:
            self.logs.pop(0)
        
        timestamp = self.get_uptime_seconds()
        log_entry = "[{}s] {}".format(timestamp, message)
        self.logs.append(log_entry)
        
        # Imprimir en consola para debugging
        print(log_entry)
    
    def get_all(self):
        """
        Obtiene todos los logs
        
        Returns:
            list: Lista de logs
        """
        return self.logs
    
    def clear(self):
        """Limpia todos los logs"""
        self.logs = []
        self.add("LOGS CLEARED")
    
    def get_json_array(self):
        """
        Obtiene los logs en formato JSON array
        
        Returns:
            str: String JSON con los logs
        """
        # Escapar comillas y convertir a JSON
        return str(self.logs).replace("'", '"')
