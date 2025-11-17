"""
Handler para sensor ultrasónico HC-SR04
"""
from machine import Pin, time_pulse_us
import time
import config


class UltrasonicSensor:
    """Sensor ultrasónico HC-SR04 para medición de distancia"""
    
    def __init__(self):
        """Inicializa los pines del sensor ultrasónico"""
        self.trig = Pin(config.ULTRASONIC_TRIG, Pin.OUT)
        self.echo = Pin(config.ULTRASONIC_ECHO, Pin.IN)
    
    def measure_distance_cm(self):
        """
        Mide la distancia en centímetros
        
        Returns:
            float: Distancia en cm, o -1 si hay error
        """
        # Preparar el pulso
        self.trig.value(0)
        time.sleep_us(2)
        
        # Enviar pulso de 10µs
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)
        
        # Medir duración del pulso de retorno
        duration = time_pulse_us(self.echo, 1, config.ULTRASONIC_TIMEOUT)
        
        if duration < 0:
            return -1.0
        
        # Calcular distancia: (duración / 2) / 29.1
        # Velocidad del sonido: 343 m/s = 0.0343 cm/µs
        # Ida y vuelta: dividir por 2
        distance = (duration / 2.0) / 29.1
        
        return distance
    
    def is_obstacle_detected(self, threshold_cm=None):
        """
        Detecta si hay un obstáculo dentro del umbral
        
        Args:
            threshold_cm (float): Distancia mínima en cm (usa config si es None)
        
        Returns:
            bool: True si hay obstáculo, False si no
        """
        if threshold_cm is None:
            threshold_cm = config.AUTO_MIN_DISTANCE
        
        distance = self.measure_distance_cm()
        
        if distance < 0:
            return False  # Error en la medición
        
        return distance < threshold_cm
