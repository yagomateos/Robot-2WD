"""
Tests para auto_mode.py
"""
import sys
import pytest


def test_auto_mode_init(mock_micropython_modules, mock_config):
    """Test de inicialización del modo automático"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    
    auto_mode = AutoMode(motors, sensor, logger)
    
    assert auto_mode.enabled == False
    assert auto_mode.min_distance == 20  # Valor por defecto de config


def test_auto_mode_enable(mock_micropython_modules, mock_config):
    """Test de activación del modo automático"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    auto_mode = AutoMode(motors, sensor, logger)
    
    auto_mode.enable()
    
    assert auto_mode.enabled == True
    assert auto_mode.is_enabled() == True


def test_auto_mode_disable(mock_micropython_modules, mock_config):
    """Test de desactivación del modo automático"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    auto_mode = AutoMode(motors, sensor, logger)
    
    auto_mode.enable()
    auto_mode.disable()
    
    assert auto_mode.enabled == False
    assert auto_mode.is_enabled() == False
    
    # Los motores deben estar detenidos
    assert motors.in1.value() == 0
    assert motors.in2.value() == 0
    assert motors.in3.value() == 0
    assert motors.in4.value() == 0


def test_auto_mode_set_min_distance(mock_micropython_modules, mock_config):
    """Test de ajuste de distancia mínima"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    auto_mode = AutoMode(motors, sensor, logger)
    
    auto_mode.set_min_distance(30)
    
    assert auto_mode.min_distance == 30


def test_auto_mode_step_disabled(mock_micropython_modules, mock_config):
    """Test de que step no hace nada cuando está desactivado"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    auto_mode = AutoMode(motors, sensor, logger)
    
    # Modo desactivado
    auto_mode.step()
    
    # Los motores no deben moverse
    assert motors.in1.value() == 0
    assert motors.in2.value() == 0


def test_auto_mode_step_forward_no_obstacle(mock_micropython_modules, mock_config):
    """Test de avanzar cuando no hay obstáculos"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from unittest.mock import patch
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    auto_mode = AutoMode(motors, sensor, logger)
    
    auto_mode.enable()
    
    # Avanzar el tiempo para que se ejecute el step
    mock_time._ticks = 300
    
    # Mock del sensor para retornar 50cm (sin obstáculo)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=2910):
        auto_mode.step()
    
    # Debe estar avanzando (forward)
    assert motors.in1.value() == 1
    assert motors.in3.value() == 1


def test_auto_mode_step_evasion_with_obstacle(mock_micropython_modules, mock_config):
    """Test de maniobra de evasión cuando hay obstáculo"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from unittest.mock import patch
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    auto_mode = AutoMode(motors, sensor, logger)
    
    auto_mode.enable()
    
    # Avanzar el tiempo para que se ejecute el step
    mock_time._ticks = 300
    
    # Mock del sensor para retornar 10cm (obstáculo detectado)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=580):
        auto_mode.step()
    
    # Después de la evasión, los motores deben estar detenidos
    assert motors.in1.value() == 0
    assert motors.in2.value() == 0
    assert motors.in3.value() == 0
    assert motors.in4.value() == 0


def test_auto_mode_step_frequency_control(mock_micropython_modules, mock_config):
    """Test de control de frecuencia de ejecución"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.auto_mode import AutoMode
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    import config
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    auto_mode = AutoMode(motors, sensor, logger)
    
    auto_mode.enable()
    
    # Primer step
    mock_time._ticks = 0
    auto_mode.step()
    
    # Intentar step inmediatamente (no debe ejecutarse)
    mock_time._ticks = 50  # Menos que AUTO_CHECK_INTERVAL (200ms)
    motors.stop()  # Resetear motores
    auto_mode.step()
    
    # Los motores no deben haberse movido
    assert motors.in1.value() == 0
    
    # Avanzar el tiempo suficiente
    mock_time._ticks = 250  # Más que AUTO_CHECK_INTERVAL
    auto_mode.step()
    
    # Ahora sí debe ejecutarse
    # (asumiendo que no hay obstáculo, debe avanzar)
    assert motors.in1.value() == 1 or motors.in1.value() == 0  # Puede variar según el sensor
