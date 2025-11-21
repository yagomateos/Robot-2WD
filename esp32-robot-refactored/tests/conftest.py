"""
Configuración de pytest con mocks para hardware de MicroPython
"""
import sys
import pytest
from unittest.mock import MagicMock, Mock


# ==========================================
# MOCKS PARA MÓDULOS DE MICROPYTHON
# ==========================================

class MockPin:
    """Mock para machine.Pin"""
    OUT = 1
    IN = 0
    
    def __init__(self, pin_num, mode):
        self.pin_num = pin_num
        self.mode = mode
        self._value = 0
    
    def value(self, val=None):
        if val is not None:
            self._value = val
        return self._value


class MockMachine:
    """Mock para el módulo machine"""
    Pin = MockPin
    
    def __init__(self):
        # Valor por defecto para time_pulse_us (10cm = 580µs)
        self._time_pulse_value = 580
    
    @staticmethod
    def reset():
        """Mock para machine.reset()"""
        pass
    
    def time_pulse_us(self, pin, level, timeout):
        """Mock para machine.time_pulse_us()"""
        # Retorna el valor configurado o el por defecto
        return self._time_pulse_value


class MockTime:
    """Mock para el módulo time de MicroPython"""
    _ticks = 0
    
    @classmethod
    def ticks_ms(cls):
        """Retorna ticks en milisegundos"""
        return cls._ticks
    
    @classmethod
    def ticks_diff(cls, new, old):
        """Calcula diferencia entre ticks"""
        return new - old
    
    @classmethod
    def sleep_ms(cls, ms):
        """Simula sleep en milisegundos"""
        cls._ticks += ms
    
    @classmethod
    def sleep_us(cls, us):
        """Simula sleep en microsegundos"""
        pass
    
    @classmethod
    def reset_ticks(cls):
        """Resetea el contador de ticks (para tests)"""
        cls._ticks = 0


class MockSocket:
    """Mock para socket"""
    SOL_SOCKET = 1
    SO_REUSEADDR = 2
    
    def __init__(self):
        self.bound = False
        self.listening = False
        self.timeout = None
    
    def setsockopt(self, level, optname, value):
        pass
    
    def bind(self, addr):
        self.bound = True
        self.addr = addr
    
    def listen(self, backlog):
        self.listening = True
    
    def settimeout(self, timeout):
        self.timeout = timeout
    
    def accept(self):
        """Mock de accept - lanza OSError para simular timeout"""
        raise OSError("timeout")
    
    def recv(self, bufsize):
        return b"GET / HTTP/1.1\r\n\r\n"
    
    def send(self, data):
        return len(data)
    
    def close(self):
        pass


# ==========================================
# FIXTURES DE PYTEST
# ==========================================

@pytest.fixture(autouse=True)
def mock_micropython_modules(monkeypatch):
    """
    Mock automático de todos los módulos de MicroPython
    Se aplica a todos los tests automáticamente
    """
    # Crear mocks de módulos
    mock_machine = MockMachine()
    mock_time = MockTime()
    mock_socket_module = MagicMock()
    mock_socket_module.socket = MockSocket
    
    # Inyectar en sys.modules antes de importar
    monkeypatch.setitem(sys.modules, 'machine', mock_machine)
    monkeypatch.setitem(sys.modules, 'socket', mock_socket_module)
    
    # Resetear ticks antes de cada test
    mock_time.reset_ticks()
    
    return {
        'machine': mock_machine,
        'time': mock_time,
        'socket': mock_socket_module
    }


@pytest.fixture
def mock_config(monkeypatch):
    """Mock del módulo config con valores de test"""
    # Importar el módulo config_template como config
    import sys
    import importlib.util
    
    # Cargar config_template
    spec = importlib.util.spec_from_file_location(
        "config",
        "/Users/yagomateos/Proyectos/Robot-2WD/esp32-robot-refactored/src/config_template.py"
    )
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    # Inyectar en sys.modules
    monkeypatch.setitem(sys.modules, 'config', config)
    
    return config


@pytest.fixture
def mock_pin():
    """Fixture para crear un MockPin"""
    return MockPin(1, MockPin.OUT)


@pytest.fixture
def mock_time_module():
    """Fixture para el módulo time mockeado"""
    mock_time = MockTime()
    mock_time.reset_ticks()
    return mock_time
