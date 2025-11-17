"""
Sistema de seguridad y Safe Mode
"""
import config


class SecurityManager:
    """Gestor de seguridad con Safe Mode automático"""
    
    def __init__(self, logger):
        """
        Inicializa el gestor de seguridad
        
        Args:
            logger (Logger): Instancia del logger
        """
        self.logger = logger
        self.fail_count = 0
        self.safe_mode = False
        self.last_error = ""
        self.last_ip = ""
    
    def add_error(self, ip, error_message):
        """
        Registra un error y actualiza contadores
        
        Args:
            ip (str): IP del cliente que generó el error
            error_message (str): Descripción del error
        """
        self.fail_count += 1
        self.last_error = error_message
        self.last_ip = ip
        
        self.logger.add("ERROR de {} -> {}".format(ip, error_message))
        
        # Activar Safe Mode si se superan los errores máximos
        if self.fail_count >= config.MAX_ERRORS_BEFORE_SAFE_MODE and not self.safe_mode:
            self.activate_safe_mode()
    
    def activate_safe_mode(self):
        """Activa el Safe Mode"""
        self.safe_mode = True
        self.logger.add("⚠️ SAFE MODE ACTIVADO - Robot bloqueado")
    
    def deactivate_safe_mode(self):
        """Desactiva el Safe Mode y resetea contadores"""
        self.fail_count = 0
        self.safe_mode = False
        self.last_error = ""
        self.last_ip = ""
        self.logger.add("✅ SAFE MODE DESACTIVADO")
    
    def is_safe_mode_active(self):
        """
        Verifica si el Safe Mode está activo
        
        Returns:
            bool: True si está activo
        """
        return self.safe_mode
    
    def get_status(self):
        """
        Obtiene el estado completo de seguridad
        
        Returns:
            dict: Estado de seguridad
        """
        return {
            "fail_count": self.fail_count,
            "safe_mode": self.safe_mode,
            "last_error": self.last_error,
            "last_ip": self.last_ip
        }
    
    def get_json(self):
        """
        Obtiene el estado en formato JSON
        
        Returns:
            str: JSON del estado de seguridad
        """
        status = self.get_status()
        return (
            '{'
            '"fail_count": ' + str(status["fail_count"]) + ','
            '"safe_mode": ' + str(status["safe_mode"]).lower() + ','
            '"last_error": "' + status["last_error"].replace('"', '\\"') + '",'
            '"last_ip": "' + status["last_ip"] + '"'
            '}'
        )
