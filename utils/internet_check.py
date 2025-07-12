# Verifica conexión a internet

import socket
import time

def hay_conexion(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

def conexion_estable(tiempo=3):
    tiempos = []
    for _ in range(tiempo):
        inicio = time.time()
        if not hay_conexion():
            return False
        fin = time.time()
        tiempos.append(fin - inicio)
    return max(tiempos) < 1.0  # menor a 1s