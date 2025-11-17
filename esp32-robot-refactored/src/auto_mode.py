"""
Modo automático con navegación autónoma y evasión de obstáculos
"""
import time
import config


class AutoMode:
    """Controlador del modo automático con evasión de obstáculos"""
    
    def __init__(self, motor_controller, sensor, logger):
        """
        Inicializa el modo automático
        
        Args:
            motor_controller (MotorController): Controlador de motores
            sensor (UltrasonicSensor): Sensor ultrasónico
            logger (Logger): Sistema de logging
        """
        self.motors = motor_controller
        self.sensor = sensor
        self.logger = logger
        
        self.enabled = False
        self.min_distance = config.AUTO_MIN_DISTANCE
        self.last_check = time.ticks_ms()
    
    def enable(self):
        """Activa el modo automático"""
        self.enabled = True
        self.logger.add("🤖 MODO AUTO ACTIVADO")
    
    def disable(self):
        """Desactiva el modo automático"""
        self.enabled = False
        self.motors.stop()
        self.logger.add("🤖 MODO AUTO DESACTIVADO")
    
    def is_enabled(self):
        """
        Verifica si el modo automático está activo
        
        Returns:
            bool: True si está activo
        """
        return self.enabled
    
    def set_min_distance(self, distance_cm):
        """
        Establece la distancia mínima de seguridad
        
        Args:
            distance_cm (float): Distancia en centímetros
        """
        self.min_distance = distance_cm
        self.logger.add("Distancia mínima ajustada a {}cm".format(distance_cm))
    
    def step(self):
        """
        Ejecuta un paso del modo automático (debe llamarse en el loop principal)
        """
        if not self.enabled:
            return
        
        # Control de frecuencia de ejecución
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_check) < config.AUTO_CHECK_INTERVAL:
            return
        
        self.last_check = now
        
        # Medir distancia
        distance = self.sensor.measure_distance_cm()
        
        if distance < 0:
            # Error en la medición, continuar con precaución
            return
        
        # Lógica de navegación
        if distance < self.min_distance:
            self._execute_evasion_maneuver()
        else:
            # Camino libre, avanzar
            self.motors.forward()
    
    def _execute_evasion_maneuver(self):
        """
        Ejecuta maniobra de evasión de obstáculo
        Secuencia: Stop → Retroceso → Giro → Stop
        """
        self.logger.add("⚠️ Obstáculo detectado - Ejecutando evasión")
        
        # Detener
        self.motors.stop()
        time.sleep_ms(config.AUTO_STOP_TIME)
        
        # Retroceder
        self.motors.backward()
        time.sleep_ms(config.AUTO_BACKWARD_TIME)
        
        # Girar (alternativa: podrías randomizar left/right)
        self.motors.turn_left()
        time.sleep_ms(config.AUTO_TURN_TIME)
        
        # Detener
        self.motors.stop()
