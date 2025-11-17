"""
Sistema de logging con buffer circular
"""
import time
import config


class Logger:
    """Sistema de logging con timestamps y buffer circular"""
    
    def __init__(self):
        self.logs = []
        self.start_time = time.ticks_ms()
    
    def get_uptime_seconds(self):
        return time.ticks_diff(time.ticks_ms(), self.start_time) // 1000
    
    def add(self, message):
        # Limitar tamaño del buffer
        if len(self.logs) >= config.MAX_LOG_ENTRIES:
            self.logs.pop(0)
        
        timestamp = self.get_uptime_seconds()
        entry = "[{}s] {}".format(timestamp, message)
        self.logs.append(entry)
        
        # Mostrar en consola para revisar
        print(entry)
    
    def get_all(self):
        return self.logs
    
    def clear(self):
        self.logs = []
        self.add("LOGS CLEARED")
    
    def get_json_array(self):
        """
        Devuelve los logs con formato seguro para JSON.
        Evita fallos en el navegador.
        """
        items = []
        
        for entry in self.logs:
            safe = entry.replace('"', '\\"')
            items.append('"' + safe + '"')
        
        return "[" + ",".join(items) + "]"
