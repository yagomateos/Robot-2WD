"""
Tests para logger.py
"""
import sys
import pytest


def test_logger_init(mock_micropython_modules, mock_config):
    """Test de inicialización del logger"""
    # Inyectar el mock de time
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.logger import Logger
    
    logger = Logger()
    
    assert logger.logs == []
    assert logger.start_time == 0


def test_logger_add(mock_micropython_modules, mock_config):
    """Test de agregar logs"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.logger import Logger
    
    logger = Logger()
    logger.add("Test message")
    
    assert len(logger.logs) == 1
    assert "Test message" in logger.logs[0]
    assert "[0s]" in logger.logs[0]


def test_logger_uptime(mock_micropython_modules, mock_config):
    """Test de cálculo de uptime"""
    mock_time = mock_micropython_modules['time'].__class__
    sys.modules['time'] = mock_time
    
    from src.logger import Logger
    
    logger = Logger()
    
    # Simular paso del tiempo
    mock_time._ticks = 5000  # 5 segundos
    
    uptime = logger.get_uptime_seconds()
    assert uptime == 5


def test_logger_circular_buffer(mock_micropython_modules, mock_config):
    """Test de buffer circular (límite de MAX_LOG_ENTRIES)"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.logger import Logger
    import config
    
    logger = Logger()
    
    # Agregar más logs que el máximo
    for i in range(config.MAX_LOG_ENTRIES + 10):
        logger.add(f"Message {i}")
    
    # El buffer no debe exceder el máximo
    assert len(logger.logs) == config.MAX_LOG_ENTRIES
    
    # El primer mensaje debe haber sido eliminado
    assert "Message 0" not in logger.logs[0]
    
    # Los últimos mensajes deben estar presentes
    assert "Message " + str(config.MAX_LOG_ENTRIES + 9) in logger.logs[-1]


def test_logger_get_all(mock_micropython_modules, mock_config):
    """Test de obtener todos los logs"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.logger import Logger
    
    logger = Logger()
    logger.add("Message 1")
    logger.add("Message 2")
    logger.add("Message 3")
    
    all_logs = logger.get_all()
    
    assert len(all_logs) == 3
    assert "Message 1" in all_logs[0]
    assert "Message 2" in all_logs[1]
    assert "Message 3" in all_logs[2]


def test_logger_clear(mock_micropython_modules, mock_config):
    """Test de limpieza de logs"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.logger import Logger
    
    logger = Logger()
    logger.add("Message 1")
    logger.add("Message 2")
    
    logger.clear()
    
    # Debe tener solo el mensaje de "LOGS CLEARED"
    assert len(logger.logs) == 1
    assert "LOGS CLEARED" in logger.logs[0]


def test_logger_json_format(mock_micropython_modules, mock_config):
    """Test de formato JSON"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.logger import Logger
    
    logger = Logger()
    logger.add("Message 1")
    logger.add("Message 2")
    
    json_array = logger.get_json_array()
    
    # Debe ser un array JSON válido
    assert json_array.startswith("[")
    assert json_array.endswith("]")
    assert "Message 1" in json_array
    assert "Message 2" in json_array


def test_logger_json_escape(mock_micropython_modules, mock_config):
    """Test de escape de caracteres especiales en JSON"""
    sys.modules['time'] = mock_micropython_modules['time'].__class__
    
    from src.logger import Logger
    
    logger = Logger()
    logger.add('Message with "quotes"')
    
    json_array = logger.get_json_array()
    
    # Las comillas deben estar escapadas
    assert '\\"quotes\\"' in json_array
