# Guía Python - Conceptos Usados en el Robot ESP32

Esta guía explica los conceptos de Python que se usan en el proyecto del robot, con ejemplos pequeños basados en el código real.

---

## 1. Importar Módulos (`import`)

**¿Qué es?** Traer funcionalidades de otros archivos o librerías.

```python
import network        # Para WiFi
import socket         # Para servidor HTTP
import time           # Para delays y tiempo
from machine import Pin, time_pulse_us  # Importar solo lo que necesitas
```

**Ejemplo simple:**
```python
import time
time.sleep(1)  # Espera 1 segundo

from machine import Pin
led = Pin(2, Pin.OUT)  # Solo importas Pin
```

---

## 2. Variables Globales

**¿Qué es?** Variables que existen en todo el programa.

```python
# Variables simples
start_ms = time.ticks_ms()
last_auto_check = time.ticks_ms()

# Listas
logs = []

# Diccionarios
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
```

**Explicación:**
- `start_ms`: Un número (tiempo en milisegundos)
- `logs`: Una lista vacía `[]` donde guardaremos texto
- `security`: Un diccionario `{}` con pares clave-valor
- Puedes acceder con: `security["fail_count"]`

---

## 3. Funciones (`def`)

**¿Qué es?** Bloques de código reutilizables.

```python
# Función sin parámetros
def stop():
    IN1.value(0)
    IN2.value(0)
    IN3.value(0)
    IN4.value(0)

# Función con parámetros
def add_log(msg):
    if len(logs) > 50:
        logs.pop(0)  # Elimina el primero
    ts = get_uptime_seconds()
    logs.append("[{}s] {}".format(ts, msg))

# Función que retorna un valor
def get_uptime_seconds():
    return time.ticks_diff(time.ticks_ms(), start_ms) // 1000
```

**Uso:**
```python
stop()                    # Llama función sin parámetros
add_log("Robot iniciado") # Llama función con parámetro
segundos = get_uptime_seconds()  # Guarda el valor retornado
```

---

## 4. Pines GPIO (MicroPython)

**¿Qué es?** Controlar los pines físicos del ESP32.

```python
from machine import Pin

# Configurar pines de salida (OUT)
IN1 = Pin(26, Pin.OUT)  # GPIO26 como salida
IN2 = Pin(27, Pin.OUT)
TRIG = Pin(5, Pin.OUT)

# Configurar pines de entrada (IN)
ECHO = Pin(18, Pin.IN)  # GPIO18 como entrada

# Controlar pines
IN1.value(1)  # Encender (HIGH)
IN1.value(0)  # Apagar (LOW)

# Leer pin
estado = ECHO.value()  # 0 o 1
```

**Ejemplo motor adelante:**
```python
def forward():
    IN1.value(1)  # Motor izq +
    IN2.value(0)  # Motor izq -
    IN3.value(1)  # Motor der +
    IN4.value(0)  # Motor der -
```

---

## 5. Diccionarios `{}`

**¿Qué es?** Colección de pares clave-valor.

```python
# Crear diccionario
auto_mode = {
    "enabled": False,      # Clave: "enabled", Valor: False
    "min_distance": 20     # Clave: "min_distance", Valor: 20
}

# Acceder a valores
if auto_mode["enabled"]:
    print("Auto mode está activo")

# Modificar valores
auto_mode["enabled"] = True
auto_mode["min_distance"] = 30

# Agregar nuevas claves
auto_mode["speed"] = 100
```

**Diccionario dentro de diccionario:**
```python
config = {
    "wifi": {
        "ssid": "MiWiFi",
        "password": "123456"
    },
    "robot": {
        "max_speed": 100
    }
}

# Acceder
nombre_wifi = config["wifi"]["ssid"]  # "MiWiFi"
```

---

## 6. Listas `[]`

**¿Qué es?** Colección ordenada de elementos.

```python
# Crear lista vacía
logs = []

# Agregar elementos
logs.append("Primer mensaje")
logs.append("Segundo mensaje")
# logs ahora es: ["Primer mensaje", "Segundo mensaje"]

# Acceder por índice (empieza en 0)
primero = logs[0]   # "Primer mensaje"
segundo = logs[1]   # "Segundo mensaje"

# Tamaño de la lista
cantidad = len(logs)  # 2

# Eliminar el primer elemento
logs.pop(0)  # Quita "Primer mensaje"

# Verificar si está llena
if len(logs) > 50:
    logs.pop(0)  # Quita el más viejo
```

**Ejemplo del código:**
```python
logs = []

def add_log(msg):
    if len(logs) > 50:     # Si hay más de 50
        logs.pop(0)        # Elimina el primero (más viejo)
    logs.append(msg)       # Agrega el nuevo al final
```

---

## 7. Strings (Texto)

