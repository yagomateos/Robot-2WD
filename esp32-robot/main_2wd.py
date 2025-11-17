import network
import socket
import time
from machine import Pin, time_pulse_us

# -------------------------
# MOTORES
# -------------------------

IN1 = Pin(26, Pin.OUT)
IN2 = Pin(27, Pin.OUT)
IN3 = Pin(14, Pin.OUT)
IN4 = Pin(12, Pin.OUT)

def stop():
    IN1.value(0); IN2.value(0)
    IN3.value(0); IN4.value(0)

def forward():
    IN1.value(1); IN2.value(0)
    IN3.value(1); IN4.value(0)

def backward():
    IN1.value(0); IN2.value(1)
    IN3.value(0); IN4.value(1)

def left():
    IN1.value(0); IN2.value(1)
    IN3.value(1); IN4.value(0)

def right():
    IN1.value(1); IN2.value(0)
    IN3.value(0); IN4.value(1)

# -------------------------
# SENSOR ULTRASONIDO
# -------------------------

TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

def medir_distancia_cm():
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)
    duracion = time_pulse_us(ECHO, 1, 30000)
    if duracion < 0:
        return -1.0
    distancia = (duracion / 2.0) / 29.1
    return distancia

# -------------------------
# TIEMPO — LOGS
# -------------------------

start_ms = time.ticks_ms()

def get_uptime_seconds():
    return time.ticks_diff(time.ticks_ms(), start_ms) // 1000

logs = []

security = {
    "fail_count": 0,
    "safe_mode": False,
    "last_error": "",
    "last_ip": "",
}

auto_mode = {
    "enabled": False,
    "min_distance": 20
}

last_auto_check = time.ticks_ms()

def add_log(msg):
    global logs
    if len(logs) > 50:
        logs.pop(0)
    ts = get_uptime_seconds()
    logs.append("[{}s] {}".format(ts, msg))

def add_error(ip, msg):
    security["fail_count"] += 1
    security["last_error"] = msg
    security["last_ip"] = ip
    add_log("ERROR de {} -> {}".format(ip, msg))
    if security["fail_count"] >= 5 and not security["safe_mode"]:
        security["safe_mode"] = True
        add_log("SAFE MODE ACTIVADO")

# -------------------------
# MODO AUTOMATICO
# -------------------------

def auto_step():
    global last_auto_check
    if not auto_mode["enabled"]:
        return
    ahora = time.ticks_ms()
    if time.ticks_diff(ahora, last_auto_check) < 200:
        return
    last_auto_check = ahora

    dist = medir_distancia_cm()
    if dist < 0:
        return

    if dist < auto_mode["min_distance"]:
        stop()
        time.sleep_ms(200)
        backward()
        time.sleep_ms(400)
        left()
        time.sleep_ms(400)
        stop()
    else:
        forward()

# -------------------------
# WIFI — CLIENTE (HOTSPOT)
# -------------------------

def iniciar_wifi_cliente():
    # Apagar AP interno
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    ssid = "Galaxy S25 Ultra F1ED"
    pwd = "5t85stns6eus2kr"

    print("Conectando a:", ssid)
    sta.connect(ssid, pwd)

    for i in range(40):
        print("Intento", i + 1, "-> conectado:", sta.isconnected())
        if sta.isconnected():
            break
        time.sleep(0.5)

    if not sta.isconnected():
        print("NO conectado. Revisa el hotspot y 2.4GHz.")
        return None

    ip = sta.ifconfig()[0]
    print("Conectado con IP:", ip)
    return ip

# -------------------------
# RESPUESTAS JSON
# -------------------------

def get_status_json(ip):
    up = get_uptime_seconds()
    body = (
        '{'
        '"uptime": ' + str(up) + ','
        '"wifi":"ok",'
        '"ip":"' + ip + '"'
        '}'
    )
    return body

def get_telemetry_json():
    up = get_uptime_seconds()
    dist = medir_distancia_cm()
    if dist < 0:
        dist = -1.0
    obst = dist != -1.0 and dist < auto_mode["min_distance"]
    body = (
        '{'
        '"uptime": ' + str(up) + ','
        '"distance_cm": ' + "{:.1f}".format(dist) + ','
        '"obstacle": ' + str(obst).lower() + ','
        '"auto_enabled": ' + str(auto_mode["enabled"]).lower() +
        '}'
    )
    return body

# -------------------------
# RESPUESTA HTTP (CON CORS)
# -------------------------

