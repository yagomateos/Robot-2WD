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
        """Detiene ambos motores"""
        self.in1.value(0)
        self.in2.value(0)
        self.in3.value(0)
        self.in4.value(0)
    
    def forward(self):
        """Mueve el robot hacia adelante"""
        self.in1.value(1)
        self.in2.value(0)
        self.in3.value(1)
        self.in4.value(0)
    
    def backward(self):
        """Mueve el robot hacia atrás"""
        self.in1.value(0)
        self.in2.value(1)
        self.in3.value(0)
        self.in4.value(1)
    
    def turn_left(self):
        """Gira el robot a la izquierda (motor izq. atrás, motor der. adelante)"""
        self.in1.value(0)
        self.in2.value(1)
        self.in3.value(1)
        self.in4.value(0)
    
    def turn_right(self):
        """Gira el robot a la derecha (motor izq. adelante, motor der. atrás)"""
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
        direction = direction.upper()
        
        commands = {
            'F': self.forward,
            'B': self.backward,
            'L': self.turn_left,
            'R': self.turn_right,
            'S': self.stop
        }
        
        if direction in commands:
            commands[direction]()
            return True
        
        return False
