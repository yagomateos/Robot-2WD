# Robot ESP32 – Dashboard React

Este panel permite controlar un robot con ESP32 y MicroPython.

## Funciones

- Movimiento (adelante, atrás, izquierda, derecha)
- Lectura de telemetría
- Panel de alarmas
- Registros en vivo

## Instalación

1. Instala dependencias:
```
npm install
```

2. Arranca el dashboard:
```
npm run dev
```

3. Conéctate a la WiFi del robot:
```
SSID: Robot-ESP32
Pass: 12345678
IP: 192.168.4.1
```

4. Abre la app en tu navegador.

## API usada

- /move
- /status
- /telemetry
- /security
- /logs