**¿Qué es?** Cadenas de texto.

```python
# Crear strings
mensaje = "Robot iniciado"
ssid = "MiWiFi"

# Concatenar (unir)
saludo = "Hola " + "Mundo"  # "Hola Mundo"

# Formatear con .format()
distancia = 15.3
texto = "Distancia: {} cm".format(distancia)
# "Distancia: 15.3 cm"

# Múltiples valores
texto = "IP: {} Puerto: {}".format("192.168.1.1", 80)
# "IP: 192.168.1.1 Puerto: 80"

# Formatear números
texto = "Distancia: {:.1f}".format(15.345)
# "Distancia: 15.3" (1 decimal)
```

**Ejemplo del código:**
```python
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
```

**Operaciones comunes:**
```python
texto = "Hola Mundo"
texto.upper()      # "HOLA MUNDO"
texto.lower()      # "hola mundo"
texto.split(" ")   # ["Hola", "Mundo"]
"X" in texto       # False
"Hola" in texto    # True
```

---

## 8. Condicionales (`if`, `elif`, `else`)

**¿Qué es?** Ejecutar código según condiciones.

```python
# If simple
if distancia < 20:
    stop()

# If-else
if auto_mode["enabled"]:
    forward()
else:
    stop()

# If-elif-else
d = "F"
if d == "F":
    forward()
elif d == "B":
    backward()
elif d == "L":
    left()
elif d == "R":
    right()
else:
    stop()
```

**Operadores de comparación:**
```python
x == y   # Igual a
x != y   # Diferente de
x < y    # Menor que
x > y    # Mayor que
x <= y   # Menor o igual
x >= y   # Mayor o igual
```

**Operadores lógicos:**
```python
# AND (y)
if dist < 20 and auto_mode["enabled"]:
    stop()

# OR (o)
if d == "F" or d == "B":
    print("Movimiento vertical")

# NOT (no)
if not sta.isconnected():
    print("No conectado")
```

**Ejemplo del código:**
```python
def auto_step():
    if not auto_mode["enabled"]:
        return  # Sale de la función

    dist = medir_distancia_cm()
    if dist < 0:
        return

    if dist < auto_mode["min_distance"]:
        stop()
        time.sleep_ms(200)
        backward()
    else:
        forward()
```

---

## 9. Loops (`for`, `while`)

### Loop `for`

**¿Qué es?** Repetir código un número de veces.

```python
# Repetir 10 veces
for i in range(10):
    print(i)  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

# Desde 1 hasta 5
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5

# Iterar sobre una lista
logs = ["mensaje1", "mensaje2", "mensaje3"]
for log in logs:
    print(log)
```

**Ejemplo del código:**
```python
# Intentar conectar WiFi 40 veces
for i in range(40):
    print("Intento", i + 1)
    if sta.isconnected():
        break  # Sale del loop
    time.sleep(0.5)
```

### Loop `while`

**¿Qué es?** Repetir código mientras una condición sea verdadera.

```python
# Loop infinito
while True:
    print("Siempre")
    time.sleep(1)

# Loop con condición
contador = 0
while contador < 5:
    print(contador)
    contador += 1  # contador = contador + 1
```

**Ejemplo del código:**
```python
def iniciar_servidor(ip):
    # ... configuración ...

    while True:  # Loop infinito del servidor
        auto_step()  # Ejecutar modo auto

        try:
            client, remote = s.accept()
        except OSError:
            continue  # Salta a la siguiente iteración

        # ... procesar petición ...
```

---

## 10. Try-Except (Manejo de Errores)

**¿Qué es?** Intentar código que puede fallar sin que el programa se rompa.

```python
# Básico
try:
    numero = int("abc")  # Esto falla
except:
    print("Error al convertir")

# Con tipo de error específico
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("No se puede dividir por cero")

# Try-except-finally
try:
    archivo = open("datos.txt")
    data = archivo.read()
except:
    print("Error al leer archivo")
finally:
    archivo.close()  # Siempre se ejecuta
```

**Ejemplo del código:**
```python
try:
    client, remote = s.accept()
except OSError:
    continue  # Si falla, continúa el loop

try:
    text = req.decode()
except:
    client.close()
    continue
```

---

## 11. Time (Tiempo y Delays)

**¿Qué es?** Trabajar con tiempo y pausas.

```python
import time

# Delays
time.sleep(1)         # Pausa 1 segundo
time.sleep_ms(500)    # Pausa 500 milisegundos
time.sleep_us(10)     # Pausa 10 microsegundos

# Tiempo actual (milisegundos)
ahora = time.ticks_ms()  # Ej: 5234567

# Diferencia de tiempo
inicio = time.ticks_ms()
# ... hacer algo ...
fin = time.ticks_ms()
duracion = time.ticks_diff(fin, inicio)
print("Tomó {} ms".format(duracion))
```

