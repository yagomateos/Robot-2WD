"""Handler para sensor ultrasónico HC-SR04.

Este módulo proporciona una interfaz para interactuar con el sensor
ultrasónico HC-SR04, permitiendo mediciones de distancia y detección
de obstáculos para navegación autónoma del robot.

Example:
    >>> sensor = UltrasonicSensor()
    >>> distance = sensor.measure_distance_cm()
    >>> if sensor.is_obstacle_detected(threshold_cm=15):
    ...     print("Obstáculo detectado")
"""
from machine import Pin, time_pulse_us
import time
import config


class UltrasonicSensor:
    """Sensor ultrasónico HC-SR04 para medición de distancia.

    Interfaz para el sensor HC-SR04 que utiliza pulsos ultrasónicos
    para medir distancias entre 2 y 400 cm. El sensor envía un pulso
    de trigger y mide el tiempo de retorno del echo.

    Attributes:
        trig (Pin): Pin de salida para trigger del sensor
        echo (Pin): Pin de entrada para echo del sensor

    Note:
        Los pines se configuran desde config.ULTRASONIC_TRIG y
        config.ULTRASONIC_ECHO respectivamente.
    """
    
    def __init__(self):
        """Inicializa los pines del sensor ultrasónico.

        Configura el pin trigger como salida y el pin echo como entrada
        usando los valores definidos en el módulo config.

        Raises:
            ValueError: Si los pines no son válidos para la placa
            OSError: Si hay un error al configurar los pines GPIO

        Note:
            Los números de pin se obtienen de config.ULTRASONIC_TRIG
            y config.ULTRASONIC_ECHO.
        """
        self.trig = Pin(config.ULTRASONIC_TRIG, Pin.OUT)
        self.echo = Pin(config.ULTRASONIC_ECHO, Pin.IN)
    
    def measure_distance_cm(self):
        """
        Mide la distancia en centímetros

        Returns:
            float: Distancia en cm (2-400), o -1 si hay error/fuera de rango

        Note:
            El HC-SR04 tiene un rango efectivo de 2-400 cm.
            Valores fuera de este rango se consideran errores de medición.
        """
        try:
            # Preparar el pulso
            self.trig.value(0)
            time.sleep_us(2)

            # Enviar pulso de 10µs
            self.trig.value(1)
            time.sleep_us(10)
            self.trig.value(0)

            # Medir duración del pulso de retorno
            duration = time_pulse_us(self.echo, 1, config.ULTRASONIC_TIMEOUT)

            # Validar que no hubo timeout
            if duration < 0:
                return -1.0

            # Validar que no excede el timeout configurado
            if duration > config.ULTRASONIC_TIMEOUT:
                return -1.0

            # Calcular distancia: (duración / 2) / 29.1
            # Velocidad del sonido: 343 m/s = 0.0343 cm/µs = 29.1 µs/cm
            # Ida y vuelta: dividir por 2
            SOUND_SPEED_FACTOR = 29.1
            distance = (duration / 2.0) / SOUND_SPEED_FACTOR

            # Validar rango del sensor HC-SR04 (2-400 cm)
            MIN_DISTANCE = 2.0
            MAX_DISTANCE = 400.0

            if distance < MIN_DISTANCE or distance > MAX_DISTANCE:
                return -1.0

            return distance

        except Exception as e:
            # Capturar cualquier error inesperado
            # No romper el programa, solo retornar error
            return -1.0
    
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
