"""
Tests para sensor_handler.py
"""
import sys
import pytest
from unittest.mock import patch


def test_sensor_init(mock_micropython_modules, mock_config):
    """Test de inicialización del sensor"""
    from src.sensor_handler import UltrasonicSensor
    
    sensor = UltrasonicSensor()
    
    assert sensor.trig is not None
    assert sensor.echo is not None


def test_measure_distance_valid(mock_micropython_modules, mock_config):
    """Test de medición exitosa dentro del rango válido"""
    from src.sensor_handler import UltrasonicSensor
    
    # Mock de time_pulse_us para retornar un valor válido
    # 10cm = 580µs (ida y vuelta)
    mock_micropython_modules['machine'].time_pulse_us = lambda pin, level, timeout: 580
    
    sensor = UltrasonicSensor()
    distance = sensor.measure_distance_cm()
    
    # Debe estar cerca de 10cm
    assert 9.5 < distance < 10.5


def test_measure_distance_various_values(mock_micropython_modules, mock_config):
    """Test de medición con diferentes distancias"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # 5cm = 290µs
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=290):
        distance = sensor.measure_distance_cm()
        assert 4.5 < distance < 5.5
    
    # 20cm = 1160µs
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=1160):
        distance = sensor.measure_distance_cm()
        assert 19.5 < distance < 20.5
    
    # 100cm = 5820µs
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=5820):
        distance = sensor.measure_distance_cm()
        assert 99 < distance < 101


def test_measure_distance_timeout(mock_micropython_modules, mock_config):
    """Test de manejo de timeout"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # Mock de time_pulse_us para retornar timeout (-1)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=-1):
        distance = sensor.measure_distance_cm()
        # Debe retornar -1.0 en caso de timeout
        assert distance == -1.0


def test_measure_distance_exceeds_timeout(mock_micropython_modules, mock_config):
    """Test cuando la duración excede el timeout configurado"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # Retornar un valor mayor al timeout (30000µs)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=35000):
        distance = sensor.measure_distance_cm()
        # Debe retornar -1.0
        assert distance == -1.0


def test_measure_distance_below_min_range(mock_micropython_modules, mock_config):
    """Test de valores por debajo del rango mínimo (< 2cm)"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # 1cm = 58µs (fuera de rango)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=58):
        distance = sensor.measure_distance_cm()
        # Debe retornar -1.0 (fuera de rango)
        assert distance == -1.0


def test_measure_distance_above_max_range(mock_micropython_modules, mock_config):
    """Test de valores por encima del rango máximo (> 400cm)"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # 450cm = 26190µs (fuera de rango)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=26190):
        distance = sensor.measure_distance_cm()
        # Debe retornar -1.0 (fuera de rango)
        assert distance == -1.0


def test_measure_distance_oserror(mock_micropython_modules, mock_config):
    """Test de manejo de errores de hardware (OSError)"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # Mock que lanza OSError
    with patch('src.sensor_handler.machine.time_pulse_us', side_effect=OSError("Hardware error")):
        distance = sensor.measure_distance_cm()
        # Debe retornar -2.0 (error de I/O)
        assert distance == -2.0


def test_is_obstacle_detected_true(mock_micropython_modules, mock_config):
    """Test de detección de obstáculo (dentro del umbral)"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # 10cm = 580µs (menor que el umbral por defecto de 20cm)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=580):
        # Con umbral por defecto (20cm)
        assert sensor.is_obstacle_detected() == True
        
        # Con umbral personalizado (15cm)
        assert sensor.is_obstacle_detected(threshold_cm=15) == True


def test_is_obstacle_detected_false(mock_micropython_modules, mock_config):
    """Test de no detección de obstáculo (fuera del umbral)"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # 50cm = 2910µs (mayor que el umbral por defecto de 20cm)
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=2910):
        # Con umbral por defecto (20cm)
        assert sensor.is_obstacle_detected() == False
        
        # Con umbral personalizado (60cm)
        assert sensor.is_obstacle_detected(threshold_cm=60) == True


def test_is_obstacle_detected_error(mock_micropython_modules, mock_config):
    """Test de detección cuando hay error en la medición"""
    from src.sensor_handler import UltrasonicSensor
    from unittest.mock import patch
    
    sensor = UltrasonicSensor()
    
    # Mock que retorna timeout
    with patch('src.sensor_handler.machine.time_pulse_us', return_value=-1):
        # En caso de error, debe retornar False
        assert sensor.is_obstacle_detected() == False