**Ejemplo del código:**
```python
start_ms = time.ticks_ms()

def get_uptime_seconds():
    ahora = time.ticks_ms()
    diferencia_ms = time.ticks_diff(ahora, start_ms)
    diferencia_s = diferencia_ms // 1000  # División entera
    return diferencia_s
```

---

## 12. Sockets (Red)

**¿Qué es?** Comunicación por red (HTTP).

```python
import socket

# Crear socket
s = socket.socket()

# Permitir reutilizar dirección
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincular a IP y puerto
addr = ("192.168.1.100", 80)
s.bind(addr)

# Escuchar conexiones (máx 1 en cola)
s.listen(1)

# Timeout (no bloquear para siempre)
s.settimeout(0.1)  # 100ms

# Aceptar conexión
client, remote_addr = s.accept()

# Recibir datos
datos = client.recv(1024)  # Máximo 1024 bytes

# Enviar datos
client.send("HTTP/1.1 200 OK\r\n\r\n")

# Cerrar
client.close()
```

**Ejemplo del código:**
```python
def iniciar_servidor(ip):
    addr = (ip, 80)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    s.settimeout(0.1)

    while True:
        try:
            client, remote = s.accept()
            req = client.recv(1024)
            # ... procesar ...
            client.send("HTTP/1.1 200 OK\r\n\r\n")
        except OSError:
            continue
        finally:
            client.close()
```

---

## 13. Network (WiFi)

**¿Qué es?** Conectar el ESP32 a WiFi.

```python
import network

# Crear interfaz WiFi en modo estación (cliente)
sta = network.WLAN(network.STA_IF)

# Activar WiFi
sta.active(True)

# Conectar a red
sta.connect("MiWiFi", "contraseña123")

# Verificar si está conectado
if sta.isconnected():
    print("Conectado!")

# Obtener información de red
ip, mascara, gateway, dns = sta.ifconfig()
print("Mi IP:", ip)

# Desconectar
sta.disconnect()
sta.active(False)
```

**Ejemplo del código:**
```python
def iniciar_wifi_cliente():
    # Apagar modo AP (Access Point)
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    # Activar modo cliente
    sta = network.WLAN(network.STA_IF)
    sta.active(True)

    # Conectar
    ssid = "MiHotspot"
    pwd = "password123"
    sta.connect(ssid, pwd)

    # Esperar conexión
    for i in range(40):
        if sta.isconnected():
            break
        time.sleep(0.5)

    if sta.isconnected():
        ip = sta.ifconfig()[0]
        return ip
    else:
        return None
```

---

## 14. Operadores Útiles

### Operadores Aritméticos
```python
a = 10
b = 3

a + b    # 13 (suma)
a - b    # 7 (resta)
a * b    # 30 (multiplicación)
a / b    # 3.333... (división)
a // b   # 3 (división entera)
a % b    # 1 (módulo, resto)
a ** b   # 1000 (potencia)
```

### Operadores de Asignación
```python
x = 5
x += 2   # x = x + 2  →  x es 7
x -= 1   # x = x - 1  →  x es 6
x *= 3   # x = x * 3  →  x es 18
x //= 2  # x = x // 2 →  x es 9
```

### Operadores de Pertenencia
```python
logs = ["msg1", "msg2", "msg3"]

"msg1" in logs       # True
"msg4" in logs       # False
"msg4" not in logs   # True

texto = "Hola Mundo"
"Hola" in texto      # True
```

---

## 15. Conversión de Tipos

```python
# String a número
texto = "123"
numero = int(texto)      # 123
decimal = float("45.6")  # 45.6

# Número a string
edad = 25
texto = str(edad)  # "25"

# Boolean a string
activo = True
texto = str(activo)        # "True"
texto = str(activo).lower() # "true"

# Formatear números
pi = 3.14159
texto = "{:.2f}".format(pi)  # "3.14" (2 decimales)
```

**Ejemplo del código:**
```python
# Convertir boolean a JSON
auto_enabled = True
json_str = str(auto_enabled).lower()  # "true"

# Formatear distancia
dist = 15.345
json_str = '{"distance": ' + "{:.1f}".format(dist) + '}'
# '{"distance": 15.3}'
```

---

## 16. Funciones Útiles

### `len()` - Longitud
```python
logs = ["msg1", "msg2"]
cantidad = len(logs)  # 2

texto = "Hola"
caracteres = len(texto)  # 4
```

### `range()` - Rango de números
```python
range(5)        # 0, 1, 2, 3, 4
range(1, 6)     # 1, 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8 (de 2 en 2)
```

### `print()` - Imprimir
```python
print("Hola")
print("Distancia:", 15.3)
print("X:", x, "Y:", y)
```

