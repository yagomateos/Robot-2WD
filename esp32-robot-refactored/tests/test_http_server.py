"""
Tests para http_server.py (utilidades)
"""
import sys
import pytest


def test_parse_path_valid(mock_micropython_modules, mock_config):
    """Test de parseo de paths válidos"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Test de paths válidos
    assert server._parse_path("GET / HTTP/1.1") == "/"
    assert server._parse_path("GET /status HTTP/1.1") == "/status"
    assert server._parse_path("GET /move?dir=F HTTP/1.1") == "/move?dir=F"


def test_parse_path_invalid(mock_micropython_modules, mock_config):
    """Test de parseo de paths inválidos"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Request line inválido debe retornar "/"
    assert server._parse_path("") == "/"
    assert server._parse_path("INVALID") == "/"


def test_get_query_param_valid(mock_micropython_modules, mock_config):
    """Test de extracción de query parameters"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Test de query parameters válidos
    assert server._get_query_param("/move?dir=F", "dir") == "F"
    assert server._get_query_param("/auto?enabled=1", "enabled") == "1"
    assert server._get_query_param("/logs?token=abc123", "token") == "abc123"
    
    # Múltiples parámetros
    assert server._get_query_param("/test?a=1&b=2&c=3", "b") == "2"


def test_get_query_param_missing(mock_micropython_modules, mock_config):
    """Test de query parameter faltante"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Parámetro no existe
    assert server._get_query_param("/move?dir=F", "speed") is None
    
    # Sin query string
    assert server._get_query_param("/status", "dir") is None


def test_escape_json_string(mock_micropython_modules, mock_config):
    """Test de escape de strings para JSON"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Test de escape de caracteres especiales
    assert server._escape_json_string('text with "quotes"') == 'text with \\"quotes\\"'
    assert server._escape_json_string('line1\\nline2') == 'line1\\\\nline2'
    assert server._escape_json_string('tab\\there') == 'tab\\\\there'
    assert server._escape_json_string('backslash\\\\test') == 'backslash\\\\\\\\test'
    
    # None debe retornar string vacío
    assert server._escape_json_string(None) == ""


def test_check_rate_limit_allowed(mock_micropython_modules, mock_config):
    """Test de rate limiting - requests permitidos"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    import config
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Primera request debe ser permitida
    assert server._check_rate_limit("192.168.1.100") == True
    
    # Requests dentro del límite deben ser permitidas
    for i in range(config.RATE_LIMIT_REQUESTS - 2):
        assert server._check_rate_limit("192.168.1.100") == True


def test_check_rate_limit_exceeded(mock_micropython_modules, mock_config):
    """Test de rate limiting - límite excedido"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    import config
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Hacer requests hasta el límite
    for i in range(config.RATE_LIMIT_REQUESTS):
        server._check_rate_limit("192.168.1.100")
    
    # La siguiente debe ser rechazada
    assert server._check_rate_limit("192.168.1.100") == False


def test_check_rate_limit_window_reset(mock_micropython_modules, mock_config):
    """Test de rate limiting - reset de ventana de tiempo"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    import config
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Hacer requests hasta el límite
    for i in range(config.RATE_LIMIT_REQUESTS):
        server._check_rate_limit("192.168.1.100")
    
    # Avanzar el tiempo más allá de la ventana
    mock_time._ticks += config.RATE_LIMIT_WINDOW_MS + 100
    
    # Ahora debe ser permitida de nuevo
    assert server._check_rate_limit("192.168.1.100") == True


def test_check_rate_limit_different_ips(mock_micropython_modules, mock_config):
    """Test de rate limiting - IPs diferentes tienen límites separados"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.http_server import HTTPServer
    from src.motor_controller import MotorController
    from src.sensor_handler import UltrasonicSensor
    from src.logger import Logger
    from src.security_manager import SecurityManager
    from src.auto_mode import AutoMode
    import config
    
    motors = MotorController()
    sensor = UltrasonicSensor()
    logger = Logger()
    security = SecurityManager(logger)
    auto_mode = AutoMode(motors, sensor, logger)
    
    server = HTTPServer("192.168.1.1", motors, sensor, logger, security, auto_mode)
    
    # Hacer requests desde IP1 hasta el límite
    for i in range(config.RATE_LIMIT_REQUESTS):
        server._check_rate_limit("192.168.1.100")
    
    # IP1 debe estar bloqueada
    assert server._check_rate_limit("192.168.1.100") == False
    
    # IP2 debe estar permitida (límite separado)
    assert server._check_rate_limit("192.168.1.101") == True
