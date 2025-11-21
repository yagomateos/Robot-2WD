"""
Tests para security_manager.py
"""
import sys
import pytest


def test_security_manager_init(mock_micropython_modules, mock_config):
    """Test de inicialización del gestor de seguridad"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    
    logger = Logger()
    security = SecurityManager(logger)
    
    assert security.fail_count == 0
    assert security.safe_mode == False
    assert security.last_error == ""
    assert security.last_ip == ""


def test_security_add_error(mock_micropython_modules, mock_config):
    """Test de agregar errores"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    
    logger = Logger()
    security = SecurityManager(logger)
    
    security.add_error("192.168.1.100", "invalid_command")
    
    assert security.fail_count == 1
    assert security.last_error == "invalid_command"
    assert security.last_ip == "192.168.1.100"


def test_security_safe_mode_activation(mock_micropython_modules, mock_config):
    """Test de activación automática de Safe Mode"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    import config
    
    logger = Logger()
    security = SecurityManager(logger)
    
    # Agregar errores hasta alcanzar el límite
    for i in range(config.MAX_ERRORS_BEFORE_SAFE_MODE):
        security.add_error("192.168.1.100", f"error_{i}")
    
    # Safe Mode debe estar activo
    assert security.safe_mode == True
    assert security.is_safe_mode_active() == True


def test_security_safe_mode_not_activated_below_threshold(mock_micropython_modules, mock_config):
    """Test de que Safe Mode no se activa por debajo del umbral"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    import config
    
    logger = Logger()
    security = SecurityManager(logger)
    
    # Agregar errores pero no alcanzar el límite
    for i in range(config.MAX_ERRORS_BEFORE_SAFE_MODE - 1):
        security.add_error("192.168.1.100", f"error_{i}")
    
    # Safe Mode NO debe estar activo
    assert security.safe_mode == False
    assert security.is_safe_mode_active() == False


def test_security_deactivate_safe_mode(mock_micropython_modules, mock_config):
    """Test de desactivación de Safe Mode"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    
    logger = Logger()
    security = SecurityManager(logger)
    
    # Activar Safe Mode manualmente
    security.activate_safe_mode()
    assert security.safe_mode == True
    
    # Desactivar
    security.deactivate_safe_mode()
    
    assert security.safe_mode == False
    assert security.fail_count == 0
    assert security.last_error == ""
    assert security.last_ip == ""


def test_security_get_status(mock_micropython_modules, mock_config):
    """Test de obtener estado de seguridad"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    
    logger = Logger()
    security = SecurityManager(logger)
    
    security.add_error("192.168.1.100", "test_error")
    
    status = security.get_status()
    
    assert status["fail_count"] == 1
    assert status["safe_mode"] == False
    assert status["last_error"] == "test_error"
    assert status["last_ip"] == "192.168.1.100"


def test_security_get_json(mock_micropython_modules, mock_config):
    """Test de formato JSON del estado"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    
    logger = Logger()
    security = SecurityManager(logger)
    
    security.add_error("192.168.1.100", "test_error")
    
    json_str = security.get_json()
    
    assert '"fail_count": 1' in json_str
    assert '"safe_mode": false' in json_str
    assert '"last_error": "test_error"' in json_str
    assert '"last_ip": "192.168.1.100"' in json_str


def test_security_json_escape_quotes(mock_micropython_modules, mock_config):
    """Test de escape de comillas en JSON"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.security_manager import SecurityManager
    from src.logger import Logger
    
    logger = Logger()
    security = SecurityManager(logger)
    
    security.add_error("192.168.1.100", 'error with "quotes"')
    
    json_str = security.get_json()
    
    # Las comillas deben estar escapadas
    assert '\\"quotes\\"' in json_str
