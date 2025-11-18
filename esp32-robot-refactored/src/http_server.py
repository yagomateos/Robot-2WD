"""
Servidor HTTP con API REST para control del robot
"""
import socket
import time
import machine
import config


class HTTPServer:
    """Servidor HTTP embebido con API REST"""
    
    def __init__(self, ip, motors, sensor, logger, security, auto_mode):
        """
        Inicializa el servidor HTTP

        Args:
            ip (str): IP del servidor
            motors (MotorController): Controlador de motores
            sensor (UltrasonicSensor): Sensor ultrasónico
            logger (Logger): Sistema de logging
            security (SecurityManager): Gestor de seguridad
            auto_mode (AutoMode): Modo automático
        """
        self.ip = ip
        self.motors = motors
        self.sensor = sensor
        self.logger = logger
        self.security = security
        self.auto_mode = auto_mode
        self.socket = None

        # Rate limiting: diccionario {IP: [timestamp1, timestamp2, ...]}
        self.request_history = {}
    
    def start(self):
        """Inicia el servidor HTTP"""
        addr = (self.ip, config.SERVER_PORT)
        
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(addr)
        self.socket.listen(1)
        self.socket.settimeout(config.SOCKET_TIMEOUT)
        
        print("\n" + "="*50)
        print("SERVIDOR HTTP INICIADO")
        print("="*50)
        print("API disponible en: http://{}:{}".format(self.ip, config.SERVER_PORT))
        print("")
        print("Endpoints públicos:")
        print("  GET  /              - Verificación del servidor")
        print("  GET  /status        - Estado del sistema")
        print("  GET  /telemetry     - Telemetría de sensores")
        print("  GET  /move?dir=X    - Control de movimiento")
        print("  GET  /auto?enabled=X - Modo automático")
        print("  GET  /security      - Estado de seguridad")
        print("")
        print("Endpoints protegidos (requieren ?token=XXX):")
        print("  GET  /logs?token=XXX   - Historial de logs")
        print("  GET  /clear?token=XXX  - Reset de Safe Mode")
        print("  GET  /restart?token=XXX - Reiniciar ESP32")
        print("="*50)
        print("")
        print("Rate limiting: {} req/{}ms por IP".format(
            config.RATE_LIMIT_REQUESTS,
            config.RATE_LIMIT_WINDOW_MS
        ))
        print("="*50)
        print("")
        
        self.motors.stop()
        self.logger.add("🚀 Servidor HTTP iniciado")
        
        # Loop principal
        self._run_loop()
    
    def _run_loop(self):
        """Loop principal del servidor"""
        while True:
            # Ejecutar paso del modo automático
            self.auto_mode.step()

            # Intentar aceptar conexión
            try:
                client, remote = self.socket.accept()
            except OSError:
                # Timeout, continuar el loop
                continue

            # Procesar request
            self._handle_request(client, remote)

    def _check_rate_limit(self, client_ip):
        """
        Verifica si un cliente ha excedido el rate limit

        Args:
            client_ip (str): IP del cliente

        Returns:
            bool: True si está permitido, False si excede el límite
        """
        now = time.ticks_ms()

        # Inicializar historial si es primera vez
        if client_ip not in self.request_history:
            self.request_history[client_ip] = []

        # Obtener historial de esta IP
        history = self.request_history[client_ip]

        # Filtrar requests dentro de la ventana de tiempo
        window_start = time.ticks_diff(now, config.RATE_LIMIT_WINDOW_MS)
        recent_requests = [ts for ts in history if time.ticks_diff(now, ts) < config.RATE_LIMIT_WINDOW_MS]

        # Actualizar historial
        self.request_history[client_ip] = recent_requests

        # Verificar límite
        if len(recent_requests) >= config.RATE_LIMIT_REQUESTS:
            return False

        # Agregar este request al historial
        recent_requests.append(now)
        return True

    def _handle_request(self, client, remote):
        """
        Maneja una petición HTTP

        Args:
            client: Socket del cliente
            remote: Información del cliente remoto
        """
        try:
            # Obtener IP del cliente
            client_ip = remote[0]

            # Verificar rate limiting
            if not self._check_rate_limit(client_ip):
                self.logger.add("RATE_LIMIT excedido: " + client_ip)
                self._send_json(client, '{"error":"too many requests"}', "429 Too Many Requests")
                return

            # Recibir datos (máximo 1024 bytes)
            MAX_REQUEST_SIZE = 1024
            request = client.recv(MAX_REQUEST_SIZE)
            if not request:
                return

            # Decodificar
            try:
                text = request.decode('utf-8')
            except UnicodeDecodeError as e:
                self.logger.add("ERROR: Request inválido (UTF-8): " + str(e))
                self._send_json(client, '{"error":"invalid encoding"}', "400 Bad Request")
                return

            # Parsear primera línea
            lines = text.split("\r\n")
            if not lines:
                return

            request_line = lines[0]

            # Manejar preflight CORS (OPTIONS)
            if request_line.startswith("OPTIONS"):
                self._send_text(client, "ok", "200 OK")
                return

            # Parsear path
            path = self._parse_path(request_line)

            # Validar longitud de path
            if len(path) > 256:
                self.logger.add("ERROR: Path demasiado largo")
                self._send_json(client, '{"error":"path too long"}', "400 Bad Request")
                return

            # Validar caracteres en path (sanitización básica)
            if ".." in path or "\\" in path:
                self.logger.add("ERROR: Path inválido (traversal): " + path)
                self._send_json(client, '{"error":"invalid path"}', "400 Bad Request")
                return

            # Rutear la petición
            self._route_request(client, path, client_ip)

        except Exception as e:
            self.logger.add("ERROR crítico en _handle_request: " + str(e))
            try:
                self._send_json(client, '{"error":"server error"}', "500 Internal Server Error")
            except OSError as close_error:
                self.logger.add("ERROR al enviar respuesta de error: " + str(close_error))

        finally:
            try:
                client.close()
            except OSError as e:
                # Error al cerrar socket, loguear pero continuar
                self.logger.add("ERROR al cerrar socket: " + str(e))
    
    def _route_request(self, client, path, client_ip):
        """
        Enruta la petición al handler correspondiente
        
        Args:
            client: Socket del cliente
            path (str): Path de la petición
            client_ip (str): IP del cliente
        """
        if path == "/":
            self._handle_root(client)
        
        elif path.startswith("/status"):
            self._handle_status(client)
        
        elif path.startswith("/telemetry"):
            self._handle_telemetry(client)
        
        elif path.startswith("/move"):
            self._handle_move(client, path, client_ip)
        
        elif path.startswith("/auto"):
            self._handle_auto(client, path)
        
        elif path.startswith("/logs"):
            self._handle_logs(client, path)

        elif path.startswith("/security"):
            self._handle_security(client)

        elif path.startswith("/clear"):
            self._handle_clear(client, path)

        elif path.startswith("/restart"):
            self._handle_restart(client, path, client_ip)

        else:
            self._handle_not_found(client, path, client_ip)
    
    # ==========================================
    # HANDLERS DE ENDPOINTS
    # ==========================================
    
    def _handle_root(self, client):
        """Handler para /"""
        self._send_text(client, "ESP32 Robot API OK")
    
    def _handle_status(self, client):
        """Handler para /status"""
        uptime = self.logger.get_uptime_seconds()
        body = (
            '{'
            '"uptime": ' + str(uptime) + ','
            '"wifi": "ok",'
            '"ip": "' + self.ip + '"'
            '}'
        )
        self._send_json(client, body)
    
    def _handle_telemetry(self, client):
        """Handler para /telemetry"""
        uptime = self.logger.get_uptime_seconds()
        distance = self.sensor.measure_distance_cm()
        
        if distance < 0:
            distance = -1.0
        
        obstacle = distance != -1.0 and distance < self.auto_mode.min_distance
        
        body = (
            '{'
            '"uptime": ' + str(uptime) + ','
            '"distance_cm": ' + "{:.1f}".format(distance) + ','
            '"obstacle": ' + str(obstacle).lower() + ','
            '"auto_enabled": ' + str(self.auto_mode.is_enabled()).lower() +
            '}'
        )
        self._send_json(client, body)
    
    def _handle_move(self, client, path, client_ip):
        """Handler para /move"""
        # Verificar Safe Mode
        if self.security.is_safe_mode_active():
            self._send_json(client, '{"error":"safe_mode"}', "403 Forbidden")
            return
        
        # Obtener dirección
        direction = self._get_query_param(path, "dir")
        
        if direction is None:
            self.security.add_error(client_ip, "missing_dir")
            self._send_json(client, '{"error":"missing dir"}', "400 Bad Request")
            return
        
        # Ejecutar comando
        if self.motors.execute_command(direction):
            # Escapar direction para JSON
            safe_dir = self._escape_json_string(direction.upper())
            self.logger.add("MOVE {}".format(safe_dir))
            self._send_json(client, '{"ok":true,"dir":"' + safe_dir + '"}')
        else:
            self.security.add_error(client_ip, "invalid_dir:" + direction)
            self._send_json(client, '{"error":"invalid dir"}', "400 Bad Request")
    
    def _handle_auto(self, client, path):
        """Handler para /auto"""
        value = self._get_query_param(path, "enabled")
        
        if value is None:
            self._send_json(client, '{"error":"missing enabled"}', "400 Bad Request")
            return
        
        # Parsear boolean
        enabled = value.lower() in ["1", "true", "yes", "on"]
        
        # Activar/desactivar modo auto
        if enabled:
            self.auto_mode.enable()
        else:
            self.auto_mode.disable()
        
        self._send_json(client, '{"auto_enabled": ' + str(enabled).lower() + '}')
    
    def _handle_logs(self, client, path):
        """Handler para /logs - Requiere token de seguridad"""
        # Verificar token
        token = self._get_query_param(path, "token")
        if token != config.SECURITY_TOKEN:
            self.logger.add("ERROR: Token inválido para /logs")
            self._send_json(client, '{"error":"unauthorized"}', "401 Unauthorized")
            return

        logs_json = self.logger.get_json_array()
        self._send_json(client, '{"logs": ' + logs_json + '}')
    
    def _handle_security(self, client):
        """Handler para /security"""
        self._send_json(client, self.security.get_json())
    
    def _handle_clear(self, client, path):
        """Handler para /clear - Requiere token de seguridad"""
        # Verificar token
        token = self._get_query_param(path, "token")
        if token != config.SECURITY_TOKEN:
            self.logger.add("ERROR: Token inválido para /clear")
            self._send_json(client, '{"error":"unauthorized"}', "401 Unauthorized")
            return

        self.security.deactivate_safe_mode()
        self.logger.add("Safe Mode desactivado con token")
        self._send_json(client, '{"ok":true}')

    def _handle_restart(self, client, path, client_ip):
        """Handler para /restart - Requiere token de seguridad"""
        # Verificar token
        token = self._get_query_param(path, "token")
        if token != config.SECURITY_TOKEN:
            self.logger.add("ERROR: Token inválido para /restart desde " + client_ip)
            self.security.add_error(client_ip, "restart_unauthorized")
            self._send_json(client, '{"error":"unauthorized"}', "401 Unauthorized")
            return

        # Token válido, proceder con reinicio
        self.logger.add("⚠️ Reinicio autorizado desde " + client_ip)
        self._send_json(client, '{"ok":true,"message":"restarting"}')
        self.motors.stop()
        time.sleep_ms(100)  # Dar tiempo para enviar respuesta
        machine.reset()

    def _handle_not_found(self, client, path, client_ip):
        """Handler para rutas no encontradas"""
        self.security.add_error(client_ip, "route_not_found:" + path)
        self._send_json(client, '{"error":"not found"}', "404 Not Found")
    
    # ==========================================
    # UTILIDADES
    # ==========================================
    
    def _parse_path(self, request_line):
        """
        Parsea el path de la request line

        Args:
            request_line (str): Primera línea de la petición HTTP

        Returns:
            str: Path de la petición
        """
        try:
            parts = request_line.split(" ")
            if len(parts) >= 2:
                return parts[1]
            return "/"
        except (IndexError, AttributeError) as e:
            self.logger.add("ERROR: Request line inválido")
            return "/"
    
    def _get_query_param(self, path, key):
        """
        Obtiene un parámetro de query string

        Args:
            path (str): Path completo con query string
            key (str): Nombre del parámetro

        Returns:
            str: Valor del parámetro o None
        """
        if "?" not in path:
            return None

        base, query = path.split("?", 1)
        params = query.split("&")

        for param in params:
            if "=" in param:
                k, v = param.split("=", 1)
                if k == key:
                    return v

        return None

    def _escape_json_string(self, text):
        """
        Escapa caracteres especiales para JSON

        Args:
            text (str): Texto a escapar

        Returns:
            str: Texto escapado para JSON
        """
        if text is None:
            return ""

        # Escapar caracteres especiales
        text = str(text)
        text = text.replace("\\", "\\\\")  # Backslash primero
        text = text.replace('"', '\\"')    # Comillas dobles
        text = text.replace("\n", "\\n")   # Nueva línea
        text = text.replace("\r", "\\r")   # Retorno de carro
        text = text.replace("\t", "\\t")   # Tab
        return text
    
    def _send_json(self, client, body, status="200 OK"):
        """
        Envía respuesta JSON con headers CORS
        
        Args:
            client: Socket del cliente
            body (str): Cuerpo JSON
            status (str): Status HTTP
        """
        header = (
            "HTTP/1.1 " + status + "\r\n"
            "Content-Type: application/json\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
            "Access-Control-Allow-Headers: *\r\n"
            "\r\n"
        )
        client.send(header + body)
    
    def _send_text(self, client, body, status="200 OK"):
        """
        Envía respuesta de texto plano con headers CORS
        
        Args:
            client: Socket del cliente
            body (str): Cuerpo de texto
            status (str): Status HTTP
        """
        header = (
            "HTTP/1.1 " + status + "\r\n"
            "Content-Type: text/plain\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
            "Access-Control-Allow-Headers: *\r\n"
            "\r\n"
        )
        client.send(header + body)
