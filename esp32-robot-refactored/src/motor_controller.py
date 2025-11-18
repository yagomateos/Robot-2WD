"""
Controlador de motores L298N para robot 2WD
"""
from machine import Pin
import config


class MotorController:
    """Controlador para motores DC mediante driver L298N"""
    
    def __init__(self):
        """Inicializa los pines de control de motores"""
        # Motor izquierdo
        self.in1 = Pin(config.MOTOR_LEFT_PIN1, Pin.OUT)
        self.in2 = Pin(config.MOTOR_LEFT_PIN2, Pin.OUT)
        
        # Motor derecho
        self.in3 = Pin(config.MOTOR_RIGHT_PIN1, Pin.OUT)
        self.in4 = Pin(config.MOTOR_RIGHT_PIN2, Pin.OUT)
        
        # Detener motores al iniciar
        self.stop()
    
    def stop(self):
        """
        Detiene ambos motores inmediatamente

        Establece todas las salidas del L298N a LOW (0V).
        El stop es inmediato, sin rampa de desaceleración.
        """
        self.in1.value(0)
        self.in2.value(0)
        self.in3.value(0)
        self.in4.value(0)

    def forward(self):
        """
        Mueve el robot hacia adelante

        Configura ambos motores para girar en sentido forward.
        Motor izquierdo: IN1=HIGH, IN2=LOW
        Motor derecho: IN3=HIGH, IN4=LOW
        """
        self.in1.value(1)
        self.in2.value(0)
        self.in3.value(1)
        self.in4.value(0)

    def backward(self):
        """
        Mueve el robot hacia atrás

        Configura ambos motores para girar en sentido reverse.
        Motor izquierdo: IN1=LOW, IN2=HIGH
        Motor derecho: IN3=LOW, IN4=HIGH
        """
        self.in1.value(0)
        self.in2.value(1)
        self.in3.value(0)
        self.in4.value(1)

    def turn_left(self):
        """
        Gira el robot a la izquierda (giro en el lugar)

        Motor izquierdo gira hacia atrás, motor derecho hacia adelante.
        Esto produce un giro sobre el eje vertical del robot.
        """
        self.in1.value(0)
        self.in2.value(1)
        self.in3.value(1)
        self.in4.value(0)

    def turn_right(self):
        """
        Gira el robot a la derecha (giro en el lugar)

        Motor izquierdo gira hacia adelante, motor derecho hacia atrás.
        Esto produce un giro sobre el eje vertical del robot.
        """
        self.in1.value(1)
        self.in2.value(0)
        self.in3.value(0)
        self.in4.value(1)
    
    def execute_command(self, direction):
        """
        Ejecuta un comando de movimiento

        Args:
            direction (str): Dirección ('F', 'B', 'L', 'R', 'S')

        Returns:
            bool: True si el comando es válido, False si no
        """
        # Validar tipo de entrada
        if not isinstance(direction, str):
            return False

        # Validar longitud (solo 1 carácter)
        if len(direction) != 1:
            return False

        # Normalizar a mayúsculas
        direction = direction.upper()

        # Mapeo de comandos a métodos
        commands = {
            'F': self.forward,
            'B': self.backward,
            'L': self.turn_left,
            'R': self.turn_right,
            'S': self.stop
        }

        # Ejecutar comando si es válido
        if direction in commands:
            commands[direction]()
            return True

        return False