### `str.replace()` - Reemplazar texto
```python
json = '{"logs": ["msg1", "msg2"]}'
json_corregido = json.replace("'", '"')
```

### `str.split()` - Dividir string
```python
linea = "GET /status HTTP/1.1"
partes = linea.split(" ")
# ["GET", "/status", "HTTP/1.1"]

metodo = partes[0]  # "GET"
ruta = partes[1]    # "/status"
```

---

## 17. Return en Funciones

**¿Qué es?** Devolver un valor desde una función.

```python
# Sin return (no devuelve nada)
def saludar():
    print("Hola!")

# Con return (devuelve valor)
def sumar(a, b):
    resultado = a + b
    return resultado

# Return múltiple
def dividir(a, b):
    cociente = a // b
    resto = a % b
    return cociente, resto

# Uso
total = sumar(5, 3)  # 8
c, r = dividir(10, 3)  # c=3, r=1
```

**Return para salir temprano:**
```python
def procesar(valor):
    if valor < 0:
        return  # Sale inmediatamente

    # Solo se ejecuta si valor >= 0
    print("Procesando:", valor)
```

---

## 18. Variables Globales en Funciones

```python
contador = 0

def incrementar():
    global contador  # Necesario para modificar
    contador += 1

incrementar()
incrementar()
print(contador)  # 2
```

**Ejemplo del código:**
```python
logs = []

def add_log(msg):
    global logs  # No necesario si solo usas append
    logs.append(msg)

security = {"fail_count": 0}

def add_error(msg):
    # No necesitas 'global' para modificar dict existente
    security["fail_count"] += 1
```

---

## Resumen de Conceptos por Frecuencia de Uso

### 🔥 Muy Frecuentes
1. **Funciones** (`def`) - Para organizar código
2. **If/else** - Para tomar decisiones
3. **Diccionarios** - Para guardar configuración
4. **Strings** - Para mensajes y JSON
5. **Pines GPIO** - Para controlar hardware

### ⭐ Frecuentes
6. **Listas** - Para logs y colecciones
7. **Loops** (`for`, `while`) - Para repetir
8. **Time** - Para delays y timestamps
9. **Try/except** - Para errores de red
10. **Variables globales** - Para estado del sistema

### 💡 Específicos del Proyecto
11. **Sockets** - Para servidor HTTP
12. **Network** - Para WiFi
13. **time_pulse_us** - Para sensor ultrasónico

---

## Ejemplo Completo: Función del Código Real

Veamos cómo se combinan todos estos conceptos:

```python
# 1. IMPORT
import time
from machine import Pin

# 2. VARIABLES GLOBALES
logs = []                    # Lista
start_ms = time.ticks_ms()   # Número
auto_mode = {                # Diccionario
    "enabled": False,
    "min_distance": 20
}

# 3. PINES GPIO
TRIG = Pin(5, Pin.OUT)
ECHO = Pin(18, Pin.IN)

# 4. FUNCIONES
def medir_distancia_cm():
    # Activar sensor
    TRIG.value(0)
    time.sleep_us(2)
    TRIG.value(1)
    time.sleep_us(10)
    TRIG.value(0)

    # Medir tiempo
    duracion = time_pulse_us(ECHO, 1, 30000)

    # Condicional
    if duracion < 0:
        return -1.0

    # Calcular distancia
    distancia = (duracion / 2.0) / 29.1
    return distancia

def add_log(msg):
    global logs

    # Control de tamaño
    if len(logs) > 50:
        logs.pop(0)

    # Formatear con timestamp
    ts = time.ticks_diff(time.ticks_ms(), start_ms) // 1000
    mensaje_completo = "[{}s] {}".format(ts, msg)

    # Agregar a lista
    logs.append(mensaje_completo)

# 5. USO
while True:
    dist = medir_distancia_cm()

    if dist > 0 and dist < 20:
        add_log("Obstáculo detectado!")
        time.sleep(1)
```

---

## Consejos Finales

1. **Indentación es importante** - Python usa espacios para definir bloques
   ```python
   if True:
       print("Correcto")  # 4 espacios
   ```

2. **Los índices empiezan en 0**
   ```python
   lista = ["a", "b", "c"]
   lista[0]  # "a"
   lista[1]  # "b"
   ```

3. **Todo es un objeto** - Números, strings, listas, todo
   ```python
   texto = "hola"
   texto.upper()  # Método del objeto string
   ```

4. **None es "nada"**
   ```python
   valor = None
   if valor is None:
       print("No hay valor")
   ```

5. **Comentarios**
   ```python
   # Comentario de una línea

   """
   Comentario
   de varias
   líneas
   """
   ```

---

**¡Ahora conoces los conceptos de Python usados en el robot!** 🐍🤖