def send_json(client, body, status="200 OK"):
    header = (
        "HTTP/1.1 " + status + "\r\n"
        "Content-Type: application/json\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: *\r\n"
        "\r\n"
    )
    client.send(header + body)

def send_text(client, body, status="200 OK"):
    header = (
        "HTTP/1.1 " + status + "\r\n"
        "Content-Type: text/plain\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: *\r\n"
        "\r\n"
    )
    client.send(header + body)

# -------------------------
# PARSEO
# -------------------------

def parse_path(line):
    try:
        parts = line.split(" ")
        return parts[1]
    except:
        return "/"

def get_query_param(path, key):
    if "?" not in path:
        return None
    base, query = path.split("?", 1)
    params = query.split("&")
    for p in params:
        if "=" in p:
            k, v = p.split("=", 1)
            if k == key:
                return v
    return None

# -------------------------
# SERVIDOR HTTP
# -------------------------

def iniciar_servidor(ip):
    addr = (ip, 80)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    s.settimeout(0.1)

    print("API en: http://{}".format(ip))
    stop()
    add_log("SERVER INICIADO")

    while True:
        auto_step()

        try:
            client, remote = s.accept()
        except OSError:
            continue

        try:
            req = client.recv(1024)
            if not req:
                client.close()
                continue

            try:
                text = req.decode()
            except:
                client.close()
                continue

            line0 = text.split("\r\n")[0]

            # Preflight CORS (OPTIONS)
            if line0.startswith("OPTIONS"):
                send_text(client, "ok", "200 OK")
                client.close()
                continue

            path = parse_path(line0)
            ip_cli = remote[0]

            if path == "/":
                send_text(client, "ESP32 Robot API OK")

            elif path.startswith("/status"):
                send_json(client, get_status_json(ip))

            elif path.startswith("/telemetry"):
                send_json(client, get_telemetry_json())

            elif path.startswith("/move"):

                if security["safe_mode"]:
                    send_json(client, '{"error":"safe_mode"}', "403 Forbidden")
                    client.close()
                    continue

                d = get_query_param(path, "dir")
                if d is None:
                    add_error(ip_cli, "missing_dir")
                    send_json(client, '{"error":"missing dir"}', "400 Bad Request")
                else:
                    d = d.upper()
                    if d == "F":
                        forward(); add_log("MOVE F")
                    elif d == "B":
                        backward(); add_log("MOVE B")
                    elif d == "L":
                        left(); add_log("MOVE L")
                    elif d == "R":
                        right(); add_log("MOVE R")
                    elif d == "S":
                        stop(); add_log("MOVE S")
                    else:
                        add_error(ip_cli, "invalid_dir:" + d)
                        send_json(client, '{"error":"invalid dir"}', "400 Bad Request")
                        client.close()
                        continue

                    send_json(client, '{"ok":true,"dir":"' + d + '"}')

            elif path.startswith("/auto"):
                v = get_query_param(path, "enabled")
                if v is None:
                    send_json(client, '{"error":"missing enabled"}', "400 Bad Request")
                else:
                    flag = v.lower() in ["1", "true", "yes", "on"]
                    auto_mode["enabled"] = flag
                    add_log("AUTO " + ("ON" if flag else "OFF"))
                    send_json(client, '{"auto_enabled": ' + str(flag).lower() + '}')

            elif path.startswith("/logs"):
                send_json(client, '{"logs": ' + str(logs).replace("'", '"') + '}')

            elif path.startswith("/security"):
                body = (
                    '{'
                    '"fail_count": ' + str(security["fail_count"]) + ','
                    '"safe_mode": ' + str(security["safe_mode"]).lower() + ','
                    '"last_error": "' + security["last_error"].replace('"','\"') + '",'
                    '"last_ip": "' + security["last_ip"] + '"'
                    '}'
                )
                send_json(client, body)

            elif path.startswith("/clear"):
                security["fail_count"] = 0
                security["safe_mode"] = False
                security["last_error"] = ""
                security["last_ip"] = ""
                add_log("SAFE MODE RESET")
                send_json(client, '{"ok":true}')

            else:
                add_error(ip_cli, "route_not_found:" + path)
                send_json(client, '{"error":"not found"}', "404 Not Found")

        finally:
            client.close()

# -------------------------
# INICIO GENERAL
# -------------------------

ip = iniciar_wifi_cliente()
if ip:
    iniciar_servidor(ip)
