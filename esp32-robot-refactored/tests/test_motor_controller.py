"""
Tests para motor_controller.py
"""
import sys
import pytest


def test_motor_controller_init(mock_micropython_modules, mock_config):
    """Test de inicialización del controlador de motores"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    
    # Verificar que se crearon los pines
    assert controller.in1 is not None
    assert controller.in2 is not None
    assert controller.in3 is not None
    assert controller.in4 is not None
    
    # Verificar que todos los pines están en 0 (stop inicial)
    assert controller.in1.value() == 0
    assert controller.in2.value() == 0
    assert controller.in3.value() == 0
    assert controller.in4.value() == 0


def test_motor_forward(mock_micropython_modules, mock_config):
    """Test de movimiento hacia adelante"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    controller.forward()
    
    # Motor izquierdo: IN1=1, IN2=0
    assert controller.in1.value() == 1
    assert controller.in2.value() == 0
    
    # Motor derecho: IN3=1, IN4=0
    assert controller.in3.value() == 1
    assert controller.in4.value() == 0


def test_motor_backward(mock_micropython_modules, mock_config):
    """Test de movimiento hacia atrás"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    controller.backward()
    
    # Motor izquierdo: IN1=0, IN2=1
    assert controller.in1.value() == 0
    assert controller.in2.value() == 1
    
    # Motor derecho: IN3=0, IN4=1
    assert controller.in3.value() == 0
    assert controller.in4.value() == 1


def test_motor_turn_left(mock_micropython_modules, mock_config):
    """Test de giro a la izquierda"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    controller.turn_left()
    
    # Motor izquierdo hacia atrás: IN1=0, IN2=1
    assert controller.in1.value() == 0
    assert controller.in2.value() == 1
    
    # Motor derecho hacia adelante: IN3=1, IN4=0
    assert controller.in3.value() == 1
    assert controller.in4.value() == 0


def test_motor_turn_right(mock_micropython_modules, mock_config):
    """Test de giro a la derecha"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    controller.turn_right()
    
    # Motor izquierdo hacia adelante: IN1=1, IN2=0
    assert controller.in1.value() == 1
    assert controller.in2.value() == 0
    
    # Motor derecho hacia atrás: IN3=0, IN4=1
    assert controller.in3.value() == 0
    assert controller.in4.value() == 1


def test_motor_stop(mock_micropython_modules, mock_config):
    """Test de detención de motores"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    
    # Primero mover
    controller.forward()
    
    # Luego detener
    controller.stop()
    
    # Todos los pines deben estar en 0
    assert controller.in1.value() == 0
    assert controller.in2.value() == 0
    assert controller.in3.value() == 0
    assert controller.in4.value() == 0


def test_execute_command_valid(mock_micropython_modules, mock_config):
    """Test de ejecución de comandos válidos"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    
    # Probar todos los comandos válidos
    assert controller.execute_command('F') == True
    assert controller.execute_command('B') == True
    assert controller.execute_command('L') == True
    assert controller.execute_command('R') == True
    assert controller.execute_command('S') == True
    
    # Probar con minúsculas (debe normalizar)
    assert controller.execute_command('f') == True
    assert controller.execute_command('b') == True


def test_execute_command_invalid(mock_micropython_modules, mock_config):
    """Test de rechazo de comandos inválidos"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    
    # Comandos inválidos
    assert controller.execute_command('X') == False
    assert controller.execute_command('Z') == False
    assert controller.execute_command('') == False
    assert controller.execute_command('FF') == False
    assert controller.execute_command('123') == False


def test_execute_command_invalid_type(mock_micropython_modules, mock_config):
    """Test de validación de tipo de entrada"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    
    # Tipos inválidos
    assert controller.execute_command(123) == False
    assert controller.execute_command(None) == False
    assert controller.execute_command(['F']) == False
    assert controller.execute_command({'dir': 'F'}) == False


def test_execute_command_changes_state(mock_micropython_modules, mock_config):
    """Test de que execute_command cambia el estado de los pines"""
    from src.motor_controller import MotorController
    
    controller = MotorController()
    
    # Ejecutar forward
    controller.execute_command('F')
    assert controller.in1.value() == 1
    assert controller.in3.value() == 1
    
    # Ejecutar stop
    controller.execute_command('S')
    assert controller.in1.value() == 0
    assert controller.in2.value() == 0
    assert controller.in3.value() == 0
    assert controller.in4.value() == 0
